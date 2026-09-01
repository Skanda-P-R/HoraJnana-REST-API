"""Tests for Pancha Pakshi (Five Birds) calculation and API integration."""

from __future__ import annotations

import pytest

from hora_server.astrology.pancha_pakshi import calculate_pancha_pakshi
from hora_server.astrology.constants import NAKSHATRAS


def test_pancha_pakshi_shukla_paksha_all_nakshatras():
    # Group 1: 1-5 -> Vulture (Earth)
    for num in range(1, 6):
        res = calculate_pancha_pakshi(num, paksha="Shukla")
        assert res.bird == "Vulture"
        assert res.element == "Earth"
        assert res.nakshatra_number == num
        assert res.nakshatra == NAKSHATRAS[num - 1]
        assert res.paksha == "Shukla"

    # Group 2: 6-11 -> Owl (Water)
    for num in range(6, 12):
        res = calculate_pancha_pakshi(num, paksha="Shukla")
        assert res.bird == "Owl"
        assert res.element == "Water"
        assert res.nakshatra_number == num
        assert res.paksha == "Shukla"

    # Group 3: 12-16 -> Crow (Fire)
    for num in range(12, 17):
        res = calculate_pancha_pakshi(num, paksha="Shukla")
        assert res.bird == "Crow"
        assert res.element == "Fire"
        assert res.nakshatra_number == num
        assert res.paksha == "Shukla"

    # Group 4: 17-22 -> Cock (Air)
    for num in range(17, 23):
        res = calculate_pancha_pakshi(num, paksha="Shukla")
        assert res.bird == "Cock"
        assert res.element == "Air"
        assert res.nakshatra_number == num
        assert res.paksha == "Shukla"

    # Group 5: 23-27 -> Peacock (Ether)
    for num in range(23, 28):
        res = calculate_pancha_pakshi(num, paksha="Shukla")
        assert res.bird == "Peacock"
        assert res.element == "Ether"
        assert res.nakshatra_number == num
        assert res.paksha == "Shukla"


def test_pancha_pakshi_krishna_paksha_all_nakshatras():
    # Group 1: 1-5 -> Peacock (Ether)
    for num in range(1, 6):
        res = calculate_pancha_pakshi(num, paksha="Krishna")
        assert res.bird == "Peacock"
        assert res.element == "Ether"
        assert res.nakshatra_number == num
        assert res.paksha == "Krishna"

    # Group 2: 6-11 -> Cock (Air)
    for num in range(6, 12):
        res = calculate_pancha_pakshi(num, paksha="Krishna")
        assert res.bird == "Cock"
        assert res.element == "Air"
        assert res.nakshatra_number == num
        assert res.paksha == "Krishna"

    # Group 3: 12-16 -> Crow (Fire)
    for num in range(12, 17):
        res = calculate_pancha_pakshi(num, paksha="Krishna")
        assert res.bird == "Crow"
        assert res.element == "Fire"
        assert res.nakshatra_number == num
        assert res.paksha == "Krishna"

    # Group 4: 17-22 -> Owl (Water)
    for num in range(17, 23):
        res = calculate_pancha_pakshi(num, paksha="Krishna")
        assert res.bird == "Owl"
        assert res.element == "Water"
        assert res.nakshatra_number == num
        assert res.paksha == "Krishna"

    # Group 5: 23-27 -> Vulture (Earth)
    for num in range(23, 28):
        res = calculate_pancha_pakshi(num, paksha="Krishna")
        assert res.bird == "Vulture"
        assert res.element == "Earth"
        assert res.nakshatra_number == num
        assert res.paksha == "Krishna"


def test_pancha_pakshi_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_pancha_pakshi(0)

    with pytest.raises(ValueError):
        calculate_pancha_pakshi(28)


def test_pancha_pakshi_in_birth_kundali(client, bengaluru_query):
    query = bengaluru_query.copy()
    query["name"] = "Rama"

    response = client.get("/api/v1/kundali/birth", query_string=query)
    assert response.status_code == 200
    data = response.get_json()

    assert "pancha_pakshi" in data
    pp = data["pancha_pakshi"]

    assert set(pp.keys()) == {
        "bird",
        "element",
        "nakshatra",
        "nakshatra_number",
        "paksha",
    }

    # On Bengaluru 2026-07-08: Revati (27), Krishna Paksha -> Vulture
    assert pp["nakshatra_number"] == 27
    assert pp["nakshatra"] == "Revati"
    assert pp["paksha"] == "Krishna"
    assert pp["bird"] == "Vulture"
    assert pp["element"] == "Earth"


def test_pancha_pakshi_in_transit_kundali(client, bengaluru_query):
    response = client.get("/api/v1/kundali", query_string=bengaluru_query)
    assert response.status_code == 200
    data = response.get_json()

    assert "pancha_pakshi" in data
    assert data["pancha_pakshi"]["bird"] == "Vulture"
    assert data["pancha_pakshi"]["element"] == "Earth"


def test_pancha_pakshi_kannada_localization(client, bengaluru_query):
    query = bengaluru_query.copy()
    query["lang"] = "kan"

    response = client.get("/api/v1/kundali/birth", query_string=query)
    assert response.status_code == 200
    data = response.get_json()

    assert "pancha_pakshi" in data
    pp = data["pancha_pakshi"]
    assert set(pp.keys()) == {
        "bird",
        "element",
        "nakshatra",
        "nakshatra_number",
        "paksha",
    }
    assert pp["bird"] == "ಹದ್ದು"
    assert pp["element"] == "ಭೂಮಿ (ಪೃಥ್ವಿ)"
    assert pp["nakshatra"] == "ರೇವತಿ"
    assert pp["nakshatra_number"] == 27
    assert pp["paksha"] == "ಕೃಷ್ಣ"
