"""Canonical names and sequences used by the calculation engines."""

from __future__ import annotations

from typing import Final


PLANET_SEQUENCE: Final[tuple[str, ...]] = (
    "Saturn",
    "Jupiter",
    "Mars",
    "Sun",
    "Venus",
    "Mercury",
    "Moon",
)

PLANET_SYMBOLS: Final[dict[str, str]] = {
    "Sun": "☉",
    "Moon": "☽",
    "Mars": "♂",
    "Mercury": "☿",
    "Jupiter": "♃",
    "Venus": "♀",
    "Saturn": "♄",
}

# Python weekday order: Monday=0 through Sunday=6.
WEEKDAY_LORDS: Final[tuple[str, ...]] = (
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Sun",
)

WEEKDAY_NAMES: Final[tuple[str, ...]] = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

VARA_NAMES: Final[tuple[str, ...]] = (
    "Somavara",
    "Mangalavara",
    "Budhavara",
    "Guruvara",
    "Shukravara",
    "Shanivara",
    "Ravivara",
)

NAKSHATRAS: Final[tuple[str, ...]] = (
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishtha",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
)

YOGAS: Final[tuple[str, ...]] = (
    "Vishkambha",
    "Priti",
    "Ayushman",
    "Saubhagya",
    "Shobhana",
    "Atiganda",
    "Sukarma",
    "Dhriti",
    "Shula",
    "Ganda",
    "Vriddhi",
    "Dhruva",
    "Vyaghata",
    "Harshana",
    "Vajra",
    "Siddhi",
    "Vyatipata",
    "Variyana",
    "Parigha",
    "Shiva",
    "Siddha",
    "Sadhya",
    "Shubha",
    "Shukla",
    "Brahma",
    "Indra",
    "Vaidhriti",
)

RASHIS: Final[tuple[str, ...]] = (
    "Mesha",
    "Vrishabha",
    "Mithuna",
    "Karka",
    "Simha",
    "Kanya",
    "Tula",
    "Vrishchika",
    "Dhanu",
    "Makara",
    "Kumbha",
    "Meena",
)

PAKSHA_TITHIS: Final[tuple[str, ...]] = (
    "Pratipada",
    "Dvitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dvadashi",
    "Trayodashi",
    "Chaturdashi",
)

REPEATING_KARANAS: Final[tuple[str, ...]] = (
    "Bava",
    "Balava",
    "Kaulava",
    "Taitila",
    "Gara",
    "Vanija",
    "Vishti",
)

MASAS: Final[tuple[str, ...]] = (
    "Chaitra",
    "Vaishakha",
    "Jyeshtha",
    "Ashadha",
    "Shravana",
    "Bhadrapada",
    "Ashvina",
    "Kartika",
    "Margashirsha",
    "Pausha",
    "Magha",
    "Phalguna",
)

RUTUS: Final[tuple[str, ...]] = (
    "Vasanta",
    "Grishma",
    "Varsha",
    "Sharad",
    "Hemanta",
    "Shishira",
)

SAMVATSARAS: Final[tuple[str, ...]] = (
    "Prabhava", "Vibhava", "Shukla", "Pramoduta", "Prajotpatti",
    "Angirasa", "Shrimukha", "Bhava", "Yuva", "Dhatu",
    "Ishvara", "Bahudhanya", "Pramadi", "Vikrama", "Vrisha",
    "Chitrabhanu", "Svabhanu", "Tarana", "Parthiva", "Vyaya",
    "Sarvajit", "Sarvadhari", "Virodhi", "Vikruti", "Khara",
    "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi",
    "Hevilambi", "Vilambi", "Vikari", "Sharvari", "Plava",
    "Shubhakrut", "Shobhakrut", "Krodhi", "Vishvavasu", "Parabhava",
    "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrut",
    "Paridhavi", "Pramadi", "Ananda", "Rakshasa", "Nala",
    "Pingala", "Kalayukta", "Siddharthi", "Raudri", "Durmati",
    "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Akshaya"
)


ENGLISH_RASIS: Final[tuple[str, ...]] = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)


DASHA_LORDS: Final[tuple[str, ...]] = (
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
)


DASHA_YEARS: Final[dict[str, int]] = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}


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


CHARA_KARAKA_NAMES: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("Atmakaraka", "AK", "Soul, Self, Physical Constitution, Life Purpose", "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ"),
    ("Amatyakaraka", "AmK", "Mind, Intellect, Career, Profession, Status", "ಮನಸ್ಸು, ಬುದ್ಧಿಶಕ್ತಿ, ವೃತ್ತಿ, ಉದ್ಯೋಗ, ಅಂತಸ್ತು"),
    ("Bhratrukaraka", "BK", "Siblings, Mentors, Gurus, Courage, Comrades", "ಸಹೋದರರು, ಗುರುಗಳು, ಧೈರ್ಯ, ಮಾರ್ಗದರ್ಶಕರು"),
    ("Matrukaraka", "MK", "Mother, Domestic Life, Emotional Peace, Real Estate", "ತಾಯಿ, ಗೃಹಜೀವನ, ಭಾವನಾತ್ಮಕ ನೆಮ್ಮದಿ, ಆಸ್ತಿ"),
    ("Putrakaraka", "PK", "Children, Progeny, Creative Intellect, Past Merits", "ಸಂತಾನ, ಮಕ್ಕಳ ಭಾಗ್ಯ, ಸೃಜನಶೀಲ ಬುದ್ಧಿ, ಪೂರ್ವಪುಣ್ಯ"),
    ("Gnatikaraka", "GK", "Relatives, Obstacles, Friction, Diseases, Competitors", "ಜ್ಞಾತಿಗಳು, ಅಡೆತಡೆಗಳು, ರೋಗ, ಶತ್ರುಗಳು, ಸ್ಪರ್ಧೆ"),
    ("Darakaraka", "DK", "Spouse, Life Partner, Marriage, Business Partnerships", "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ"),
)

CHARA_KARAKA_PLANETS: Final[frozenset[str]] = frozenset(
    {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
)


