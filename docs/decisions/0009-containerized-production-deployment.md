# ADR 0009 — Containerized Production Deployment

> Status: Accepted
> Date: 2026-07-13

# Context

Automation Framework exposes browser automations through a FastAPI HTTP API.

The framework had already reached production quality regarding:

* layered architecture;
* reusable infrastructure;
* Playwright integration;
* HTTP API;
* authentication;
* documentation;
* testing.

The remaining work consisted of defining a production deployment architecture that preserved these engineering principles.

The deployment architecture needed to:

* remain simple;
* avoid unnecessary infrastructure;
* support HTTPS;
* persist authenticated browser sessions;
* preserve the current concurrency guarantees;
* require minimal operational maintenance.

# Decision

The production deployment is based on Docker Compose.

The deployment consists of two containers.

```text
Internet
    │
    ▼
Caddy
    │
    ▼
Automation Framework
```

## Application Container

The application container is responsible for:

* FastAPI;
* Uvicorn;
* Playwright;
* browser automation;
* business operations.

It runs:

* one process;
* one Uvicorn worker.

The application is not exposed directly to the public network.

## Reverse Proxy

Caddy is used as the reverse proxy.

Caddy provides:

* HTTPS termination;
* automatic certificate management;
* HTTP to HTTPS redirection;
* reverse proxy functionality.

The application is only reachable through the internal Docker network.

## Persistent State

The deployment intentionally minimizes persistent state.

Only the following information is persisted:

* Playwright authentication state;
* TLS certificates;
* deployment configuration.

Browser instances remain ephemeral.

Generated reports remain request-scoped.

## Authentication

Two authentication mechanisms remain independent.

External clients authenticate using the API Bearer token.

Browser automation authenticates independently against Dinantia.

No deployment component combines these responsibilities.

## Concurrency

The deployment intentionally supports:

* one automation container;
* one Uvicorn process;
* one worker.

The existing Automation Lock relies on this execution model.

Scaling through multiple workers or multiple application replicas is explicitly outside the scope of the current architecture.

# Consequences

## Positive

The deployment:

* remains simple;
* is easy to understand;
* requires minimal operational knowledge;
* supports automatic HTTPS;
* minimizes persistent runtime state;
* preserves browser authentication across requests;
* aligns with the existing layered architecture.

The application can be rebuilt or recreated without losing operational state.

Recovery procedures remain straightforward.

## Negative

The deployment intentionally does not provide:

* horizontal scaling;
* distributed execution;
* high availability;
* load balancing;
* request queues;
* background workers.

These capabilities require architectural changes rather than deployment changes.

# Alternatives Considered

## Nginx

Nginx would satisfy the reverse proxy requirements.

However, it requires additional certificate management infrastructure.

Caddy provides automatic HTTPS with substantially less operational complexity.

## Apache HTTP Server

Apache was considered unnecessarily complex for the current deployment requirements.

## Direct FastAPI Exposure

Publishing the FastAPI application directly to the Internet was rejected.

Using a dedicated reverse proxy provides:

* TLS termination;
* certificate management;
* network isolation;
* simpler application configuration.

## Multiple Uvicorn Workers

Multiple workers were rejected because they invalidate the current Automation Lock guarantees.

Supporting multiple workers would require a different concurrency architecture.

## Kubernetes

Container orchestration platforms such as Kubernetes were considered outside the current operational requirements.

The deployment intentionally optimizes for simplicity.

Docker Compose provides all required functionality with significantly lower operational overhead.

# Compliance

This deployment remains consistent with the architectural principles defined by the Automation Framework.

In particular it preserves:

* layered architecture;
* provider isolation;
* reusable infrastructure;
* business-oriented APIs;
* explicit dependency management;
* minimal operational complexity.
