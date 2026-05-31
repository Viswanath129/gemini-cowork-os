# Security Policy

## Supported Versions

Currently, only the `main` branch (unreleased Alpha) is actively developed. 

## Reporting a Vulnerability

If you discover a security vulnerability in Gemini Cowork OS—particularly bypasses of the Human-In-The-Loop (HITL) approval system, sandbox escapes, or prompt injection vectors that result in unauthorized file system access—please do not report it publicly.

Instead, please email `security@example.com` (placeholder) with the details.

## Threat Model

Gemini Cowork OS relies heavily on LLM reasoning to execute local tools. 
By default:
1. Destructive tools (Delete, Overwrite, Email) MUST have `requires_approval=True`.
2. The runtime is designed to be executed inside an isolated Docker container or VM.
3. Running this OS on your host machine with highly privileged credentials is not recommended during the Alpha phase.
