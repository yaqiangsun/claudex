"""Buddy companion implementation."""
import hashlib
from typing import Any, Literal

# Import types
from .types import (
    RARITIES,
    RARITY_WEIGHTS,
    STAT_NAMES,
    CompanionBones,
    Companion,
    Rarity,
    Species,
    Eye,
    Hat,
    StatName,
    Eye as EyeType,
    Hat as HatType,
    Species as SpeciesType,
)


def _mulberry32(seed: int):
    """Mulberry32 — tiny seeded PRNG."""
    a = seed & 0xFFFFFFFF

    def next_random() -> float:
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = (a ^ (a >> 15)) * (1 | a)
        t = (t + ((t ^ (t >> 7)) * (61 | t))) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    return next_random


def _hash_string(s: str) -> int:
    """Hash string to 32-bit integer."""
    h = 2166136261
    for char in s:
        h ^= ord(char)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _pick(rng, arr: list) -> Any:
    """Pick random element from array."""
    return arr[int(rng() * len(arr))]


def _roll_rarity(rng) -> Rarity:
    """Roll for rarity based on weights."""
    total = sum(RARITY_WEIGHTS.values())
    roll = rng() * total
    for rarity in RARITIES:
        roll -= RARITY_WEIGHTS[rarity]
        if roll < 0:
            return rarity
    return 'common'


RARITY_FLOOR = {
    'common': 5,
    'uncommon': 15,
    'rare': 25,
    'epic': 35,
    'legendary': 50,
}


def _roll_stats(rng, rarity: Rarity) -> dict[StatName, int]:
    """Roll stats - one peak, one dump, rest scattered."""
    floor = RARITY_FLOOR[rarity]
    peak = _pick(rng, STAT_NAMES)
    dump = _pick(rng, STAT_NAMES)
    while dump == peak:
        dump = _pick(rng, STAT_NAMES)

    stats: dict[StatName, int] = {}
    for name in STAT_NAMES:
        if name == peak:
            stats[name] = min(100, floor + 50 + int(rng() * 30))
        elif name == dump:
            stats[name] = max(1, floor - 10 + int(rng() * 15))
        else:
            stats[name] = floor + int(rng() * 40)
    return stats


SALT = 'friend-2026-401'


class Roll:
    """Result of rolling a companion."""

    def __init__(self, bones: CompanionBones, inspiration_seed: int):
        self.bones = bones
        self.inspiration_seed = inspiration_seed


def _roll_from(rng) -> Roll:
    """Create a roll from RNG."""
    from .types import EYES, HATS, SPECIES

    rarity = _roll_rarity(rng)
    bones = CompanionBones(
        rarity=rarity,
        species=_pick(rng, SPECIES),
        eye=_pick(rng, EYES),
        hat=rarity == 'common' and 'none' or _pick(rng, HATS),
        shiny=rng() < 0.01,
        stats=_roll_stats(rng, rarity),
    )
    return Roll(bones, int(rng() * 1e9))


# Cache for roll results
_roll_cache: dict[str, Roll] = {}


def roll(user_id: str) -> Roll:
    """Roll companion for user ID (cached)."""
    key = user_id + SALT
    if key in _roll_cache:
        return _roll_cache[key]
    value = _roll_from(_mulberry32(_hash_string(key)))
    _roll_cache[key] = value
    return value


def roll_with_seed(seed: str) -> Roll:
    """Roll companion with specific seed."""
    return _roll_from(_mulberry32(_hash_string(seed)))


def companion_user_id() -> str:
    """Get user ID for companion."""
    # TODO: implement with actual config
    from ..utils.config import get_global_config

    config = get_global_config()
    if hasattr(config, 'oauth_account') and config.oauth_account:
        return config.oauth_account.account_uuid
    if hasattr(config, 'userID'):
        return config.userID
    return 'anon'


def get_companion() -> Companion | None:
    """Get companion from config."""
    from ..utils.config import get_global_config

    config = get_global_config()
    if not hasattr(config, 'companion') or not config.companion:
        return None

    stored = config.companion
    bones_result = roll(companion_user_id())
    bones = bones_result.bones

    return Companion(
        rarity=bones.rarity,
        species=bones.species,
        eye=bones.eye,
        hat=bones.hat,
        shiny=bones.shiny,
        stats=bones.stats,
        name=stored.name,
        personality=stored.personality,
        hatched_at=stored.hatched_at,
    )


__all__ = [
    'roll',
    'roll_with_seed',
    'companion_user_id',
    'get_companion',
    'Roll',
]