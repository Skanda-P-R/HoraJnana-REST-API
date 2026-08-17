# Implementation Specification — Atmakaraka & Darakaraka (Chara Karakas)

This document provides a comprehensive astrological foundation, mathematical formulation, architectural design, and implementation specification for integrating **Atmakaraka (AK)**, **Darakaraka (DK)**, and the complete **7-Chara Karaka (Sapta Chara Karaka)** system into the HoraJnana REST API for both **Transit Kundali** (`/api/v1/kundali`) and **Birth Kundali** (`/api/v1/kundali/birth`).

---

## 1. Astrological Background & Theoretical Foundations

In Vedic Astrology (*Jyotisha*), particularly in the **Jaimini Upadesha Sutras** and Maharishi Parashara's **Brihat Parashara Hora Shastra (BPHS, Chapter 32)**, planets (*Grahas*) assume two distinct kinds of roles:
1. **Sthira Karakas (Fixed Significators)**: Natural significators that never change across charts (e.g., Sun for Father/Soul, Moon for Mother/Mind, Venus for Spouse/Pleasure, Mars for Siblings/Courage, Jupiter for Guru/Children).
2. **Chara Karakas (Variable / Temporal Significators)**: Significators whose roles dynamically change in every chart based strictly on the advanced degree of longitude traversed within the respective zodiac sign (*Rasi*).

Among all the Chara Karakas, **Atmakaraka** and **Darakaraka** are considered the two most critical personal pivot points in a Kundali.

---

### 1.1 Atmakaraka (*Atma Karaka* / ಆತ್ಮಕಾರಕ) — The Soul Significator

- **Etymology**: *Atma* (Soul/Self) + *Karaka* (Significator/Doer).
- **Definition**: The planet that has attained the **highest degree of longitude** (from $0^\circ 00' 00''$ to $29^\circ 59' 59''$) within its occupied zodiac sign.
- **Astrological Significance**:
  - **King of the Chart**: BPHS states that just as a king is the sovereign ruler over all affairs in a kingdom, the Atmakaraka is the undisputed king over all Grahas and Bhavas in the horoscope. If the Atmakaraka is well-placed and strong, the native overcomes hardships; if afflicted, life demands arduous karmic lessons.
  - **Soul's Highest Purpose & Reincarnation**: Indicates the soul's primary spiritual mission, inner desire (*Icha Sakthi*), karmic baggage, and path to liberation (*Moksha*).
  - **Physical Self & Health**: Governs physical constitution, vitality, and primary personality traits.
- **Karakamsa (ಕಾರಕಾಂಶ)**:
  - The Navamsha (D9) sign occupied by the Atmakaraka is called the **Karakamsa**.
  - Karakamsa is of prime importance in Jaimini astrology: the planets placed in or aspecting the Karakamsa and its 12th house reveal the native's true vocation, spiritual Ishta Devata, and spiritual evolution.

---

### 1.2 Darakaraka (*Dara Karaka* / ದಾರಕಾರಕ) — The Spouse & Relationship Significator

