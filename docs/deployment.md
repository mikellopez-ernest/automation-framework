# Deployment Guide

> Status: Stable
> Last updated: 2026-07-13

# Overview

Automation Framework is deployed as an application stack connected to a shared reverse proxy infrastructure.

The production architecture is:

```text
Internet
    │
    ▼
Shared Caddy reverse proxy
    │
    ▼
External Docker network: proxy
    │
    ▼
Automation Framework
    │
    ▼
Playwright
    │
    ▼
External Platform
```

Caddy is deployed independently from the application.

It acts as the global HTTP and HTTPS entry point for the server and may route traffic to multiple applications, including Automation Framework and future services such as WordPress or other internal APIs.

Automation Framework is deployed through its own Docker Compose stack.

The application stack:

* does not publish ports to the host;
* does not manage TLS certificates;
* does not own the reverse proxy;
* connects to the external Docker network named `proxy`.

The shared Caddy stack:

* publishes ports 80 and 443;
* manages TLS certificates;
* redirects HTTP traffic to HTTPS;
* routes requests to application containers through the `proxy` network.

# Deployment Architecture

The production deployment is intentionally split into two independent stacks.

## Automation Framework stack

The application stack is defined by:

```text
docker-compose.yml
```

It contains only the `automation` service.

The service runs:

* FastAPI;
* Uvicorn;
* Playwright;
* Chromium;
* Automation Framework.

It connects to the external Docker network:

```text
proxy
```

The application is not exposed directly to the host or the Internet.

## Shared Caddy stack

The shared reverse proxy stack is defined by:

```text
infrastructure/caddy/docker-compose.yml
```

Its configuration is stored in:

```text
infrastructure/caddy/Caddyfile
```

Caddy is responsible for:

* public HTTP and HTTPS access;
* automatic TLS certificate management;
* HTTP-to-HTTPS redirects;
* routing traffic to application containers;
* serving future applications hosted on the same server.

Both stacks can be started, stopped, updated and maintained independently.


# Reverse Proxy Design

Automation Framework exposes a single public entry point.

The deployment architecture is intentionally structured as:

```text id="6a8bkg"
Internet

↓

HTTPS

↓

Caddy

↓

FastAPI

↓

Playwright
```

The FastAPI application is never exposed directly to the public network.

Only Caddy publishes ports on the host.

Communication between Caddy and the application occurs exclusively through the internal Docker network.

## Why Caddy

Several reverse proxies could provide the required functionality.

Caddy was selected because it offers:

* automatic HTTPS by default;
* automatic certificate renewal;
* simple configuration;
* native HTTP/2 and HTTP/3 support;
* excellent Docker integration;
* minimal operational overhead.

No additional certificate management tooling is required.

## Automatic HTTPS

When the configured domain points to the deployment server, Caddy automatically:

1. requests a TLS certificate;
2. validates domain ownership;
3. installs the certificate;
4. renews it before expiration.

Certificate management therefore becomes part of normal application operation.

No manual renewal process is required.

## Network Isolation

The application container does not expose any ports to the host.

Instead, Docker Compose creates an isolated internal network.

Communication follows this path:

```text id="7wd5zi"
Client

↓

HTTPS

↓

Caddy

↓

automation:8000
```

The hostname `automation` is the Docker Compose service name.

No public traffic reaches the FastAPI container directly.

This provides an additional security boundary and simplifies firewall configuration.

## TLS Certificates

Certificate data is stored in the persistent Docker volume:

```text id="4m6rbb"
caddy_data
```

This allows certificates and ACME account information to survive:

* container recreation;
* application updates;
* host reboots.

Deleting this volume causes Caddy to request new certificates during the next deployment.

This is normally safe, but repeated unnecessary certificate requests may eventually encounter certificate authority rate limits.

## Public Exposure

Only the following ports should be reachable from the Internet:

| Port | Protocol | Purpose                  |
| ---: | :------: | ------------------------ |
|   80 |    TCP   | HTTP and ACME validation |
|  443 |    TCP   | HTTPS                    |
|  443 |    UDP   | HTTP/3                   |

Port **8000** must never be published directly by the application container in production.


# Operational Philosophy

The production deployment intentionally keeps the runtime architecture simple.

The current system does not require:

