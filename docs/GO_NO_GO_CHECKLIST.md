# Go/No-Go Release Checklist

This checklist must be verified before any public push to the GitHub repository.

## Repository Integrity
- [ ] No API keys committed (Check `.env`, logs, and config files).
- [ ] No secrets committed.
- [ ] No local machine paths (Check `os.getcwd()` and hardcoded strings).
- [ ] No personal information.
- [ ] No temporary files (Check `.gitignore` for `.checkpoints/`, `__pycache__/`, etc.).
- [ ] No large unnecessary assets.

## Build Verification
- [ ] Backend starts successfully (`uvicorn backend.app.main:app`).
- [ ] Frontend starts successfully (`npm run dev`).
- [ ] Installation guide verified on clean machine.
- [ ] Environment variables documented (`.env.example`).

## Documentation Verification
- [ ] README accurate and sets correct expectations.
- [ ] Architecture diagrams match current implementation.
- [ ] Claims mapped to evidence (`CLAIMS_VS_EVIDENCE.md`).
- [ ] Known limitations documented.

## Open Source Readiness
- [ ] License selected (MIT).
- [ ] Contributing guide present.
- [ ] Security policy present.
- [ ] Code of conduct present.

## Alpha Honesty Check
- [ ] Mocked systems (LLM ReAct loop) clearly labeled.
- [ ] Unverified systems (Playwright, Docx) clearly labeled.
- [ ] Experimental components (Judgment Engine) clearly labeled.
- [ ] Benchmark results separated from future goals.

---

## Final Question
If an experienced engineer cloned this repository today, would they feel misled?

**STATUS**: [PENDING]
