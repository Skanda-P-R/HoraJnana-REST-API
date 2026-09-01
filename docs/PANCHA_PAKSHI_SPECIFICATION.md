# Implementation Specification — Pancha Pakshi (Five Birds)

This document provides the complete astrological foundations, mathematical formulation, system architecture, and API specification for the **Pancha Pakshi** (Five Birds) system integrated into the HoraJnana REST API for Janma Kundali (`/api/v1/kundali/birth`) and Transit Kundali (`/api/v1/kundali`).

---

## 1. Astrological Background & Theoretical Foundations

**Pancha Pakshi Shastra** (Tamil: பஞ்ச பட்சி சாஸ்திரம், Sanskrit: पञ्चपक्षीशास्त्रम्) is an ancient, esoteric Vedic-Siddhic astrological system originating from South India, traditionally attributed to Sage **Agathiyar** (Agastya) and Sage **Bhogar**.

The Sanskrit term *Pancha* translates to "Five" and *Pakshi* translates to "Bird". The system correlates cosmic vibrations and bio-rhythms with five celestial birds, each presiding over one of the five primordial elements (*Pancha Mahabhutas*):

1. **Vulture** (*Valluru* / *Pingala*) — **Earth** (*Prithvi*)
2. **Owl** (*Aanthai* / *Uluka*) — **Water** (*Jala*)
3. **Crow** (*Kaagam* / *Kaka*) — **Fire** (*Agni*)
4. **Cock / Rooster** (*Kozhi* / *Kukkuta*) — **Air** (*Vayu*)
5. **Peacock** (*Mayil* / *Mayura*) — **Ether / Space** (*Akasha*)

### 1.1 The Birth Bird (*Janma Pakshi*)