* a database;
* a message broker;
* a background job worker;
* a task queue;
* a scheduler;
* permanent report storage;
* multiple application replicas.

Each API request represents a complete business operation.

The request lifecycle is:

```text
HTTP request

↓

Authentication

↓

Automation Lock

↓

Browser startup

↓

Business operation

↓

HTTP response

↓

Temporary resource cleanup
```

Browser instances are ephemeral.

Each automation request creates a browser, performs the required operation and closes the browser before the request lifecycle finishes.

Only the Playwright authentication state is persistent.

This separation is intentional:

```text
Browser process        → ephemeral

Temporary downloads    → request-scoped

Generated reports      → deleted after response

Authentication state   → persistent
```

The deployment therefore persists only the minimum runtime data required to reuse authenticated browser sessions.

This approach reduces:

* operational complexity;
* stale browser processes;
* permanent filesystem state;
* manual cleanup requirements;
* coupling between application instances;
* infrastructure maintenance.

The deployment must remain aligned with the current concurrency guarantees.

Production uses:

```text
one automation container

one Uvicorn process

one Uvicorn worker
```

Horizontal scaling, multiple workers and distributed execution are outside the current architecture.

They should only be introduced together with an explicit concurrency design, such as an external queue or distributed lock.


# Required Files

The deployment uses the following files in the repository root:

```text
.
├── .dockerignore
├── .env
├── .env.example
├── Caddyfile
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

The `.env` file contains environment-specific configuration and secrets.

It must never be committed to Git.

# Production Directory Layout

The framework can be deployed from any directory.

However, a dedicated deployment directory is recommended.

Example:

```text
/opt/automation-framework
│
├── .env
├── .env.example
├── Caddyfile
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
│
├── automation/
├── docs/
│
└── backups/
```

The repository itself contains all deployment configuration.

No external configuration directories are required.

## Repository

The Git repository should contain:

* application source code;
* deployment configuration;
* documentation;
* Docker configuration.

It should not contain:

* generated reports;
* Playwright sessions;
* TLS certificates;
* secrets;
* backups.

## Runtime Data

Runtime state is intentionally stored outside the container filesystem through Docker named volumes.

The deployment currently persists only:

* Playwright authentication state;
* Caddy runtime data;
* TLS certificates.

Everything else is recreated automatically whenever a container starts.

## Backups

A dedicated directory for exported backups is recommended:

```text
backups/
```

Example:

```text
backups/
├── automation-auth-2026-07-13.tar.gz
├── caddy-data-2026-07-13.tar.gz
└── deployment-notes.md
```

Backups should not be committed to Git.

## Secrets

The `.env` file should remain inside the deployment directory.

Recommended permissions:

```text
-rw-------
```

Only the deployment administrator should have read access.

## Logs

Application logs are not stored inside the repository.

Operational logs should be obtained through:

```bash
docker compose logs
```

This avoids creating local log files that require manual rotation or cleanup.

## Philosophy

The deployment directory intentionally remains small.

The application stores almost no persistent runtime state.

This makes it straightforward to:

* move the deployment to another server;
* recreate containers;
* restore from backups;
* understand which files are operationally important.

# Requirements

The production server requires:

* Docker Engine
* Docker Compose v2
* a public domain
* a public IPv4 address, or a correctly configured IPv6 address
* inbound TCP access to ports 80 and 443
* inbound UDP access to port 443 if HTTP/3 is used

The domain must resolve to the public IP address of the server.

Example:

```text
automation.example.com → 203.0.113.10
```

# DNS Configuration

Create an `A` record for the deployment domain.

Example:

```text
Type: A
Name: automation
Value: 203.0.113.10
```

An `AAAA` record may also be configured when the server has working public IPv6 connectivity.

Do not configure an invalid `AAAA` record. A domain resolving to an unreachable IPv6 address may cause certificate issuance or client connectivity failures.

DNS changes must be propagated before starting the production deployment.

# Firewall and Router Configuration

The following ports must reach the server:

| Protocol | Port | Purpose                  |
| -------- | ---- | ------------------------ |
| TCP      | 80   | HTTP and ACME validation |
| TCP      | 443  | HTTPS                    |
| UDP      | 443  | HTTP/3                   |

If the server is behind a router or NAT gateway, forward these ports to the Docker host.

Port 8000 must not be exposed publicly.

# Environment Configuration

Create the production environment file from the template:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
AUTOMATION_DOMAIN=automation.example.com
AUTOMATION_API_TOKEN=replace-with-a-random-token
AUTOMATION_DINANTIA_USERNAME=replace-with-username
AUTOMATION_DINANTIA_PASSWORD=replace-with-password
AUTOMATION_DINANTIA_STORAGE_STATE_PATH=/app/.playwright/auth/dinantia.json
```

