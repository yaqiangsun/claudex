"""Cost hook for tracking usage."""
from .cost_tracker import (
    get_cost_counter,
    get_total_cost_usd,
    get_total_input_tokens,
    get_total_output_tokens,
    reset_cost_state,
)


def use_cost_tracking():
    """Hook for cost tracking."""
    return {
        'cost': get_total_cost_usd(),
        'input_tokens': get_total_input_tokens(),
        'output_tokens': get_total_output_tokens(),
    }


__all__ = ['use_cost_tracking', 'reset_cost_state']