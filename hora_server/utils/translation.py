"""Astrological and calendric terminology translations and payload localization."""

from __future__ import annotations

from typing import Any

TRANSLATIONS: dict[str, str] = {
    # Planets
    "Sun": "ಸೂರ್ಯ",
    "Moon": "ಚಂದ್ರ",
    "Mars": "ಕುಜ",
    "Mercury": "ಬುಧ",
    "Jupiter": "ಗುರು",
    "Venus": "ಶುಕ್ರ",
    "Saturn": "ಶನಿ",
    "Rahu": "ರಾಹು",
    "Ketu": "ಕೇತು",

    # Planet chart abbreviations
    "Su": "ಸೂ",
    "Mo": "ಚಂ",
    "Ma": "ಕು",
    "Me": "ಬು",
    "Ju": "ಗು",
    "Ve": "ಶು",
    "Sa": "ಶ",
    "Ra": "ರಾ",
    "Ke": "ಕೇ",

    # Rasis (Sanskrit transliterated in API)
    "Mesha": "ಮೇಷ",
    "Vrishabha": "ವೃಷಭ",
    "Mithuna": "ಮಿಥುನ",
    "Karka": "ಕಟಕ",
    "Simha": "ಸಿಂಹ",
    "Kanya": "ಕನ್ಯಾ",
    "Tula": "ತುಲಾ",
    "Vrishchika": "ವೃಶ್ಚಿಕ",
    "Dhanu": "ಧನು",
    "Makara": "ಮಕರ",
    "Kumbha": "ಕುಂಭ",
    "Meena": "ಮೀನ",

    # Rasis (English zodiac names used in Kundali module)
    "Aries": "ಮೇಷ",
    "Taurus": "ವೃಷಭ",
    "Gemini": "ಮಿಥುನ",
    "Cancer": "ಕಟಕ",
    "Leo": "ಸಿಂಹ",
    "Virgo": "ಕನ್ಯಾ",
    "Libra": "ತುಲಾ",
    "Scorpio": "ವೃಶ್ಚಿಕ",
    "Sagittarius": "ಧನು",
    "Capricorn": "ಮಕರ",
    "Aquarius": "ಕುಂಭ",
    "Pisces": "ಮೀನ",

    # Nakshatras
    "Ashwini": "ಅಶ್ವಿನಿ",
    "Bharani": "ಭರಣಿ",
    "Krittika": "ಕೃತ್ತಿಕಾ",
    "Rohini": "ರೋಹಿಣಿ",
    "Mrigashira": "ಮೃಗಶಿರ",
    "Ardra": "ಆರ್ದ್ರ",
    "Punarvasu": "ಪುನರ್ವಸು",
    "Pushya": "ಪುಷ್ಯ",
    "Ashlesha": "ಆಶ್ಲೇಷ",
    "Magha": "ಮಘಾ",
    "Purva Phalguni": "ಪೂರ್ವ ಫಲ್ಗುಣಿ",
    "Uttara Phalguni": "ಉತ್ತರ ಫಲ್ಗುಣಿ",
    "Hasta": "ಹಸ್ತ",
    "Chitra": "ಚಿತ್ರಾ",
    "Swati": "ಸ್ವಾತಿ",
    "Vishakha": "ವಿಶಾಖ",
    "Anuradha": "ಅನುರಾಧ",
    "Jyeshtha": "ಜ್ಯೇಷ್ಠ",
    "Mula": "ಮೂಲ",
    "Purva Ashadha": "ಪೂರ್ವಾಷಾಢ",
    "Uttara Ashadha": "ಉತ್ತರಾಷಾಢ",
    "Shravana": "ಶ್ರವಣ",
    "Dhanishtha": "ಧನಿಷ್ಠ",
    "Shatabhisha": "ಶತಭಿಷ",
    "Purva Bhadrapada": "ಪೂರ್ವ ಭಾದ್ರಪದ",
    "Uttara Bhadrapada": "ಉತ್ತರ ಭಾದ್ರಪದ",
    "Revati": "ರೇವತಿ",

    # Yogas
    "Vishkambha": "ವಿಷ್ಕಂಭ",
    "Priti": "ಪ್ರೀತಿ",
    "Ayushman": "ಆಯುಷ್ಮಾನ್",
    "Saubhagya": "ಸೌಭ್ಯಾಗ್ಯ",
    "Shobhana": "ಶೋಭನ",
    "Atiganda": "ಅತಿಗಂಡ",
    "Sukarma": "ಸುಕರ್ಮ",
    "Dhriti": "ಧೃತಿ",
    "Shula": "ಶೂಲ",
    "Ganda": "ಗಂಡ",
    "Vriddhi": "ವೃದ್ಧಿ",
    "Dhruva": "ಧ್ರುವ",
    "Vyaghata": "ವ್ಯಾಘಾತ",
    "Harshana": "ಹರ್ಷಣ",
    "Vajra": "ವಜ್ರ",
    "Siddhi": "ಸಿದ್ಧಿ",
    "Vyatipata": "ವ್ಯತೀಪಾತ",
    "Variyana": "ವರೀಯಾನ್",
    "Parigha": "ಪರಿಘ",
    "Shiva": "ಶಿವ",
    "Siddha": "ಸಿದ್ಧ",
    "Sadhya": "ಸಾಧ್ಯ",
    "Shubha": "ಶುಭ",
    "Shukla": "ಶುಕ್ಲ",
    "Brahma": "ಬ್ರಹ್ಮ",
    "Indra": "ಇಂದ್ರ",
    "Vaidhriti": "ವೈಧೃತಿ",

    # Karanas
    "Kimstughna": "ಕಿಂಸ್ತುಘ್ನ",
    "Bava": "ಬವ",
    "Balava": "ಬಾಲವ",
    "Kaulava": "ಕೌಲವ",
    "Taitila": "ತೈತಿಲ",
    "Gara": "ಗರ",
    "Vanija": "ವಣಿಜ",
    "Vishti": "ವಿಷ್ಟಿ",
    "Shakuni": "ಶಕುನಿ",
    "Chatushpada": "ಚತುಷ್ಪಾದ",
    "Naga": "ನಾಗ",

    # Tithi/Paksha words
    "Krishna": "ಕೃಷ್ಣ",
    "Shukla": "ಶುಕ್ಲ",
    "Pratipada": "ಪ್ರತಿಪದೆ",
    "Dvitiya": "ದ್ವಿತೀಯ",
    "Tritiya": "ತೃತೀಯ",
    "Chaturthi": "ಚತುರ್ಥಿ",
    "Panchami": "ಪಂಚಮಿ",
    "Shashthi": "ಷಷ್ಠಿ",
    "Saptami": "ಸಪ್ತಮಿ",
    "Ashtami": "ಅಷ್ಟಮಿ",
    "Navami": "ನವಮಿ",
    "Dashami": "ದಶಮಿ",
    "Ekadashi": "ಏಕಾದಶಿ",
    "Dvadashi": "ದ್ವಾದಶಿ",
    "Trayodashi": "ತ್ರಯೋದಶಿ",
    "Chaturdashi": "ಚತುರ್ದಶಿ",
    "Purnima": "ಪೌರ್ಣಮಿ",
    "Amavasya": "ಅಮಾವಾಸ್ಯೆ",

    # Weekdays (English / Sanskrit)
    "Monday": "ಸೋಮವಾರ",
    "Tuesday": "ಮಂಗಳವಾರ",
    "Wednesday": "ಬುಧವಾರ",
    "Thursday": "ಗುರುವಾರ",
    "Friday": "ಶುಕ್ರವಾರ",
    "Saturday": "ಶನಿವಾರ",
    "Sunday": "ಭಾನುವಾರ",
    "Somavara": "ಸೋಮವಾರ",
    "Mangalavara": "ಮಂಗಳವಾರ",
    "Budhavara": "ಬುಧವಾರ",
    "Guruvara": "ಗುರುವಾರ",
    "Shukravara": "ಶುಕ್ರವಾರ",
    "Shanivara": "ಶನಿವಾರ",
    "Ravivara": "ರವಿವಾರ",

    # Ayanas
    "Uttarayana": "ಉತ್ತರಾಯಣ",
    "Dakshinayana": "ದಕ್ಷಿಣಾಯನ",

    # Rutus (Seasons)
    "Vasanta": "ವಸಂತ",
    "Grishma": "ಗ್ರೀಷ್ಮ",
    "Varsha": "ವರ್ಷ",
    "Sharad": "ಶರದ್",
    "Hemanta": "ಹೇಮಂತ",
    "Shishira": "ಶಿಶಿರ",

    # Months (Masas)
    "Chaitra": "ಚೈತ್ರ",
    "Vaishakha": "ವೈಶಾಖ",
    "Jyeshtha": "ಜ್ಯೇಷ್ಠ",
    "Ashadha": "ಆಷಾಢ",
    "Shravana": "ಶ್ರಾವಣ",
    "Bhadrapada": "ಭಾದ್ರಪದ",
    "Ashvina": "ಆಶ್ವಯುಜ",
    "Kartika": "ಕಾರ್ತಿಕ",
    "Margashirsha": "ಮಾರ್ಗಶಿರ",
    "Pausha": "ಪುಷ್ಯ",
    "Magha": "ಮಾಘ",
    "Phalguna": "ಫಾಲ್ಗುಣ",
    "Adhika": "ಅಧಿಕ",

    # Samvatsaras
    "Prabhava": "ಪ್ರಭವ",
    "Vibhava": "ವಿಭವ",
    "Shukla": "ಶುಕ್ಲ",
    "Pramoduta": "ಪ್ರಮೋದೂತ",
    "Prajotpatti": "ಪ್ರಜೋತ್ಪತ್ತಿ",
    "Angirasa": "ಅಂಗಿರಸ",
    "Shrimukha": "ಶ್ರೀಮುಖ",
    "Bhava": "ಭಾವ",
    "Yuva": "ಯುವ",
    "Dhatu": "ಧಾತು",
    "Ishvara": "ಈಶ್ವರ",
    "Bahudhanya": "ಬಹುಧಾನ್ಯ",
    "Pramadi": "ಪ್ರಮಾದಿ",
    "Vikrama": "ವಿಕ್ರಮ",
    "Vrisha": "ವೃಷ",
    "Chitrabhanu": "ಚಿತ್ರಭಾನು",
    "Svabhanu": "ಸ್ವಭಾನು",
    "Tarana": "ತಾರಣ",
    "Parthiva": "ಪಾರ್ಥಿವ",
    "Vyaya": "ವ್ಯಯ",
    "Sarvajit": "ಸರ್ವಜಿತ್",
    "Sarvadhari": "ಸರ್ವಾಧಾರಿ",
    "Virodhi": "ವಿರೋಧಿ",
    "Vikruti": "ವಿಕೃತಿ",
    "Khara": "ಖರ",
    "Nandana": "ನಂದನ",
    "Vijaya": "ವಿಜಯ",
    "Jaya": "ಜಯ",
    "Manmatha": "ಮನ್ಮಥ",
    "Durmukhi": "ದುರ್ಮುಖಿ",
    "Hevilambi": "ಹೇವಿಲಂಬಿ",
    "Vilambi": "ವಿಲಂಬಿ",
    "Vikari": "ವಿಕಾರಿ",
    "Sharvari": "ಶಾರ್ವರಿ",
    "Plava": "ಪ್ಲವ",
    "Shubhakrut": "ಶುಭಕೃತ್",
    "Shobhakrut": "ಶೋಭಕೃತ್",
    "Krodhi": "ಕ್ರೋಧಿ",
    "Vishvavasu": "ವಿಶ್ವಾವಸು",
    "Parabhava": "ಪರಾಭವ",
    "Plavanga": "ಪ್ಲವಂಗ",
    "Kilaka": "ಕೀಲಕ",
    "Saumya": "ಸೌಮ್ಯ",
    "Sadharana": "ಸಾಧಾರಣ",
    "Virodhikrut": "ವಿರೋಧಿಕೃತ್",
    "Paridhavi": "ಪರಿದಾವಿ",
    "Ananda": "ಆನಂದ",
    "Rakshasa": "ರಾಕ್ಷಸ",
    "Nala": "ನಳ",
    "Pingala": "ಪಿಂಗಳ",
    "Kalayukta": "ಕಾಲಯುಕ್ತ",
    "Siddharthi": "ಸಿದ್ಧಾರ್ಥಿ",
    "Raudri": "ರೌದ್ರಿ",
    "Durmati": "ದುರ್ಮತಿ",
    "Dundubhi": "ದುಂದುಭಿ",
    "Rudhirodgari": "ರುಧಿರೋದ್ಗಾರಿ",
    "Raktakshi": "ರಕ್ತಾಕ್ಷಿ",
    "Krodhana": "ಕ್ರೋಧನ",
    "Akshaya": "ಅಕ್ಷಯ",

    # Muhurtas
    "Rahu Kalam": "ರಾಹುಕಾಲ",
    "Gulika Kalam": "ಗುಳಿಕ ಕಾಲ",
    "Yamaganda": "ಯಮಗಂಡ",
    "Abhijit Muhurta": "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ",

    # Hora Period
    "day": "ಹಗಲು",
    "night": "ರಾತ್ರಿ",

    # Chara Karakas
    "Atmakaraka": "ಆತ್ಮಕಾರಕ",
    "Amatyakaraka": "ಅಮಾತ್ಯಕಾರಕ",
    "Bhratrukaraka": "ಭ್ರಾತೃಕಾರಕ",
    "Matrukaraka": "ಮಾತೃಕಾರಕ",
    "Putrakaraka": "ಪುತ್ರಕಾರಕ",
    "Gnatikaraka": "ಜ್ಞಾತಿಕಾರಕ",
    "Darakaraka": "ದಾರಕಾರಕ",

    # Chara Karaka Significations
    "Soul, Self, Physical Constitution, Life Purpose": "ಆತ್ಮ, ಸ್ವಯಂ, ಶಾರೀರಿಕ ರಚನೆ, ಜೀವನ ಉದ್ದೇಶ",
    "Mind, Intellect, Career, Profession, Status": "ಮನಸ್ಸು, ಬುದ್ಧಿಶಕ್ತಿ, ವೃತ್ತಿ, ಉದ್ಯೋಗ, ಅಂತಸ್ತು",
    "Siblings, Mentors, Gurus, Courage, Comrades": "ಸಹೋದರರು, ಗುರುಗಳು, ಧೈರ್ಯ, ಮಾರ್ಗದರ್ಶಕರು",
    "Mother, Domestic Life, Emotional Peace, Real Estate": "ತಾಯಿ, ಗೃಹಜೀವನ, ಭಾವನಾತ್ಮಕ ನೆಮ್ಮದಿ, ಆಸ್ತಿ",
    "Children, Progeny, Creative Intellect, Past Merits": "ಸಂತಾನ, ಮಕ್ಕಳ ಭಾಗ್ಯ, ಸೃಜನಶೀಲ ಬುದ್ಧಿ, ಪೂರ್ವಪುಣ್ಯ",
    "Relatives, Obstacles, Friction, Diseases, Competitors": "ಜ್ಞಾತಿಗಳು, ಅಡೆತಡೆಗಳು, ರೋಗ, ಶತ್ರುಗಳು, ಸ್ಪರ್ಧೆ",
    "Spouse, Life Partner, Marriage, Business Partnerships": "ಪತಿ/ಪತ್ನಿ, ಜೀವನ ಸಂಗಾತಿ, ವೈವಾಹಿಕ ಜೀವನ, ವ್ಯಾಪಾರ ಪಾಲುದಾರಿಕೆ",

    # Ashtakoota Kootas
    "Varna": "ವರ್ಣ",
    "Vashya": "ವಶ್ಯ",
    "Tara": "ತಾರಾ",
    "Tara (Dina)": "ತಾರಾ (ದಿನ)",
    "Yoni": "ಯೋನಿ",
    "Graha Maitri": "ಗ್ರಹ ಮೈತ್ರಿ",
    "Gana": "ಗಣ",
    "Bhakoot": "ಭಕೂಟ",
    "Nadi": "ನಾಡಿ",

    # Varna Classifications
    "Brahmin": "ಬ್ರಾಹ್ಮಣ",
    "Kshatriya": "ಕ್ಷತ್ರಿಯ",
    "Vaishya": "ವೈಶ್ಯ",
    "Shudra": "ಶೂದ್ರ",

    # Vashya Classifications
    "Chatushpada": "ಚತುಷ್ಪಾದ",
    "Manava": "ಮಾನವ",
    "Jalachara": "ಜಲಚರ",
    "Vanachara": "ವನಚರ",
    "Keeta": "ಕೀಟ",

    # 9 Taras
    "Janma": "ಜನ್ಮ",
    "Sampat": "ಸಂಪತ್",
    "Vipat": "ವಿಪತ್",
    "Kshema": "ಕ್ಷೇಮ",
    "Pratyak": "ಪ್ರತ್ಯಕ್",
    "Sadhana": "ಸಾಧನಾ",
    "Sadhaka": "ಸಾಧಕ",
    "Vadha": "ವಧ",
    "Naidhana": "ನೈಧನ",
    "Mitra": "ಮಿತ್ರ",
    "Parama Mitra": "ಪರಮ ಮಿತ್ರ",

    # 14 Animal Yonis
    "Horse": "ಅಶ್ವ (ಕುದುರೆ)",
    "Elephant": "ಗಜ (ಆನೆ)",
    "Sheep": "ಮೇಷ (ಕುರಿ)",
    "Serpent": "ಸರ್ಪ (ಹಾವು)",
    "Dog": "ಶ್ವಾನ (ನಾಯಿ)",
    "Cat": "ಮಾರ್ಜಾಲ (ಬೆಕ್ಕು)",
    "Rat": "ಮೂಷಕ (ಇಲಿ)",
    "Cow": "ಗೋವು (ಹಸು)",
    "Buffalo": "ಮಹಿಷ (ಕೋಣ)",
    "Tiger": "ವ್ಯಾಘ್ರ (ಹುಲಿ)",
    "Deer": "ಮೃಗ (ಜಿಂಕೆ)",
    "Monkey": "ವಾನರ (ಕೋತಿ)",
    "Mongoose": "ನಕುಲ (ಮುಂಗುಸಿ)",
    "Lion": "ಸಿಂಹ",

    # Ganas
    "Deva": "ದೇವ",
    "Manushya": "ಮನುಷ್ಯ",
    "Rakshasa": "ರಾಕ್ಷಸ",

    # Nadis
    "Adi": "ಆದಿ",
    "Madhya": "ಮಧ್ಯ",
    "Antya": "ಅಂತ್ಯ",

    # Results & Verdicts
    "Uttama": "ಉತ್ತಮ",
    "Madhyama": "ಮಧ್ಯಮ",
    "Adhama": "ಅಧಮ",

    # Doshas
    "Nadi Dosha": "ನಾಡಿ ದೋಷ",
    "Bhakoot Dosha": "ಭಕೂಟ ದೋಷ",
    "Bhakoot Dosha (Navapanchama)": "ಭಕೂಟ ದೋಷ (ನವಪಂಚಮ)",
    "Bhakoot Dosha (Dvidvadasha)": "ಭಕೂಟ ದೋಷ (ದ್ವಿದ್ವಾದಶ)",
    "Bhakoot Dosha (Shadashtaka)": "ಭಕೂಟ ದೋಷ (ಷಡಾಷ್ಟಕ)",
    "Gana Dosha": "ಗಣ ದೋಷ",
    "Varna Dosha": "ವರ್ಣ ದೋಷ",
    "Vashya Dosha": "ವಶ್ಯ ದೋಷ",
    "Tara Dosha": "ತಾರಾ ದೋಷ",
    "Graha Maitri Dosha": "ಗ್ರಹ ಮೈತ್ರಿ ದೋಷ",
    "Yoni Vairi Dosha": "ಯೋನಿ ವೈರಿ ದೋಷ",

    # Manglik / Kuja Dosha
    "Manglik": "ಮಾಂಗ್ಲಿಕ್ (ಕುಜ ದೋಷ)",
    "Non-Manglik": "ಮಾಂಗ್ಲಿಕ್ ರಹಿತ",
    "Compatible (Sama Manglik)": "ಸಮ ಕುಜದೋಷ (ಹೊಂದಾಣಿಕೆಯಾಗುತ್ತದೆ)",
    "Compatible (Non-Manglik)": "ಕುಜದೋಷ ರಹಿತ (ಹೊಂದಾಣಿಕೆಯಾಗುತ್ತದೆ)",
    "Partial / Requires Remedial Guidance": "ಭಾಗಶಃ ಹೊಂದಾಣಿಕೆ / ಜ್ಯೋತಿಷ್ಯ ಪರಿಹಾರ ಅಗತ್ಯ",

    # Summary Messages
    "Excellent match with strong emotional, biological, and genetic harmony.": "ಉತ್ತಮ ಹೊಂದಾಣಿಕೆ - ಭಾವನಾತ್ಮಕ, ದೈಹಿಕ ಮತ್ತು ಅನುವಂಶಿಕ ಸಾಮರಸ್ಯ ಹೊಂದಿದೆ.",
    "Good match with favorable overall compatibility approved for marriage.": "ಉತ್ತಮ ಹೊಂದಾಣಿಕೆ - ವಿವಾಹಕ್ಕೆ ಪ್ರಶಸ್ತವಾದ ಹೊಂದಾಣಿಕೆ ಇದೆ.",
    "Moderate match with acceptable baseline points. Detailed chart review suggested.": "ಮಧ್ಯಮ ಹೊಂದಾಣಿಕೆ - ಜಾತಕದ ಸಮಗ್ರ ಪರಿಶೀಲನೆ ಅಗತ್ಯ.",
    "Not recommended due to unmitigated Nadi Dosha impacting progeny health.": "ನಾಡಿ ದೋಷವಿರುವುದರಿಂದ ವಿವಾಹಕ್ಕೆ ಶಿಫಾರಸು ಮಾಡಲಾಗುವುದಿಲ್ಲ.",
    "Not recommended due to unmitigated Bhakoot Dosha.": "ಭಕೂಟ ದೋಷವಿರುವುದರಿಂದ ವಿವಾಹಕ್ಕೆ ಶಿಫಾರಸು ಮಾಡಲಾಗುವುದಿಲ್ಲ.",
    "Low compatibility score. Astrological consultation recommended.": "ಹೊಂದಾಣಿಕೆ ಅಂಕಗಳು ಕಡಿಮೆ ಇವೆ. ಜ್ಯೋತಿಷ್ಯ ಸಲಹೆ ಅಗತ್ಯ.",

    # Static Descriptions
    "Groom's Varna is equal to or higher than Bride's Varna, indicating harmony in temperament and work ethic.": "ವರನ ವರ್ಣವು ಕನ್ಯೆಯ ವರ್ಣಕ್ಕೆ ಸಮಾನ ಅಥವಾ ಅಧಿಕವಾಗಿದೆ, ಕರ್ತವ್ಯ ಮತ್ತು ಸ್ವಭಾವ ಸಾಮರಸ್ಯವಿದೆ.",
    "Groom's Varna is lower than Bride's Varna.": "ವರನ ವರ್ಣವು ಕನ್ಯೆಯ ವರ್ಣಕ್ಕಿಂತ ಕಡಿಮೆಯಾಗಿದೆ (ವರ್ಣ ದೋಷ).",
    "Full mutual attraction, amenable temperament, and natural devotion.": "ಪೂರ್ಣ ಆಕರ್ಷಣೆ, ಪರಸ್ಪರ ಪ್ರೀತಿ ಮತ್ತು ಅನುಕೂಲಕರ ಸ್ವಭಾವ.",
    "Good mutual harmony and natural power balance between partners.": "ಉತ್ತಮ ಪರಸ್ಪರ ಸಾಮರಸ್ಯ ಮತ್ತು ಸಮತೋಲನ.",
    "Moderate harmony with neutral attraction.": "ಮಧ್ಯಮ ಹೊಂದಾಣಿಕೆ ಮತ್ತು ತಟಸ್ಥ ಆಕರ್ಷಣೆ.",
    "Incompatible Vashya nature leading to struggle for dominance.": "ವಶ್ಯ ಹೊಂದಾಣಿಕೆ ಇಲ್ಲ (ವಶ್ಯ ದೋಷ).",
    "Same Janma Nakshatra; Tara alignment is auspicious.": "ಏಕ ನಕ್ಷತ್ರ - ತಾರಾ ಹೊಂದಾಣಿಕೆ ಶುಭಕರವಾಗಿದೆ.",
    "Same Gana (Deva), providing great temperament and mutual wavelength.": "ಏಕ ಗಣ (ದೇವ ಗಣ) - ಅತ್ಯುತ್ತಮ ಸ್ವಭಾವ ಮತ್ತು ಪರಸ್ಪರ ಹೊಂದಾಣಿಕೆ.",
    "Same Gana (Manushya), providing great temperament and mutual wavelength.": "ಏಕ ಗಣ (ಮನುಷ್ಯ ಗಣ) - ಅತ್ಯುತ್ತಮ ಸ್ವಭಾವ ಮತ್ತು ಪರಸ್ಪರ ಹೊಂದಾಣಿಕೆ.",
    "Same Gana (Rakshasa), providing great temperament and mutual wavelength.": "ಏಕ ಗಣ (ರಾಕ್ಷಸ ಗಣ) - ಅತ್ಯುತ್ತಮ ಸ್ವಭಾವ ಮತ್ತು ಪರಸ್ಪರ ಹೊಂದಾಣಿಕೆ.",
    "Bride is Deva and Groom is Manushya, providing moderate temperament compatibility.": "ಕನ್ಯೆಯು ದೇವ ಗಣ ಹಾಗೂ ವರನು ಮನುಷ್ಯ ಗಣ - ಮಧ್ಯಮ ಹೊಂದಾಣಿಕೆ (೪ ಅಂಕ).",
    "Bride is Deva and Groom is Rakshasa; temperament difference mitigated to 2 points.": "ಕನ್ಯೆಯು ದೇವ ಗಣ ಹಾಗೂ ವರನು ರಾಕ್ಷಸ ಗಣ - ಗಣ ದೋಷ ಭಾಗಶಃ ಶಾಂತವಾಗಿದೆ (೨ ಅಂಕ).",
    "Bride is Manushya and Groom is Deva, generating mutual respect and harmony.": "ಕನ್ಯೆಯು ಮನುಷ್ಯ ಗಣ ಹಾಗೂ ವರನು ದೇವ ಗಣ - ಪರಸ್ಪರ ಗೌರವ ಮತ್ತು ಸಾಮರಸ್ಯ (೫ ಅಂಕ).",
    "Bride is Manushya and Groom is Rakshasa; behavioral friction mitigated to 1 point.": "ಕನ್ಯೆಯು ಮನುಷ್ಯ ಗಣ ಹಾಗೂ ವರನು ರಾಕ್ಷಸ ಗಣ - ಗಣ ದೋಷ ಭಾಗಶಃ ಶಾಂತವಾಗಿದೆ (೧ ಅಂಕ).",
    "Bride is Rakshasa and Groom is Deva; high temperament incompatibility.": "ಕನ್ಯೆಯು ರಾಕ್ಷಸ ಗಣ ಹಾಗೂ ವರನು ದೇವ ಗಣ - ಸ್ವಭಾವ ಹೊಂದಾಣಿಕೆ ಕೊರತೆ (ಗಣ ದೋಷ).",
    "Bride is Rakshasa and Groom is Manushya; high behavioral clash.": "ಕನ್ಯೆಯು ರಾಕ್ಷಸ ಗಣ ಹಾಗೂ ವರನು ಮನುಷ್ಯ ಗಣ - ವರ್ತನೆಯಲ್ಲಿ ಭಿನ್ನಾಭಿಪ್ರಾಯ (ಗಣ ದೋಷ).",
    "5/9 (Navapanchama) placement indicates progeny or Dharma friction (Bhakoot Dosha).": "೫/೯ (ನವಪಂಚಮ) ಸಂಬಂಧ - ಸಂತಾನ ಅಥವಾ ಧರ್ಮ ವಿಚಾರದಲ್ಲಿ ಭಿನ್ನಾಭಿಪ್ರಾಯ (ಭಕೂಟ ದೋಷ).",
    "2/12 (Dvidvadasha) placement indicates financial strain or emotional distance (Bhakoot Dosha).": "೨/೧೨ (ದ್ವಿದ್ವಾದಶ) ಸಂಬಂಧ - ಆರ್ಥಿಕ ಅಥವಾ ಭಾವನಾತ್ಮಕ ಅಂತರ (ಭಕೂಟ ದೋಷ).",
    "6/8 (Shadashtaka) placement indicates health vulnerabilities or friction (Bhakoot Dosha).": "೬/೮ (ಷಡಾಷ್ಟಕ) ಸಂಬಂಧ - ಆರೋಗ್ಯ ಮತ್ತು ಮನಸ್ತಾಪದ ಸಾಧ್ಯತೆ (ಭಕೂಟ ದೋಷ).",
    "Both partners have Kuja Dosha, resulting in mutual cancellation and balance.": "ಇಬ್ಬರ ಜಾತಕದಲ್ಲೂ ಕುಜ ದೋಷವಿದ್ದು, ಪರಸ್ಪರ ರದ್ದಾಗುತ್ತದೆ (ಸಮ ಕುಜದೋಷ).",
    "Neither partner has Kuja Dosha. The match is harmonious.": "ಇಬ್ಬರ ಜಾತಕದಲ್ಲೂ ಕುಜ ದೋಷವಿಲ್ಲ. ಹೊಂದಾಣಿಕೆ ಉತ್ತಮವಾಗಿದೆ.",
    "Groom has Kuja Dosha while Bride does not. Astrological guidance is advised.": "ವರನಿಗೆ ಕುಜ ದೋಷವಿದೆ, ಕನ್ಯೆಗೆ ಇಲ್ಲ. ಜ್ಯೋತಿಷ್ಯ ಸಲಹೆ ಅಗತ್ಯ.",
    "Bride has Kuja Dosha while Groom does not. Astrological guidance is advised.": "ಕನ್ಯೆಗೆ ಕುಜ ದೋಷವಿದೆ, ವರನಿಗೆ ಇಲ್ಲ. ಜ್ಯೋತಿಷ್ಯ ಸಲಹೆ ಅಗತ್ಯ.",
}