## Domain

`AUTOMATION_DOMAIN` must contain only the hostname.

Correct:

```dotenv
AUTOMATION_DOMAIN=automation.example.com
```

Incorrect:

```dotenv
AUTOMATION_DOMAIN=https://automation.example.com/
```

## API token

Generate a strong random token:

```bash
openssl rand -hex 32
```

Store the generated value in:

```dotenv
AUTOMATION_API_TOKEN=<generated-token>
```

The token must:

* remain secret
* never be committed
* never appear in application logs
* only be transmitted over HTTPS

## Dinantia credentials

Configure the account used by the browser automation:

```dotenv
AUTOMATION_DINANTIA_USERNAME=<username>
AUTOMATION_DINANTIA_PASSWORD=<password>
```

These credentials are independent from API authentication.

They must never be exposed to API clients.

# Validate the Deployment Configuration

Validate the resolved Docker Compose configuration:

```bash
docker compose config
```

Validate the Caddy configuration:

```bash
docker compose run --rm caddy \
  caddy validate --config /etc/caddy/Caddyfile
```

Both commands must complete successfully before starting the deployment.

# Build and Start

Build the application image:

```bash
docker compose build
```

Start the deployment:

```bash
docker compose up -d
```

Check service status:

```bash
docker compose ps
```

Both services should be running:

```text
automation-framework
automation-caddy
```

# Deployment Lifecycle

The production deployment follows a predictable lifecycle.

## Initial Deployment

```text
Clone repository

↓

Create .env

↓

Validate configuration

↓

Build Docker image

↓

Start containers

↓

Caddy obtains TLS certificate

↓

Health check

↓

Production ready
```

During the initial deployment:

* the application image is built;
* Docker volumes are created automatically;
* Caddy obtains the first TLS certificate;
* the Playwright authentication state does not yet exist.

The first authenticated browser automation creates the persistent storage state.

## Normal Operation

During normal operation each request is completely independent.

```text
HTTP request

↓

Bearer authentication

↓

Automation Lock

↓

Playwright

↓

Business operation

↓

HTTP response

↓

Browser shutdown

↓

Temporary cleanup
```

The browser process never remains running between requests.

Only the authenticated session is preserved.

## Application Update

Updating the application follows the same sequence every time.

```text
Pull latest version

↓

Run quality checks

↓

Rebuild Docker image

↓

Recreate container

↓

Health check

↓

Production
```

Normally this corresponds to:

```bash
git pull

uv run ruff check .
uv run mypy
uv run pytest

docker compose build
docker compose up -d
```

The following data survives application updates:

* Playwright authentication state;
* Caddy certificates;
* Caddy runtime configuration.

No manual migration is normally required because no application database exists.

## Failure Recovery

If the application container stops unexpectedly:

```text
Container stops

↓

Docker restart policy

↓

Container starts again

↓

Playwright session reused

↓

Application available
```

Because the authentication state is stored outside the container, restarting the application does not normally require a new login to Dinantia.

# Deployment Lifecycle

The production deployment follows a predictable lifecycle.

## Initial Deployment

```text
Clone repository

↓

Create .env

↓

Validate configuration

↓

Build Docker image

↓

Start containers

↓

Caddy obtains TLS certificate

↓

Health check

↓

Production ready
```

During the initial deployment:

* the application image is built;
* Docker volumes are created automatically;
* Caddy obtains the first TLS certificate;
* the Playwright authentication state does not yet exist.

The first authenticated browser automation creates the persistent storage state.

## Normal Operation

During normal operation each request is completely independent.

```text
HTTP request

↓

Bearer authentication

↓

Automation Lock

↓

Playwright

↓

Business operation

↓

HTTP response

↓

Browser shutdown

↓

Temporary cleanup
```

The browser process never remains running between requests.

Only the authenticated session is preserved.

## Application Update

