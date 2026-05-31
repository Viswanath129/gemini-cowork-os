# Architecture Overview

Gemini Cowork OS shifts the focus from "Prompt -> Response" to a persistent, parallel, and observable operating environment.

## Data Flow Diagram

```mermaid
graph TD
    User([User]) -->|High-Level Goal| API[FastAPI Gateway]
    API --> Orchestrator
    
    subgraph Execution Layer
        Orchestrator -->|Detects Ambiguity| Interpreter[Goal Interpreter]
        Interpreter -->|Generates DAG| Kernel[Execution Kernel]
        Kernel -->|Checkpoints State| DB[(Local Storage)]
        Kernel -->|Dispatches| Engine[Execution Engine]
    end
    
    subgraph Swarm Layer
        Engine --> Swarm[Agent Swarm]
        Swarm --> A1[Researcher]
        Swarm --> A2[Data Analyst]
        Swarm --> A3[QA Agent]
        
        A1 <--> Blackboard[Shared Blackboard]
        A2 <--> Blackboard
        A3 <--> Blackboard
    end
    
    subgraph Governance Layer
        Engine --> Guardian[Goal Guardian]
        Guardian -->|Re-anchors| Orchestrator
        Engine --> Obs[Observability Layer]
        Obs -->|Metrics| MissionControl[Mission Control UI]
    end
    
    subgraph Deliverables
        A3 --> Factory[Deliverable Factory]
        A3 --> Trust[Trust Engine]
    end
```

## Component Breakdown

1. **Orchestrator**: The entry point. Runs the user's prompt through the Judgment Engine to detect material ambiguity before executing.
2. **Execution Kernel**: The heart of the OS. Saves the state of the DAG after every step. Detects deadlocks and handles resuming from failure.
3. **Agent Swarm & Blackboard**: An `asyncio`-driven worker pool. Agents post findings to a Shared Blackboard. Findings must be "Promoted" to become Canonical Knowledge.
4. **Goal Guardian**: A supervisory loop that runs every N steps to compare current progress against the original objective to prevent agent drift.
5. **Observability Layer**: Tracks Latency, Tokens, Cost, Meaningful Work Ratio (MWR), and Judgment Accuracy Score (JAS).
6. **Trust Engine**: Maintains the Explainability Graph. `Claim -> Evidence -> Source -> Agent`.
