# Gemini Cowork OS

An experimental operating system framework for studying human-AI decision making. 

**Lead Differentiator**: **Mission Ownership Engine.** We move beyond simple "Task Execution" to "Outcome Ownership." The system doesn't just run code; it accepts responsibility for achieving the final strategic objective (e.g., training the best model, delivering a verified report) end-to-end.

**Current Status**: v0.1.0-alpha (Architecture Preview)

---

### 📄 [CLAIMS_VS_EVIDENCE.md](docs/CLAIMS_VS_EVIDENCE.md) | 📄 [ARCHITECTURE_OVERVIEW.md](docs/ARCHITECTURE_OVERVIEW.md) | 📄 [REPOSITORY_AUDIT.md](docs/REPOSITORY_AUDIT.md) | 📄 [BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md) | 📄 [KILLED_ASSUMPTIONS.md](results/KILLED_ASSUMPTIONS.md)

---

## 🧪 Research Mission
Gemini Cowork OS is not a finished product; it is a **forensic research platform**. We explore how autonomous systems can move from "Prompt Execution" to "Alignment-First Collaboration." Our focus is on trust, judgment, and the empirical measurement of human-AI synergy.

## 🎯 Core Principles
- **Evidence over assumptions**: We prioritize what users actually do over architectural theories.
- **Decision quality over task completion**: Success is measured by the improvement in human decision-making.
- **Transparency over hype**: All claims are tracked via `CLAIMS_VS_EVIDENCE.md`.
- **Human agency over automation**: The system clarifies and challenges, but the user owns the decision.
- **Permission Before Authority**: Credentials must remain local and out-of-chat; authority is delegated intentionally, never assumed.

## 🛠️ How This Repository Was Built
This repository is a self-referential experiment. Much of the architecture, code scaffolding, documentation, and evaluation frameworks were generated and refined through a custom **Gemini Cowork** process itself.

In this workflow:
1. **The Human (Kasiviswanath Vegisetti)**: Conceived the vision, defined the strategic direction, audited implementation risks, and directed the multi-phase roadmap.
2. **The AI (Gemini Cowork)**: Generated the technical architecture, implemented the initial Python scaffolding, drafted the forensic documentation, and codified the chaos benchmarks.

This collaboration allows for a level of structural rigor and documentation depth that exceeds traditional single-author prototypes.

## 🧠 Core Architecture
```text
Mission Control
        │
Execution Kernel (Checkpointing & Deadlock Detection)
        │
Orchestrator (Ambiguity Gates & Re-planning)
        │
Goal Guardian (Drift Prevention)
        │
Agent Swarm (Parallel Execution)
        │
Shared Blackboard (Coordination)
        │
Trust Engine (Claim-to-Source Traceability)
```

## ✨ Core Features
- **Execution Kernel**: Persistent state checkpointing and recovery. Survives power failures during 4-hour jobs.
- **Ambiguity Gates**: The system asks clarifying questions *before* wasting tokens on vague goals.
- **Parallel Swarms**: Scales to N concurrent agents using `asyncio` worker pools and Shared Blackboard coordination.
- **Trust Engine**: Every claim in a generated deliverable is traceable to its source and the agent that found it.
- **Mission Control**: Forensic observability tracking Meaningful Work Ratio, Cost, and Token Burn in real-time.

## 📦 Installation

```bash
git clone https://github.com/your-org/gemini-cowork-os.git
cd gemini-cowork-os

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install
```

## ⚡ Quick Start

Start the Execution Kernel and API:
```bash
uvicorn backend.app.main:app --reload
```

Start the Mission Control UI:
```bash
cd frontend
npm run dev
```

Submit your first goal via API:
```bash
curl -X POST http://localhost:8000/api/v1/goals \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Research the top 100 AI startups and generate a PPTX."}'
```

## 🧪 The Benchmark Philosophy
We do not optimize for standard LLM benchmarks. We optimize for **Human Collaboration Entropy**. See our `BENCHMARK_PROTOCOL.md` for our "Chaos Matrix" (Ambiguity Attacks, Broken Inputs, Contradictory Humans).

## 🤝 Contributing
We welcome contributions from AI engineers, researchers, and agent developers. See `CONTRIBUTING.md`.

## 📜 License
MIT License.
