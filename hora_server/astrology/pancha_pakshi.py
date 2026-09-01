"""Pancha Pakshi (Five Birds) calculation module based on Tamil Siddha astrology."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from hora_server.astrology.constants import NAKSHATRAS


# The 5 Birds and their elements
BIRD_ELEMENTS: Final[dict[str, str]] = {
    "Vulture": "Earth",
    "Owl": "Water",
    "Crow": "Fire",
    "Cock": "Air",
    "Peacock": "Ether",
}

# Nakshatra group boundaries (1-indexed):
# Group 1: 1-5 (Ashwini, Bharani, Krittika, Rohini, Mrigashira) -> 5 stars
# Group 2: 6-11 (Ardra, Punarvasu, Pushya, Ashlesha, Magha, Purva Phalguni) -> 6 stars
# Group 3: 12-16 (Uttara Phalguni, Hasta, Chitra, Swati, Vishakha) -> 5 stars
# Group 4: 17-22 (Anuradha, Jyeshtha, Mula, Purva Ashadha, Uttara Ashadha, Shravana) -> 6 stars
# Group 5: 23-27 (Dhanishtha, Shatabhisha, Purva Bhadrapada, Uttara Bhadrapada, Revati) -> 5 stars

SHUKLA_PAKSHA_BIRDS: Final[tuple[str, str, str, str, str]] = (
    "Vulture",
    "Owl",
    "Crow",
    "Cock",
    "Peacock",
)

KRISHNA_PAKSHA_BIRDS: Final[tuple[str, str, str, str, str]] = (
    "Peacock",
    "Cock",
    "Crow",
    "Owl",
    "Vulture",
)


@dataclass(frozen=True)
class PanchaPakshiResult:
    bird: str
    element: str
    nakshatra: str
    nakshatra_number: int
    paksha: str


def _nakshatra_group_index(nakshatra_number: int) -> int:
    """Return 0-indexed group number (0..4) for nakshatra 1..27."""
    if 1 <= nakshatra_number <= 5:
        return 0
    if 6 <= nakshatra_number <= 11:
        return 1
    if 12 <= nakshatra_number <= 16:
        return 2
    if 17 <= nakshatra_number <= 22:
        return 3
    if 23 <= nakshatra_number <= 27:
        return 4
    raise ValueError(f"Nakshatra number must be between 1 and 27, got {nakshatra_number}")


def calculate_pancha_pakshi(
    nakshatra_number: int,
    nakshatra_name: str | None = None,
    paksha: str = "Shukla",
) -> PanchaPakshiResult:
    """Calculate the Pancha Pakshi birth bird from Nakshatra number and Paksha."""
    if not (1 <= nakshatra_number <= 27):
        raise ValueError(f"Nakshatra number must be 1..27, got {nakshatra_number}")

    if not nakshatra_name:
        nakshatra_name = NAKSHATRAS[nakshatra_number - 1]

    paksha_normalized = "Krishna" if "krishna" in paksha.lower() or "dark" in paksha.lower() or "waning" in paksha.lower() else "Shukla"
    group_idx = _nakshatra_group_index(nakshatra_number)

    if paksha_normalized == "Shukla":
        bird_name = SHUKLA_PAKSHA_BIRDS[group_idx]
    else:
        bird_name = KRISHNA_PAKSHA_BIRDS[group_idx]

    element = BIRD_ELEMENTS[bird_name]

    return PanchaPakshiResult(
        bird=bird_name,
        element=element,
        nakshatra=nakshatra_name,
        nakshatra_number=nakshatra_number,
        paksha=paksha_normalized,
    )
