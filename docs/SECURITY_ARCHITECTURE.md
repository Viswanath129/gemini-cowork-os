# Security Architecture: Permission & Authority

A true digital teammate must enforce a strict separation between **Reasoning** and **Authority**. Gemini Cowork OS v2 moves toward an "Out-of-Chat" security model to prevent the exposure of secrets and ensure human agency.

## 1. Principle: Permission Before Authority
The system should never silently acquire or assume authority. Credentials must remain local to the human principal's environment, never appearing in the LLM reasoning context or chat logs.

## 2. Secure Credential Layers

### 🟢 Level 1: Read-Only (Always Allowed)
Access to public datasets, non-sensitive local files (specified in `.coworkignore`), and internal project memory.

### 🟡 Level 2: Draft & Propose (Auto-Report)
The ability to draft emails, generate reports, or create branch commits. The system acts, but reports results immediately to Mission Control for audit.

### 🟠 Level 3: Authenticated Action (Ask Once)
High-stakes operations like creating a GitHub repository or sending a Slack message. 
- **Requirement**: Cowork initiates a local OAuth flow or reads from a local Secret Vault (e.g., Windows Credential Manager).
- **Control**: User approves the "Authority Delegation" once per session.

### 🔴 Level 4: High-Stakes (Mandatory Approval)
Spending money, permanent file deletion, or publishing to production.
- **Requirement**: Mandatory cryptographic or token-based human approval *at the moment of execution*.

## 3. Implementation Roadmap: Identity Layer
1. **Local Secret Store**: Replace hardcoded tokens with lookups to local OS-level credential managers.
2. **MCP Auth Handshake**: Use the Model Context Protocol to standardize how tools request temporary authority.
3. **Audit Trail**: Every delegated action is logged in `FAILURE_REPORT.csv` if it deviates from the Mission Brief.

## 4. Why We Don't Ask for Tokens in Chat
Asking a user to "Paste your token" is a failure of teammate judgment. It exposes secrets to history and trains users in bad security habits. A mature digital coworker handles authentication via local, secure, and established industry standards (OAuth/Vaults).
