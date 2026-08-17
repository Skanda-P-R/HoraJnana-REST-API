# Implementation Specification — Yogi, Aviyogi & Sahayogi (Transit & Birth Kundali)

This document provides a comprehensive astrological explanation, mathematical formulation, and detailed implementation plan for integrating **Yogi**, **Aviyogi (Avayogi)**, and **Duplicate Yogi (Sahayogi)** calculations into the HoraJnana REST API for both **Transit Kundali** (`/api/v1/kundali`) and **Birth Kundali** (`/api/v1/kundali/birth`).

---

## 1. Astrological Background: What are Yogi and Aviyogi?

In Vedic Astrology (Jyotisha), **Yogi**, **Aviyogi (Avayogi)**, and **Duplicate Yogi (Sahayogi)** are mathematical sensitive points (Sphutas) and their associated planetary rulers (Grahas) that indicate auspiciousness, prosperity, obstacles, and catalysts in a chart.

### 1.1 Yogi Planet (*Yogi Graha* / ಯೋಗಿ ಗ್ರಹ)
- **Definition**: The planet that rules the **Nakshatra** (constellation) where the **Yogi Point (Yoga Sphuta)** falls.
- **Significance**: 
  - Represents prosperity, good fortune, vitality, material success, and favorable timing.
  - During the Dasha/Antardasha of the Yogi planet, or when benefic planets transit the Yogi point/house, positive events and opportunities manifest smoothly.
  - The house occupied by the Yogi Point or Yogi planet in a birth/transit chart becomes a source of strength and growth.

### 1.2 Aviyogi / Avayogi Planet (*Avayogi Graha* / ಅವಯೋಗಿ ಗ್ರಹ)
- **Definition**: The planet that rules the **Nakshatra** where the **Avayogi Point (Avayoga Sphuta)** falls.
- **Significance**:
  - Acts as the counter-force or obstacle-creator to the Yogi planet.
  - Represents challenges, delays, friction, financial drain, or karmic testing.
  - During the Dasha/Antardasha of the Avayogi planet, or when malefics transit this point, the native experiences hurdles that demand extra patience and effort.
  - However, if the Avayogi planet is placed in Dusthana houses (6th, 8th, or 12th) or is debilitated, its obstructing power is considerably neutralized.

### 1.3 Duplicate Yogi / Sahayogi (*Sahayogi* / ಸಹಯೋಗಿ ಅಥವಾ ದ್ವಿತೀಯ ಯೋಗಿ)
- **Definition**: The planetary ruler of the **Zodiac Sign (Rasi)** where the **Yogi Point** is located.
- **Significance**:
  - Acts as an ally and co-supporter to the Yogi planet, assisting in unlocking prosperity and sustaining fortune.

### 1.4 Duplicate Avayogi (*Dvitiya Avayogi* / ದ್ವಿತೀಯ ಅವಯೋಗಿ)
- **Definition**: The planetary ruler of the **Zodiac Sign (Rasi)** where the **Avayogi Point** is located.
- **Significance**:
  - Secondary planet associated with obstruction or the sphere where obstacles may physically manifest.

---

## 2. Mathematical Calculation from Existing Calculations

The HoraJnana system already calculates high-precision geocentric sidereal positions for the **Sun** ($L_{\text{Sun}}$), **Moon** ($L_{\text{Moon}}$), and **Ascendant / Lagna** ($L_{\text{Lagna}}$) using Swiss Ephemeris.

