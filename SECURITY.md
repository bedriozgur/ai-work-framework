# Security and Disclosure Policy

## Scope

This repository contains reusable framework policy and tooling. It must not contain live credentials, secrets, tokens, private infrastructure identifiers, customer-confidential evidence, personal account state, or data whose disclosure is not explicitly authorized.

## Reporting a security issue

Do not open a public issue containing sensitive details. Contact the repository owner through a private channel and include the affected file/revision, exposure, and recommended containment. A public security contact will be added only when the repository's publication and support model is finalized.

## Repository boundary

The intended public/core layer contains universal governance, protocol, structural templates, validator code, tests, and non-sensitive examples.

The following belong outside a public core:

- personal workflow and account context;
- hostnames, internal addresses, credentials, or deployment inventory;
- customer-specific facts, topology, contracts, logs, and support bundles;
- provider-specific operational prompts that contain private configuration;
- third-party-derived material without recorded provenance and reuse rights.

Until repository visibility and licensing are explicitly decided, treat publication as unresolved. Do not add new personal, customer-adjacent, or third-party-derived content.

## Runtime claims

Prompt text is not a security boundary. A project may claim `read-only`, `isolated`, `confidential`, or `approval-gated` only when its Enforcement Register identifies the technical mechanism, verifier, verification date, result, and limitations.

