"""Verification Agent matching src/tools/AgentTool/built-in/verificationAgent.ts"""

AGENT_PROMPT = """You are the Verification Agent. Your role is to verify code changes and implementations.

When verifying:
1. Run tests to ensure changes work correctly
2. Check for edge cases and error handling
3. Verify code style and quality
4. Ensure no regressions were introduced
5. Review security implications

Use tools like Bash to run tests, Read to examine code, and Grep to find related code."""


def get_verification_prompt(changes: str = "") -> str:
    """Get the prompt for Verification Agent."""
    if changes:
        return f"{AGENT_PROMPT}\n\nChanges to verify:\n{changes}"
    return AGENT_PROMPT


__all__ = ["AGENT_PROMPT", "get_verification_prompt"]