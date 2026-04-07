"""Run agent matching src/tools/AgentTool/runAgent.ts"""
from typing import Dict, Any, Optional, Callable
from .constants import AgentStatus
from .agent_memory import AgentMemory
from .agent_tool_utils import AgentToolUtils


class RunAgent:
    """Handles running an agent."""

    def __init__(
        self,
        run_callback: Optional[Callable] = None,
        max_iterations: int = 100,
    ):
        self.run_callback = run_callback
        self.max_iterations = max_iterations

    def run(
        self,
        agent_id: str,
        prompt: str,
        tools: Optional[list[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run an agent with the given prompt."""
        memory = AgentMemory(agent_id)
        memory.set_context("initial_prompt", prompt)
        if context:
            for key, value in context.items():
                memory.set_context(key, value)

        status = AgentStatus.RUNNING
        iterations = 0
        result = None

        while status == AgentStatus.RUNNING and iterations < self.max_iterations:
            iterations += 1

            # Process one iteration
            if self.run_callback:
                try:
                    result = self.run_callback(memory, tools or [])
                    memory.add_entry(f"Iteration {iterations}: {result}", "action")

                    # Check if should stop
                    if result.get("done"):
                        status = AgentStatus.COMPLETED
                except Exception as e:
                    memory.add_entry(f"Error: {e}", "error")
                    status = AgentStatus.FAILED
                    result = {"error": str(e)}
            else:
                # No callback provided, complete immediately
                status = AgentStatus.COMPLETED
                result = {"output": "Agent executed", "done": True}

        if iterations >= self.max_iterations:
            status = AgentStatus.FAILED
            result = {"error": "Max iterations reached"}

        return {
            "agent_id": agent_id,
            "status": status,
            "iterations": iterations,
            "result": result,
            "memory": memory.get_history(),
        }


__all__ = ["RunAgent"]