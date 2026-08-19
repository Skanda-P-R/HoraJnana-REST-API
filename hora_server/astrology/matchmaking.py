"""Astrological calculation engine for Vedic Ashtakoota Kundali Matchmaking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from hora_server.astrology.constants import (
    ENGLISH_RASIS,
    NAKSHATRAS,
    RASI_LORDS,
    RASHIS,
)
from hora_server.astrology.kundali import Kundali


# Varna Definitions (Rasi 1-12 based)
# Brahmin: Cancer(4), Scorpio(8), Pisces(12) -> Rank 4
# Kshatriya: Aries(1), Leo(5), Sagittarius(9) -> Rank 3
# Vaishya: Taurus(2), Virgo(6), Capricorn(10) -> Rank 2
# Shudra: Gemini(3), Libra(7), Aquarius(11) -> Rank 1
VARNA_BY_RASI: Final[dict[int, tuple[str, int]]] = {
    1: ("Kshatriya", 3),
    2: ("Vaishya", 2),
    3: ("Shudra", 1),
    4: ("Brahmin", 4),
    5: ("Kshatriya", 3),
    6: ("Vaishya", 2),
    7: ("Shudra", 1),
    8: ("Brahmin", 4),
    9: ("Kshatriya", 3),
    10: ("Vaishya", 2),
    11: ("Shudra", 1),
    12: ("Brahmin", 4),
}

# Vashya Category by Rasi
VASHYA_BY_RASI: Final[dict[int, str]] = {
    1: "Chatushpada",
    2: "Chatushpada",
    3: "Manava",
    4: "Jalachara",
    5: "Vanachara",
    6: "Manava",
    7: "Manava",
    8: "Keeta",
    9: "Manava",       # 1st half Manava / 2nd half Chatushpada
    10: "Jalachara",   # 1st half Chatushpada / 2nd half Jalachara
    11: "Manava",
    12: "Jalachara",
}

# Standard classical 12x12 Vashya points matrix (Groom Rasi 1-12 x Bride Rasi 1-12)
VASHYA_MATRIX: Final[dict[tuple[int, int], float]] = {
    # Mesha (1) - Chatushpada
    (1, 1): 2.0, (1, 2): 1.0, (1, 3): 1.0, (1, 4): 1.0, (1, 5): 0.0, (1, 6): 1.0,
    (1, 7): 1.0, (1, 8): 1.0, (1, 9): 1.0, (1, 10): 1.0, (1, 11): 0.0, (1, 12): 0.5,
    # Vrishabha (2) - Chatushpada
    (2, 1): 1.0, (2, 2): 2.0, (2, 3): 1.0, (2, 4): 1.0, (2, 5): 0.0, (2, 6): 1.0,
    (2, 7): 2.0, (2, 8): 1.0, (2, 9): 1.0, (2, 10): 1.0, (2, 11): 1.0, (2, 12): 0.5,
    # Mithuna (3) - Manava
    (3, 1): 1.0, (3, 2): 1.0, (3, 3): 2.0, (3, 4): 1.0, (3, 5): 0.5, (3, 6): 2.0,
    (3, 7): 2.0, (3, 8): 0.5, (3, 9): 1.0, (3, 10): 1.0, (3, 11): 2.0, (3, 12): 1.0,
    # Karka (4) - Jalachara
    (4, 1): 1.0, (4, 2): 1.0, (4, 3): 1.0, (4, 4): 2.0, (4, 5): 0.0, (4, 6): 1.0,
    (4, 7): 1.0, (4, 8): 2.0, (4, 9): 1.0, (4, 10): 2.0, (4, 11): 1.0, (4, 12): 2.0,
    # Simha (5) - Vanachara
    (5, 1): 0.0, (5, 2): 0.0, (5, 3): 0.5, (5, 4): 0.0, (5, 5): 2.0, (5, 6): 0.5,
    (5, 7): 1.0, (5, 8): 0.0, (5, 9): 0.5, (5, 10): 0.0, (5, 11): 0.5, (5, 12): 0.0,
    # Kanya (6) - Manava
    (6, 1): 1.0, (6, 2): 1.0, (6, 3): 2.0, (6, 4): 1.0, (6, 5): 0.5, (6, 6): 2.0,
    (6, 7): 2.0, (6, 8): 0.5, (6, 9): 1.0, (6, 10): 1.0, (6, 11): 2.0, (6, 12): 1.0,
    # Tula (7) - Manava
    (7, 1): 1.0, (7, 2): 2.0, (7, 3): 2.0, (7, 4): 1.0, (7, 5): 1.0, (7, 6): 2.0,
    (7, 7): 2.0, (7, 8): 0.5, (7, 9): 1.0, (7, 10): 1.0, (7, 11): 2.0, (7, 12): 1.0,
    # Vrishchika (8) - Keeta
    (8, 1): 1.0, (8, 2): 1.0, (8, 3): 0.5, (8, 4): 2.0, (8, 5): 0.0, (8, 6): 0.5,
    (8, 7): 0.5, (8, 8): 2.0, (8, 9): 0.5, (8, 10): 0.5, (8, 11): 0.5, (8, 12): 1.0,
    # Dhanu (9) - Manava / Chatushpada
    (9, 1): 1.0, (9, 2): 1.0, (9, 3): 1.0, (9, 4): 1.0, (9, 5): 0.5, (9, 6): 1.0,
    (9, 7): 1.0, (9, 8): 0.5, (9, 9): 2.0, (9, 10): 1.0, (9, 11): 1.0, (9, 12): 2.0,
    # Makara (10) - Chatushpada / Jalachara
    (10, 1): 1.0, (10, 2): 1.0, (10, 3): 1.0, (10, 4): 2.0, (10, 5): 0.0, (10, 6): 1.0,
    (10, 7): 1.0, (10, 8): 0.5, (10, 9): 1.0, (10, 10): 2.0, (10, 11): 1.0, (10, 12): 2.0,
    # Kumbha (11) - Manava
    (11, 1): 0.0, (11, 2): 1.0, (11, 3): 2.0, (11, 4): 1.0, (11, 5): 0.5, (11, 6): 2.0,
    (11, 7): 2.0, (11, 8): 0.5, (11, 9): 1.0, (11, 10): 1.0, (11, 11): 2.0, (11, 12): 1.0,
    # Meena (12) - Jalachara
    (12, 1): 0.5, (12, 2): 0.5, (12, 3): 1.0, (12, 4): 2.0, (12, 5): 0.0, (12, 6): 1.0,
    (12, 7): 1.0, (12, 8): 1.0, (12, 9): 2.0, (12, 10): 2.0, (12, 11): 1.0, (12, 12): 2.0,
}

TARA_NAMES: Final[tuple[str, ...]] = (
    "Janma",
    "Sampat",
    "Vipat",
    "Kshema",
    "Pratyak",
    "Sadhana",
    "Vadha",
    "Mitra",
    "Parama Mitra",
)


# 14 Yonis for 27 Nakshatras (0-indexed)
NAKSHATRA_YONI: Final[tuple[str, ...]] = (
    "Horse",      # 0: Ashwini
    "Elephant",   # 1: Bharani
    "Sheep",      # 2: Krittika
    "Serpent",    # 3: Rohini
    "Serpent",    # 4: Mrigashira
    "Dog",        # 5: Ardra
    "Cat",        # 6: Punarvasu
    "Sheep",      # 7: Pushya
    "Cat",        # 8: Ashlesha
    "Rat",        # 9: Magha
    "Rat",        # 10: Purva Phalguni
    "Cow",        # 11: Uttara Phalguni
    "Buffalo",    # 12: Hasta
    "Tiger",      # 13: Chitra
    "Buffalo",    # 14: Swati
    "Tiger",      # 15: Vishakha
    "Deer",       # 16: Anuradha
    "Deer",       # 17: Jyeshtha
    "Dog",        # 18: Mula
    "Monkey",     # 19: Purva Ashadha
    "Mongoose",   # 20: Uttara Ashadha
    "Monkey",     # 21: Shravana
    "Lion",       # 22: Dhanishtha
    "Horse",      # 23: Shatabhisha
    "Lion",       # 24: Purva Bhadrapada
    "Cow",        # 25: Uttara Bhadrapada
    "Elephant",   # 26: Revati
)

YONI_LIST: Final[tuple[str, ...]] = (
    "Horse", "Elephant", "Sheep", "Serpent", "Dog", "Cat", "Rat",
    "Cow", "Buffalo", "Tiger", "Deer", "Monkey", "Mongoose", "Lion",
)

# Yoni Compatibility Table (14 animals x 14 animals) - indexed by (Groom, Bride)
YONI_MATRIX: Final[dict[tuple[str, str], float]] = {
    # Groom: Horse
    ("Horse", "Horse"): 4.0, ("Horse", "Elephant"): 2.0, ("Horse", "Sheep"): 3.0, ("Horse", "Serpent"): 2.0,
    ("Horse", "Dog"): 2.0, ("Horse", "Rat"): 3.0, ("Horse", "Cat"): 3.0, ("Horse", "Tiger"): 1.0,
    ("Horse", "Buffalo"): 0.0, ("Horse", "Deer"): 3.0, ("Horse", "Cow"): 3.0, ("Horse", "Mongoose"): 2.0,
    ("Horse", "Monkey"): 2.0, ("Horse", "Lion"): 1.0,
    # Groom: Elephant
    ("Elephant", "Horse"): 2.0, ("Elephant", "Elephant"): 4.0, ("Elephant", "Sheep"): 3.0, ("Elephant", "Serpent"): 2.0,
    ("Elephant", "Dog"): 2.0, ("Elephant", "Rat"): 3.0, ("Elephant", "Cat"): 2.0, ("Elephant", "Tiger"): 3.0,
    ("Elephant", "Buffalo"): 3.0, ("Elephant", "Deer"): 3.0, ("Elephant", "Cow"): 3.0, ("Elephant", "Mongoose"): 2.0,
    ("Elephant", "Monkey"): 2.0, ("Elephant", "Lion"): 0.0,
    # Groom: Sheep
    ("Sheep", "Horse"): 3.0, ("Sheep", "Elephant"): 3.0, ("Sheep", "Sheep"): 4.0, ("Sheep", "Serpent"): 2.0,
    ("Sheep", "Dog"): 2.0, ("Sheep", "Rat"): 3.0, ("Sheep", "Cat"): 3.0, ("Sheep", "Tiger"): 1.0,
    ("Sheep", "Buffalo"): 3.0, ("Sheep", "Deer"): 3.0, ("Sheep", "Cow"): 3.0, ("Sheep", "Mongoose"): 2.0,
    ("Sheep", "Monkey"): 0.0, ("Sheep", "Lion"): 1.0,
    # Groom: Serpent
    ("Serpent", "Horse"): 2.0, ("Serpent", "Elephant"): 2.0, ("Serpent", "Sheep"): 2.0, ("Serpent", "Serpent"): 4.0,
    ("Serpent", "Dog"): 2.0, ("Serpent", "Rat"): 1.0, ("Serpent", "Cat"): 1.0, ("Serpent", "Tiger"): 2.0,
    ("Serpent", "Buffalo"): 2.0, ("Serpent", "Deer"): 2.0, ("Serpent", "Cow"): 2.0, ("Serpent", "Mongoose"): 0.0,
    ("Serpent", "Monkey"): 2.0, ("Serpent", "Lion"): 1.0,
    # Groom: Dog
    ("Dog", "Horse"): 2.0, ("Dog", "Elephant"): 2.0, ("Dog", "Sheep"): 2.0, ("Dog", "Serpent"): 2.0,
    ("Dog", "Dog"): 4.0, ("Dog", "Rat"): 2.0, ("Dog", "Cat"): 1.0, ("Dog", "Tiger"): 2.0,
    ("Dog", "Buffalo"): 2.0, ("Dog", "Deer"): 0.0, ("Dog", "Cow"): 2.0, ("Dog", "Mongoose"): 2.0,
    ("Dog", "Monkey"): 2.0, ("Dog", "Lion"): 2.0,
    # Groom: Rat
    ("Rat", "Horse"): 3.0, ("Rat", "Elephant"): 3.0, ("Rat", "Sheep"): 3.0, ("Rat", "Serpent"): 1.0,
    ("Rat", "Dog"): 2.0, ("Rat", "Rat"): 4.0, ("Rat", "Cat"): 0.0, ("Rat", "Tiger"): 2.0,
    ("Rat", "Buffalo"): 3.0, ("Rat", "Deer"): 2.0, ("Rat", "Cow"): 3.0, ("Rat", "Mongoose"): 1.0,
    ("Rat", "Monkey"): 2.0, ("Rat", "Lion"): 2.0,
    # Groom: Cat
    ("Cat", "Horse"): 3.0, ("Cat", "Elephant"): 3.0, ("Cat", "Sheep"): 3.0, ("Cat", "Serpent"): 1.0,
    ("Cat", "Dog"): 1.0, ("Cat", "Rat"): 0.0, ("Cat", "Cat"): 4.0, ("Cat", "Tiger"): 2.0,
    ("Cat", "Buffalo"): 3.0, ("Cat", "Deer"): 3.0, ("Cat", "Cow"): 3.0, ("Cat", "Mongoose"): 2.0,
    ("Cat", "Monkey"): 2.0, ("Cat", "Lion"): 2.0,
    # Groom: Tiger
    ("Tiger", "Horse"): 1.0, ("Tiger", "Elephant"): 1.0, ("Tiger", "Sheep"): 1.0, ("Tiger", "Serpent"): 2.0,
    ("Tiger", "Dog"): 2.0, ("Tiger", "Rat"): 2.0, ("Tiger", "Cat"): 2.0, ("Tiger", "Tiger"): 4.0,
    ("Tiger", "Buffalo"): 1.0, ("Tiger", "Deer"): 1.0, ("Tiger", "Cow"): 0.0, ("Tiger", "Mongoose"): 2.0,
    ("Tiger", "Monkey"): 2.0, ("Tiger", "Lion"): 3.0,
    # Groom: Buffalo
    ("Buffalo", "Horse"): 0.0, ("Buffalo", "Elephant"): 3.0, ("Buffalo", "Sheep"): 3.0, ("Buffalo", "Serpent"): 2.0,
    ("Buffalo", "Dog"): 2.0, ("Buffalo", "Rat"): 3.0, ("Buffalo", "Cat"): 3.0, ("Buffalo", "Tiger"): 1.0,
    ("Buffalo", "Buffalo"): 4.0, ("Buffalo", "Deer"): 3.0, ("Buffalo", "Cow"): 3.0, ("Buffalo", "Mongoose"): 2.0,
    ("Buffalo", "Monkey"): 2.0, ("Buffalo", "Lion"): 1.0,
    # Groom: Deer
    ("Deer", "Horse"): 3.0, ("Deer", "Elephant"): 3.0, ("Deer", "Sheep"): 3.0, ("Deer", "Serpent"): 2.0,
    ("Deer", "Dog"): 0.0, ("Deer", "Rat"): 3.0, ("Deer", "Cat"): 3.0, ("Deer", "Tiger"): 1.0,
    ("Deer", "Buffalo"): 3.0, ("Deer", "Deer"): 4.0, ("Deer", "Cow"): 3.0, ("Deer", "Mongoose"): 2.0,
    ("Deer", "Monkey"): 2.0, ("Deer", "Lion"): 1.0,
    # Groom: Cow
    ("Cow", "Horse"): 3.0, ("Cow", "Elephant"): 3.0, ("Cow", "Sheep"): 3.0, ("Cow", "Serpent"): 2.0,
    ("Cow", "Dog"): 2.0, ("Cow", "Rat"): 3.0, ("Cow", "Cat"): 3.0, ("Cow", "Tiger"): 0.0,
    ("Cow", "Buffalo"): 3.0, ("Cow", "Deer"): 3.0, ("Cow", "Cow"): 4.0, ("Cow", "Mongoose"): 2.0,
    ("Cow", "Monkey"): 2.0, ("Cow", "Lion"): 1.0,
    # Groom: Mongoose
    ("Mongoose", "Horse"): 2.0, ("Mongoose", "Elephant"): 2.0, ("Mongoose", "Sheep"): 2.0, ("Mongoose", "Serpent"): 0.0,
    ("Mongoose", "Dog"): 2.0, ("Mongoose", "Rat"): 1.0, ("Mongoose", "Cat"): 2.0, ("Mongoose", "Tiger"): 2.0,
    ("Mongoose", "Buffalo"): 2.0, ("Mongoose", "Deer"): 2.0, ("Mongoose", "Cow"): 2.0, ("Mongoose", "Mongoose"): 4.0,
    ("Mongoose", "Monkey"): 2.0, ("Mongoose", "Lion"): 2.0,
    # Groom: Monkey
    ("Monkey", "Horse"): 2.0, ("Monkey", "Elephant"): 2.0, ("Monkey", "Sheep"): 0.0, ("Monkey", "Serpent"): 1.0,
    ("Monkey", "Dog"): 2.0, ("Monkey", "Rat"): 2.0, ("Monkey", "Cat"): 2.0, ("Monkey", "Tiger"): 2.0,
    ("Monkey", "Buffalo"): 2.0, ("Monkey", "Deer"): 2.0, ("Monkey", "Cow"): 2.0, ("Monkey", "Mongoose"): 2.0,
    ("Monkey", "Monkey"): 4.0, ("Monkey", "Lion"): 2.0,
    # Groom: Lion
    ("Lion", "Horse"): 1.0, ("Lion", "Elephant"): 0.0, ("Lion", "Sheep"): 1.0, ("Lion", "Serpent"): 2.0,
    ("Lion", "Dog"): 2.0, ("Lion", "Rat"): 1.0, ("Lion", "Cat"): 2.0, ("Lion", "Tiger"): 3.0,
    ("Lion", "Buffalo"): 3.0, ("Lion", "Deer"): 1.0, ("Lion", "Cow"): 1.0, ("Lion", "Mongoose"): 2.0,
    ("Lion", "Monkey"): 2.0, ("Lion", "Lion"): 4.0,
}

# Planetary Natural Relationships (Naisargika Sambandha)
PLANET_FRIENDS: Final[dict[str, frozenset[str]]] = {
    "Sun": frozenset({"Moon", "Mars", "Jupiter"}),
    "Moon": frozenset({"Sun", "Mercury"}),
    "Mars": frozenset({"Sun", "Moon", "Jupiter"}),
    "Mercury": frozenset({"Sun", "Venus"}),
    "Jupiter": frozenset({"Sun", "Moon", "Mars"}),
    "Venus": frozenset({"Mercury", "Saturn"}),
    "Saturn": frozenset({"Mercury", "Venus"}),
}

PLANET_ENEMIES: Final[dict[str, frozenset[str]]] = {
    "Sun": frozenset({"Venus", "Saturn"}),
    "Moon": frozenset(),
    "Mars": frozenset({"Mercury"}),
    "Mercury": frozenset({"Moon"}),
    "Jupiter": frozenset({"Mercury", "Venus"}),
    "Venus": frozenset({"Sun", "Moon"}),
    "Saturn": frozenset({"Sun", "Moon", "Mars"}),
}

# Gana by Nakshatra (0-indexed)
# Deva: 0, 4, 6, 7, 12, 14, 16, 21, 26
# Manushya: 1, 3, 5, 10, 11, 19, 20, 24, 25
# Rakshasa: 2, 8, 9, 13, 15, 17, 18, 22, 23
DEVA_NAKSHATRAS: Final[frozenset[int]] = frozenset({0, 4, 6, 7, 12, 14, 16, 21, 26})
MANUSHYA_NAKSHATRAS: Final[frozenset[int]] = frozenset({1, 3, 5, 10, 11, 19, 20, 24, 25})
RAKSHASA_NAKSHATRAS: Final[frozenset[int]] = frozenset({2, 8, 9, 13, 15, 17, 18, 22, 23})

# Nadi by Nakshatra (0-indexed)
# Adi: 0, 5, 6, 11, 12, 17, 18, 23, 24
# Madhya: 1, 4, 7, 10, 13, 16, 19, 22, 25
# Antya: 2, 3, 8, 9, 14, 15, 20, 21, 26
ADI_NAKSHATRAS: Final[frozenset[int]] = frozenset({0, 5, 6, 11, 12, 17, 18, 23, 24})
MADHYA_NAKSHATRAS: Final[frozenset[int]] = frozenset({1, 4, 7, 10, 13, 16, 19, 22, 25})
ANTYA_NAKSHATRAS: Final[frozenset[int]] = frozenset({2, 3, 8, 9, 14, 15, 20, 21, 26})


@dataclass(frozen=True)
class ProfileSummary:
    name: str
    datetime: str
    location: str
    moon_rasi: str
    moon_rasi_number: int
    moon_rasi_lord: str
    nakshatra: str
    nakshatra_number: int
    nakshatra_lord: str
    pada: int
    varna: str
    vashya: str
    yoni: str
    gana: str
    nadi: str


@dataclass(frozen=True)
class KootaResult:
    name: str
    obtained_points: float
    max_points: float
    groom_attribute: str
    bride_attribute: str
    is_favorable: bool
    dosha: str | None
    parihara_applied: bool
    description: str


@dataclass(frozen=True)
class ManglikProfile:
    is_manglik: bool
    status: str
    mars_house_lagna: int
    mars_house_moon: int


@dataclass(frozen=True)
class ManglikAnalysis:
    groom_manglik: ManglikProfile
    bride_manglik: ManglikProfile
    manglik_compatibility: str
    description: str


@dataclass(frozen=True)
class MatchMakingResult:
    groom_info: ProfileSummary
    bride_info: ProfileSummary
    total_points: float
    max_points: float
    percentage: float
    result: str
    is_recommended: bool
    summary_message: str
    kootas: dict[str, KootaResult]
    doshas_summary: dict[str, Any]
    manglik_analysis: ManglikAnalysis | None


def get_gana(nak_idx: int) -> str:
    if nak_idx in DEVA_NAKSHATRAS:
        return "Deva"
    if nak_idx in MANUSHYA_NAKSHATRAS:
        return "Manushya"
    return "Rakshasa"


def get_nadi(nak_idx: int) -> str:
    if nak_idx in ADI_NAKSHATRAS:
        return "Adi"
    if nak_idx in MADHYA_NAKSHATRAS:
        return "Madhya"
    return "Antya"


def calculate_varna(groom_rasi_num: int, bride_rasi_num: int) -> KootaResult:
    g_varna, g_rank = VARNA_BY_RASI[groom_rasi_num]
    b_varna, b_rank = VARNA_BY_RASI[bride_rasi_num]

    if g_rank >= b_rank:
        pts = 1.0
        fav = True
        dosha = None
        desc = "Groom's Varna is equal to or higher than Bride's Varna, indicating harmony in temperament and work ethic."
    else:
        pts = 0.0
        fav = False
        dosha = "Varna Dosha"
        desc = "Groom's Varna is lower than Bride's Varna."

    return KootaResult(
        name="Varna",
        obtained_points=pts,
        max_points=1.0,
        groom_attribute=g_varna,
        bride_attribute=b_varna,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=False,
        description=desc,
    )


def calculate_vashya(groom_rasi_num: int, bride_rasi_num: int) -> KootaResult:
    g_vashya = VASHYA_BY_RASI[groom_rasi_num]
    b_vashya = VASHYA_BY_RASI[bride_rasi_num]
    pts = VASHYA_MATRIX.get((groom_rasi_num, bride_rasi_num), 0.5)

    fav = pts >= 1.0
    dosha = None if pts > 0.0 else "Vashya Dosha"
    if pts == 2.0:
        desc = "Full mutual attraction, amenable temperament, and natural devotion."
    elif pts == 1.0:
        desc = "Good mutual harmony and natural power balance between partners."
    elif pts == 0.5:
        desc = "Moderate harmony with neutral attraction."
    else:
        desc = "Incompatible Vashya nature leading to struggle for dominance."

    return KootaResult(
        name="Vashya",
        obtained_points=pts,
        max_points=2.0,
        groom_attribute=g_vashya,
        bride_attribute=b_vashya,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=False,
        description=desc,
    )


def calculate_tara(groom_nak_idx: int, bride_nak_idx: int) -> KootaResult:
    # 9-Tara cycle classification (1-indexed: 1 to 9) from Nakshatra index (0 to 26)
    # 1: Janma, 2: Sampat, 3: Vipat, 4: Kshema, 5: Pratyak, 6: Sadhana, 7: Vadha, 8: Mitra, 9: Parama Mitra
    t1 = (groom_nak_idx % 9) + 1
    t2 = (bride_nak_idx % 9) + 1

    g_tara = TARA_NAMES[t1 - 1]
    b_tara = TARA_NAMES[t2 - 1]

    # Check Nakshatra lords for Tara Dosha Parihara
    # Nakshatra lords in 9-cycle: 0: Ketu, 1: Venus, 2: Sun, 3: Moon, 4: Mars, 5: Rahu, 6: Jupiter, 7: Saturn, 8: Mercury
    nak_lords = ("Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury")
    g_lord = nak_lords[groom_nak_idx % 9]
    b_lord = nak_lords[bride_nak_idx % 9]

    g_friends = PLANET_FRIENDS.get(g_lord, frozenset())
    b_friends = PLANET_FRIENDS.get(b_lord, frozenset())
    lords_friendly = (g_lord == b_lord) or (b_lord in g_friends and g_lord in b_friends)

    # Auspicious Taras (Shubha): 2 (Sampat), 4 (Kshema), 6 (Sadhana), 8 (Mitra), 9 (Parama Mitra) -> 1.5 pts each
    # Inauspicious Taras (Ashubha): 1 (Janma), 3 (Vipat), 5 (Pratyak), 7 (Vadha) -> 0 pts each
    # Exception: If both share the exact same Janma Nakshatra, Tara alignment is auspicious -> 3.0 pts
    if groom_nak_idx == bride_nak_idx:
        pts = 3.0
        fav = True
        dosha = None
        desc = "Same Janma Nakshatra; Tara alignment is auspicious."
    else:
        auspicious_taras = {2, 4, 6, 8, 9}
        g_good = t1 in auspicious_taras
        b_good = t2 in auspicious_taras

        if g_good and b_good:
            pts = 3.0
            fav = True
            dosha = None
            desc = f"Both Tara alignments (Groom: {g_tara}, Bride: {b_tara}) are auspicious, fostering destiny, health, and mutual longevity."
        elif g_good or b_good:
            pts = 1.5
            fav = True
            dosha = None
            favorable_person = "Groom" if g_good else "Bride"
            desc = f"Tara alignment is favorable for {favorable_person} (Groom: {g_tara}, Bride: {b_tara}), awarding 1.5 points."
        elif lords_friendly:
            pts = 1.5
            fav = True
            dosha = None
            desc = f"Tara Dosha between Groom ({g_tara}) and Bride ({b_tara}) is mitigated to 1.5 points due to friendly Nakshatra lords ({g_lord} and {b_lord})."
        else:
            pts = 0.0
            fav = False
            dosha = "Tara Dosha"
            desc = f"Both Tara alignments (Groom: {g_tara}, Bride: {b_tara}) are inauspicious (Janma/Vipat/Pratyak/Vadha)."

    return KootaResult(
        name="Tara",
        obtained_points=pts,
        max_points=3.0,
        groom_attribute=g_tara,
        bride_attribute=b_tara,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=(pts == 1.5 and not g_good and not b_good),
        description=desc,
    )






def calculate_yoni(groom_nak_idx: int, bride_nak_idx: int) -> KootaResult:
    g_yoni = NAKSHATRA_YONI[groom_nak_idx]
    b_yoni = NAKSHATRA_YONI[bride_nak_idx]

    pts = YONI_MATRIX.get((g_yoni, b_yoni), 2.0)
    fav = pts >= 2.0
    dosha = "Yoni Vairi Dosha" if pts == 0.0 else None

    if pts == 4.0:
        desc = f"Same animal Yoni ({g_yoni}), assuring utmost physical and biological compatibility."
    elif pts == 3.0:
        desc = f"Friendly animal Yonis ({g_yoni} and {b_yoni}), ensuring great physical intimacy and mutual affection."
    elif pts == 2.0:
        desc = f"Neutral animal Yonis ({g_yoni} and {b_yoni}) providing adequate mutual harmony."
    elif pts == 1.0:
        desc = f"Inimical animal Yonis ({g_yoni} and {b_yoni}), causing occasional physical or biological friction."
    else:
        desc = f"Sworn enemy animal Yonis ({g_yoni} vs {b_yoni}), indicating physical discord (Vairi Yoni)."

    return KootaResult(
        name="Yoni",
        obtained_points=pts,
        max_points=4.0,
        groom_attribute=g_yoni,
        bride_attribute=b_yoni,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=False,
        description=desc,
    )


def calculate_graha_maitri(groom_rasi_num: int, bride_rasi_num: int) -> KootaResult:
    g_lord = RASI_LORDS[groom_rasi_num - 1]
    b_lord = RASI_LORDS[bride_rasi_num - 1]

    if g_lord == b_lord:
        pts = 5.0
        fav = True
        dosha = None
        desc = f"Same Rasi lord ({g_lord}), indicating profound mental and intellectual harmony."
    else:
        g_friends = PLANET_FRIENDS.get(g_lord, frozenset())
        g_enemies = PLANET_ENEMIES.get(g_lord, frozenset())
        b_friends = PLANET_FRIENDS.get(b_lord, frozenset())
        b_enemies = PLANET_ENEMIES.get(b_lord, frozenset())

        g_to_b = 1 if b_lord in g_friends else (-1 if b_lord in g_enemies else 0)
        b_to_g = 1 if g_lord in b_friends else (-1 if g_lord in b_enemies else 0)

        if g_to_b == 1 and b_to_g == 1:
            pts = 5.0
            fav = True
            dosha = None
            desc = f"Mutual friends ({g_lord} and {b_lord}), assuring deep understanding and affection."
        elif (g_to_b == 1 and b_to_g == 0) or (g_to_b == 0 and b_to_g == 1):
            pts = 4.0
            fav = True
            dosha = None
            desc = f"One-sided friendship and neutrality between {g_lord} and {b_lord}, fostering healthy mental compatibility."
        elif g_to_b == 0 and b_to_g == 0:
            pts = 3.0
            fav = True
            dosha = None
            desc = f"Mutual neutrality between {g_lord} and {b_lord}, indicating stable communication."
        elif (g_to_b == 1 and b_to_g == -1) or (g_to_b == -1 and b_to_g == 1):
            pts = 1.0
            fav = False
            dosha = "Graha Maitri Dosha"
            desc = f"Mixed relationship (Friend/Enemy) between {g_lord} and {b_lord}, leading to intellectual disagreements."
        elif (g_to_b == 0 and b_to_g == -1) or (g_to_b == -1 and b_to_g == 0):
            pts = 0.5
            fav = False
            dosha = "Graha Maitri Dosha"
            desc = f"Neutral/Enemy relationship between {g_lord} and {b_lord}, creating mental misunderstandings."
        else:
            pts = 0.0
            fav = False
            dosha = "Graha Maitri Dosha"
            desc = f"Mutual enemies ({g_lord} and {b_lord}), indicating psychological friction and frequent clashes."

    return KootaResult(
        name="Graha Maitri",
        obtained_points=pts,
        max_points=5.0,
        groom_attribute=g_lord,
        bride_attribute=b_lord,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=False,
        description=desc,
    )


def calculate_gana(groom_nak_idx: int, bride_nak_idx: int) -> KootaResult:
    g_gana = get_gana(groom_nak_idx)
    b_gana = get_gana(bride_nak_idx)

    # Classical Gana matrix (Rows: Bride, Columns: Groom)
    if g_gana == b_gana:
        pts = 6.0
        fav = True
        dosha = None
        desc = f"Same Gana ({g_gana}), providing great temperament and mutual wavelength."
    elif b_gana == "Deva" and g_gana == "Manushya":
        pts = 4.0
        fav = True
        dosha = None
        desc = "Bride is Deva and Groom is Manushya, providing moderate temperament compatibility."
    elif b_gana == "Deva" and g_gana == "Rakshasa":
        pts = 2.0
        fav = False
        dosha = "Gana Dosha"
        desc = "Bride is Deva and Groom is Rakshasa; temperament difference mitigated to 2 points."
    elif b_gana == "Manushya" and g_gana == "Deva":
        pts = 5.0
        fav = True
        dosha = None
        desc = "Bride is Manushya and Groom is Deva, generating mutual respect and harmony."
    elif b_gana == "Manushya" and g_gana == "Rakshasa":
        pts = 1.0
        fav = False
        dosha = "Gana Dosha"
        desc = "Bride is Manushya and Groom is Rakshasa; behavioral friction mitigated to 1 point."
    elif b_gana == "Rakshasa" and g_gana == "Deva":
        pts = 0.0
        fav = False
        dosha = "Gana Dosha"
        desc = "Bride is Rakshasa and Groom is Deva; high temperament incompatibility."
    else:  # Bride Rakshasa and Groom Manushya
        pts = 0.0
        fav = False
        dosha = "Gana Dosha"
        desc = "Bride is Rakshasa and Groom is Manushya; high behavioral clash."

    return KootaResult(
        name="Gana",
        obtained_points=pts,
        max_points=6.0,
        groom_attribute=g_gana,
        bride_attribute=b_gana,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=False,
        description=desc,
    )


def calculate_bhakoot(
    groom_rasi_num: int,
    bride_rasi_num: int,
    groom_nak_idx: int,
    bride_nak_idx: int,
) -> KootaResult:
    # Calculate distance of Bride Rasi from Groom Rasi (1 to 12)
    dist = ((bride_rasi_num - groom_rasi_num) % 12) + 1
    g_rasi_name = RASHIS[groom_rasi_num - 1]
    b_rasi_name = RASHIS[bride_rasi_num - 1]
    g_lord = RASI_LORDS[groom_rasi_num - 1]
    b_lord = RASI_LORDS[bride_rasi_num - 1]

    # Inauspicious Bhakoot patterns: 2/12 (Dvidvadasha), 6/8 (Shadashtaka), 9/5 (in certain cases)
    # Check if 2/12 or 6/8
    is_dvidvadasha = dist in (2, 12)
    is_shadashtaka = dist in (6, 8)
    is_navapanchama = dist in (5, 9)

    # Check Parihara (cancellation of Bhakoot Dosha)
    # 1. Same Rasi Lord (e.g. Mesha-Vrishchika ruled by Mars, Vrishabha-Tula ruled by Venus)
    # 2. Rasi lords are mutual friends
    lords_identical = g_lord == b_lord
    g_friends = PLANET_FRIENDS.get(g_lord, frozenset())
    b_friends = PLANET_FRIENDS.get(b_lord, frozenset())
    lords_mutual_friends = (b_lord in g_friends) and (g_lord in b_friends)
    parihara = lords_identical or lords_mutual_friends

    relation_str = f"{dist}/{((groom_rasi_num - bride_rasi_num) % 12) + 1}"

    if dist in (1, 7, 3, 11, 4, 10):
        pts = 7.0
        fav = True
        dosha = None
        parihara_applied = False
        desc = f"Auspicious {relation_str} Rasi relationship fostering marital happiness, health, and prosperity."
    elif is_navapanchama:
        pts = 0.0
        fav = False
        dosha = "Bhakoot Dosha (Navapanchama)"
        parihara_applied = parihara
        if parihara:
            desc = f"5/9 (Navapanchama) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords ({g_lord} and {b_lord})."
        else:
            desc = "5/9 (Navapanchama) placement indicates progeny or Dharma friction (Bhakoot Dosha)."
    elif is_dvidvadasha:
        pts = 0.0
        fav = False
        dosha = "Bhakoot Dosha (Dvidvadasha)"
        parihara_applied = parihara
        if parihara:
            desc = f"2/12 (Dvidvadasha) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords ({g_lord} and {b_lord})."
        else:
            desc = "2/12 (Dvidvadasha) placement indicates financial strain or emotional distance (Bhakoot Dosha)."
    else:  # 6/8 Shadashtaka
        pts = 0.0
        fav = False
        dosha = "Bhakoot Dosha (Shadashtaka)"
        parihara_applied = parihara
        if parihara:
            desc = f"6/8 (Shadashtaka) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords ({g_lord} and {b_lord})."
        else:
            desc = "6/8 (Shadashtaka) placement indicates health vulnerabilities or friction (Bhakoot Dosha)."


    return KootaResult(
        name="Bhakoot",
        obtained_points=pts,
        max_points=7.0,
        groom_attribute=f"{g_rasi_name} ({groom_rasi_num})",
        bride_attribute=f"{b_rasi_name} ({bride_rasi_num})",
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=parihara_applied,
        description=desc,
    )


def calculate_nadi(
    groom_nak_idx: int,
    bride_nak_idx: int,
    groom_rasi_num: int,
    bride_rasi_num: int,
    groom_pada: int,
    bride_pada: int,
) -> KootaResult:
    g_nadi = get_nadi(groom_nak_idx)
    b_nadi = get_nadi(bride_nak_idx)
    g_nak_name = NAKSHATRAS[groom_nak_idx]
    b_nak_name = NAKSHATRAS[bride_nak_idx]

    if g_nadi != b_nadi:
        pts = 8.0
        fav = True
        dosha = None
        parihara_applied = False
        desc = f"Different Nadis ({g_nadi} and {b_nadi}) assure optimal genetic diversity, vitality, and progeny health."
    else:
        # Same Nadi -> Potential Nadi Dosha. Check canonical Parihara exceptions:
        # 1. Same Rasi, Different Nakshatra
        # 2. Same Nakshatra, Different Rasi
        # 3. Same Nakshatra, Same Rasi, Different Padas (with identical/friendly lords)
        same_rasi = groom_rasi_num == bride_rasi_num
        same_nak = groom_nak_idx == bride_nak_idx
        diff_pada = groom_pada != bride_pada

        pts = 0.0
        fav = False
        dosha = "Nadi Dosha"

        if same_rasi and not same_nak:
            parihara_applied = True
            desc = f"Both share {g_nadi} Nadi (0/8 pts); Nadi Dosha is astrologically mitigated because Groom and Bride share the same Rasi ({RASHIS[groom_rasi_num - 1]}) with different Nakshatras ({g_nak_name} & {b_nak_name})."
        elif same_nak and not same_rasi:
            parihara_applied = True
            desc = f"Both share {g_nadi} Nadi (0/8 pts); Nadi Dosha is astrologically mitigated because Nakshatra ({g_nak_name}) spans different Rasis."
        elif same_nak and same_rasi and diff_pada:
            parihara_applied = True
            desc = f"Both share {g_nadi} Nadi (0/8 pts); Nadi Dosha is astrologically mitigated due to different birth Padas ({groom_pada} & {bride_pada}) within {g_nak_name}."
        else:
            parihara_applied = False
            desc = f"Both share {g_nadi} Nadi (0/8 pts), causing Nadi Dosha which can impact physiological harmony and progeny health."


    return KootaResult(
        name="Nadi",
        obtained_points=pts,
        max_points=8.0,
        groom_attribute=g_nadi,
        bride_attribute=b_nadi,
        is_favorable=fav,
        dosha=dosha,
        parihara_applied=parihara_applied,
        description=desc,
    )


def calculate_manglik_profile(kundali: Kundali) -> ManglikProfile:
    # Find Mars and Moon house positions
    mars_planet = next((p for p in kundali.planets if p.planet == "Mars"), None)
    moon_planet = next((p for p in kundali.planets if p.planet == "Moon"), None)

    mars_house_lagna = mars_planet.house if mars_planet else 1
    moon_house = moon_planet.house if moon_planet else 1

    # Calculate Mars house relative to Moon
    mars_house_moon = ((mars_planet.rasi_number - moon_planet.rasi_number) % 12) + 1 if (mars_planet and moon_planet) else 1

    # Traditional Manglik houses: 1, 2, 4, 7, 8, 12
    manglik_houses = {1, 2, 4, 7, 8, 12}
    is_manglik_lagna = mars_house_lagna in manglik_houses
    is_manglik_moon = mars_house_moon in manglik_houses

    is_manglik = is_manglik_lagna or is_manglik_moon
    status = "Manglik" if is_manglik else "Non-Manglik"

    return ManglikProfile(
        is_manglik=is_manglik,
        status=status,
        mars_house_lagna=mars_house_lagna,
        mars_house_moon=mars_house_moon,
    )


def calculate_manglik_analysis(
    groom_kundali: Kundali,
    bride_kundali: Kundali,
) -> ManglikAnalysis:
    g_m = calculate_manglik_profile(groom_kundali)
    b_m = calculate_manglik_profile(bride_kundali)

    if g_m.is_manglik and b_m.is_manglik:
        compat = "Compatible (Sama Manglik)"
        desc = "Both partners have Kuja Dosha, resulting in mutual cancellation and balance."
    elif not g_m.is_manglik and not b_m.is_manglik:
        compat = "Compatible (Non-Manglik)"
        desc = "Neither partner has Kuja Dosha. The match is harmonious."
    elif g_m.is_manglik and not b_m.is_manglik:
        compat = "Partial / Requires Remedial Guidance"
        desc = "Groom has Kuja Dosha while Bride does not. Astrological guidance is advised."
    else:
        compat = "Partial / Requires Remedial Guidance"
        desc = "Bride has Kuja Dosha while Groom does not. Astrological guidance is advised."

    return ManglikAnalysis(
        groom_manglik=g_m,
        bride_manglik=b_m,
        manglik_compatibility=compat,
        description=desc,
    )


def calculate_match_making(
    groom_kundali: Kundali,
    bride_kundali: Kundali,
    groom_name: str,
    bride_name: str,
    groom_datetime_str: str,
    bride_datetime_str: str,
    groom_location_str: str,
    bride_location_str: str,
    include_manglik: bool = True,
) -> MatchMakingResult:
    # Extract Moon details for Groom
    g_moon = next(p for p in groom_kundali.planets if p.planet == "Moon")
    g_nak_span = 360.0 / 27.0
    g_nak_idx = int(g_moon.longitude // g_nak_span) % 27
    g_pada = int((g_moon.longitude % g_nak_span) // (g_nak_span / 4.0)) + 1
    g_rasi_num = g_moon.rasi_number
    g_rasi_name = RASHIS[g_rasi_num - 1]
    g_rasi_lord = RASI_LORDS[g_rasi_num - 1]
    g_varna, _ = VARNA_BY_RASI[g_rasi_num]
    g_vashya = VASHYA_BY_RASI[g_rasi_num]
    g_yoni = NAKSHATRA_YONI[g_nak_idx]
    g_gana = get_gana(g_nak_idx)
    g_nadi = get_nadi(g_nak_idx)

    # Extract Moon details for Bride
    b_moon = next(p for p in bride_kundali.planets if p.planet == "Moon")
    b_nak_span = 360.0 / 27.0
    b_nak_idx = int(b_moon.longitude // b_nak_span) % 27
    b_pada = int((b_moon.longitude % b_nak_span) // (b_nak_span / 4.0)) + 1
    b_rasi_num = b_moon.rasi_number
    b_rasi_name = RASHIS[b_rasi_num - 1]
    b_rasi_lord = RASI_LORDS[b_rasi_num - 1]
    b_varna, _ = VARNA_BY_RASI[b_rasi_num]
    b_vashya = VASHYA_BY_RASI[b_rasi_num]
    b_yoni = NAKSHATRA_YONI[b_nak_idx]
    b_gana = get_gana(b_nak_idx)
    b_nadi = get_nadi(b_nak_idx)

    groom_info = ProfileSummary(
        name=groom_name,
        datetime=groom_datetime_str,
        location=groom_location_str,
        moon_rasi=g_rasi_name,
        moon_rasi_number=g_rasi_num,
        moon_rasi_lord=g_rasi_lord,
        nakshatra=NAKSHATRAS[g_nak_idx],
        nakshatra_number=g_nak_idx + 1,
        nakshatra_lord=g_rasi_lord,  # We will set proper nak lord in service
        pada=g_pada,
        varna=g_varna,
        vashya=g_vashya,
        yoni=g_yoni,
        gana=g_gana,
        nadi=g_nadi,
    )

    bride_info = ProfileSummary(
        name=bride_name,
        datetime=bride_datetime_str,
        location=bride_location_str,
        moon_rasi=b_rasi_name,
        moon_rasi_number=b_rasi_num,
        moon_rasi_lord=b_rasi_lord,
        nakshatra=NAKSHATRAS[b_nak_idx],
        nakshatra_number=b_nak_idx + 1,
        nakshatra_lord=b_rasi_lord,
        pada=b_pada,
        varna=b_varna,
        vashya=b_vashya,
        yoni=b_yoni,
        gana=b_gana,
        nadi=b_nadi,
    )

    # Calculate 8 Kootas
    varna_res = calculate_varna(g_rasi_num, b_rasi_num)
    vashya_res = calculate_vashya(g_rasi_num, b_rasi_num)
    tara_res = calculate_tara(g_nak_idx, b_nak_idx)
    yoni_res = calculate_yoni(g_nak_idx, b_nak_idx)
    graha_maitri_res = calculate_graha_maitri(g_rasi_num, b_rasi_num)
    gana_res = calculate_gana(g_nak_idx, b_nak_idx)
    bhakoot_res = calculate_bhakoot(g_rasi_num, b_rasi_num, g_nak_idx, b_nak_idx)
    nadi_res = calculate_nadi(g_nak_idx, b_nak_idx, g_rasi_num, b_rasi_num, g_pada, b_pada)

    kootas = {
        "varna": varna_res,
        "vashya": vashya_res,
        "tara": tara_res,
        "yoni": yoni_res,
        "graha_maitri": graha_maitri_res,
        "gana": gana_res,
        "bhakoot": bhakoot_res,
        "nadi": nadi_res,
    }

    total_points = sum(k.obtained_points for k in kootas.values())
    max_points = 36.0
    percentage = round((total_points / max_points) * 100.0, 2)

    has_nadi_dosha = nadi_res.dosha is not None
    has_bhakoot_dosha = bhakoot_res.dosha is not None
    has_gana_dosha = gana_res.dosha is not None

    dosha_details = []
    for k in kootas.values():
        if k.dosha:
            dosha_details.append({"koota": k.name, "dosha": k.dosha, "description": k.description})

    doshas_summary = {
        "has_nadi_dosha": has_nadi_dosha,
        "has_bhakoot_dosha": has_bhakoot_dosha,
        "has_gana_dosha": has_gana_dosha,
        "dosha_details": dosha_details,
    }

    # Determine Verdict
    if total_points >= 28.0 and not has_nadi_dosha:
        result = "Uttama"
        is_recommended = True
        summary_message = "Excellent match with strong emotional, biological, and genetic harmony."
    elif total_points >= 18.0 and not has_nadi_dosha:
        result = "Madhyama"
        is_recommended = True
        summary_message = "Good match with favorable overall compatibility approved for marriage."
    else:
        result = "Adhama"
        is_recommended = False
        if has_nadi_dosha:
            summary_message = "Not recommended due to unmitigated Nadi Dosha impacting progeny health."
        else:
            summary_message = "Low compatibility score (below 18 points); match is not recommended."

    manglik_analysis = None
    if include_manglik:
        manglik_analysis = calculate_manglik_analysis(groom_kundali, bride_kundali)

    return MatchMakingResult(
        groom_info=groom_info,
        bride_info=bride_info,
        total_points=total_points,
        max_points=max_points,
        percentage=percentage,
        result=result,
        is_recommended=is_recommended,
        summary_message=summary_message,
        kootas=kootas,
        doshas_summary=doshas_summary,
        manglik_analysis=manglik_analysis,
    )
