"""Current transit Kundali calculation using Swiss sidereal positions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final

import swisseph as swe

from hora_server.astronomy.ephemeris import Ayanamsa, EphemerisEngine
from hora_server.astrology.constants import (
    CHARA_KARAKA_NAMES,
    CHARA_KARAKA_PLANETS,
    DASHA_LORDS,
    ENGLISH_RASIS,
    NAKSHATRAS,
    RASI_LORDS,
)


RASI_NAMES: Final[tuple[str, ...]] = ENGLISH_RASIS

PLANET_BODIES: Final[tuple[tuple[str, str, int], ...]] = (
    ("Sun", "Su", swe.SUN),
    ("Moon", "Mo", swe.MOON),
    ("Mars", "Ma", swe.MARS),
    ("Mercury", "Me", swe.MERCURY),
    ("Jupiter", "Ju", swe.JUPITER),
    ("Venus", "Ve", swe.VENUS),
    ("Saturn", "Sa", swe.SATURN),
    ("Rahu", "Ra", swe.MEAN_NODE),
)


@dataclass(frozen=True)
class KundaliLagna:
    rasi: str
    number: int
    longitude: float
    degree_in_rasi: float


@dataclass(frozen=True)
class KundaliPlanet:
    planet: str
    symbol: str
    longitude: float
    degree_in_rasi: float
    rasi: str
    rasi_number: int
    house: int
    retrograde: bool


@dataclass(frozen=True)
class KundaliHouse:
    house: int
    rasi: str
    rasi_number: int
    planets: tuple[str, ...]


@dataclass(frozen=True)
class YogiPointDetails:
    longitude: float
    degree_in_rasi: float
    rasi: str
    rasi_number: int
    rasi_lord: str
    nakshatra: str
    nakshatra_number: int
    nakshatra_lord: str
    pada: int
    house: int


@dataclass(frozen=True)
class YogiAvayogi:
    yogi_planet: str
    duplicate_yogi: str
    avayogi_planet: str
    duplicate_avayogi: str
    yogi_point: YogiPointDetails
    avayogi_point: YogiPointDetails


@dataclass(frozen=True)
class CharaKarakaDetails:
    rank: int
    karaka: str
    karaka_code: str
    planet: str
    symbol: str
    degree_in_rasi: float
    longitude: float
    rasi: str
    rasi_number: int
    rasi_lord: str
    house: int
    nakshatra: str
    nakshatra_number: int
    nakshatra_lord: str
    pada: int
    navamsha_rasi: str
    navamsha_rasi_number: int
    retrograde: bool
    signification: str


@dataclass(frozen=True)
class CharaKarakaReport:
    atmakaraka: CharaKarakaDetails
    darakaraka: CharaKarakaDetails
    karakas: tuple[CharaKarakaDetails, ...]


@dataclass(frozen=True)
class Kundali:
    lagna: KundaliLagna
    houses: tuple[KundaliHouse, ...]
    planets: tuple[KundaliPlanet, ...]
    yogi_avayogi: YogiAvayogi | None = None
    chara_karakas: CharaKarakaReport | None = None


def _rasi_number(longitude: float) -> int:
    return int((longitude % 360) // 30) + 1


def _rasi_name(number: int) -> str:
    return RASI_NAMES[number - 1]


def _degree_in_rasi(longitude: float) -> float:
    return longitude % 30


def _house_for_rasi(rasi_number: int, lagna_number: int) -> int:
    return ((rasi_number - lagna_number) % 12) + 1


def _planet(
    name: str,
    symbol: str,
    longitude: float,
    speed_longitude: float,
    lagna_number: int,
) -> KundaliPlanet:
    rasi_number = _rasi_number(longitude)
    is_retrograde = speed_longitude < 0 if name not in ("Rahu", "Ketu") else False
    return KundaliPlanet(
        planet=name,
        symbol=symbol,
        longitude=longitude % 360,
        degree_in_rasi=_degree_in_rasi(longitude),
        rasi=_rasi_name(rasi_number),
        rasi_number=rasi_number,
        house=_house_for_rasi(rasi_number, lagna_number),
        retrograde=is_retrograde,
    )


def calculate_yogi_avayogi(
    sun_longitude: float,
    moon_longitude: float,
    lagna_number: int,
) -> YogiAvayogi:
    nak_span = 360.0 / 27.0
    pada_span = nak_span / 4.0

    # 1. Yogi Point (Yoga Sphuta) = (Sun + Moon + 93° 20') % 360
    # 93° 20' = 93 + 20/60 = 280/3 degrees
    yogi_longitude = (sun_longitude + moon_longitude + (93.0 + 20.0 / 60.0)) % 360.0
    yogi_rasi_num = _rasi_number(yogi_longitude)
    yogi_degree = _degree_in_rasi(yogi_longitude)
    yogi_nak_idx = int(yogi_longitude // nak_span) % 27
    yogi_pada = int((yogi_longitude % nak_span) // pada_span) + 1
    yogi_nak_lord = DASHA_LORDS[yogi_nak_idx % 9]
    yogi_rasi_lord = RASI_LORDS[yogi_rasi_num - 1]
    yogi_house = _house_for_rasi(yogi_rasi_num, lagna_number)

    yogi_point = YogiPointDetails(
        longitude=yogi_longitude,
        degree_in_rasi=yogi_degree,
        rasi=_rasi_name(yogi_rasi_num),
        rasi_number=yogi_rasi_num,
        rasi_lord=yogi_rasi_lord,
        nakshatra=NAKSHATRAS[yogi_nak_idx],
        nakshatra_number=yogi_nak_idx + 1,
        nakshatra_lord=yogi_nak_lord,
        pada=yogi_pada,
        house=yogi_house,
    )

    # 2. Avayogi Point (Avayoga Sphuta) = (Yogi Point + 186° 40') % 360
    # 186° 40' = 186 + 40/60 = 560/3 degrees
    avayogi_longitude = (yogi_longitude + (186.0 + 40.0 / 60.0)) % 360.0
    avayogi_rasi_num = _rasi_number(avayogi_longitude)
    avayogi_degree = _degree_in_rasi(avayogi_longitude)
    avayogi_nak_idx = int(avayogi_longitude // nak_span) % 27
    avayogi_pada = int((avayogi_longitude % nak_span) // pada_span) + 1
    avayogi_nak_lord = DASHA_LORDS[avayogi_nak_idx % 9]
    avayogi_rasi_lord = RASI_LORDS[avayogi_rasi_num - 1]
    avayogi_house = _house_for_rasi(avayogi_rasi_num, lagna_number)

    avayogi_point = YogiPointDetails(
        longitude=avayogi_longitude,
        degree_in_rasi=avayogi_degree,
        rasi=_rasi_name(avayogi_rasi_num),
        rasi_number=avayogi_rasi_num,
        rasi_lord=avayogi_rasi_lord,
        nakshatra=NAKSHATRAS[avayogi_nak_idx],
        nakshatra_number=avayogi_nak_idx + 1,
        nakshatra_lord=avayogi_nak_lord,
        pada=avayogi_pada,
        house=avayogi_house,
    )

    return YogiAvayogi(
        yogi_planet=yogi_nak_lord,
        duplicate_yogi=yogi_rasi_lord,
        avayogi_planet=avayogi_nak_lord,
        duplicate_avayogi=avayogi_rasi_lord,
        yogi_point=yogi_point,
        avayogi_point=avayogi_point,
    )


def _navamsha_rasi_number(longitude: float) -> int:
    """Calculate the Navamsha (D9) Rasi number (1-12) for a given sidereal longitude."""
    # 108 navamsha divisions in 360 degrees (each is exactly 3°20' = 10/3 degrees)
    nav_index = int(((longitude % 360.0) * 108.0 / 360.0) + 1e-9)
    return (nav_index % 12) + 1


def calculate_chara_karakas(
    planets: tuple[KundaliPlanet, ...],
    lagna_number: int,
) -> CharaKarakaReport:
    """Calculate the 7 Chara Karakas (Sapta Chara Karakas) from planetary positions."""
    physical_planets = [p for p in planets if p.planet in CHARA_KARAKA_PLANETS]
    physical_planets.sort(
        key=lambda p: (round(p.degree_in_rasi, 8), p.longitude),
        reverse=True,
    )

    nak_span = 360.0 / 27.0
    pada_span = nak_span / 4.0

    karaka_details_list: list[CharaKarakaDetails] = []
    for rank, (planet, (k_name, k_code, k_sig_en, _)) in enumerate(
        zip(physical_planets, CHARA_KARAKA_NAMES, strict=True),
        start=1,
    ):
        nak_idx = int(planet.longitude // nak_span) % 27
        pada = int((planet.longitude % nak_span) // pada_span) + 1
        nak_lord = DASHA_LORDS[nak_idx % 9]
        rasi_lord = RASI_LORDS[planet.rasi_number - 1]
        nav_rasi_num = _navamsha_rasi_number(planet.longitude)
        nav_rasi_name = _rasi_name(nav_rasi_num)

        karaka_details_list.append(
            CharaKarakaDetails(
                rank=rank,
                karaka=k_name,
                karaka_code=k_code,
                planet=planet.planet,
                symbol=planet.symbol,
                degree_in_rasi=planet.degree_in_rasi,
                longitude=planet.longitude,
                rasi=planet.rasi,
                rasi_number=planet.rasi_number,
                rasi_lord=rasi_lord,
                house=planet.house,
                nakshatra=NAKSHATRAS[nak_idx],
                nakshatra_number=nak_idx + 1,
                nakshatra_lord=nak_lord,
                pada=pada,
                navamsha_rasi=nav_rasi_name,
                navamsha_rasi_number=nav_rasi_num,
                retrograde=planet.retrograde,
                signification=k_sig_en,
            )
        )

    return CharaKarakaReport(
        atmakaraka=karaka_details_list[0],
        darakaraka=karaka_details_list[-1],
        karakas=tuple(karaka_details_list),
    )


def calculate_kundali(
    instant: datetime,
    latitude: float,
    longitude: float,
    engine: EphemerisEngine,
    ayanamsa: Ayanamsa,
) -> Kundali:
    ascendant = engine.sidereal_ascendant(
        instant, ayanamsa, latitude, longitude
    )
    lagna_number = _rasi_number(ascendant)
    lagna = KundaliLagna(
        rasi=_rasi_name(lagna_number),
        number=lagna_number,
        longitude=ascendant,
        degree_in_rasi=_degree_in_rasi(ascendant),
    )

    body_positions = engine.sidereal_body_positions(
        instant,
        ayanamsa,
        tuple((name, body) for name, _, body in PLANET_BODIES),
    )
    planets = [
        _planet(
            name,
            symbol,
            body_positions[name].longitude,
            body_positions[name].speed_longitude,
            lagna_number,
        )
        for name, symbol, _ in PLANET_BODIES
    ]

    rahu = body_positions["Rahu"]
    planets.append(
        _planet(
            "Ketu",
            "Ke",
            rahu.longitude + 180,
            rahu.speed_longitude,
            lagna_number,
        )
    )

    planet_names_by_house: dict[int, list[str]] = {house: [] for house in range(1, 13)}
    for planet in planets:
        planet_names_by_house[planet.house].append(planet.planet)

    houses = tuple(
        KundaliHouse(
            house=house,
            rasi=_rasi_name(((lagna_number + house - 2) % 12) + 1),
            rasi_number=((lagna_number + house - 2) % 12) + 1,
            planets=tuple(planet_names_by_house[house]),
        )
        for house in range(1, 13)
    )

    sun_lon = body_positions["Sun"].longitude
    moon_lon = body_positions["Moon"].longitude
    yogi_avayogi = calculate_yogi_avayogi(sun_lon, moon_lon, lagna_number)
    chara_karakas = calculate_chara_karakas(tuple(planets), lagna_number)

    return Kundali(
        lagna=lagna,
        houses=houses,
        planets=tuple(planets),
        yogi_avayogi=yogi_avayogi,
        chara_karakas=chara_karakas,
    )

