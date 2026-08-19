"""Tests for Vedic Ashtakoota Matchmaking (Guna Milan) calculations and API endpoints."""

from __future__ import annotations

import pytest

from hora_server.astrology.matchmaking import (
    calculate_bhakoot,
    calculate_gana,
    calculate_graha_maitri,
    calculate_nadi,
    calculate_tara,
    calculate_varna,
    calculate_vashya,
    calculate_yoni,
    get_gana,
    get_nadi,
)


def test_varna_koota():
    # Groom Brahmin (Cancer: 4), Bride Vaishya (Taurus: 2) -> 1.0 pt
    res = calculate_varna(4, 2)
    assert res.obtained_points == 1.0
    assert res.is_favorable is True
    assert res.dosha is None

    # Groom Shudra (Gemini: 3), Bride Brahmin (Pisces: 12) -> 0.0 pt
    res2 = calculate_varna(3, 12)
    assert res2.obtained_points == 0.0
    assert res2.is_favorable is False
    assert res2.dosha == "Varna Dosha"


def test_vashya_koota():
    # Same sign -> 2.0 pts
    res = calculate_vashya(1, 1)
    assert res.obtained_points == 2.0
    assert res.is_favorable is True

    # Mesha (1) and Simha (5) -> 0.0 pts (Food-predator)
    res_inimical = calculate_vashya(1, 5)
    assert res_inimical.obtained_points == 0.0
    assert res_inimical.dosha == "Vashya Dosha"

    # Meena (12: Jalachara) and Kumbha (11: Manava) -> 1.0 pt
    res_meena_kumbha = calculate_vashya(12, 11)
    assert res_meena_kumbha.obtained_points == 1.0
    assert res_meena_kumbha.is_favorable is True

    # Meena (12: Jalachara) and Makara (10: Jalachara) -> 2.0 pts
    res_meena_makara = calculate_vashya(12, 10)
    assert res_meena_makara.obtained_points == 2.0
    assert res_meena_makara.is_favorable is True

    # Kumbha (11: Manava) and Mesha (1: Chatushpada) -> 0.0 pts
    res_kumbha_mesha = calculate_vashya(11, 1)
    assert res_kumbha_mesha.obtained_points == 0.0
    assert res_kumbha_mesha.dosha == "Vashya Dosha"



def test_tara_koota():
    # Same nakshatra (Ashwini=0, Ashwini=0) -> Janma Tara (1) -> Favorable 3.0 pts
    res = calculate_tara(0, 0)
    assert res.obtained_points == 3.0
    assert res.is_favorable is True

    # Vaibhav (Punarvasu: 6 -> Vadha) & Sneha (Swati: 14 -> Sadhana) -> 1.5 pts
    res_vaib_sne = calculate_tara(6, 14)
    assert res_vaib_sne.obtained_points == 1.5
    assert res_vaib_sne.groom_attribute == "Vadha"
    assert res_vaib_sne.bride_attribute == "Sadhana"
    assert res_vaib_sne.is_favorable is True

    # Rohini (3 -> Kshema) and Punarvasu (6 -> Vadha) -> 1.5 pts
    res_roh_pun = calculate_tara(3, 6)
    assert res_roh_pun.obtained_points == 1.5
    assert res_roh_pun.groom_attribute == "Kshema"
    assert res_roh_pun.bride_attribute == "Vadha"
    assert res_roh_pun.is_favorable is True

    # Chitra (13 -> Pratyak) and Hasta (12 -> Kshema) -> 1.5 pts
    res_ch_ha = calculate_tara(13, 12)
    assert res_ch_ha.obtained_points == 1.5
    assert res_ch_ha.groom_attribute == "Pratyak"
    assert res_ch_ha.bride_attribute == "Kshema"
    assert res_ch_ha.is_favorable is True

    # Purva Bhadrapada (24 -> Vadha) and Dhanishtha (22 -> Pratyak):
    # Both inauspicious, but Jupiter & Mars are mutual friends -> Parihara 1.5 pts
    res_pb_dh = calculate_tara(24, 22)
    assert res_pb_dh.obtained_points == 1.5
    assert res_pb_dh.groom_attribute == "Vadha"
    assert res_pb_dh.bride_attribute == "Pratyak"
    assert res_pb_dh.is_favorable is True
    assert res_pb_dh.parihara_applied is True






