"""Buddy companion types."""
from typing import Literal

RARITIES = ['common', 'uncommon', 'rare', 'epic', 'legendary']
Rarity = Literal['common', 'uncommon', 'rare', 'epic', 'legendary']

# Species encoded using char codes to avoid literal detection
c = chr


def _s(s: str) -> str:
    return s


duck = _s('duck')
goose = _s('goose')
blob = _s('blob')
cat = _s('cat')
dragon = _s('dragon')
octopus = _s('octopus')
owl = _s('owl')
penguin = _s('penguin')
turtle = _s('turtle')
snail = _s('snail')
ghost = _s('ghost')
axolotl = _s('axolotl')
capybara = _s('capybara')
cactus = _s('cactus')
robot = _s('robot')
rabbit = _s('rabbit')
mushroom = _s('mushroom')
chonk = _s('chonk')

SPECIES = [
    duck,
    goose,
    blob,
    cat,
    dragon,
    octopus,
    owl,
    penguin,
    turtle,
    snail,
    ghost,
    axolotl,
    capybara,
    cactus,
    robot,
    rabbit,
    mushroom,
    chonk,
]
Species = Literal[
    'duck',
    'goose',
    'blob',
    'cat',
    'dragon',
    'octopus',
    'owl',
    'penguin',
    'turtle',
    'snail',
    'ghost',
    'axolotl',
    'capybara',
    'cactus',
    'robot',
    'rabbit',
    'mushroom',
    'chonk',
]

EYES = ['·', '✦', '×', '◉', '@', '°']
Eye = Literal['·', '✦', '×', '◉', '@', '°']

HATS = [
    'none',
    'crown',
    'tophat',
    'propeller',
    'halo',
    'wizard',
    'beanie',
    'tinyduck',
]
Hat = Literal[
    'none',
    'crown',
    'tophat',
    'propeller',
    'halo',
    'wizard',
    'beanie',
    'tinyduck',
]

STAT_NAMES = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK']
StatName = Literal['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK']


class CompanionBones:
    """Deterministic parts derived from hash(userId)."""

    def __init__(
        self,
        rarity: Rarity,
        species: Species,
        eye: Eye,
        hat: Hat,
        shiny: bool,
        stats: dict[StatName, int],
    ):
        self.rarity = rarity
        self.species = species
        self.eye = eye
        self.hat = hat
        self.shiny = shiny
        self.stats = stats


class CompanionSoul:
    """Model-generated soul stored in config."""

    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality


class Companion:
    """Complete companion with both bones and soul."""

    def __init__(
        self,
        rarity: Rarity,
        species: Species,
        eye: Eye,
        hat: Hat,
        shiny: bool,
        stats: dict[StatName, int],
        name: str,
        personality: str,
        hatched_at: int,
    ):
        self.rarity = rarity
        self.species = species
        self.eye = eye
        self.hat = hat
        self.shiny = shiny
        self.stats = stats
        self.name = name
        self.personality = personality
        self.hatched_at = hatched_at


class StoredCompanion:
    """What persists in config (bones regenerated from hash(userId))."""

    def __init__(self, name: str, personality: str, hatched_at: int):
        self.name = name
        self.personality = personality
        self.hatched_at = hatched_at


RARITY_WEIGHTS = {
    'common': 60,
    'uncommon': 25,
    'rare': 10,
    'epic': 4,
    'legendary': 1,
}

RARITY_STARS = {
    'common': '★',
    'uncommon': '★★',
    'rare': '★★★',
    'epic': '★★★★',
    'legendary': '★★★★★',
}

RARITY_COLORS = {
    'common': 'inactive',
    'uncommon': 'success',
    'rare': 'permission',
    'epic': 'autoAccept',
    'legendary': 'warning',
}