Updating the application follows the same sequence every time.

```text
Pull latest version

↓

Run quality checks

↓

Rebuild Docker image

↓

Recreate container

↓

Health check

↓

Production
```

Normally this corresponds to:

```bash
git pull

uv run ruff check .
uv run mypy
uv run pytest

docker compose build
docker compose up -d
```

The following data survives application updates:

* Playwright authentication state;
* Caddy certificates;
* Caddy runtime configuration.

No manual migration is normally required because no application database exists.

## Failure Recovery

If the application container stops unexpectedly:

```text
Container stops

↓

Docker restart policy

↓

Container starts again

↓

Playwright session reused

↓

Application available
```

Because the authentication state is stored outside the container, restarting the application does not normally require a new login to Dinantia.


# First Startup

On the first request requiring Dinantia access:

1. the API validates the Bearer token;
2. the Automation Lock is acquired;
3. Playwright starts Chromium;
4. the framework authenticates against Dinantia;
5. the Playwright storage state is created;
6. the operation continues;
7. the browser closes.

The storage state is written to:

```text
/app/.playwright/auth/dinantia.json
```

inside the automation container.

The directory is backed by the named Docker volume:

```text
automation_auth
```

Subsequent requests reuse the stored authenticated session whenever it remains valid.

# Validate the Deployment

## Health check

Test the public HTTPS endpoint:

```bash
curl https://automation.example.com/health
```

Expected response:

```json
{"status":"ok"}
```

## Authenticated endpoint

Use the configured Bearer token:

```bash
curl \
  --request POST \
  --header "Authorization: Bearer ${AUTOMATION_API_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{"school_year":"2025-26"}' \
  --output tracking-report.xlsx \
  https://automation.example.com/api/v1/dinantia/tracking/export
```

Validate that:

* the response is successful;
* the Excel file is downloaded;
* the generated file is valid;
* temporary files are deleted automatically;
* the Playwright storage state remains available for future requests.

# Persistent Volumes

The deployment defines three named volumes.

## `automation_auth`

Contains the persistent Playwright authentication state.

Mounted at:

```text
/app/.playwright/auth
```

This volume is sensitive because it may contain an authenticated browser session.

## `caddy_data`

Contains Caddy runtime data, including:

* TLS certificates
* private keys
* certificate account information

This volume must be preserved.

## `caddy_config`

Contains Caddy configuration state used at runtime.

# Temporary Files

Generated reports are request-scoped.

They are:

1. created in a temporary directory;
2. returned through the HTTP response;
3. deleted after the response is transmitted.

No report volume is required.

The `downloads` directory is not used for permanent production storage.

# Logs

Show logs for all services:

```bash
docker compose logs
```

Follow logs continuously:

```bash
docker compose logs -f
```

Show API logs only:

```bash
docker compose logs -f automation
```

Show Caddy logs only:

```bash
docker compose logs -f caddy
```

Show recent logs:

```bash
docker compose logs --tail 100
```

Secrets and authentication tokens must never be written to logs.

# Service Management

Start the deployment:

```bash
docker compose up -d
```

Stop the containers without deleting them:

```bash
docker compose stop
```

Start stopped containers:

```bash
docker compose start
```

Restart all services:

```bash
docker compose restart
```

Stop and remove containers and networks:

```bash
docker compose down
```

Named volumes are preserved by `docker compose down`.

Do not use the following command unless persistent data must intentionally be deleted:

```bash
docker compose down --volumes
```

That command removes the Playwright session and Caddy certificate data.

# Updating the Application

Pull or deploy the new application version:

```bash
git pull
```

Run the local quality pipeline:

```bash
uv run ruff check .
uv run mypy
uv run pytest
```

Rebuild the application image:

```bash
docker compose build automation
```

Recreate the application container:

```bash
docker compose up -d automation
```

If deployment configuration or Caddy has also changed:

```bash
docker compose up -d --build
```

Check the result:

```bash
docker compose ps
docker compose logs --tail 100
```

Validate the health endpoint:

```bash
curl https://automation.example.com/health
```

The named volumes remain intact during normal rebuilds and container recreation.

# Backup Strategy

The application does not store generated reports permanently.

The persistent data requiring consideration is:

* Playwright storage state
* Caddy certificate data
* deployment configuration
* environment secrets

## Repository

