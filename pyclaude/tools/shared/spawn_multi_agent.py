"""Spawn multi-agent matching src/tools/shared/spawnMultiAgent.ts"""
from typing import List, Dict, Any, Optional, Callable
import asyncio


class MultiAgentSpawner:
    """Handles spawning multiple agents for parallel execution."""

    def __init__(self, agent_factory: Callable):
        self.agent_factory = agent_factory

    async def spawn_parallel(
        self,
        prompts: List[str],
        agent_type: str = "general-purpose",
    ) -> List[Dict[str, Any]]:
        """Spawn multiple agents to run in parallel."""
        tasks = [self._spawn_one(prompt, agent_type) for prompt in prompts]
        return await asyncio.gather(*tasks)

    async def spawn_sequential(
        self,
        prompts: List[str],
        agent_type: str = "general-purpose",
    ) -> List[Dict[str, Any]]:
        """Spawn multiple agents to run sequentially."""
        results = []
        for prompt in prompts:
            result = await self._spawn_one(prompt, agent_type)
            results.append(result)
        return results

    async def _spawn_one(self, prompt: str, agent_type: str) -> Dict[str, Any]:
        """Spawn a single agent."""
        agent = self.agent_factory(agent_type)
        return await agent.run(prompt)


async def spawn_multi_agent(
    prompts: List[str],
    mode: str = "parallel",
    agent_type: str = "general-purpose",
    agent_factory: Optional[Callable] = None,
) -> List[Dict[str, Any]]:
    """Spawn multiple agents based on mode."""
    if agent_factory is None:
        raise ValueError("agent_factory is required")

    spawner = MultiAgentSpawner(agent_factory)

    if mode == "parallel":
        return await spawner.spawn_parallel(prompts, agent_type)
    elif mode == "sequential":
        return await spawner.spawn_sequential(prompts, agent_type)
    else:
        raise ValueError(f"Unknown mode: {mode}")


__all__ = ["MultiAgentSpawner", "spawn_multi_agent"]