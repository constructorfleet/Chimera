# Chimera

![Chimera Logo](assets/chimera-logo.svg)

Chimera is a multi-modal routing platform that stitches audio, vision, and language systems together over a message-driven backbone. This repository contains the infrastructure skeleton needed to bootstrap development across the bus, services, and deployment layers.

## Project layout

- `backbone/` – broker, cache, and streaming configuration plus backup helpers.
- `ansible/` – playbooks and templates for distributing the bus stack.
- `services/` – individual service packages sharing the `lattice` common utilities.
- `docker/` – base Docker images shared across services.
- `tests/` – verification of the scaffold structure.

## Python version

All Python components target **Python 3.14** to align with the shared base images and dependencies.