Back up the Git repository through the normal source control workflow.

The `.env` file must not be committed.

## Environment configuration

Store `.env` in a secure password manager or encrypted backup.

It contains:

* API authentication token
* Dinantia credentials
* public deployment domain

## Playwright authentication state

The `automation_auth` volume may be backed up to avoid requiring a new browser login after server restoration.

However, the application can recreate this state automatically using the configured Dinantia credentials.

Treat any backup of this volume as sensitive.

## Caddy data

Back up `caddy_data` if preserving the existing certificate account and certificates is operationally useful.

Caddy can normally obtain new certificates after restoration, provided that:

* DNS is correct;
* ports 80 and 443 are reachable;
* certificate authority limits are not exceeded.

# Disaster Recovery

This section describes how to restore the Automation Framework after a complete server loss.

Typical scenarios include:

* hardware failure;
* operating system corruption;
* accidental server deletion;
* migration to new hardware;
* disaster recovery testing.

The framework is intentionally designed so that recovery requires only a small amount of persistent information.

## Required Assets

A complete recovery requires:

* the Git repository;
* the `.env` file;
* the optional Playwright authentication backup;
* the optional Caddy data backup.

Generated reports are never required.

Temporary downloads are never required.

## Recovery Procedure

The recommended recovery sequence is:

```text
Provision new server

↓

Install Docker

↓

Clone repository

↓

Restore .env

↓

Restore Docker volumes (optional)

↓

docker compose up -d

↓

Health check

↓

Production
```

## Step 1 — Provision the Server

Prepare a clean server with:

* Docker Engine;
* Docker Compose;
* Internet connectivity;
* the required firewall rules;
* DNS pointing to the server.

## Step 2 — Clone the Repository

```bash
git clone <repository-url>

cd automation-framework
```

The repository contains all deployment configuration.

## Step 3 — Restore the Environment

Restore the original `.env` file.

This file contains:

* deployment domain;
* API authentication token;
* Dinantia credentials.

Without this file the deployment cannot operate correctly.

## Step 4 — Restore Docker Volumes (Optional)

If backups are available:

Restore:

* Playwright authentication state;
* Caddy runtime data.

If these backups are unavailable:

* the framework will authenticate again against Dinantia;
* Caddy will request new TLS certificates automatically.

Therefore volume restoration is recommended but not strictly required.

## Step 5 — Start the Deployment

```bash
docker compose up -d
```

Docker automatically recreates:

* containers;
* networks;
* missing volumes.

## Step 6 — Validate the Deployment

Verify:

```bash
docker compose ps
```

Then:

```bash
curl https://automation.example.com/health
```

Finally execute a complete authenticated export to verify:

* API authentication;
* Playwright startup;
* Dinantia authentication;
* report generation;
* temporary cleanup.

## Recovery Time

Typical recovery requires only:

* Docker installation;
* repository checkout;
* environment restoration;
* container startup.

No database migration is required.

No manual application configuration is required.

No browser installation is required.

## Recovery Philosophy

The framework deliberately minimizes persistent state.

Only three categories of information are operationally important:

* deployment configuration;
* authentication information;
* TLS certificates.

Everything else is recreated automatically.

This significantly reduces recovery complexity and shortens the time required to return the service to production.

## Recovery Validation Checklist

After recovery verify:

* HTTPS is working.
* The TLS certificate is valid.
* `/health` returns `200 OK`.
* API authentication succeeds.
* The Playwright browser starts correctly.
* Dinantia authentication succeeds.
* The generated Excel file is valid.
* Temporary files are removed automatically.
* The storage state is recreated or restored successfully.

The deployment should be considered fully recovered only after a complete end-to-end automation has been executed successfully.

# Back Up a Named Volume

Docker Compose prefixes named volumes using the Compose project name.

The final Docker volume name usually follows this pattern:

```text
<compose-project-name>_<volume-name>
```

For example:

```text
automation_automation_auth
automation_caddy_data
automation_caddy_config
```

However, these names are not guaranteed to remain the same.

The Compose project name may change depending on:

* the repository directory name;
* the `COMPOSE_PROJECT_NAME` environment variable;
* the `--project-name` or `-p` Docker Compose option;
* the deployment environment.

Before creating a backup, always list the existing Docker volumes:

```bash
docker volume ls
```