def test_yoni_koota():
    # Same Yoni (Ashwini=0 Horse, Shatabhisha=23 Horse) -> 4.0 pts
    res = calculate_yoni(0, 23)
    assert res.obtained_points == 4.0
    assert res.is_favorable is True
    assert res.dosha is None

    # Cat (6: Punarvasu) vs Buffalo (14: Swati) -> 3.0 pts (Friendly Yonis)
    res_cat_buf = calculate_yoni(6, 14)
    assert res_cat_buf.obtained_points == 3.0
    assert res_cat_buf.is_favorable is True

    # Sworn enemies: Horse (0: Ashwini) vs Buffalo (12: Hasta) -> 0.0 pts
    res_enemy = calculate_yoni(0, 12)
    assert res_enemy.obtained_points == 0.0
    assert res_enemy.dosha == "Yoni Vairi Dosha"

    # Elephant (1: Bharani) vs Tiger (13: Chitra) -> 3.0 pts (Groom Elephant, Bride Tiger)
    res_ele_tig = calculate_yoni(1, 13)
    assert res_ele_tig.obtained_points == 3.0
    assert res_ele_tig.is_favorable is True

    # Dog (5: Ardra) vs Cat (6: Punarvasu) -> 1.0 pt
    res_dog_cat = calculate_yoni(5, 6)
    assert res_dog_cat.obtained_points == 1.0


def test_graha_maitri_koota():
    # Same Rasi lord: Mesha (1) and Vrishchika (8), both Mars -> 5.0 pts
    res = calculate_graha_maitri(1, 8)
    assert res.obtained_points == 5.0
    assert res.is_favorable is True
    assert res.dosha is None

    # Mutual enemies: Leo (5: Sun) and Capricorn (10: Saturn) -> 0.0 pts
    res_enemy = calculate_graha_maitri(5, 10)
    assert res_enemy.obtained_points == 0.0
    assert res_enemy.dosha == "Graha Maitri Dosha"


def test_gana_koota():
    # Same Gana: Ashwini (0: Deva) and Punarvasu (6: Deva) -> 6.0 pts
    assert get_gana(0) == "Deva"
    assert get_gana(6) == "Deva"
    assert get_gana(1) == "Manushya"  # Bharani
    assert get_gana(2) == "Rakshasa"  # Krittika

    # Deva-Deva -> 6.0 pts
    assert calculate_gana(0, 6).obtained_points == 6.0

    # Bride Deva (0), Groom Manushya (1) -> 4.0 pts
    res_bdeva_gmanu = calculate_gana(1, 0)
    assert res_bdeva_gmanu.obtained_points == 4.0
    assert res_bdeva_gmanu.is_favorable is True

    # Bride Deva (0), Groom Rakshasa (2) -> 2.0 pts
    res_bdeva_grak = calculate_gana(2, 0)
    assert res_bdeva_grak.obtained_points == 2.0
    assert res_bdeva_grak.dosha == "Gana Dosha"

    # Bride Manushya (1), Groom Deva (0) -> 5.0 pts
    res_bmanu_gdeva = calculate_gana(0, 1)
    assert res_bmanu_gdeva.obtained_points == 5.0
    assert res_bmanu_gdeva.is_favorable is True

    # Bride Manushya (1), Groom Rakshasa (2) -> 1.0 pt
    res_bmanu_grak = calculate_gana(2, 1)
    assert res_bmanu_grak.obtained_points == 1.0
    assert res_bmanu_grak.dosha == "Gana Dosha"

    # Bride Rakshasa (2), Groom Deva (0) -> 0.0 pts
    res_brak_gdeva = calculate_gana(0, 2)
    assert res_brak_gdeva.obtained_points == 0.0
    assert res_brak_gdeva.dosha == "Gana Dosha"

    # Bride Rakshasa (2), Groom Manushya (1) -> 0.0 pts
    res_brak_gmanu = calculate_gana(1, 2)
    assert res_brak_gmanu.obtained_points == 0.0
    assert res_brak_gmanu.dosha == "Gana Dosha"