### 2.1 Yogi Point Calculation (Yoga Sphuta)
1. Obtain the sidereal longitude of the Sun ($L_{\text{Sun}} \in [0^\circ, 360^\circ)$).
2. Obtain the sidereal longitude of the Moon ($L_{\text{Moon}} \in [0^\circ, 360^\circ)$).
3. Add the constant **$93^\circ 20'$** ($93.333333^\circ$, which represents 7 Nakshatra spans of $13^\circ 20'$ each):
   $$\text{Longitude}_{\text{Yogi}} = (L_{\text{Sun}} + L_{\text{Moon}} + 93^\circ 20') \pmod{360^\circ}$$
4. Determine the **Rasi** and **Degree in Rasi**:
   $$\text{Rasi Number}_{\text{Yogi}} = \lfloor \text{Longitude}_{\text{Yogi}} / 30^\circ \rfloor + 1 \quad (\text{1 = Mesha / Aries to 12 = Meena / Pisces})$$
   $$\text{Degree in Rasi}_{\text{Yogi}} = \text{Longitude}_{\text{Yogi}} \pmod{30^\circ}$$
5. Determine the **Nakshatra** and **Pada**:
   $$\text{Nakshatra Index}_{\text{Yogi}} = \lfloor \text{Longitude}_{\text{Yogi}} / (13^\circ 20') \rfloor \quad (\text{0 = Ashwini to 26 = Revati})$$
   $$\text{Pada}_{\text{Yogi}} = \lfloor (\text{Longitude}_{\text{Yogi}} \pmod{13^\circ 20'}) / (3^\circ 20') \rfloor + 1 \quad (1 \text{ to } 4)$$
6. Determine the **Yogi Planet** and **Duplicate Yogi**:
   - **Yogi Planet** = Vimshottari Lord of the Yogi Nakshatra:
     $$\text{Lord of } (\text{Nakshatra Index}_{\text{Yogi}} \pmod 9) \in \{\text{Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury}\}$$
   - **Duplicate Yogi (Sahayogi)** = Rasi Lord of the Yogi Rasi (e.g., Mars for Aries/Scorpio, Venus for Taurus/Libra, Mercury for Gemini/Virgo, Moon for Cancer, Sun for Leo, Jupiter for Sagittarius/Pisces, Saturn for Capricorn/Aquarius).
7. Determine the **House** from Lagna:
   $$\text{House}_{\text{Yogi}} = ((\text{Rasi Number}_{\text{Yogi}} - \text{Lagna Rasi Number}) \pmod{12}) + 1$$

---

### 2.2 Avayogi Point Calculation (Avayoga Sphuta)
1. Add the constant **$186^\circ 40'$** ($186.666667^\circ$, which represents exactly 14 Nakshatras) to the Yogi Point:
   $$\text{Longitude}_{\text{Avayogi}} = (\text{Longitude}_{\text{Yogi}} + 186^\circ 40') \pmod{360^\circ}$$
   *(Note: This is equivalent to $(L_{\text{Sun}} + L_{\text{Moon}} + 280^\circ 00') \pmod{360^\circ}$).*
2. Determine the **Rasi** and **Degree in Rasi**:
   $$\text{Rasi Number}_{\text{Avayogi}} = \lfloor \text{Longitude}_{\text{Avayogi}} / 30^\circ \rfloor + 1$$
   $$\text{Degree in Rasi}_{\text{Avayogi}} = \text{Longitude}_{\text{Avayogi}} \pmod{30^\circ}$$
3. Determine the **Nakshatra** and **Pada**:
   $$\text{Nakshatra Index}_{\text{Avayogi}} = (\text{Nakshatra Index}_{\text{Yogi}} + 14) \pmod{27}$$
   $$\text{Pada}_{\text{Avayogi}} = \text{Pada}_{\text{Yogi}}$$
4. Determine the **Aviyogi Planet** and **Duplicate Avayogi**:
   - **Aviyogi Planet** = Vimshottari Lord of the Avayogi Nakshatra.
   - **Duplicate Avayogi** = Rasi Lord of the Avayogi Rasi.
5. Determine the **House** from Lagna:
   $$\text{House}_{\text{Avayogi}} = ((\text{Rasi Number}_{\text{Avayogi}} - \text{Lagna Rasi Number}) \pmod{12}) + 1$$

---

### 2.3 Reference Astronomical Rasi Lord Mapping

| Rasi Number | English Name | Sanskrit Name | Kannada Name | Ruling Planet (Rasi Lord) |
|-------------|--------------|---------------|--------------|---------------------------|
| 1 | Aries | Mesha | ಮೇಷ | Mars (ಕುಜ) |
| 2 | Taurus | Vrishabha | ವೃಷಭ | Venus (ಶುಕ್ರ) |
| 3 | Gemini | Mithuna | ಮಿಥುನ | Mercury (ಬುಧ) |
| 4 | Cancer | Karka | ಕಟಕ | Moon (ಚಂದ್ರ) |
| 5 | Leo | Simha | ಸಿಂಹ | Sun (ಸೂರ್ಯ) |
| 6 | Virgo | Kanya | ಕನ್ಯಾ | Mercury (ಬುಧ) |
| 7 | Libra | Tula | ತುಲಾ | Venus (ಶುಕ್ರ) |
| 8 | Scorpio | Vrishchika | ವೃಶ್ಚಿಕ | Mars (ಕುಜ) |
| 9 | Sagittarius | Dhanu | ಧನು | Jupiter (ಗುರು) |
| 10 | Capricorn | Makara | ಮಕರ | Saturn (ಶನಿ) |
| 11 | Aquarius | Kumbha | ಕುಂಭ | Saturn (ಶನಿ) |
| 12 | Pisces | Meena | ಮೀನ | Jupiter (ಗುರು) |

---

## 3. Proposed API Schema & Contract

The new feature is **100% backward-compatible and additive**. It enriches the JSON payloads returned by:
- `GET /api/v1/kundali` (Transit Kundali)
- `GET /api/v1/kundali/birth` (Birth Kundali)

### 3.1 JSON Payload Structure

```json
{
  "date": "2026-07-08",
  "datetime": "2026-07-08T12:00:00+05:30",
  "timezone": "Asia/Kolkata",
  "ayanamsa": "Lahiri",
  "lagna": {
    "rasi": "Virgo",
    "number": 6,
    "longitude": 166.977,
    "degree_in_rasi": 16.977
  },
  "houses": [ ... ],
  "planets": [ ... ],
  "yogi_avayogi": {
    "yogi_planet": "Moon",
    "duplicate_yogi": "Mercury",
    "avayogi_planet": "Mercury",
    "duplicate_avayogi": "Jupiter",
    "yogi_point": {
      "longitude": 172.9458,
      "degree_in_rasi": 22.9458,
      "rasi": "Virgo",
      "rasi_number": 6,
      "rasi_lord": "Mercury",
      "nakshatra": "Hasta",
      "nakshatra_number": 13,
      "nakshatra_lord": "Moon",
      "pada": 4,
      "house": 1
    },
    "avayogi_point": {
      "longitude": 359.6125,
      "degree_in_rasi": 29.6125,
      "rasi": "Pisces",
      "rasi_number": 12,
      "rasi_lord": "Jupiter",
      "nakshatra": "Revati",
      "nakshatra_number": 27,
      "nakshatra_lord": "Mercury",
      "pada": 4,
      "house": 7
    }
  },
  "panchanga": {
    "tithi": "Navami",
    "nakshatra": "Ashwini",
    "yoga": "Sadhya",
    "karana": "Gara",
    "vara": "Wednesday",
    "vara_sanskrit": "Budhavara",
    "samvatsara": "Parabhava",
    "ayana": "Dakshinayana",
    "rutu": "Varsha",
    "masa": "Ashadha",
    "paksha": "Krishna"
  },
  "panchanga_details": {
    "tithi": { ... },
    "nakshatra": { ... },
    "yoga": { ... },
    "karana": { ... }
  }
}

```

### 3.2 Kannada Localization (`lang=kan`)
When `lang=kan` is passed, the values are automatically localized by `hora_server/utils/translation.py`:
- `yogi_planet`: `"ಚಂದ್ರ"`
- `duplicate_yogi`: `"ಬುಧ"`
- `avayogi_planet`: `"ಬುಧ"`
- `duplicate_avayogi`: `"ಗುರು"`
- `nakshatra`: `"ಹಸ್ತ"`, `"ರೇವತಿ"`
- `rasi`: `"ಕನ್ಯಾ"`, `"ಮೀನ"`

---

## 4. Detailed Implementation Architecture

### 4.1 New Data Models (`hora_server/astrology/kundali.py`)

Add dataclasses for structured representation:

```python
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
```

Enrich `Kundali` dataclass with optional or default `yogi_avayogi: YogiAvayogi | None = None`.

### 4.2 Calculation Function (`hora_server/astrology/kundali.py`)

```python
def calculate_yogi_avayogi(
    sun_longitude: float,
    moon_longitude: float,
    lagna_number: int,
) -> YogiAvayogi:
    # 1. Yogi Point Longitude
    yogi_lon = (sun_longitude + moon_longitude + (93.0 + 20.0 / 60.0)) % 360.0
    yogi_rasi_num = int(yogi_lon // 30) + 1
    yogi_deg = yogi_lon % 30.0
    yogi_nak_idx = int(yogi_lon // (360.0 / 27.0))
    yogi_pada = int((yogi_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1
    yogi_nak_lord = DASHA_LORDS[yogi_nak_idx % 9]
    yogi_rasi_lord = RASI_LORDS[yogi_rasi_num - 1]
    yogi_house = ((yogi_rasi_num - lagna_number) % 12) + 1

    # 2. Avayogi Point Longitude
    avayogi_lon = (yogi_lon + (186.0 + 40.0 / 60.0)) % 360.0
    avayogi_rasi_num = int(avayogi_lon // 30) + 1
    avayogi_deg = avayogi_lon % 30.0
    avayogi_nak_idx = int(avayogi_lon // (360.0 / 27.0))
    avayogi_pada = int((avayogi_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1
    avayogi_nak_lord = DASHA_LORDS[avayogi_nak_idx % 9]
    avayogi_rasi_lord = RASI_LORDS[avayogi_rasi_num - 1]
    avayogi_house = ((avayogi_rasi_num - lagna_number) % 12) + 1

    ...
```

### 4.3 Constants (`hora_server/astrology/constants.py`)
Add `RASI_LORDS` mapping tuple:
```python
RASI_LORDS: Final[tuple[str, ...]] = (
    "Mars",     # 1: Aries / Mesha
    "Venus",    # 2: Taurus / Vrishabha
    "Mercury",  # 3: Gemini / Mithuna
    "Moon",     # 4: Cancer / Karka
    "Sun",      # 5: Leo / Simha
    "Mercury",  # 6: Virgo / Kanya
    "Venus",    # 7: Libra / Tula
    "Mars",     # 8: Scorpio / Vrishchika
    "Jupiter",  # 9: Sagittarius / Dhanu
    "Saturn",   # 10: Capricorn / Makara
    "Saturn",   # 11: Aquarius / Kumbha
    "Jupiter",  # 12: Pisces / Meena
)
```

### 4.4 Service Layer (`hora_server/service.py`)
Add serialization helper `_yogi_avayogi_payload(self, yogi: YogiAvayogi) -> dict[str, Any]` and include `"yogi_avayogi"` in `kundali(self, context: RequestContext)`.

### 4.5 Localization (`hora_server/utils/translation.py`)
Verify that translation dictionaries map all planet, nakshatra, and rasi names to Kannada so that `localize_payload` works seamlessly without changes.

---

## 5. Verification and Testing Plan

### 5.1 Unit Tests (`tests/test_kundali.py` & `tests/test_birth_chart_and_locations.py`)
1. **Mathematical Accuracy**: Test exact degrees, nakshatras, padas, and planet lords against reference astronomical dates.
2. **Schema Verification**: Ensure `yogi_avayogi` contains all required subfields and correct types.
3. **Transit vs Birth Kundali**: Verify that both `/api/v1/kundali` and `/api/v1/kundali/birth` return identical mathematical structures for the specified moment.
4. **Kannada Localization**: Test `lang=kan` returns Kannada strings for `yogi_planet`, `duplicate_yogi`, `avayogi_planet`, etc.
5. **Edge Cases**:
   - Yogi Point near $0^\circ$ / $360^\circ$ boundary.
   - Nakshatra boundaries (e.g. exactly at $13^\circ 20'$).
   - Same planet acting as Avayogi and Duplicate Yogi.

---

## 6. Summary of Benefits

- Provides traditional Vedic predictive tools for both daily transit monitoring and birth chart readings.
- Zero breaking changes to existing client applications or widget integrations.
- Completely deterministic calculations powered by Swiss Ephemeris.