Identify the volumes corresponding to:

* `automation_auth`
* `caddy_data`
* `caddy_config`

Use the actual names reported by Docker in all backup and restore commands.

Never assume that the volume prefix is `automation_`.

# Examples

Create a backup directory:

```bash
mkdir -p backups
```

Back up the authentication volume:

```bash
docker run --rm \
  --volume automation_automation_auth:/source:ro \
  --volume "$(pwd)/backups:/backup" \
  alpine \
  tar -czf /backup/automation-auth.tar.gz -C /source .
```

Back up Caddy data:

```bash
docker run --rm \
  --volume automation_caddy_data:/source:ro \
  --volume "$(pwd)/backups:/backup" \
  alpine \
  tar -czf /backup/caddy-data.tar.gz -C /source .
```

Docker Compose volume names may vary depending on the Compose project name.

List the actual names before creating a backup:

```bash
docker volume ls
```

# Restore a Named Volume

Stop the deployment:

```bash
docker compose down
```

Create the required volumes:

```bash
docker compose up --no-start
```

Restore the authentication volume:

```bash
docker run --rm \
  --volume automation_automation_auth:/target \
  --volume "$(pwd)/backups:/backup:ro" \
  alpine \
  sh -c "rm -rf /target/* && tar -xzf /backup/automation-auth.tar.gz -C /target"
```

Restore Caddy data:

```bash
docker run --rm \
  --volume automation_caddy_data:/target \
  --volume "$(pwd)/backups:/backup:ro" \
  alpine \
  sh -c "rm -rf /target/* && tar -xzf /backup/caddy-data.tar.gz -C /target"
```

Start the deployment:

```bash
docker compose up -d
```

# Security Model

The deployment follows a layered security model.

Each layer protects a different aspect of the system.

```text
Internet
    │
    ▼
HTTPS
    │
    ▼
Caddy
    │
    ▼
Bearer Authentication
    │
    ▼
Automation Framework
    │
    ▼
Playwright
    │
    ▼
Dinantia
```

Compromising one layer should not automatically compromise the others.

## TLS

All public traffic must use HTTPS.

TLS is terminated by Caddy.

The application itself never manages certificates.

Automatic certificate renewal reduces operational overhead and avoids expired certificates.

## Reverse Proxy

Only Caddy publishes ports to the host.

The FastAPI application remains isolated inside the Docker network.

The API must never expose:

```text
8000/tcp
```

directly to the Internet.

## API Authentication

The HTTP API is protected using a static Bearer token.

This protects access to business operations.

The API token should:

* be randomly generated;
* never be committed to Git;
* never appear in logs;
* only be transmitted over HTTPS.

The API token is completely independent from Dinantia credentials.

## Dinantia Credentials

The framework authenticates against Dinantia using its own account.

These credentials exist only inside:

```text
.env
```

They must never be:

* returned by the API;
* written to logs;
* committed to source control.

## Playwright Storage State

The persistent authentication state is sensitive.

Anyone with access to:

```text
/app/.playwright/auth
```

may be able to reuse the authenticated browser session.

For this reason:

* the directory is stored in a dedicated Docker volume;
* it is excluded from Git;
* backups should be protected appropriately.

## Docker Volumes

Only three Docker volumes contain persistent runtime information.

| Volume          | Sensitivity |
| --------------- | ----------- |
| automation_auth | High        |
| caddy_data      | High        |
| caddy_config    | Medium      |

Generated reports are intentionally excluded because they are temporary.

## Running as Non-Root

The application container runs as the dedicated user:

```text
automation
```

The container does not execute as `root`.

This limits filesystem access in the event of an application compromise.

## Secrets

Sensitive information includes:

* `.env`;
* API token;
* Dinantia credentials;
* Playwright storage state;
* TLS private keys;
* backup archives containing any of the above.

These files should:

* remain outside Git;
* have restricted filesystem permissions;
* be included in secure backup procedures.

## Docker Host

Container security also depends on the Docker host.

Production administrators should:

* keep Docker updated;
* install operating system security updates;
* restrict SSH access;
* avoid unnecessary privileged containers.

## Future Authentication

The current deployment intentionally uses a single static API token.

Future versions may introduce:

* multiple API users;
* token rotation;
* OAuth;
* OpenID Connect;
* audit logging;
* fine-grained authorization.