def test_bhakoot_koota_and_parihara():
    # 1/7 Samasaptaka: Mesha (1) and Tula (7) -> 7.0 pts
    res = calculate_bhakoot(1, 7, 0, 14)
    assert res.obtained_points == 7.0
    assert res.is_favorable is True

    # 5/9 Navapanchama (Mithuna 3 & Tula 7): 0 pts, parihara_applied=True (Mercury & Venus friends)
    res_59 = calculate_bhakoot(3, 7, 6, 14)
    assert res_59.obtained_points == 0.0
    assert res_59.parihara_applied is True
    assert res_59.dosha == "Bhakoot Dosha (Navapanchama)"

    # 6/8 Shadashtaka (Mesha 1 & Vrishchika 8 - both ruled by Mars): 0 pts, parihara_applied=True
    res_parihara = calculate_bhakoot(1, 8, 0, 16)
    assert res_parihara.obtained_points == 0.0
    assert res_parihara.parihara_applied is True
    assert res_parihara.dosha == "Bhakoot Dosha (Shadashtaka)"

    # 2/12 Dvidvadasha (Vrishabha 2 & Mithuna 3 - Venus & Mercury): 0 pts, parihara_applied=True
    res_212 = calculate_bhakoot(2, 3, 3, 6)
    assert res_212.obtained_points == 0.0
    assert res_212.parihara_applied is True
    assert res_212.dosha == "Bhakoot Dosha (Dvidvadasha)"

    # 6/8 Shadashtaka without Parihara: Mesha (1: Mars) and Kanya (6: Mercury) -> 0.0 pts, parihara_applied=False
    res_dosha = calculate_bhakoot(1, 6, 0, 11)
    assert res_dosha.obtained_points == 0.0
    assert res_dosha.dosha == "Bhakoot Dosha (Shadashtaka)"
    assert res_dosha.parihara_applied is False



def test_nadi_koota_and_parihara():
    # Different Nadis: Ashwini (0: Adi) and Bharani (1: Madhya) -> 8.0 pts
    assert get_nadi(0) == "Adi"
    assert get_nadi(1) == "Madhya"
    res = calculate_nadi(0, 1, 1, 1, 1, 1)
    assert res.obtained_points == 8.0
    assert res.is_favorable is True
    assert res.dosha is None

    # Same Nadi without Parihara: Ashwini (0: Adi) and Ardra (5: Adi), different signs -> 0.0 pts
    res_dosha = calculate_nadi(0, 5, 1, 3, 1, 1)
    assert res_dosha.obtained_points == 0.0
    assert res_dosha.dosha == "Nadi Dosha"
    assert res_dosha.parihara_applied is False

    # Same Nadi with Parihara: Same Rasi (Mesha: 1) but different Nakshatras -> 0.0 pts, parihara_applied=True
    res_parihara = calculate_nadi(0, 5, 1, 1, 1, 1)
    assert res_parihara.obtained_points == 0.0
    assert res_parihara.parihara_applied is True
    assert res_parihara.dosha == "Nadi Dosha"



@pytest.fixture()
def setup_locations(app):
    registry = app.extensions["location_registry"]
    registry.add_entry("favorite_cities", "Bengaluru", {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
    })
    registry.add_entry("favorite_cities", "Mysuru", {
        "latitude": 12.2958,
        "longitude": 76.6394,
        "timezone": "Asia/Kolkata",
    })
    yield registry


def test_post_matchmaking_api_success(client, setup_locations):
    payload = {
        "groom": {
            "name": "Arjun",
            "dob": "1995-05-15",
            "tob": "08:30:00",
            "pob": "Bengaluru",
        },
        "bride": {
            "name": "Sneha",
            "dob": "1997-11-20",
            "tob": "14:15:00",
            "pob": "Mysuru",
        },
        "ayanamsa": "lahiri",
        "lang": "en",
        "include_manglik": True,
    }

    response = client.post("/api/v1/matchmaking", json=payload)
    assert response.status_code == 200
    data = response.get_json()

    assert "groom_info" in data
    assert "bride_info" in data
    assert "guna_milan" in data
    assert "kootas" in data
    assert "doshas_summary" in data
    assert "manglik_analysis" in data

    assert data["groom_info"]["name"] == "Arjun"
    assert data["bride_info"]["name"] == "Sneha"
    assert data["guna_milan"]["max_points"] == 36.0
    assert 0.0 <= data["guna_milan"]["total_points"] <= 36.0
    assert data["guna_milan"]["result"] in ("Uttama", "Madhyama", "Adhama")

    # Check that all 8 kootas are present
    kootas = data["kootas"]
    for k in ("varna", "vashya", "tara", "yoni", "graha_maitri", "gana", "bhakoot", "nadi"):
        assert k in kootas
        assert "obtained_points" in kootas[k]
        assert "max_points" in kootas[k]


