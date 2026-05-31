# Release v0.1.0-alpha (Architecture Preview)

We are thrilled to open-source the architecture for **Gemini Cowork OS**.

## Vision
To build an operating environment for human-AI decision making that helps humans make better decisions while preserving their agency.

## Implemented Architecture
This release establishes the core structural foundation:
- **Execution Kernel**: Definitions for DAG-based execution and checkpointing.
- **Swarm Intelligence**: Foundations for parallel asyncio agent workers and a Shared Blackboard.
- **Governance**: Scaffolding for the Goal Guardian, Judgment Engine, and Observability Layer.
- **Forensic Validation**: The complete Alpha Testing matrix (Benchmarks A-Z) and forensic tracking artifacts (`KILLED_ASSUMPTIONS.md`, `TIMES_THE_METRICS_LIED.md`).

## ⚠️ Alpha Disclaimer & Known Limitations
This is an **Architecture Preview**, not a fully functional product. 
- LLM interactions inside `Agent.run_task` are currently mocked.
- Browser automation and Deliverable generation are stubs.
- The React UI is a static scaffold.

We are releasing this now to validate the *design philosophy* with the open-source community before wiring up the final LLM integrations.

## Future Roadmap (Phase 2)
1. Wire up `google-genai` / LiteLLM for actual ReAct loops.
2. Implement the Playwright browser controller.
3. Build out the Mission Control React dashboards to visualize the Observability Layer telemetry.
4. Execute the first 50 missions to populate the Alpha Test Logs.