These capabilities are intentionally outside the scope of the current architecture.

## Security Philosophy

The deployment intentionally minimizes the attack surface.

Persistent state is reduced to the minimum required for operation.

Browser instances remain ephemeral.

Secrets remain externalized.

The application exposes a single HTTPS entry point.

Operational simplicity is considered a security feature rather than merely a convenience.

# Concurrency Limitation

Automation execution is serialized within one Python process.

Production must therefore use:

```text
one Uvicorn worker
one automation container
```

Do not:

* increase the Uvicorn worker count;
* scale the `automation` service horizontally;
* start multiple replicas sharing the same account;
* bypass the Automation Lock.

Future scalability requires a different architecture, such as an external job queue or distributed concurrency control.

It must not be implemented by weakening the current execution guarantees.

# Health Monitoring

The application exposes:

```text
GET /health
```

This endpoint can be used by:

* uptime monitoring services
* infrastructure monitoring
* deployment validation
* reverse proxies

Example:

```bash
curl --fail --silent https://automation.example.com/health
```

A successful request returns:

```json
{"status":"ok"}
```

The health endpoint confirms that the API process is responding.

It does not execute Playwright or validate the current Dinantia session.

# Monitoring and Health Checks

The Automation Framework intentionally exposes a minimal monitoring interface.

The current deployment provides one public health endpoint:

```text
GET /health
```

Its purpose is to indicate that the HTTP API is operational.

## What the Health Endpoint Verifies

A successful response confirms that:

* the FastAPI application is running;
* the HTTP server is accepting requests;
* routing is functioning correctly;
* the application process is responsive.

Typical response:

```json
{"status":"ok"}
```

This endpoint is suitable for:

* uptime monitoring;
* reverse proxy health checks;
* deployment validation;
* container orchestration;
* external monitoring services.

Example:

```bash
curl --fail --silent https://automation.example.com/health
```

## What the Health Endpoint Does Not Verify

The health endpoint intentionally does **not** execute a browser automation.

Therefore it does not verify:

* Playwright startup;
* Chromium availability;
* Dinantia availability;
* Dinantia credentials;
* validity of the stored authentication session;
* report generation.

Keeping the endpoint lightweight avoids unnecessary browser startup and allows health checks to run frequently without affecting normal operation.

## Operational Monitoring

A production administrator should monitor:

* container status;
* HTTPS availability;
* API response time;
* API error rate;
* disk usage;
* Docker volume usage;
* certificate validity.

Useful commands:

```bash
docker compose ps

docker compose logs --tail 100

docker volume ls
```

## Functional Monitoring

Infrastructure monitoring alone is not sufficient.

The recommended operational validation is a periodic end-to-end request using the public API.

A successful functional test verifies:

1. Bearer authentication.
2. Automation Lock.
3. Browser startup.
4. Playwright execution.
5. Dinantia authentication.
6. Report generation.
7. Temporary file cleanup.

This provides a much stronger indication of system health than the `/health` endpoint alone.

## Future Monitoring

The current deployment intentionally keeps monitoring simple.

Possible future enhancements include:

* Prometheus metrics;
* structured logging;
* request duration metrics;
* browser execution statistics;
* distributed tracing;
* alerting integration.

These capabilities should only be introduced when operational requirements justify the additional complexity.

# Troubleshooting

## Caddy cannot obtain a certificate

Check:

* DNS resolves to the correct public IP;
* ports 80 and 443 reach the server;
* no other application is using those ports;
* an invalid IPv6 record is not configured;
* Caddy logs contain the certificate error.

Commands:

```bash
docker compose logs caddy
```

```bash
dig automation.example.com
```

## The health endpoint is unavailable

Check container status:

```bash
docker compose ps
```

Check API logs:

```bash
docker compose logs automation
```

Check Caddy logs:

```bash
docker compose logs caddy
```

Validate the internal API from the Caddy container:

```bash
docker compose exec caddy \
  wget -qO- http://automation:8000/health
```

## The API returns `401 Unauthorized`

Check that the request contains:

```text
Authorization: Bearer <API_TOKEN>
```

Verify that the token matches `AUTOMATION_API_TOKEN` in `.env`.

Do not print the token in logs or shell history unnecessarily.

## The API returns `409 Conflict`

