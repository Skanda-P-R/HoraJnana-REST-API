from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from hora_server.astronomy.ephemeris import EphemerisEngine, Positions
from hora_server.astrology.panchanga import (
    karana_name,
    phase_index,
    tithi_name,
)
from hora_server.utils.errors import ApiError


@pytest.mark.parametrize(
    ("index", "expected"),
    [
        (0, "Shukla Pratipada"),
        (14, "Purnima"),
        (15, "Krishna Pratipada"),
        (28, "Krishna Chaturdashi"),
        (29, "Amavasya"),
    ],
)
def test_tithi_names(index, expected):
    assert tithi_name(index)[0] == expected


def test_all_fixed_and_repeating_karanas():
    assert karana_name(0) == "Kimstughna"
    assert [karana_name(index) for index in range(1, 8)] == [
        "Bava",
        "Balava",
        "Kaulava",
        "Taitila",
        "Gara",
        "Vanija",
        "Vishti",
    ]
    assert karana_name(56) == "Vishti"
    assert karana_name(57) == "Shakuni"
    assert karana_name(58) == "Chatushpada"
    assert karana_name(59) == "Naga"


def test_tithi_and_karana_use_tropical_elongation_only():
    first = Positions(0, 20, 75, 350, 1, 24, "swiss")
    second = Positions(0, 20, 75, 100, 200, 25, "swiss")

    assert phase_index(first, "tithi") == phase_index(second, "tithi")
    assert phase_index(first, "karana") == phase_index(second, "karana")


def test_angular_classification_wraps_at_360_degrees():
    almost_new_moon = Positions(0, 0, 359.999999, 0, 359.999999, 24, "swiss")
    new_moon = Positions(0, 0, 0, 0, 0, 24, "swiss")

    assert phase_index(almost_new_moon, "tithi") == 29
    assert phase_index(new_moon, "tithi") == 0
    assert phase_index(almost_new_moon, "nakshatra") == 26
    assert phase_index(new_moon, "nakshatra") == 0


def test_threaded_ayanamsa_requests_do_not_leak_global_mode():
    project_root = Path(__file__).resolve().parents[1]
    engine = EphemerisEngine(
        str(project_root / "hora_server" / "ephe"), strict_swiss=True
    )
    instant = datetime(2026, 7, 8, 6, 30, tzinfo=ZoneInfo("UTC"))
    lahiri = engine.resolve_ayanamsa("lahiri")
    raman = engine.resolve_ayanamsa("raman")

    def calculate(mode):
        return engine.positions(instant, mode)

    with ThreadPoolExecutor(max_workers=8) as executor:
        values = list(executor.map(calculate, [lahiri, raman] * 20))

    lahiri_values = values[0::2]
    raman_values = values[1::2]
    assert len({round(value.moon_sidereal, 10) for value in lahiri_values}) == 1
    assert len({round(value.moon_sidereal, 10) for value in raman_values}) == 1
    assert lahiri_values[0].moon_sidereal != raman_values[0].moon_sidereal
    assert all(value.ephemeris == "swiss" for value in values)


def test_each_serialized_transition_is_on_new_side_of_boundary(app, client, bengaluru_query):
    data = client.get("/api/v1/panchanga", query_string=bengaluru_query).get_json()
    service = app.extensions["panchanga_service"]
    mode = service.engine.resolve_ayanamsa("lahiri")

    for kind in ("tithi", "nakshatra", "yoga", "karana"):
        transition = datetime.fromisoformat(
            data["panchanga_details"][kind]["ends_at"]
        )
        before = service.engine.positions(transition - timedelta(seconds=1), mode)
        at_boundary = service.engine.positions(transition, mode)
        assert phase_index(before, kind) != phase_index(at_boundary, kind)


def test_each_engine_restores_its_own_global_ephemeris_path(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    good = EphemerisEngine(
        str(project_root / "hora_server" / "ephe"), strict_swiss=True
    )
    empty = EphemerisEngine(str(tmp_path), strict_swiss=True)
    instant = datetime(2026, 7, 8, tzinfo=ZoneInfo("UTC"))
    mode = good.resolve_ayanamsa("lahiri")

    assert good.positions(instant, mode).ephemeris == "swiss"
    with pytest.raises(ApiError) as error:
        empty.positions(instant, mode)
    assert error.value.code == "ephemeris_unavailable"
    assert good.positions(instant, mode).ephemeris == "swiss"


def test_panchanga_details_returns_all_daily_yogas_and_karanas(client, bengaluru_query):
    response = client.get("/api/v1/panchanga", query_string=bengaluru_query)
    assert response.status_code == 200
    data = response.get_json()

    panchanga_details = data["panchanga_details"]
    assert "all" in panchanga_details["karana"]
    assert "all" in panchanga_details["yoga"]

    # Check Karanas
    karanas = panchanga_details["karana"]["all"]
    assert 2 <= len(karanas) <= 3
    for item in karanas:
        assert "name" in item
        assert "ends_at" in item
        assert isinstance(item["name"], str) and len(item["name"]) > 0
        assert datetime.fromisoformat(item["ends_at"]) is not None

    # Check chronological ordering of Karana transitions
    karana_ends = [datetime.fromisoformat(k["ends_at"]) for k in karanas]
    assert karana_ends == sorted(karana_ends)
    assert len(set(karana_ends)) == len(karana_ends)

    # Check Yogas
    yogas = panchanga_details["yoga"]["all"]
    assert 1 <= len(yogas) <= 3
    for item in yogas:
        assert "name" in item
        assert "ends_at" in item
        assert isinstance(item["name"], str) and len(item["name"]) > 0
        assert datetime.fromisoformat(item["ends_at"]) is not None

    # Check chronological ordering of Yoga transitions
    yoga_ends = [datetime.fromisoformat(y["ends_at"]) for y in yogas]
    assert yoga_ends == sorted(yoga_ends)
    assert len(set(yoga_ends)) == len(yoga_ends)

    # Ensure tithi and nakshatra do not have 'all'
    assert "all" not in panchanga_details["tithi"]
    assert "all" not in panchanga_details["nakshatra"]


def test_daily_yogas_and_karanas_kannada_localization(client, bengaluru_query):
    query = {**bengaluru_query, "lang": "kan"}
    response = client.get("/api/v1/panchanga", query_string=query)
    assert response.status_code == 200
    data = response.get_json()

    karanas = data["panchanga_details"]["karana"]["all"]
    yogas = data["panchanga_details"]["yoga"]["all"]

    for item in karanas:
        # Verify name is non-ASCII Kannada
        assert any(ord(c) > 127 for c in item["name"])
        # Verify timestamp remains a valid ISO format
        assert datetime.fromisoformat(item["ends_at"]) is not None

    for item in yogas:
        assert any(ord(c) > 127 for c in item["name"])
        assert datetime.fromisoformat(item["ends_at"]) is not None

