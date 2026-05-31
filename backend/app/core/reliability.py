import asyncio
import time
import logging
from typing import Callable, Any, Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ToolReliabilityConfig(BaseModel):
    max_retries: int = 3
    timeout_seconds: float = 30.0
    backoff_factor: float = 2.0
    fallback_result: Optional[Any] = None

class ReliabilityWrapper:
    """
    Ensures 'Ugly Real-World Tools' survive failures.
    Handles: Retries, Timeouts, Exponential Backoff, and Fallbacks.
    """
    @staticmethod
    async def execute_with_reliability(
        func: Callable, 
        args: Dict[str, Any], 
        config: ToolReliabilityConfig
    ) -> Any:
        attempt = 0
        current_delay = 1.0
        
        while attempt < config.max_retries:
            attempt += 1
            try:
                # Execution with timeout
                return await asyncio.wait_for(func(**args), timeout=config.timeout_seconds)
                
            except (asyncio.TimeoutError, Exception) as e:
                logger.warning(f"Tool Failure (Attempt {attempt}): {str(e)}")
                
                if attempt >= config.max_retries:
                    if config.fallback_result is not None:
                        logger.error(f"Tool permanently failed after {attempt} retries. Returning fallback.")
                        return config.fallback_result
                    raise e
                
                # Exponential Backoff
                await asyncio.sleep(current_delay)
                current_delay *= config.backoff_factor

class ToolHealthMonitor:
    """Tracks tool success rates and 'Circuit Breakers' if a tool is persistently down."""
    def __init__(self):
        self.stats: Dict[str, Dict[str, int]] = {}

    def record_call(self, tool_name: str, success: bool):
        if tool_name not in self.stats:
            self.stats[tool_name] = {"success": 0, "failure": 0}
        
        key = "success" if success else "failure"
        self.stats[tool_name][key] += 1
        
        # Check for Circuit Breaker (e.g., > 5 failures in a row)
        if self.stats[tool_name]["failure"] > 10 and self.stats[tool_name]["success"] == 0:
            logger.critical(f"CIRCUIT BREAKER: Tool '{tool_name}' is persistently failing. Disabling tool.")
