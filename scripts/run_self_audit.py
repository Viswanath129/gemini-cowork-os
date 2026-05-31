import asyncio
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.orchestrator import Orchestrator
from backend.app.core.benchmarks import BenchmarkRunner, BenchmarkTask

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_audit():
    """
    Executes Benchmark 3: Analyze GitHub repository and generate improvement plan.
    This provides empirical evidence of the autonomous loop.
    """
    logger.info("--- STARTING SELF-AUDIT MISSION ---")
    
    orchestrator = Orchestrator(checkpoint_dir=".checkpoints_audit")
    runner = BenchmarkRunner(orchestrator)
    
    task = BenchmarkTask(
        id="self-audit-01",
        goal="Analyze the current Gemini Cowork OS repository files and generate a prioritized improvement plan for Phase 2.",
        expected_outcome_type="report"
    )
    
    # Execute the suite
    await runner.run_suite([task])
    
    # Generate and print the report
    report = runner.generate_report()
    logger.info("--- MISSION COMPLETE ---")
    print("\nEMPIRICAL VALIDATION REPORT")
    print("============================")
    for category, stats in report.items():
        print(f"\n[{category}]")
        for key, value in stats.items():
            print(f"- {key}: {value}")

if __name__ == "__main__":
    asyncio.run(run_audit())