Every individual is governed by a **Birth Bird (*Janma Pakshi*)** determined at the exact moment of birth based on two astronomical factors:
1. **Janma Nakshatra** (The Moon's sidereal lunar mansion, numbered 1 to 27 from Ashwini to Revati).
2. **Paksha** (The lunar fortnight at birth: *Shukla Paksha* [Waxing / Bright Half] or *Krishna Paksha* [Waning / Dark Half]).

The Birth Bird remains permanent throughout the native's lifetime, representing their core elemental constitution, behavioral dynamics, and inner energetic resonance.

---

## 2. Mathematical Mapping & Assignment Matrix

The 27 Nakshatras of the sidereal zodiac are divided into **5 groups** in a canonical **5–6–5–6–5** distribution:

### 2.1 Nakshatra Groupings (1 to 27)

- **Group 1 (5 Nakshatras):**
  1. Ashwini
  2. Bharani
  3. Krittika
  4. Rohini
  5. Mrigashira

- **Group 2 (6 Nakshatras):**
  6. Ardra
  7. Punarvasu
  8. Pushya
  9. Ashlesha
  10. Magha
  11. Purva Phalguni

- **Group 3 (5 Nakshatras):**
  12. Uttara Phalguni
  13. Hasta
  14. Chitra
  15. Swati
  16. Vishakha

- **Group 4 (6 Nakshatras):**
  17. Anuradha
  18. Jyeshtha
  19. Mula
  20. Purva Ashadha
  21. Uttara Ashadha
  22. Shravana

- **Group 5 (5 Nakshatras):**
  23. Dhanishtha
  24. Shatabhisha
  25. Purva Bhadrapada
  26. Uttara Bhadrapada
  27. Revati

$$\sum \text{Nakshatras} = 5 + 6 + 5 + 6 + 5 = 27$$

---

### 2.2 Bird Assignment by Lunar Fortnight (Paksha)

The assignment of birds is symmetric across the lunar fortnights:

| Group | Nakshatras | Shukla Paksha (Waxing) | Krishna Paksha (Waning) |
| :---: | :--- | :--- | :--- |
| **1** | Ashwini – Mrigashira (1–5) | **Vulture** (*Valluru / Pingala*) | **Peacock** (*Mayil / Mayura*) |
| **2** | Ardra – Purva Phalguni (6–11) | **Owl** (*Aanthai / Uluka*) | **Cock** (*Kozhi / Kukkuta*) |
| **3** | Uttara Phalguni – Vishakha (12–16) | **Crow** (*Kaagam / Kaka*) | **Crow** (*Kaagam / Kaka*) |
| **4** | Anuradha – Shravana (17–22) | **Cock** (*Kozhi / Kukkuta*) | **Owl** (*Aanthai / Uluka*) |
| **5** | Dhanishtha – Revati (23–27) | **Peacock** (*Mayil / Mayura*) | **Vulture** (*Valluru / Pingala*) |

> [!NOTE]
> In **Shukla Paksha**, the bird sequence follows direct cosmic manifestation: **Vulture $\rightarrow$ Owl $\rightarrow$ Crow $\rightarrow$ Cock $\rightarrow$ Peacock**.
> In **Krishna Paksha**, the bird sequence is completely mirrored / reversed: **Peacock $\rightarrow$ Cock $\rightarrow$ Crow $\rightarrow$ Owl $\rightarrow$ Vulture**.
> The central 3rd Group (Crow) remains constant in both fortnights.

---

## 3. Pancha Pakshi Bird Characteristics & Five Activities

### 3.1 Bird Profile Matrix

| Bird | Tamil Name | Sanskrit Name | Kannada Name | Element | Sanskrit Element | Cosmic Quality |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Vulture** | Valluru | Pingala | ಹದ್ದು (ವಲ್ಲೂರು) | Earth | Prithvi | Stability, Groundedness, Tenacity |
| **Owl** | Aanthai | Uluka | ಗೂಬೆ (ಆಂದೈ) | Water | Jala | Wisdom, Intuition, Hidden Vision |
| **Crow** | Kaagam | Kaka | ಕಾಗೆ (ಕಾಕ) | Fire | Agni | Dynamic Action, Cunning, Alertness |
| **Cock** | Kozhi | Kukkuta | ಹುಂಜ / ಕೋಳಿ | Air | Vayu | Awareness, Awakening, Vitality |
| **Peacock** | Mayil | Mayura | ನವಿಲು (ಮಯೂರ) | Ether | Akasha | Grace, Spiritual Harmony, Creativity |

---

### 3.2 The Five Avasthas (Activities / States)

Each bird cycles through five fundamental states of activity during day and night:

| # | Activity | Tamil Term | Sanskrit Term | Kannada Term | Astrological Influence |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Ruling** | Aalpathi | Rajya | ಆಡಳಿತ (ರಾಜ್ಯ) | Maximum power ($100\%$ strength); optimal for high-impact decisions, executive actions, inaugurations. |
| 2 | **Eating** | Unnal | Bhojana | ಊಟ (ಭೋಜನ) | Very auspicious ($80\%$ strength); favorable for negotiations, commerce, financial gains, and study. |
| 3 | **Walking** | Nadakkal | Gamana | ನಡಿಗೆ (ಗಮನ) | Neutral/Moderate ($50\%$ strength); suited for routine travel, physical work, mundane duties. |
| 4 | **Sleeping** | Urangal | Nidra | ನಿದ್ರೆ (ಶಯನ) | Inactive/Weak ($20\%$ strength); suitable only for relaxation, meditation, and rest; avoid initiatives. |
| 5 | **Dying** | Iranthal | Marna | ಮರಣ (ಮರಣಾವಸ್ಥೆ) | Highly inauspicious ($0\%$ strength); most vulnerable phase; avoid crucial endeavors and conflict. |

---

## 4. API Specification & JSON Response Schema

### 4.1 Endpoint Signatures

- `GET /api/v1/kundali/birth` (Janma Kundali with birth bird)
- `GET /api/v1/kundali` (Transit Kundali with current transit bird)

### 4.2 Response Structure (`pancha_pakshi` block)

```json
{
  "pancha_pakshi": {
    "bird": "Vulture",
    "element": "Earth",
    "nakshatra": "Revati",
    "nakshatra_number": 27,
    "paksha": "Krishna"
  }
}
```

### 4.3 Kannada Localization (`?lang=kan`)

When `lang=kan` is specified in query parameters:

```json
{
  "pancha_pakshi": {
    "bird": "ಹದ್ದು",
    "element": "ಭೂಮಿ (ಪೃಥ್ವಿ)",
    "nakshatra": "ರೇವತಿ",
    "nakshatra_number": 27,
    "paksha": "ಕೃಷ್ಣ"
  }
}
```

---

## 5. Verification & Test Suite

The feature is comprehensively verified via `tests/test_pancha_pakshi.py`:

1. **Exhaustive Shukla Paksha mapping**: Tests all 27 stars against canonical Agathiyar assignments.
2. **Exhaustive Krishna Paksha mapping**: Tests all 27 stars against reversed assignments.
3. **Boundary testing**: Tests edge nakshatras (1, 5, 6, 11, 12, 16, 17, 22, 23, 27) and invalid numbers ($<1$ or $>27$).
4. **Integration test on `/kundali/birth`**: Confirms full payload with correct bird, elements, nakshatra, paksha, and activities.
5. **Integration test on `/kundali`**: Confirms transit presence.
6. **Kannada localization test**: Confirms full Kannada translation fidelity.
7. **Regression Suite**: All **123 tests** across the entire repository test suite execute and pass with 100% success (`pytest`).
