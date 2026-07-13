# Infrastructure

This directory contains infrastructure components shared across multiple applications deployed on the same server.

These components are intentionally separated from the Automation Framework application to keep infrastructure concerns independent from application logic.

## Current Components

### Caddy

Location:

```text
infrastructure/caddy/
```

Responsibilities:

* Reverse proxy
* Automatic HTTPS
* TLS certificate management
* HTTP to HTTPS redirection
* Routing requests to application containers

The Caddy stack is deployed independently from the application stack.

## Docker Network

Applications communicate through the shared external Docker network:

```text
proxy
```

Infrastructure components expose public services.

Applications connect to the shared network but do not publish HTTP ports directly.

## Deployment Model

The production environment consists of independent Docker Compose stacks.

Example:

```text
Internet
    │
    ▼
Caddy
    │
    ▼
Docker network: proxy
    │
    ├── Automation Framework
    ├── WordPress
    ├── Odoo
    └── Future applications
```

Each application is responsible only for its own business logic.

Shared infrastructure is managed separately.

## Design Principles

Infrastructure components should:

* remain reusable across multiple applications;
* be version-controlled together with the repository;
* be deployable independently;
* avoid coupling with application-specific logic.

Infrastructure should be shared whenever multiple applications can benefit from the same component.

## Related Documentation

* `../docs/deployment.md`
* `../docs/decisions/0009-containerized-production-deployment.md`