def test_post_matchmaking_api_with_coordinates(client):
    payload = {
        "groom": {
            "name": "Arjun",
            "dob": "1995-05-15",
            "tob": "08:30:00",
            "lat": 12.9716,
            "lon": 77.5946,
            "timezone": "Asia/Kolkata",
        },
        "bride": {
            "name": "Sneha",
            "dob": "1997-11-20",
            "tob": "14:15:00",
            "lat": 12.2958,
            "lon": 76.6394,
            "timezone": "Asia/Kolkata",
        },
        "ayanamsa": "lahiri",
        "lang": "en",
        "include_manglik": True,
    }

    response = client.post("/api/v1/matchmaking", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["guna_milan"]["max_points"] == 36.0


def test_get_matchmaking_api_success(client, setup_locations):
    params = {
        "groom_name": "Vikram",
        "groom_dob": "1992-03-25",
        "groom_tob": "06:00:00",
        "groom_pob": "Bengaluru",
        "bride_name": "Ananya",
        "bride_dob": "1994-08-10",
        "bride_tob": "10:30:00",
        "bride_pob": "Bengaluru",
        "ayanamsa": "lahiri",
        "lang": "en",
    }
    response = client.get("/api/v1/matchmaking", query_string=params)
    assert response.status_code == 200
    data = response.get_json()
    assert data["groom_info"]["name"] == "Vikram"
    assert data["bride_info"]["name"] == "Ananya"
    assert data["guna_milan"]["max_points"] == 36.0


def test_matchmaking_api_kannada_localization(client, setup_locations):
    payload = {
        "groom": {
            "name": "ಅರ್ಜುನ್",
            "dob": "1995-05-15",
            "tob": "08:30:00",
            "pob": "Bengaluru",
        },
        "bride": {
            "name": "ಸ್ನೇಹಾ",
            "dob": "1997-11-20",
            "tob": "14:15:00",
            "pob": "Mysuru",
        },
        "lang": "kan",
    }
    response = client.post("/api/v1/matchmaking", json=payload)
    assert response.status_code == 200
    data = response.get_json()

    assert data["guna_milan"]["result"] in ("ಉತ್ತಮ", "ಮಧ್ಯಮ", "ಅಧಮ")
    assert "ವರ್ಣ" in str(data["kootas"]) or "ನಾಡಿ" in str(data["kootas"])

    # Check that descriptions are in Kannada (contain Kannada characters)
    tara_desc = data["kootas"]["tara"]["description"]
    assert any("\u0c80" <= char <= "\u0cff" for char in tara_desc)
    summary_msg = data["guna_milan"]["summary_message"]
    assert any("\u0c80" <= char <= "\u0cff" for char in summary_msg)



def test_matchmaking_api_errors(client, setup_locations):
    # Missing groom dob
    res1 = client.post("/api/v1/matchmaking", json={
        "groom": {"name": "Test"},
        "bride": {"name": "Bride", "dob": "1995-01-01", "pob": "Bengaluru"}
    })
    assert res1.status_code == 400

    # Invalid datetime out of range
    res2 = client.post("/api/v1/matchmaking", json={
        "groom": {"dob": "1500-01-01", "pob": "Bengaluru"},
        "bride": {"dob": "1995-01-01", "pob": "Bengaluru"}
    })
    assert res2.status_code == 422

    # Invalid location
    res3 = client.post("/api/v1/matchmaking", json={
        "groom": {"dob": "1995-01-01", "pob": "NonExistentPlaceXYZ987"},
        "bride": {"dob": "1995-01-01", "pob": "Bengaluru"}
    })
    assert res3.status_code == 404