Another automation is already running.

Only one browser automation may execute at a time.

Retry after the current operation finishes.

## Dinantia authentication fails

Check:

* username and password in `.env`;
* whether the account can log in through a normal browser;
* API container logs;
* whether the stored session has become invalid.

The framework should automatically perform a new login when the stored session expires.

## Storage state is not preserved

Check the volume:

```bash
docker volume ls
```

Inspect the mounted directory:

```bash
docker compose exec automation \
  ls -la /app/.playwright/auth
```

Verify that Compose mounts:

```text
automation_auth:/app/.playwright/auth
```

## Permission denied when saving storage state

Inspect directory ownership:

```bash
docker compose exec automation \
  ls -ld /app/.playwright/auth
```

The directory must be writable by the `automation` user.

## Chromium fails to start

Check API logs:

```bash
docker compose logs automation
```

Rebuild the image without using cached layers:

```bash
docker compose build --no-cache automation
```

Then recreate the service:

```bash
docker compose up -d automation
```

# Production Checklist

Before exposing the deployment publicly, verify:

* DNS points to the server.
* Ports 80 and 443 are reachable.
* `.env` contains production values.
* The API token is strong and secret.
* Dinantia credentials are valid.
* `.env` is ignored by Git.
* Compose configuration validates.
* Caddy configuration validates.
* Both containers are running.
* HTTPS works without certificate warnings.
* `/health` returns `{"status":"ok"}`.
* The authenticated export endpoint works.
* The generated Excel file is valid.
* The storage state persists after container recreation.
* The API is not directly exposed on port 8000.
* Ruff, MyPy and Pytest are green.

# Architectural Decisions

The production deployment follows the same engineering principles as the rest of the Automation Framework.

Deployment decisions are intentionally conservative.

The objective is long-term maintainability rather than maximum feature count.

## Single Process

The application intentionally runs:

```text id="o5v0b9"
one container

one Uvicorn process

one worker
```

This guarantees that the Automation Lock protects every browser execution.

Supporting multiple workers would require a different concurrency architecture rather than a deployment change.

## Stateless Application

The application itself remains stateless.

Only the minimum operational state is persisted:

* Playwright authentication;
* TLS certificates;
* deployment configuration.

No application database exists.

No generated reports are stored permanently.

## Provider Isolation

Deployment infrastructure is completely provider-independent.

Docker, Docker Compose and Caddy know nothing about:

* Dinantia;
* future providers;
* Playwright workflows;
* business operations.

This mirrors the architectural separation implemented inside the framework itself.

## Minimal Infrastructure

The deployment intentionally avoids unnecessary infrastructure.

It does not require:

* Redis;
* RabbitMQ;
* PostgreSQL;
* MySQL;
* Kubernetes;
* background workers;
* distributed schedulers.

The current architecture does not justify these components.

Introducing them would increase operational complexity without improving the existing deployment model.

## Container Responsibilities

Each container has one responsibility.

### automation

Responsible for:

* HTTP API;
* browser automation;
* business operations.

### caddy

Responsible for:

* HTTPS;
* reverse proxy;
* certificate management.

Neither container performs the responsibilities of the other.

## Persistent State

Persistent state has been deliberately minimized.

| Persistent                | Ephemeral                  |
| ------------------------- | -------------------------- |
| Playwright session        | Browser instances          |
| TLS certificates          | Temporary downloads        |
| Deployment configuration  | Generated reports          |
| Environment configuration | Request-specific resources |

This reduces operational complexity while preserving browser authentication efficiency.

## Failure Isolation

Application failures should remain localized.

For example:

* restarting the application should not affect certificates;
* renewing certificates should not restart the API;
* browser failures should not affect deployment infrastructure.

Separating responsibilities into independent containers improves operational resilience.

## Deployment Philosophy

The deployment is designed around a simple principle:

> Persist only what cannot be recreated.

Everything else should be rebuilt automatically.

This philosophy simplifies:

* deployment;
* updates;
* rollback;
* disaster recovery;
* maintenance.

It also aligns with the architectural principles defined throughout the Automation Framework documentation.

# Related Documentation

* `architecture.md`
* `api-design.md`
* `authentication-and-sessions.md`
* `project-status.md`
* `roadmap.md`
* `testing-and-debugging.md`
