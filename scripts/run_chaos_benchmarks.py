import asyncio
import sys
import os
import logging
from pydantic import BaseModel

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.orchestrator import Orchestrator
from backend.app.core.benchmarks import BenchmarkRunner, BenchmarkTask
from backend.app.core.models import TaskStatus

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChaosScenario(BaseModel):
    id: str
    name: str
    goal: str
    inject_fault: str # CORRUPT_INPUT, BROKEN_TOOL, CONTRADICTORY_GOAL, MID_MISSION_PIVOT

async def run_chaos_benchmarks():
    """
    Executes adversarial 'Chaos Benchmarks' to investigate failure modes.
    """
    logger.info("--- STARTING CHAOS BENCHMARK SUITE ---")
    
    orchestrator = Orchestrator(checkpoint_dir=".checkpoints_chaos")
    runner = BenchmarkRunner(orchestrator)
    
    scenarios = [
        ChaosScenario(
            id="chaos-01",
            name="Corrupted PDF Input",
            goal="Process the provided research folder (Scenario: Contains 2 corrupted PDFs).",
            inject_fault="CORRUPT_INPUT"
        ),
        ChaosScenario(
            id="chaos-02",
            name="Primary Tool Failure",
            goal="Research Indian semiconductor trends (Scenario: Primary Search API is disabled).",
            inject_fault="BROKEN_TOOL"
        ),
        ChaosScenario(
            id="chaos-03",
            name="Mid-Mission Pivot",
            goal="Analyze AI robotics market (Scenario: Pivot to 'Humanoid only' halfway).",
            inject_fault="MID_MISSION_PIVOT"
        )
    ]
    
    tasks = [BenchmarkTask(id=s.id, goal=s.goal, expected_outcome_type="report") for s in scenarios]
    
    # Execute Chaos Suite
    await runner.run_suite(tasks)
    
    # Generate and print the report
    report = runner.generate_report()
    
    logger.info("--- CHAOS SUITE COMPLETE ---")
    print("\nFORENSIC FAILURE INVESTIGATION REPORT")
    print("======================================")
    for category, stats in report.items():
        print(f"\n[{category}]")
        for key, value in stats.items():
            print(f"- {key}: {value}")
            
    # Add Repair Efficacy details
    efficacy = orchestrator.obs_global.get_repair_efficacy()
    print("\n[Autonomous Repair Efficacy]")
    for key, value in efficacy.items():
        print(f"- {key}: {value}")

if __name__ == "__main__":
    asyncio.run(run_chaos_benchmarks())