import re


def translate_dynamic_description(text: str) -> str | None:
    """Translates dynamic description strings into natural Kannada."""
    # Rasi name with number: "Kanya (6)" -> "ಕನ್ಯಾ (೬)"
    m = re.match(r"^([A-Za-z]+)\s*\((\d+)\)$", text)
    if m:
        r_name, r_num = m.group(1), m.group(2)
        r_kn = TRANSLATIONS.get(r_name, r_name)
        return f"{r_kn} ({r_num})"

    # Tara: "Both Tara alignments (Groom: X, Bride: Y) are auspicious..."
    m = re.match(r"^Both Tara alignments \(Groom:\s*([^,]+),\s*Bride:\s*([^)]+)\) are auspicious.*", text)
    if m:
        g_t = TRANSLATIONS.get(m.group(1).strip(), m.group(1).strip())
        b_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        return f"ವರ ಮತ್ತು ಕನ್ಯೆಯ ತಾರಾ ಹೊಂದಾಣಿಕೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t}) ಶುಭಕರವಾಗಿದ್ದು, ಆಯಸ್ಸು ಮತ್ತು ಆರೋಗ್ಯ ವೃದ್ಧಿಸುತ್ತದೆ."

    # Tara: "Both Tara alignments (X & Y) are auspicious..."
    m = re.match(r"^Both Tara alignments \(([^&]+)\s*&\s*([^)]+)\) are auspicious.*", text)
    if m:
        g_t = TRANSLATIONS.get(m.group(1).strip(), m.group(1).strip())
        b_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        return f"ವರ ಮತ್ತು ಕನ್ಯೆಯ ತಾರಾ ಹೊಂದಾಣಿಕೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t}) ಶುಭಕರವಾಗಿದ್ದು, ಆಯಸ್ಸು ಮತ್ತು ಆರೋಗ್ಯ ವೃದ್ಧಿಸುತ್ತದೆ."

    # Tara: "Tara alignment is favorable for Person (Groom: X, Bride: Y), awarding 1.5 points."
    m = re.match(r"^Tara alignment is favorable for ([A-Za-z]+) \(Groom:\s*([^,]+),\s*Bride:\s*([^)]+)\).*", text)
    if m:
        person = "ವರ" if m.group(1) == "Groom" else "ಕನ್ಯೆ"
        g_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        b_t = TRANSLATIONS.get(m.group(3).strip(), m.group(3).strip())
        return f"{person}ರಿಗೆ ತಾರಾ ಹೊಂದಾಣಿಕೆ ಶುಭಕರವಾಗಿದೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t}), ೧.೫ ಅಂಕಗಳು ದೊರೆತಿವೆ."

    # Tara: "Tara alignment is favorable for Person (X & Y), awarding 1.5 points."
    m = re.match(r"^Tara alignment is favorable for ([A-Za-z]+) \(([^&]+)\s*&\s*([^)]+)\).*", text)
    if m:
        person = "ವರ" if m.group(1) == "Groom" else "ಕನ್ಯೆ"
        g_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        b_t = TRANSLATIONS.get(m.group(3).strip(), m.group(3).strip())
        return f"{person}ರಿಗೆ ತಾರಾ ಹೊಂದಾಣಿಕೆ ಶುಭಕರವಾಗಿದೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t}), ೧.೫ ಅಂಕಗಳು ದೊರೆತಿವೆ."

    # Tara Parihara: "Tara Dosha between Groom (X) and Bride (Y) is mitigated to 1.5 points due to friendly Nakshatra lords (L1 and L2)."
    m = re.match(r"^Tara Dosha between Groom \(([^)]+)\) and Bride \(([^)]+)\) is mitigated to 1\.5 points due to friendly Nakshatra lords \(([^)]+) and ([^)]+)\)\.", text)
    if m:
        g_t = TRANSLATIONS.get(m.group(1).strip(), m.group(1).strip())
        b_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        l1 = TRANSLATIONS.get(m.group(3).strip(), m.group(3).strip())
        l2 = TRANSLATIONS.get(m.group(4).strip(), m.group(4).strip())
        return f"ವರ ({g_t}) ಮತ್ತು ಕನ್ಯೆಯ ({b_t}) ತಾರಾ ದೋಷವು ಮಿತ್ರ ನಕ್ಷತ್ರಾಧಿಪತಿಗಳಿಂದ ({l1} ಮತ್ತು {l2}) ರದ್ದಾಗಿ ೧.೫ ಅಂಕಗಳು ದೊರೆತಿವೆ."

    # Tara Inauspicious: "Both Tara alignments (Groom: X, Bride: Y) are inauspicious..."
    m = re.match(r"^Both Tara alignments \(Groom:\s*([^,]+),\s*Bride:\s*([^)]+)\) are inauspicious.*", text)
    if m:
        g_t = TRANSLATIONS.get(m.group(1).strip(), m.group(1).strip())
        b_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        return f"ಇಬ್ಬರ ತಾರಾ ಹೊಂದಾಣಿಕೆಯೂ ಅಶುಭಕರವಾಗಿದೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t} - ತಾರಾ ದೋಷ)."

    # Tara Inauspicious: "Both Tara alignments (X & Y) fall in inauspicious zones..."
    m = re.match(r"^Both Tara alignments \(([^&]+)\s*&\s*([^)]+)\) fall in inauspicious zones.*", text)
    if m:
        g_t = TRANSLATIONS.get(m.group(1).strip(), m.group(1).strip())
        b_t = TRANSLATIONS.get(m.group(2).strip(), m.group(2).strip())
        return f"ಇಬ್ಬರ ತಾರಾ ಹೊಂದಾಣಿಕೆಯೂ ಅಶುಭಕರವಾಗಿದೆ (ವರ: {g_t}, ಕನ್ಯೆ: {b_t} - ತಾರಾ ದೋಷ)."

    # Yoni: "Same animal Yoni (X)..."
    m = re.match(r"^Same animal Yoni \(([^)]+)\).*", text)
    if m:
        y = TRANSLATIONS.get(m.group(1), m.group(1))
        return f"ಏಕ ಯೋನಿ ({y}) - ಅತ್ಯುತ್ತಮ ದೈಹಿಕ ಮತ್ತು ಜೈವಿಕ ಸಾಮರಸ್ಯ."

    # Yoni: "Friendly animal Yonis (X and Y)..."
    m = re.match(r"^Friendly animal Yonis \(([^)]+) and ([^)]+)\).*", text)
    if m:
        y1 = TRANSLATIONS.get(m.group(1), m.group(1))
        y2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಮಿತ್ರ ಯೋನಿಗಳು ({y1} ಮತ್ತು {y2}) - ಉತ್ತಮ ದೈಹಿಕ ಆಕರ್ಷಣೆ ಮತ್ತು ಪ್ರೀತಿ."

    # Yoni: "Neutral animal Yonis (X and Y)..."
    m = re.match(r"^Neutral animal Yonis \(([^)]+) and ([^)]+)\).*", text)
    if m:
        y1 = TRANSLATIONS.get(m.group(1), m.group(1))
        y2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಸಮ ಯೋನಿಗಳು ({y1} ಮತ್ತು {y2}) - ಸಾಧಾರಣ ದೈಹಿಕ ಸಾಮರಸ್ಯ."

    # Yoni: "Inimical animal Yonis (X and Y)..."
    m = re.match(r"^Inimical animal Yonis \(([^)]+) and ([^)]+)\).*", text)
    if m:
        y1 = TRANSLATIONS.get(m.group(1), m.group(1))
        y2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಶತ್ರು ಯೋನಿಗಳು ({y1} ಮತ್ತು {y2}) - ದೈಹಿಕ ಹೊಂದಾಣಿಕೆಯಲ್ಲಿ ವ್ಯತ್ಯಾಸ."

    # Yoni: "Sworn enemy animal Yonis (X vs Y)..."
    m = re.match(r"^Sworn enemy animal Yonis \(([^)]+) vs ([^)]+)\).*", text)
    if m:
        y1 = TRANSLATIONS.get(m.group(1), m.group(1))
        y2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಪರಸ್ಪರ ವೈರಿ ಯೋನಿಗಳು ({y1} ಮತ್ತು {y2}) - ತೀವ್ರ ದೈಹಿಕ ಅಸಾಮರಸ್ಯ (ಯೋನಿ ವೈರಿ ದೋಷ)."

    # Graha Maitri: "Same Rasi lord (X)..."
    m = re.match(r"^Same Rasi lord \(([^)]+)\).*", text)
    if m:
        lord = TRANSLATIONS.get(m.group(1), m.group(1))
        return f"ಏಕ ರಾಶ್ಯಾಧಿಪತಿ ({lord}) - ಗಾಢ ಮಾನಸಿಕ ಮತ್ತು ಬೌದ್ಧಿಕ ಸಾಮರಸ್ಯ."

    # Graha Maitri: "Mutual friends (X and Y)..."
    m = re.match(r"^Mutual friends \(([^)]+) and ([^)]+)\).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಪರಸ್ಪರ ಮಿತ್ರ ರಾಶ್ಯಾಧಿಪತಿಗಳು ({l1} ಮತ್ತು {l2}) - ಉತ್ತಮ ಅನ್ಯೋನ್ಯತೆ ಮತ್ತು ಗೌರವ."

    # Graha Maitri: "One-sided friendship and neutrality between X and Y..."
    m = re.match(r"^One-sided friendship and neutrality between ([A-Za-z]+) and ([A-Za-z]+).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಮಿತ್ರ ಮತ್ತು ಸಮ ಸಂಬಂಧ ({l1} ಮತ್ತು {l2}) - ಉತ್ತಮ ಮಾನಸಿಕ ಹೊಂದಾಣಿಕೆ."

    # Graha Maitri: "Mutual neutrality between X and Y..."
    m = re.match(r"^Mutual neutrality between ([A-Za-z]+) and ([A-Za-z]+).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಪರಸ್ಪರ ಸಮ ಗ್ರಹಗಳು ({l1} ಮತ್ತು {l2}) - ಸ್ಥಿರ ಮಾನಸಿಕ ಸಂಬಂಧ."

    # Graha Maitri: "Mixed relationship (Friend/Enemy) between X and Y..."
    m = re.match(r"^Mixed relationship \(Friend/Enemy\) between ([A-Za-z]+) and ([A-Za-z]+).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಮಿಶ್ರ ಸಂಬಂಧ ({l1} ಮತ್ತು {l2}) - ವೈಚಾರಿಕ ಭಿನ್ನಾಭಿಪ್ರಾಯ (ಗ್ರಹ ಮೈತ್ರಿ ದೋಷ)."

    # Graha Maitri: "Neutral/Enemy relationship between X and Y..."
    m = re.match(r"^Neutral/Enemy relationship between ([A-Za-z]+) and ([A-Za-z]+).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಸಮ-ಶತ್ರು ಸಂಬಂಧ ({l1} ಮತ್ತು {l2}) - ಗ್ರಹ ಮೈತ್ರಿ ಕೊರತೆ."

    # Graha Maitri: "Mutual enemies (X and Y)..."
    m = re.match(r"^Mutual enemies \(([^)]+) and ([^)]+)\).*", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಪರಸ್ಪರ ಶತ್ರು ಗ್ರಹಗಳು ({l1} ಮತ್ತು {l2}) - ಮಾನಸಿಕ ಸಾಮರಸ್ಯದ ಕೊರತೆ (ಗ್ರಹ ಮೈತ್ರಿ ದೋಷ)."

    # Bhakoot: "Auspicious X/Y Rasi relationship..."
    m = re.match(r"^Auspicious ([0-9/]+) Rasi relationship fostering marital happiness, health, and prosperity\.", text)
    if m:
        rel = m.group(1)
        return f"ಶುಭ {rel} ರಾಶಿ ಸಂಬಂಧ - ದಾಂಪತ್ಯ ಸುಖ, ಆರೋಗ್ಯ ಮತ್ತು ಸಮೃದ್ಧಿ."

    # Bhakoot Parihara: "5/9 (Navapanchama) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords (L1 and L2)."
    m = re.match(r"^5/9 \(Navapanchama\) placement \(0/7 pts\); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords \(([^)]+) and ([^)]+)\)\.", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"೫/೯ (ನವಪಂಚಮ) ಸಂಬಂಧ (೦/೭ ಅಂಕ); ರಾಶ್ಯಾಧಿಪತಿಗಳ ಮಿತ್ರತ್ವದಿಂದ ({l1} ಮತ್ತು {l2}) ಭಕೂಟ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Bhakoot Parihara: "2/12 (Dvidvadasha) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords (L1 and L2)."
    m = re.match(r"^2/12 \(Dvidvadasha\) placement \(0/7 pts\); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords \(([^)]+) and ([^)]+)\)\.", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"೨/೧೨ (ದ್ವಿದ್ವಾದಶ) ಸಂಬಂಧ (೦/೭ ಅಂಕ); ರಾಶ್ಯಾಧಿಪತಿಗಳ ಮಿತ್ರತ್ವದಿಂದ ({l1} ಮತ್ತು {l2}) ಭಕೂಟ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Bhakoot Parihara: "6/8 (Shadashtaka) placement (0/7 pts); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords (L1 and L2)."
    m = re.match(r"^6/8 \(Shadashtaka\) placement \(0/7 pts\); Bhakoot Dosha is astrologically mitigated due to friendly/identical Rasi lords \(([^)]+) and ([^)]+)\)\.", text)
    if m:
        l1 = TRANSLATIONS.get(m.group(1), m.group(1))
        l2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"೬/೮ (ಷಡಾಷ್ಟಕ) ಸಂಬಂಧ (೦/೭ ಅಂಕ); ರಾಶ್ಯಾಧಿಪತಿಗಳ ಮಿತ್ರತ್ವದಿಂದ ({l1} ಮತ್ತು {l2}) ಭಕೂಟ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Nadi: "Different Nadis (X and Y) assure optimal genetic diversity, vitality, and progeny health."
    m = re.match(r"^Different Nadis \(([^)]+) and ([^)]+)\) assure optimal genetic diversity, vitality, and progeny health\.", text)
    if m:
        n1 = TRANSLATIONS.get(m.group(1), m.group(1))
        n2 = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ವಿಭಿನ್ನ ನಾಡಿಗಳು ({n1} ಮತ್ತು {n2}) - ಉತ್ತಮ ವಂಶಾಭಿವೃದ್ಧಿ, ದೈಹಿಕ ಸಾಮರ್ಥ್ಯ ಮತ್ತು ಸಂತಾನ ಸೌಖ್ಯ."

    # Nadi Parihara 1: "Both share X Nadi (0/8 pts); Nadi Dosha is astrologically mitigated because Groom and Bride share the same Rasi (Rasi) with different Nakshatras (N1 & N2)."
    m = re.match(r"^Both share ([A-Za-z]+) Nadi \(0/8 pts\); Nadi Dosha is astrologically mitigated because Groom and Bride share the same Rasi \(([^)]+)\) with different Nakshatras \(([^&]+)\s*&\s*([^)]+)\)\.", text)
    if m:
        nadi = TRANSLATIONS.get(m.group(1), m.group(1))
        rasi = TRANSLATIONS.get(m.group(2), m.group(2))
        n1 = TRANSLATIONS.get(m.group(3).strip(), m.group(3).strip())
        n2 = TRANSLATIONS.get(m.group(4).strip(), m.group(4).strip())
        return f"ಇಬ್ಬರದ್ದೂ {nadi} ನಾಡಿ (೦/೮ ಅಂಕ); ಏಕ ರಾಶಿ ({rasi}) ಹಾಗೂ ಭಿನ್ನ ನಕ್ಷತ್ರಗಳಾಗಿರುವುದರಿಂದ ({n1} ಮತ್ತು {n2}) ನಾಡಿ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Nadi Parihara 2: "Both share X Nadi (0/8 pts); Nadi Dosha is astrologically mitigated because Nakshatra (N) spans different Rasis."
    m = re.match(r"^Both share ([A-Za-z]+) Nadi \(0/8 pts\); Nadi Dosha is astrologically mitigated because Nakshatra \(([^)]+)\) spans different Rasis\.", text)
    if m:
        nadi = TRANSLATIONS.get(m.group(1), m.group(1))
        nak = TRANSLATIONS.get(m.group(2), m.group(2))
        return f"ಇಬ್ಬರದ್ದೂ {nadi} ನಾಡಿ (೦/೮ ಅಂಕ); ನಕ್ಷತ್ರವು ({nak}) ಭಿನ್ನ ರಾಶಿಗಳಲ್ಲಿ ಹಂಚಿರುವುದರಿಂದ ನಾಡಿ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Nadi Parihara 3: "Both share X Nadi (0/8 pts); Nadi Dosha is astrologically mitigated due to different birth Padas (P1 & P2) within N."
    m = re.match(r"^Both share ([A-Za-z]+) Nadi \(0/8 pts\); Nadi Dosha is astrologically mitigated due to different birth Padas \((\d+)\s*&\s*(\d+)\) within ([^.]+)\.", text)
    if m:
        nadi = TRANSLATIONS.get(m.group(1), m.group(1))
        p1 = m.group(2)
        p2 = m.group(3)
        nak = TRANSLATIONS.get(m.group(4).strip(), m.group(4).strip())
        return f"ಇಬ್ಬರದ್ದೂ {nadi} ನಾಡಿ (೦/೮ ಅಂಕ); {nak} ನಕ್ಷತ್ರದ ಭಿನ್ನ ಪಾದಗಳಾಗಿರುವುದರಿಂದ ({p1} ಮತ್ತು {p2}) ನಾಡಿ ದೋಷ ಶಾಂತವಾಗಿದೆ."

    # Nadi Unmitigated: "Both share X Nadi (0/8 pts), causing Nadi Dosha which can impact physiological harmony and progeny health."
    m = re.match(r"^Both share ([A-Za-z]+) Nadi \(0/8 pts\), causing Nadi Dosha which can impact physiological harmony and progeny health\.", text)
    if m:
        nadi = TRANSLATIONS.get(m.group(1), m.group(1))
        return f"ಇಬ್ಬರದ್ದೂ {nadi} ನಾಡಿ (೦/೮ ಅಂಕ) - ಏಕ ನಾಡಿ ದೋಷವಿದ್ದು, ಸಂತಾನ ಮತ್ತು ಆರೋಗ್ಯದ ಮೇಲೆ ಪರಿಣಾಮ ಬೀರಬಹುದು."

    return None


def translate_string(text: str) -> str:
    # Localize "X min" remaining duration
    if text.endswith(" min"):
        num_part = text[:-4]
        return f"{num_part} ನಿಮಿಷ"

    if text in TRANSLATIONS:
        return TRANSLATIONS[text]

    dyn = translate_dynamic_description(text)
    if dyn is not None:
        return dyn

    words = text.split(" ")
    translated = []
    for word in words:
        translated.append(TRANSLATIONS.get(word, word))
    return " ".join(translated)



def localize_payload(payload: Any, lang: str) -> Any:
    if lang != "kan":
        return payload

    if isinstance(payload, dict):
        return {
            key: localize_payload(value, lang) for key, value in payload.items()
        }
    elif isinstance(payload, list):
        return [localize_payload(item, lang) for item in payload]
    elif isinstance(payload, str):
        return translate_string(payload)
    else:
        return payload