- **Etymology**: *Dara* (Wife/Husband/Spouse) + *Karaka* (Significator).
- **Definition**: The planet that has attained the **lowest degree of longitude** (closest to $0^\circ 00' 00''$) within its occupied zodiac sign among the considered Grahas.
- **Astrological Significance**:
  - **Spouse & Life Partner**: Governs the personality, physical characteristics, temperament, background, and marital compatibility of the spouse.
  - **Romantic & Intimate Relationships**: Indicates the quality of love, romantic bonding, affection, and emotional fulfillment.
  - **Business Partnerships & Public Relations**: Represents the native's capacity for close one-on-one business associations, contracts, and public dealings.
- **AK–DK Relationship (The Soul and the Partner)**:
  - The relationship between Atmakaraka (1st harmonic / Self) and Darakaraka (7th harmonic / Other) represents the polarity of individual consciousness versus union with others. In synastry and compatibility, matching the AK and DK positions of two individuals reveals deep karmic connections.

---

### 1.3 The 7-Karaka System vs. 8-Karaka System

Classical literature details two traditions for Chara Karaka calculation:

| Feature | 7-Karaka Scheme (*Sapta Karaka*) | 8-Karaka Scheme (*Ashta Karaka*) |
|---|---|---|
| **Classical Authority** | Maharishi Parashara (BPHS), Jaimini Sutras, B.V. Raman, K.N. Rao, Jagannatha Hora standard | Alternative chapter in BPHS, Pt. Sanjay Rath |
| **Planets Evaluated** | **7 Physical Planets**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn | **8 Planets**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn + **Rahu** |
| **Exclusion of Rahu/Ketu** | Rahu and Ketu are mathematical shadow nodes (*Chhaya Grahas*) without mass/physical bodies; Ketu never receives Karaka status. | Rahu is assigned traversed degree $(30^\circ - \text{degree})$ due to retrograde motion. |
| **5th vs. 4th Karaka** | Pitrukaraka is merged into Matrukaraka or Bhratrukaraka; Putrakaraka represents children. | Matrukaraka (Mother) and Pitrukaraka (Father) are separate. |
| **Atmakaraka (AK)** | Planet with the **1st highest degree** ($0^\circ-30^\circ$) | Planet with the **1st highest degree** ($0^\circ-30^\circ$) |
| **Darakaraka (DK)** | Planet with the **7th highest (lowest) degree** | Planet with the **8th highest (lowest) degree** |

> [!IMPORTANT]
> **Recommended & Standard Approach**: The **7-Karaka (Sapta Chara Karaka)** system is the universally recognized gold standard in Vedic astrology for Atmakaraka and Darakaraka calculation across contemporary Jyotisha literature, software (Jagannatha Hora, Parashara's Light, Kundli Pro), and academic lineages (K.N. Rao / B.V. Raman). 
> In this implementation:
> 1. The **7-Karaka system** is utilized as the default primary standard for calculating Atmakaraka and Darakaraka.
> 2. The API outputs dedicated high-level `atmakaraka` and `darakaraka` objects, as well as the full ordered list of all 7 `chara_karakas`.

---

### 1.4 The Complete 7 Chara Karakas Overview

The 7 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn) sorted in descending order of degrees within their sign:

| Rank | Karaka | Sanskrit Name | Kannada Name | Abbreviation | Core Astrological Significations |
|:---:|---|---|---|:---:|---|
| **1** | **Atmakaraka** | आत्मकारक | ಆತ್ಮಕಾರಕ | **AK** | Soul, Self, Destiny, Physical Body, Life Mission, Karakamsa |
| **2** | **Amatyakaraka** | अमात्यकारक | ಅಮಾತ್ಯಕಾರಕ | **AmK** | Mind, Intellect, Career, Profession, Status, Minister / Advisor |
| **3** | **Bhratrukaraka** | भ्रातृकारक | ಭ್ರಾತೃಕಾರಕ | **BK** | Siblings, Mentors, Gurus, Courage, Advisors, Comrades |
| **4** | **Matrukaraka** | मातृकारक | ಮಾತೃಕಾರಕ | **MK** | Mother, Domestic Life, Emotional Peace, Real Estate, Vehicles |
| **5** | **Putrakaraka** | पुत्रकारक | ಪುತ್ರಕಾರಕ | **PK** | Children, Progeny, Creative Intellect, Higher Wisdom, Past Merits |
| **6** | **Gnatikaraka** | ज्ञािकारक | ಜ್ಞಾತಿಕಾರಕ | **GK** | Relatives, Obstacles, Friction, Diseases, Debts, Competitors |
| **7** | **Darakaraka** | दारककारक | ದಾರಕಾರಕ | **DK** | Spouse, Life Partner, Marriage, Business Partnerships |

---

## 2. Mathematical Calculation from Existing Architecture

The HoraJnana engine calculates exact geocentric sidereal longitudes ($\lambda$) using the Swiss Ephemeris engine with the requested Ayanamsa (e.g., Lahiri / Chitrapaksha).

### 2.1 Degree in Rasi Calculation
For each physical planet $p \in \{\text{Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn}\}$:
$$\text{degree\_in\_rasi}(p) = \lambda_p \pmod{30^\circ}$$

Where:
- $\lambda_p \in [0^\circ, 360^\circ)$ is the sidereal longitude.
- $\text{degree\_in\_rasi}(p) \in [0^\circ, 30^\circ)$ represents the degree traversed in the sign.

### 2.2 Sorting and Karaka Assignment
1. Filter the planetary list to the 7 physical bodies (excluding Rahu, Ketu, and outer planets).
2. Sort the 7 planets in **descending order** of `degree_in_rasi`:
   $$p_{(1)}, p_{(2)}, p_{(3)}, p_{(4)}, p_{(5)}, p_{(6)}, p_{(7)}$$
   such that:
   $$\text{degree\_in\_rasi}(p_{(1)}) \ge \text{degree\_in\_rasi}(p_{(2)}) \ge \dots \ge \text{degree\_in\_rasi}(p_{(7)})$$

3. Assign the Chara Karakas:
   - $\text{Atmakaraka (AK)} = p_{(1)}$ (Highest degree)
   - $\text{Amatyakaraka (AmK)} = p_{(2)}$
   - $\text{Bhratrukaraka (BK)} = p_{(3)}$
   - $\text{Matrukaraka (MK)} = p_{(4)}$
   - $\text{Putrakaraka (PK)} = p_{(5)}$
   - $\text{Gnatikaraka (GK)} = p_{(6)}$
   - $\text{Darakaraka (DK)} = p_{(7)}$ (Lowest degree)

### 2.3 Tie-Breaking Rule (Infinitesimal Case)
In double-precision floating-point astronomy calculations from Swiss Ephemeris ($10^{-8}$ degree precision, corresponding to $0.00036$ arcseconds), exact collisions are practically impossible. However, if two planets have identical degrees down to micro-arcseconds:
- Secondary sort key: higher total longitude or planetary natural seniority order (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn) to maintain 100% deterministic reproducibility.

### 2.4 Navamsha (D9) & Karakamsa Calculation
The Navamsha is the 9th harmonic divisional chart ($3^\circ 20'$ per division, 108 divisions of $360^\circ$).
For any longitude $\lambda \in [0^\circ, 360^\circ)$:
$$\text{Navamsha Division Index} = \lfloor \frac{\lambda}{3^\circ 20'} \rfloor = \lfloor \frac{\lambda}{10 / 3} \rfloor = \lfloor \frac{3 \lambda}{10} \rfloor \in [0, 107]$$
$$\text{Navamsha Sign Number} = (\text{Navamsha Division Index} \pmod{12}) + 1 \quad (1 = \text{Aries} \dots 12 = \text{Pisces})$$
$$\text{Navamsha Sign Name} = \text{ENGLISH\_RASIS}[\text{Navamsha Sign Number} - 1]$$

For Atmakaraka, this Navamsha sign is explicitly reported as **`karakamsa`** (or `navamsha_rasi`).

---

## 3. Proposed API Schema & Contract

The new feature is **100% backward-compatible and additive**. It enriches the JSON payloads returned by:
- `GET /api/v1/kundali` (Transit Kundali)
- `GET /api/v1/kundali/birth` (Birth Kundali)

### 3.1 JSON Payload Structure

```json
{
  "date": "2026-08-17",
  "datetime": "2026-08-17T16:48:18+05:30",
  "timezone": "Asia/Kolkata",
  "ayanamsa": "Lahiri",
  "lagna": {
    "rasi": "Sagittarius",
    "number": 9,
    "longitude": 252.1245,
    "degree_in_rasi": 12.1245
  },
  "houses": [ ... ],
  "planets": [ ... ],
  "atmakaraka": {
    "planet": "Jupiter",
    "symbol": "Ju",
    "karaka": "Atmakaraka",
    "karaka_code": "AK",
    "degree_in_rasi": 28.4521,
    "longitude": 358.4521,
    "rasi": "Pisces",
    "rasi_number": 12,
    "rasi_lord": "Jupiter",
    "house": 4,
    "nakshatra": "Revati",
    "nakshatra_number": 27,
    "nakshatra_lord": "Mercury",
    "pada": 4,
    "navamsha_rasi": "Pisces",
    "navamsha_rasi_number": 12,
    "retrograde": false,
    "signification": "Soul, Self, Physical Constitution, Life Purpose"
  },
  "darakaraka": {
    "planet": "Venus",
    "symbol": "Ve",
    "karaka": "Darakaraka",
    "karaka_code": "DK",
    "degree_in_rasi": 2.1584,
    "longitude": 122.1584,
    "rasi": "Leo",
    "rasi_number": 5,
    "rasi_lord": "Sun",
    "house": 9,
    "nakshatra": "Magha",
    "nakshatra_number": 10,
    "nakshatra_lord": "Ketu",
    "pada": 1,
    "navamsha_rasi": "Aries",
    "navamsha_rasi_number": 1,
    "retrograde": false,
    "signification": "Spouse, Life Partner, Marriage, Business Partnerships"
  },
  "chara_karakas": [
    {
      "rank": 1,
      "karaka": "Atmakaraka",
      "karaka_code": "AK",
      "planet": "Jupiter",
      "symbol": "Ju",
      "degree_in_rasi": 28.4521,
      "longitude": 358.4521,
      "rasi": "Pisces",
      "rasi_number": 12,
      "house": 4,
      "nakshatra": "Revati",
      "pada": 4,
      "navamsha_rasi": "Pisces",
      "retrograde": false
    },
    {
      "rank": 2,
      "karaka": "Amatyakaraka",
      "karaka_code": "AmK",
      "planet": "Saturn",
      "symbol": "Sa",
      "degree_in_rasi": 24.1205,
      "longitude": 354.1205,
      "rasi": "Pisces",
      "rasi_number": 12,
      "house": 4,
      "nakshatra": "Revati",
      "pada": 3,
      "navamsha_rasi": "Aquarius",
      "retrograde": true
    },
    {
      "rank": 3,
      "karaka": "Bhratrukaraka",
      "karaka_code": "BK",
      "planet": "Sun",
      "symbol": "Su",
      "degree_in_rasi": 21.0543,
      "longitude": 141.0543,
      "rasi": "Leo",
      "rasi_number": 5,
      "house": 9,
      "nakshatra": "Purva Phalguni",
      "pada": 3,
      "navamsha_rasi": "Libra",
      "retrograde": false
    },
    {
      "rank": 4,
      "karaka": "Matrukaraka",
      "karaka_code": "MK",
      "planet": "Moon",
      "symbol": "Mo",
      "degree_in_rasi": 18.7214,
      "longitude": 198.7214,
      "rasi": "Libra",
      "rasi_number": 7,
      "house": 11,
      "nakshatra": "Swati",
      "pada": 4,
      "navamsha_rasi": "Pisces",
      "retrograde": false
    },
    {
      "rank": 5,
      "karaka": "Putrakaraka",
      "karaka_code": "PK",
      "planet": "Mars",
      "symbol": "Ma",
      "degree_in_rasi": 14.3312,
      "longitude": 74.3312,
      "rasi": "Gemini",
      "rasi_number": 3,
      "house": 7,
      "nakshatra": "Ardra",
      "pada": 3,
      "navamsha_rasi": "Aquarius",
      "retrograde": false
    },
    {
      "rank": 6,
      "karaka": "Gnatikaraka",
      "karaka_code": "GK",
      "planet": "Mercury",
      "symbol": "Me",
      "degree_in_rasi": 8.9421,
      "longitude": 128.9421,
      "rasi": "Leo",
      "rasi_number": 5,
      "house": 9,
      "nakshatra": "Magha",
      "pada": 3,
      "navamsha_rasi": "Gemini",
      "retrograde": true
    },
    {
      "rank": 7,
      "karaka": "Darakaraka",
      "karaka_code": "DK",
      "planet": "Venus",
      "symbol": "Ve",
      "degree_in_rasi": 2.1584,
      "longitude": 122.1584,
      "rasi": "Leo",
      "rasi_number": 5,
      "house": 9,
      "nakshatra": "Magha",
      "pada": 1,
      "navamsha_rasi": "Aries",
      "retrograde": false
    }
  ],
  "yogi_avayogi": { ... },
  "panchanga": { ... },
  "panchanga_details": { ... }
}
```

---

### 3.2 Field Dictionary

| Field Name | Type | Description |
|---|---|---|
| `atmakaraka` | Object | Complete details of the Atmakaraka (highest degree planet). |
| `darakaraka` | Object | Complete details of the Darakaraka (lowest degree planet). |
| `chara_karakas` | Array[Object] | Ordered list of all 7 Chara Karakas from highest to lowest degree. |
| `karaka` | String | Standard English name of the Karaka (e.g., `"Atmakaraka"`, `"Darakaraka"`). Localized in Kannada when `lang=kan`. |
| `karaka_code` | String | Canonical 2-3 letter abbreviation (`AK`, `AmK`, `BK`, `MK`, `PK`, `GK`, `DK`). |
| `planet` | String | Name of the planet (e.g., `"Jupiter"`). Localized in Kannada when `lang=kan`. |
| `symbol` | String | Planet abbreviation (`Ju`, `Ve`, etc.). Localized in Kannada when `lang=kan`. |
| `degree_in_rasi` | Float | Degree within the sign ($0^\circ - 30^\circ$, rounded to 4 decimal places). |
| `longitude` | Float | Full sidereal longitude ($0^\circ - 360^\circ$, rounded to 4 decimal places). |
| `rasi` | String | Sign name (e.g., `"Pisces"`). Localized in Kannada when `lang=kan`. |
| `rasi_number` | Integer | Zodiac sign index ($1 = \text{Aries} \dots 12 = \text{Pisces}$). |
| `rasi_lord` | String | Ruling planet of the sign. Localized in Kannada when `lang=kan`. |
| `house` | Integer | Whole sign house index from Lagna ($1 \dots 12$). |
| `nakshatra` | String | Nakshatra name (e.g., `"Revati"`). Localized in Kannada when `lang=kan`. |
| `nakshatra_number` | Integer | Nakshatra index ($1 \dots 27$). |
| `nakshatra_lord` | String | Vimshottari lord of the Nakshatra. Localized in Kannada when `lang=kan`. |
| `pada` | Integer | Nakshatra quarter ($1 \dots 4$). |
| `navamsha_rasi` | String | Navamsha (D9) sign name (For AK, this is **Karakamsa**). Localized in Kannada when `lang=kan`. |
| `navamsha_rasi_number`| Integer | Navamsha (D9) sign number ($1 \dots 12$). |
| `retrograde` | Boolean | `true` if planet is in retrograde motion, `false` otherwise. |
| `signification` | String | Concise summary of traditional significations. |

---

### 3.3 Kannada Localization (`lang=kan`)

When `lang=kan` is passed, all textual fields are automatically localized using `hora_server/utils/translation.py`:

```json
{
  "atmakaraka": {
    "planet": "ಗುರು",
    "symbol": "ಗು",
    "karaka": "ಆತ್ಮಕಾರಕ",
    "karaka_code": "AK",
    "degree_in_rasi": 28.4521,
    "longitude": 358.4521,
    "rasi": "ಮೀನ",
    "rasi_number": 12,
    "rasi_lord": "ಗುರು",
    "house": 4,
    "nakshatra": "ರೇವತಿ",
    "nakshatra_number": 27,
    "nakshatra_lord": "ಬುಧ",
    "pada": 4,
    "navamsha_rasi": "ಮೀನ",
    "navamsha_rasi_number": 12,
    "retrograde": false,
    "signification": "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ"
  },
  "darakaraka": {
    "planet": "ಶುಕ್ರ",
    "symbol": "ಶು",
    "karaka": "ದಾರಕಾರಕ",
    "karaka_code": "DK",
    "degree_in_rasi": 2.1584,
    "longitude": 122.1584,
    "rasi": "ಸಿಂಹ",
    "rasi_number": 5,
    "rasi_lord": "ಸೂರ್ಯ",
    "house": 9,
    "nakshatra": "ಮಘಾ",
    "nakshatra_number": 10,
    "nakshatra_lord": "ಕೇತು",
    "pada": 1,
    "navamsha_rasi": "ಮೇಷ",
    "navamsha_rasi_number": 1,
    "retrograde": false,
    "signification": "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ"
  }
}
```

---

## 4. Detailed Implementation Architecture

### 4.1 New Data Models (`hora_server/astrology/kundali.py`)

Add dataclasses for structured representation:

```python
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
```

Enrich the main `Kundali` dataclass:

```python
@dataclass(frozen=True)
class Kundali:
    lagna: KundaliLagna
    houses: tuple[KundaliHouse, ...]
    planets: tuple[KundaliPlanet, ...]
    yogi_avayogi: YogiAvayogi | None = None
    chara_karakas: CharaKarakaReport | None = None
```

---

### 4.2 Constants & Definitions (`hora_server/astrology/constants.py`)

Define the 7 Chara Karaka roles, codes, and English/Kannada significations:

```python
CHARA_KARAKA_NAMES: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("Atmakaraka", "AK", "Soul, Self, Physical Constitution, Life Purpose", "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ"),
    ("Amatyakaraka", "AmK", "Mind, Intellect, Career, Profession, Status", "ಮನಸ್ಸು, ಬುದ್ಧಿಶಕ್ತಿ, ವೃತ್ತಿ, ಉದ್ಯೋಗ, ಅಂತಸ್ತು"),
    ("Bhratrukaraka", "BK", "Siblings, Mentors, Gurus, Courage, Comrades", "ಸಹೋದರರು, ಗುರುಗಳು, ಧೈರ್ಯ, ಮಾರ್ಗದರ್ಶಕರು"),
    ("Matrukaraka", "MK", "Mother, Domestic Life, Emotional Peace, Real Estate", "ತಾಯಿ, ಗೃಹಜೀವನ, ಭಾವನಾತ್ಮಕ ನೆಮ್ಮದಿ, ಆಸ್ತಿ"),
    ("Putrakaraka", "PK", "Children, Progeny, Creative Intellect, Past Merits", "ಸಂತಾನ, ಮಕ್ಕಳ ಭಾಗ್ಯ, ಸೃಜನಶೀಲ ಬುದ್ಧಿ, ಪೂರ್ವಪುಣ್ಯ"),
    ("Gnatikaraka", "GK", "Relatives, Obstacles, Friction, Diseases, Competitors", "ಜ್ಞಾತಿಗಳು, ಅಡೆತಡೆಗಳು, ರೋಗ, ಶತ್ರುಗಳು, ಸ್ಪರ್ಧೆ"),
    ("Darakaraka", "DK", "Spouse, Life Partner, Marriage, Business Partnerships", "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ"),
)

# 7 Physical Grahas evaluated for Chara Karakas
CHARA_KARAKA_PLANETS: Final[frozenset[str]] = frozenset(
    {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
)
```

---

### 4.3 Calculation Function (`hora_server/astrology/kundali.py`)

```python
def _navamsha_rasi_number(longitude: float) -> int:
    """Calculate the Navamsha (D9) Rasi number (1-12) for a given sidereal longitude."""
    nav_index = int((longitude % 360.0) // (360.0 / 108.0))  # 108 padas/navamshas
    return (nav_index % 12) + 1


def calculate_chara_karakas(
    planets: tuple[KundaliPlanet, ...],
    lagna_number: int,
) -> CharaKarakaReport:
    """Calculate the 7 Chara Karakas (Sapta Chara Karakas) from planetary positions."""
    # Filter 7 physical planets
    physical_planets = [p for p in planets if p.planet in CHARA_KARAKA_PLANETS]

    # Sort descending by degree_in_rasi; secondary sort by planet seniority order
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
```

---

### 4.4 Service Layer Serialization (`hora_server/service.py`)

Add serialization helper methods:

```python
@staticmethod
def _chara_karaka_item_payload(item: CharaKarakaDetails) -> dict[str, Any]:
    return {
        "rank": item.rank,
        "karaka": item.karaka,
        "karaka_code": item.karaka_code,
        "planet": item.planet,
        "symbol": item.symbol,
        "degree_in_rasi": round(item.degree_in_rasi, 4),
        "longitude": round(item.longitude, 4),
        "rasi": item.rasi,
        "rasi_number": item.rasi_number,
        "rasi_lord": item.rasi_lord,
        "house": item.house,
        "nakshatra": item.nakshatra,
        "nakshatra_number": item.nakshatra_number,
        "nakshatra_lord": item.nakshatra_lord,
        "pada": item.pada,
        "navamsha_rasi": item.navamsha_rasi,
        "navamsha_rasi_number": item.navamsha_rasi_number,
        "retrograde": item.retrograde,
        "signification": item.signification,
    }
```

Include in `kundali(self, context: RequestContext)`:

```python
if kundali.chara_karakas is not None:
    payload["atmakaraka"] = self._chara_karaka_item_payload(
        kundali.chara_karakas.atmakaraka
    )
    payload["darakaraka"] = self._chara_karaka_item_payload(
        kundali.chara_karakas.darakaraka
    )
    payload["chara_karakas"] = [
        self._chara_karaka_item_payload(k)
        for k in kundali.chara_karakas.karakas
    ]
```

---

### 4.5 Translation Dictionary Additions (`hora_server/utils/translation.py`)

Add the following entries to `TRANSLATIONS`:

```python
    # Chara Karakas
    "Atmakaraka": "ಆತ್ಮಕಾರಕ",
    "Amatyakaraka": "ಅಮಾತ್ಯಕಾರಕ",
    "Bhratrukaraka": "ಭ್ರಾತೃಕಾರಕ",
    "Matrukaraka": "ಮಾತೃಕಾರಕ",
    "Putrakaraka": "ಪುತ್ರಕಾರಕ",
    "Gnatikaraka": "ಜ್ಞಾತಿಕಾರಕ",
    "Darakaraka": "ದಾರಕಾರಕ",

    # Significations
    "Soul, Self, Physical Constitution, Life Purpose": "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ",
    "Mind, Intellect, Career, Profession, Status": "ಮನಸ್ಸು, ಬುದ್ಧಿಶಕ್ತಿ, ವೃತ್ತಿ, ಉದ್ಯೋಗ, ಅಂತಸ್ತು",
    "Siblings, Mentors, Gurus, Courage, Comrades": "ಸಹೋದರರು, ಗುರುಗಳು, ಧೈರ್ಯ, ಮಾರ್ಗದರ್ಶಕರು",
    "Mother, Domestic Life, Emotional Peace, Real Estate": "ತಾಯಿ, ಗೃಹಜೀವನ, ಭಾವನಾತ್ಮಕ ನೆಮ್ಮದಿ, ಆಸ್ತಿ",
    "Children, Progeny, Creative Intellect, Past Merits": "ಸಂತಾನ, ಮಕ್ಕಳ ಭಾಗ್ಯ, ಸೃಜನಶೀಲ ಬುದ್ಧಿ, ಪೂರ್ವಪುಣ್ಯ",
    "Relatives, Obstacles, Friction, Diseases, Competitors": "ಜ್ಞಾತಿಗಳು, ಅಡೆತಡೆಗಳು, ರೋಗ, ಶತ್ರುಗಳು, ಸ್ಪರ್ಧೆ",
    "Spouse, Life Partner, Marriage, Business Partnerships": "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ",
```

---

## 5. Verification and Testing Plan

### 5.1 Automated Unit & Integration Tests

1. **Mathematical Accuracy & Order Verification**:
   - Verify that Atmakaraka has strictly the highest `degree_in_rasi` among the 7 physical planets.
   - Verify that Darakaraka has strictly the lowest `degree_in_rasi` among the 7 physical planets.
   - Verify that all 7 Chara Karakas are in strict descending order of `degree_in_rasi`.
   - Verify that Rahu and Ketu are excluded from Chara Karakas.
2. **Navamsha & Karakamsa Verification**:
   - Verify that `navamsha_rasi` matches the classical 9th harmonic calculation.
3. **Endpoint Consistency**:
   - Verify that `/api/v1/kundali` and `/api/v1/kundali/birth` return identical Atmakaraka and Darakaraka details for the same instant and coordinates.
4. **Kannada Localization (`lang=kan`)**:
   - Verify that `karaka`, `planet`, `rasi`, `nakshatra`, and `signification` strings are properly converted to Kannada.
5. **Regression & Backward Compatibility**:
   - Verify that all existing fields in `/kundali` (`lagna`, `houses`, `planets`, `panchanga`, `yogi_avayogi`) remain completely intact.
   - Verify all test suites (`pytest`) pass with 100% success.

---

## 6. Summary of Key Benefits

- **Traditional Accuracy**: Adheres faithfully to classical Parashari & Jaimini principles.
- **Rich Context**: Provides not only the planet name, but full astronomical and astrological context (degrees, nakshatra, pada, Navamsha/Karakamsa, house placement, retrograde status, and traditional signification).
- **Dual Endpoint Enrichment**: Available across both Transit Kundali and Birth Kundali.
- **Zero Breaking Changes**: Fully additive schema enhancement.
