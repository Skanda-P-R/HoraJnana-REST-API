"""Tests for Atmakaraka, Darakaraka, and 7-Chara Karaka calculations."""

from __future__ import annotations

import pytest

from hora_server.astrology.constants import CHARA_KARAKA_PLANETS
from hora_server.astrology.kundali import (
    _navamsha_rasi_number,
    calculate_chara_karakas,
)


def test_navamsha_rasi_number_calculation():
    # Aries 0° -> Navamsha 1 (Aries)
    assert _navamsha_rasi_number(0.0) == 1
    # Aries 3°20' -> Navamsha 2 (Taurus)
    assert _navamsha_rasi_number(3.3334) == 2
    # Aries 29° -> Navamsha 9 (Sagittarius)
    assert _navamsha_rasi_number(29.0) == 9
    # Taurus 0° (30.0°) -> Navamsha 10 (Capricorn)
    assert _navamsha_rasi_number(30.0) == 10
    # Pisces 29° (359.0°) -> Navamsha 12 (Pisces)
    assert _navamsha_rasi_number(359.0) == 12


def test_chara_karakas_in_transit_kundali(client, bengaluru_query):
    response = client.get("/api/v1/kundali", query_string=bengaluru_query)
    assert response.status_code == 200
    data = response.get_json()

    assert "atmakaraka" in data
    assert "darakaraka" in data
    assert "chara_karakas" in data

    ak = data["atmakaraka"]
    dk = data["darakaraka"]
    karakas = data["chara_karakas"]

    # Verify 7 karakas
    assert len(karakas) == 7

    # Verify descending degree order
    degrees = [k["degree_in_rasi"] for k in karakas]
    assert degrees == sorted(degrees, reverse=True)

    # Verify ranks and codes
    expected_codes = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK"]
    expected_names = [
        "Atmakaraka",
        "Amatyakaraka",
        "Bhratrukaraka",
        "Matrukaraka",
        "Putrakaraka",
        "Gnatikaraka",
        "Darakaraka",
    ]
    for idx, item in enumerate(karakas):
        assert item["rank"] == idx + 1
        assert item["karaka_code"] == expected_codes[idx]
        assert item["karaka"] == expected_names[idx]
        assert item["planet"] in CHARA_KARAKA_PLANETS
        assert "signification" in item
        assert "navamsha_rasi" in item
        assert 1 <= item["navamsha_rasi_number"] <= 12

    # Atmakaraka is the first item (highest degree)
    assert ak["karaka"] == "Atmakaraka"
    assert ak["karaka_code"] == "AK"
    assert ak["rank"] == 1
    assert ak["planet"] == karakas[0]["planet"]
    assert ak["degree_in_rasi"] == karakas[0]["degree_in_rasi"]
    assert ak["longitude"] == karakas[0]["longitude"]
    assert ak["rasi"] == karakas[0]["rasi"]
    assert ak["rasi_number"] == karakas[0]["rasi_number"]
    assert ak["house"] == karakas[0]["house"]
    assert ak["nakshatra"] == karakas[0]["nakshatra"]
    assert ak["pada"] == karakas[0]["pada"]
    assert ak["navamsha_rasi"] == karakas[0]["navamsha_rasi"]
    assert ak["signification"] == "Soul, Self, Physical Constitution, Life Purpose"

    # Darakaraka is the last item (lowest degree)
    assert dk["karaka"] == "Darakaraka"
    assert dk["karaka_code"] == "DK"
    assert dk["rank"] == 7
    assert dk["planet"] == karakas[-1]["planet"]
    assert dk["degree_in_rasi"] == karakas[-1]["degree_in_rasi"]
    assert dk["longitude"] == karakas[-1]["longitude"]
    assert dk["signification"] == "Spouse, Life Partner, Marriage, Business Partnerships"

    # Verify Rahu and Ketu are excluded from Chara Karakas
    planet_names = [k["planet"] for k in karakas]
    assert "Rahu" not in planet_names
    assert "Ketu" not in planet_names

    # Check for the known Bengaluru 2026-07-08 reference transit chart:
    # Sun: Gemini (81.9045 -> deg 21.9045)
    # Moon: Pisces (357.7080 -> deg 27.7080) -> Highest degree (AK)!
    # Mars: Taurus (42.4714 -> deg 12.4714)
    # Mercury: Gemini (89.4395 -> deg 29.4395) -> Highest is Mercury (29.4395)!
    # Jupiter: Cancer (97.5019 -> deg 7.5019)
    # Venus: Leo (124.1491 -> deg 4.1491) -> Lowest is Venus (4.1491, DK)!
    # Saturn: Pisces (350.2275 -> deg 20.2275)
    assert ak["planet"] == "Mercury"
    assert ak["degree_in_rasi"] == pytest.approx(29.4395, abs=0.001)
    assert ak["retrograde"] is True

    assert dk["planet"] == "Venus"
    assert dk["degree_in_rasi"] == pytest.approx(4.1491, abs=0.001)
    assert dk["retrograde"] is False


def test_chara_karakas_in_birth_kundali(client, bengaluru_query):
    response = client.get(
        "/api/v1/kundali/birth",
        query_string={**bengaluru_query, "name": "Test Native"},
    )
    assert response.status_code == 200
    data = response.get_json()

    assert data["name"] == "Test Native"
    assert "atmakaraka" in data
    assert "darakaraka" in data
    assert "chara_karakas" in data

    assert data["atmakaraka"]["planet"] == "Mercury"
    assert data["atmakaraka"]["karaka"] == "Atmakaraka"
    assert data["darakaraka"]["planet"] == "Venus"
    assert data["darakaraka"]["karaka"] == "Darakaraka"


def test_chara_karakas_kannada_localization(client, bengaluru_query):
    response = client.get(
        "/api/v1/kundali",
        query_string={**bengaluru_query, "lang": "kan"},
    )
    assert response.status_code == 200
    data = response.get_json()

    ak = data["atmakaraka"]
    dk = data["darakaraka"]
    karakas = data["chara_karakas"]

    assert ak["karaka"] == "ಆತ್ಮಕಾರಕ"
    assert ak["planet"] == "ಬುಧ"
    assert ak["signification"] == "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ"

    assert dk["karaka"] == "ದಾರಕಾರಕ"
    assert dk["planet"] == "ಶುಕ್ರ"
    assert dk["signification"] == "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ"

    kannada_karaka_names = [
        "ಆತ್ಮಕಾರಕ",
        "ಅಮಾತ್ಯಕಾರಕ",
        "ಭ್ರಾತೃಕಾರಕ",
        "ಮಾತೃಕಾರಕ",
        "ಪುತ್ರಕಾರಕ",
        "ಜ್ಞಾತಿಕಾರಕ",
        "ದಾರಕಾರಕ",
    ]
    for idx, k in enumerate(karakas):
        assert k["karaka"] == kannada_karaka_names[idx]
