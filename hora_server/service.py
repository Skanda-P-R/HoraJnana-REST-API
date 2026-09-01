"""Application service composing astronomy, astrology, and API representations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from typing import Any, Mapping
from zoneinfo import ZoneInfo

from hora_server.astronomy import (
    Ayanamsa,
    EphemerisEngine,
    Positions,
    SolarCalculator,
    SolarDay,
)
from hora_server.astrology.constants import (
    NAKSHATRAS,
    VARA_NAMES,
    WEEKDAY_NAMES,
    YOGAS,
)
from hora_server.astrology.hora import (
    PlanetaryHour,
    current_planetary_hour,
    planetary_hours,
    remaining_seconds,
)
from hora_server.astrology.kundali import (
    CharaKarakaDetails,
    Kundali,
    KundaliHouse,
    KundaliLagna,
    KundaliPlanet,
    YogiAvayogi,
    YogiPointDetails,
    calculate_kundali,
)
from hora_server.astrology.matchmaking import (
    MatchMakingResult,
    calculate_match_making,
)
from hora_server.astrology.muhurta import MuhurtaInterval, calculate_muhurta
from hora_server.astrology.dasha import calculate_dasha
from hora_server.astrology.pancha_pakshi import (
    PanchaPakshiResult,
    calculate_pancha_pakshi,
)
from hora_server.astrology.panchanga import (
    Limb,
    Panchanga,
    calculate_panchanga,
    find_next_transition,
    karana_name,
    phase_index,
    tithi_name,
)
from hora_server.utils.datetime import (
    duration_seconds,
    interval_text,
    isoformat,
    parse_iso_datetime,
    remaining_text,
    time_text,
)
from hora_server.registry import LocationRegistry
from hora_server.utils.errors import ApiError
from hora_server.utils.timezone import TimezoneResolver
from hora_server.utils.translation import localize_payload


@dataclass(frozen=True)
class RequestContext:
    latitude: float
    longitude: float
    timezone: ZoneInfo
    instant: datetime
    ayanamsa: Ayanamsa
    lang: str = "en"


class PanchangaService:
    def __init__(
        self,
        engine: EphemerisEngine,
        solar: SolarCalculator,
        timezone_resolver: TimezoneResolver,
        default_ayanamsa: str = "lahiri",
        registry: LocationRegistry | None = None,
        default_latitude: float = 12.9716,
        default_longitude: float = 77.5946,
    ) -> None:
        self.engine = engine
        self.solar = solar
        self.timezone_resolver = timezone_resolver
        self.default_ayanamsa = default_ayanamsa
        self.registry = registry
        self.default_latitude = default_latitude
        self.default_longitude = default_longitude

    @staticmethod
    def _number_or_default(
        query: Mapping[str, str],
        name: str,
        minimum: float,
        maximum: float,
        default: float,
    ) -> float:
        raw = query.get(name)
        if raw is None or not raw.strip() or raw.strip().lower() in {"null", "undefined"}:
            return default
        try:
            value = float(raw)
        except ValueError as exc:
            raise ApiError(
                f"{name} must be a number",
                code="invalid_parameter",
                details={"parameter": name, "value": raw},
            ) from exc
        if not math.isfinite(value) or not minimum <= value <= maximum:
            raise ApiError(
                f"{name} must be between {minimum:g} and {maximum:g}",
                code="invalid_parameter",
                details={"parameter": name, "value": raw},
            )
        return value

    def request_context(self, query: Mapping[str, str]) -> RequestContext:
        location_resolved = False
        latitude = None
        longitude = None
        timezone_str = None

        location_name = query.get("location")
        if location_name:
            if self.registry:
                resolved_data = self.registry.resolve(location_name)
                if resolved_data:
                    latitude = resolved_data["latitude"]
                    longitude = resolved_data["longitude"]
                    timezone_str = resolved_data["timezone"]
                    location_resolved = True
                else:
                    raise ApiError(
                        f"Location '{location_name}' not found in registry",
                        code="location_not_found",
                        status_code=404,
                        details={"location": location_name},
                    )
            else:
                raise ApiError(
                    "Location registry is not configured",
                    code="registry_not_configured",
                    status_code=500,
                )

        if not location_resolved:
            latitude = round(
                self._number_or_default(query, "lat", -90, 90, self.default_latitude), 4
            )
            longitude = round(
                self._number_or_default(query, "lon", -180, 180, self.default_longitude), 4
            )
            timezone_str = query.get("timezone")

        timezone = self.timezone_resolver.resolve(
            latitude, longitude, timezone_str
        )
        
        datetime_val = query.get("datetime")
        if not datetime_val:
            date_param = query.get("date")
            time_param = query.get("time")
            if date_param and time_param:
                datetime_val = f"{date_param.strip()}T{time_param.strip()}"
            else:
                datetime_val = date_param

        instant = parse_iso_datetime(datetime_val, timezone)
        if not 1800 <= instant.year <= 2399:
            if "datetime" in query:
                parameter_name = "datetime"
            elif "date" in query and "time" in query:
                parameter_name = "date/time"
            elif "date" in query:
                parameter_name = "date"
            else:
                parameter_name = "datetime"
            raise ApiError(
                f"{parameter_name} must fall within the supported range 1800-2399",
                code="datetime_out_of_range",
                status_code=422,
                details={
                    "parameter": parameter_name,
                    "date": instant.date().isoformat(),
                },
            )
        requested_ayanamsa = query.get("ayanamsa") or query.get("ayanamsha")
        ayanamsa = self.engine.resolve_ayanamsa(
            requested_ayanamsa, self.default_ayanamsa
        )
        lang = (query.get("lang") or "en").strip().lower()
        if lang not in ("en", "kan"):
            lang = "en"
        return RequestContext(latitude, longitude, timezone, instant, ayanamsa, lang)

    def parse_profile_context(
        self,
        data: Mapping[str, Any],
        prefix: str = "",
        default_ayanamsa: str | None = None,
        default_lang: str = "en",
    ) -> tuple[RequestContext, str]:
        p = f"{prefix}_" if prefix and not prefix.endswith("_") else prefix
        name = str(
            data.get(f"{p}name")
            or (data.get("name") if not p else None)
            or ("Groom" if "groom" in p.lower() else "Bride")
        ).strip()

        location_resolved = False
        latitude = None
        longitude = None
        timezone_str = None

        location_name = (
            data.get(f"{p}pob")
            or data.get(f"{p}location")
            or (data.get("pob") if not p else None)
            or (data.get("location") if not p else None)
        )
        if location_name and str(location_name).strip():
            location_name = str(location_name).strip()
            if self.registry:
                resolved_data = self.registry.resolve(location_name)
                if resolved_data:
                    latitude = resolved_data["latitude"]
                    longitude = resolved_data["longitude"]
                    timezone_str = resolved_data["timezone"]
                    location_resolved = True
                else:
                    raise ApiError(
                        f"Location '{location_name}' for {prefix or 'profile'} not found in registry",
                        code="location_not_found",
                        status_code=404,
                        details={"location": location_name, "profile": prefix or "profile"},
                    )
            else:
                raise ApiError(
                    "Location registry is not configured",
                    code="registry_not_configured",
                    status_code=500,
                )

        if not location_resolved:
            lat_val = data.get(f"{p}lat") or (data.get("lat") if not p else None)
            lon_val = data.get(f"{p}lon") or (data.get("lon") if not p else None)

            lat_query = {f"{p}lat": str(lat_val)} if lat_val is not None else {}
            lon_query = {f"{p}lon": str(lon_val)} if lon_val is not None else {}

            latitude = round(
                self._number_or_default(lat_query, f"{p}lat", -90, 90, self.default_latitude), 4
            )
            longitude = round(
                self._number_or_default(lon_query, f"{p}lon", -180, 180, self.default_longitude), 4
            )
            tz_val = (
                data.get(f"{p}timezone")
                or data.get(f"{p}tz")
                or (data.get("timezone") if not p else None)
                or (data.get("tz") if not p else None)
            )
            if tz_val:
                timezone_str = str(tz_val).strip()

        timezone = self.timezone_resolver.resolve(latitude, longitude, timezone_str)

        # Datetime resolving
        dt_val = data.get(f"{p}datetime") or (data.get("datetime") if not p else None)
        if not dt_val:
            dob = (
                data.get(f"{p}dob")
                or data.get(f"{p}date")
                or (data.get("dob") if not p else None)
                or (data.get("date") if not p else None)
            )
            tob = (
                data.get(f"{p}tob")
                or data.get(f"{p}time")
                or (data.get("tob") if not p else None)
                or (data.get("time") if not p else None)
            )
            if dob:
                dob_str = str(dob).strip()
                tob_str = str(tob).strip() if tob else "12:00:00"
                dt_val = f"{dob_str}T{tob_str}"

        if not dt_val:
            profile_label = prefix.capitalize() if prefix else "Profile"
            raise ApiError(
                f"Missing birth date (dob) for {profile_label}",
                code="invalid_parameter",
                status_code=400,
                details={"profile": prefix or "profile"},
            )

        instant = parse_iso_datetime(str(dt_val), timezone)
        if not 1800 <= instant.year <= 2399:
            profile_label = prefix.capitalize() if prefix else "Profile"
            raise ApiError(
                f"{profile_label} birth datetime must fall within the supported range 1800-2399",
                code="datetime_out_of_range",
                status_code=422,
                details={"profile": prefix or "profile", "date": instant.date().isoformat()},
            )

        req_ayanamsa = (
            data.get(f"{p}ayanamsa")
            or data.get("ayanamsa")
            or data.get("ayanamsha")
            or default_ayanamsa
        )
        ayanamsa = self.engine.resolve_ayanamsa(req_ayanamsa, self.default_ayanamsa)
        lang = str(data.get("lang") or default_lang).strip().lower()
        if lang not in ("en", "kan"):
            lang = "en"

        return RequestContext(latitude, longitude, timezone, instant, ayanamsa, lang), name


    def solar_day(self, context: RequestContext) -> SolarDay:
        return self.solar.containing_vedic_day(
            context.instant,
            context.latitude,
            context.longitude,
            context.timezone,
        )

    @staticmethod
    def _base(context: RequestContext, solar_day: SolarDay) -> dict[str, Any]:
        return {
            "date": solar_day.date.isoformat(),
            "local_date": context.instant.date().isoformat(),
            "vedic_day_date": solar_day.date.isoformat(),
            "datetime": isoformat(context.instant),
            "timezone": context.timezone.key,
            "location": f"{context.latitude:.6f},{context.longitude:.6f}",
            "coordinates": {
                "latitude": context.latitude,
                "longitude": context.longitude,
            },
            "ayanamsa": context.ayanamsa.display_name,
        }

    @staticmethod
    def _solar_payload(solar_day: SolarDay) -> dict[str, Any]:
        return {
            "sunrise": time_text(solar_day.sunrise),
            "sunset": time_text(solar_day.sunset),
            "sunrise_at": isoformat(solar_day.sunrise),
            "sunset_at": isoformat(solar_day.sunset),
            "next_sunrise_at": isoformat(solar_day.next_sunrise),
            "solar_noon_at": isoformat(solar_day.solar_noon),
            "daylight_midpoint_at": isoformat(solar_day.daylight_midpoint),
            "day_duration_seconds": round(solar_day.day_duration_seconds, 3),
            "night_duration_seconds": round(solar_day.night_duration_seconds, 3),
            "day_hora_seconds": round(solar_day.day_duration_seconds / 12, 3),
            "night_hora_seconds": round(solar_day.night_duration_seconds / 12, 3),
        }

    @staticmethod
    def _limb_payload(limb: Limb) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": limb.name,
            "number": limb.number,
            "progress": round(limb.progress, 8),
            "longitude_degrees": round(limb.longitude, 8),
            "ends_at": isoformat(limb.ends_at) if limb.ends_at else None,
        }
        if limb.extra:
            payload.update(limb.extra)
        return payload

    def _panchanga_payload(self, panchanga: Panchanga) -> dict[str, Any]:
        return {
            "panchanga": {
                "tithi": panchanga.tithi.name,
                "nakshatra": panchanga.nakshatra.name,
                "yoga": panchanga.yoga.name,
                "karana": panchanga.karana.name,
                "vara": panchanga.vara,
                "vara_sanskrit": panchanga.vara_sanskrit,
                "samvatsara": panchanga.samvatsara,
                "ayana": panchanga.ayana,
                "rutu": panchanga.rutu,
                "masa": panchanga.masa,
                "paksha": panchanga.paksha,
            },
            "panchanga_details": {
                "tithi": self._limb_payload(panchanga.tithi),
                "nakshatra": self._limb_payload(panchanga.nakshatra),
                "yoga": self._limb_payload(panchanga.yoga),
                "karana": self._limb_payload(panchanga.karana),
            },
            "moon": {
                "rasi": panchanga.moon_rasi,
                "nakshatra": panchanga.nakshatra.name,
                "pada": panchanga.moon_pada,
                "sidereal_longitude": round(
                    panchanga.positions.moon_sidereal, 8
                ),
            },
            "sun": {
                "rasi": panchanga.sun_rasi,
                "sidereal_longitude": round(panchanga.positions.sun_sidereal, 8),
            },
        }

    @staticmethod
    def _hour_payload(
        instant: datetime, hour: PlanetaryHour, next_planet: str
    ) -> dict[str, Any]:
        seconds = remaining_seconds(instant, hour)
        return {
            "planet": hour.planet,
            "symbol": hour.symbol,
            "number": hour.number,
            "period": hour.period,
            "period_number": hour.period_number,
            "started": time_text(hour.start),
            "ends": time_text(hour.end),
            "started_at": isoformat(hour.start),
            "ends_at": isoformat(hour.end),
            "remaining": remaining_text(seconds),
            "remaining_seconds": seconds,
            "next": next_planet,
        }

    @staticmethod
    def _hora_schedule_item(hour: PlanetaryHour) -> dict[str, Any]:
        return {
            "planet": hour.planet,
            "symbol": hour.symbol,
            "number": hour.period_number,
            "starts": time_text(hour.start),
            "ends": time_text(hour.end),
            "starts_at": isoformat(hour.start),
            "ends_at": isoformat(hour.end),
        }


    @staticmethod
    def _planetary_hour_item(
        hour: PlanetaryHour, instant: datetime
    ) -> dict[str, Any]:
        instant_utc = instant.astimezone(UTC)
        return {
            "number": hour.number,
            "period": hour.period,
            "period_number": hour.period_number,
            "planet": hour.planet,
            "symbol": hour.symbol,
            "start": isoformat(hour.start),
            "end": isoformat(hour.end),
            "display": interval_text(hour.start, hour.end),
            "is_current": (
                hour.start.astimezone(UTC)
                <= instant_utc
                < hour.end.astimezone(UTC)
            ),
        }

    @staticmethod
    def _interval_payload(interval: MuhurtaInterval) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": interval.name,
            "start": isoformat(interval.start),
            "end": isoformat(interval.end),
            "display": interval_text(interval.start, interval.end),
            "duration_seconds": round(
                duration_seconds(interval.start, interval.end), 3
            ),
        }
        if interval.segment is not None:
            payload["day_eighth"] = interval.segment
        if interval.traditionally_auspicious is not None:
            payload["traditionally_auspicious"] = interval.traditionally_auspicious
        if interval.note:
            payload["note"] = interval.note
        return payload

    def _meta(self, positions: Positions) -> dict[str, Any]:
        return {
            "engine": "Swiss Ephemeris",
            "engine_version": self.engine.version,
            "ephemeris_backend": positions.ephemeris,
            "julian_day_ut": round(positions.julian_day_ut, 8),
            "ayanamsa_degrees": round(positions.ayanamsa_degrees, 8),
            "longitude_model": "geocentric apparent ecliptic",
            "solar_event_convention": (
                "Hindu rising: geocentric solar-disc center at geometric horizon, no refraction"
            ),
            "solar_event_swiss_flag": "BIT_HINDU_RISING",
            "vedic_day_convention": "sunrise to next sunrise",
            "transition_tolerance_seconds": 1,
        }

    @staticmethod
    def _kundali_lagna_payload(lagna: KundaliLagna) -> dict[str, Any]:
        return {
            "rasi": lagna.rasi,
            "number": lagna.number,
            "longitude": round(lagna.longitude, 4),
            "degree_in_rasi": round(lagna.degree_in_rasi, 4),
        }

    @staticmethod
    def _kundali_house_payload(house: KundaliHouse) -> dict[str, Any]:
        return {
            "house": house.house,
            "rasi": house.rasi,
            "planets": list(house.planets),
        }

    @staticmethod
    def _kundali_planet_payload(planet: KundaliPlanet) -> dict[str, Any]:
        return {
            "planet": planet.planet,
            "symbol": planet.symbol,
            "longitude": round(planet.longitude, 4),
            "degree_in_rasi": round(planet.degree_in_rasi, 4),
            "rasi": planet.rasi,
            "house": planet.house,
            "retrograde": planet.retrograde,
        }

    @staticmethod
    def _yogi_point_payload(point: YogiPointDetails) -> dict[str, Any]:
        return {
            "longitude": round(point.longitude, 4),
            "degree_in_rasi": round(point.degree_in_rasi, 4),
            "rasi": point.rasi,
            "rasi_number": point.rasi_number,
            "rasi_lord": point.rasi_lord,
            "nakshatra": point.nakshatra,
            "nakshatra_number": point.nakshatra_number,
            "nakshatra_lord": point.nakshatra_lord,
            "pada": point.pada,
            "house": point.house,
        }

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

    def _yogi_avayogi_payload(self, yogi: YogiAvayogi) -> dict[str, Any]:
        return {
            "yogi_planet": yogi.yogi_planet,
            "duplicate_yogi": yogi.duplicate_yogi,
            "avayogi_planet": yogi.avayogi_planet,
            "duplicate_avayogi": yogi.duplicate_avayogi,
            "yogi_point": self._yogi_point_payload(yogi.yogi_point),
            "avayogi_point": self._yogi_point_payload(yogi.avayogi_point),
        }

    def _panchanga(
        self,
        context: RequestContext,
        solar_day: SolarDay,
        include_transitions: bool,
    ) -> Panchanga:
        return calculate_panchanga(
            context.instant,
            solar_day.date.weekday(),
            self.engine,
            context.ayanamsa,
            include_transitions=include_transitions,
            day_start=solar_day.sunrise,
            day_end=solar_day.next_sunrise,
        )

    def kundali_model(self, context: RequestContext) -> Kundali:
        return calculate_kundali(
            context.instant,
            context.latitude,
            context.longitude,
            self.engine,
            context.ayanamsa,
        )

    @staticmethod
    def _pancha_pakshi_payload(result: PanchaPakshiResult) -> dict[str, Any]:
        return {
            "bird": result.bird,
            "element": result.element,
            "nakshatra": result.nakshatra,
            "nakshatra_number": result.nakshatra_number,
            "paksha": result.paksha,
        }

    def kundali(self, context: RequestContext) -> dict[str, Any]:
        kundali = self.kundali_model(context)
        solar_day = self.solar_day(context)
        panchanga = self._panchanga(context, solar_day, include_transitions=True)
        panchanga_payload = self._panchanga_payload(panchanga)

        pancha_pakshi = calculate_pancha_pakshi(
            nakshatra_number=panchanga.nakshatra.number,
            nakshatra_name=panchanga.nakshatra.name,
            paksha=panchanga.paksha,
        )

        payload: dict[str, Any] = {
            "date": context.instant.date().isoformat(),
            "datetime": isoformat(context.instant),
            "timezone": context.timezone.key,
            "lagna": self._kundali_lagna_payload(kundali.lagna),
            "houses": [
                self._kundali_house_payload(house) for house in kundali.houses
            ],
            "planets": [
                self._kundali_planet_payload(planet)
                for planet in kundali.planets
            ],
            "ayanamsa": context.ayanamsa.display_name,
            "panchanga": panchanga_payload["panchanga"],
            "panchanga_details": panchanga_payload["panchanga_details"],
            "pancha_pakshi": self._pancha_pakshi_payload(pancha_pakshi),
        }
        if kundali.yogi_avayogi is not None:
            payload["yogi_avayogi"] = self._yogi_avayogi_payload(
                kundali.yogi_avayogi
            )
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
        return localize_payload(payload, context.lang)


    def _dasha_period_payload(self, period: Any) -> dict[str, Any]:
        return {
            "level": period.level,
            "lord": period.lord,
            "start": isoformat(period.start),
            "end": isoformat(period.end),
            "duration_years": period.duration_years,
            "sub_periods": [
                self._dasha_period_payload(sub) for sub in period.sub_periods
            ],
        }

    def _dasha_moon_payload(self, moon: Any) -> dict[str, Any]:
        return {
            "longitude": round(moon.longitude, 4),
            "degree_in_rasi": round(moon.degree_in_rasi, 4),
            "rasi": moon.rasi,
            "rasi_number": moon.rasi_number,
            "nakshatra": moon.nakshatra,
            "nakshatra_number": moon.nakshatra_number,
            "nakshatra_lord": moon.nakshatra_lord,
            "nakshatra_pada": moon.nakshatra_pada,
        }

    def _dasha_balance_payload(self, balance: Any) -> dict[str, Any]:
        return {
            "lord": balance.lord,
            "total_years": balance.total_years,
            "elapsed_years": balance.elapsed_years,
            "remaining_years": balance.remaining_years,
            "elapsed_fraction": balance.elapsed_fraction,
            "remaining_fraction": balance.remaining_fraction,
        }

    def _dasha_active_payload(self, active: Any) -> dict[str, Any]:
        payload = {
            "mahadasha": active.mahadasha,
            "antardasha": active.antardasha,
        }
        if active.pratyantardasha is not None:
            payload["pratyantardasha"] = active.pratyantardasha
        return payload

    def dasha(
        self,
        context: RequestContext,
        depth: int = 2,
        year_type: str = "365.25",
        active_at: datetime | None = None,
    ) -> dict[str, Any]:
        try:
            year_days = float(year_type)
        except ValueError:
            year_days = 365.25

        if year_days not in (365.25, 360.0):
            year_days = 365.25

        pos = self.engine.positions(context.instant, context.ayanamsa)
        moon_longitude = pos.moon_sidereal

        moon_details, balance, timeline, active = calculate_dasha(
            moon_longitude,
            context.instant,
            year_days=year_days,
            depth=depth,
            active_at=active_at,
        )

        payload = {
            "date": context.instant.date().isoformat(),
            "datetime": isoformat(context.instant),
            "timezone": context.timezone.key,
            "ayanamsa": context.ayanamsa.display_name,
            "year_type": str(year_days),
            "moon": self._dasha_moon_payload(moon_details),
            "dasha_balance": self._dasha_balance_payload(balance),
            "active_dasha": self._dasha_active_payload(active),
            "timeline": [
                self._dasha_period_payload(period) for period in timeline
            ],
        }

        return localize_payload(payload, context.lang)

    def all(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        panchanga = self._panchanga(context, solar_day, include_transitions=True)
        hours = planetary_hours(solar_day)
        intervals = calculate_muhurta(solar_day)
        current, next_planet = current_planetary_hour(context.instant, hours)
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["hora"] = self._hour_payload(
            context.instant, current, next_planet
        )
        payload.update(self._panchanga_payload(panchanga))
        payload.update(
            {
                key: interval_text(value.start, value.end)
                for key, value in intervals.items()
            }
        )
        payload["muhurta"] = {
            key: self._interval_payload(value) for key, value in intervals.items()
        }
        payload["meta"] = self._meta(panchanga.positions)
        return localize_payload(payload, context.lang)

    def hora(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        hours = planetary_hours(solar_day)
        positions = self.engine.positions(context.instant, context.ayanamsa)
        current, next_planet = current_planetary_hour(context.instant, hours)
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["hora"] = self._hour_payload(
            context.instant, current, next_planet
        )
        payload["day_hora"] = [
            self._hora_schedule_item(hour) for hour in hours[:12]
        ]
        payload["night_hora"] = [
            self._hora_schedule_item(hour) for hour in hours[12:]
        ]
        payload["meta"] = self._meta(positions)
        return localize_payload(payload, context.lang)

    def planetary_hours(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        hours = planetary_hours(solar_day)
        positions = self.engine.positions(context.instant, context.ayanamsa)
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["planetary_hours"] = [
            self._planetary_hour_item(hour, context.instant) for hour in hours
        ]
        payload["meta"] = self._meta(positions)
        return localize_payload(payload, context.lang)

    def panchanga(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        panchanga = self._panchanga(context, solar_day, include_transitions=True)
        payload = self._base(context, solar_day)
        payload.update(self._panchanga_payload(panchanga))
        payload["meta"] = self._meta(panchanga.positions)
        return localize_payload(payload, context.lang)

    def day(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        positions = self.engine.positions(context.instant, context.ayanamsa)
        weekday = solar_day.date.weekday()
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload.update(
            {
                "vara": WEEKDAY_NAMES[weekday],
                "vara_sanskrit": VARA_NAMES[weekday],
                "meta": self._meta(positions),
            }
        )
        return localize_payload(payload, context.lang)

    def muhurta(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        intervals = calculate_muhurta(solar_day)
        positions = self.engine.positions(context.instant, context.ayanamsa)
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["muhurta"] = {
            key: self._interval_payload(value) for key, value in intervals.items()
        }
        payload["meta"] = self._meta(positions)
        return localize_payload(payload, context.lang)

    def rahu(self, context: RequestContext) -> dict[str, Any]:
        solar_day = self.solar_day(context)
        intervals = calculate_muhurta(solar_day)
        positions = self.engine.positions(context.instant, context.ayanamsa)
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["rahu_kalam"] = interval_text(
            intervals["rahu_kalam"].start, intervals["rahu_kalam"].end
        )
        payload["rahu_kalam_details"] = self._interval_payload(
            intervals["rahu_kalam"]
        )
        payload["related_intervals"] = {
            key: self._interval_payload(intervals[key])
            for key in ("gulika", "yamaganda")
        }
        payload["meta"] = self._meta(positions)
        return localize_payload(payload, context.lang)

    @staticmethod
    def _limb_name(kind: str, index: int) -> str:
        if kind == "tithi":
            return tithi_name(index)[0]
        if kind == "karana":
            return karana_name(index)
        if kind == "nakshatra":
            return NAKSHATRAS[index]
        if kind == "yoga":
            return YOGAS[index]
        raise ValueError(kind)

    def calendar(self, context: RequestContext) -> dict[str, Any]:
        local_date = context.instant.date()
        solar_day = self.solar.for_date(
            local_date,
            context.latitude,
            context.longitude,
            context.timezone,
        )
        day_start = datetime.combine(local_date, time.min, context.timezone)
        day_end = datetime.combine(
            local_date + timedelta(days=1), time.min, context.timezone
        )
        events: list[dict[str, Any]] = [
            {"type": "sunrise", "at": isoformat(solar_day.sunrise)},
            {"type": "sunset", "at": isoformat(solar_day.sunset)},
        ]

        for kind in ("tithi", "nakshatra", "yoga", "karana"):
            cursor = day_start
            for _ in range(4):
                current_index = phase_index(
                    self.engine.positions(cursor, context.ayanamsa), kind
                )
                transition = find_next_transition(
                    cursor, kind, self.engine, context.ayanamsa
                )
                if transition >= day_end:
                    break
                after = transition.astimezone(UTC) + timedelta(seconds=2)
                next_index = phase_index(
                    self.engine.positions(after, context.ayanamsa), kind
                )
                events.append(
                    {
                        "type": f"{kind}_transition",
                        "at": isoformat(transition),
                        "from": self._limb_name(kind, current_index),
                        "to": self._limb_name(kind, next_index),
                    }
                )
                cursor = after.astimezone(context.timezone)

        snapshot = calculate_panchanga(
            solar_day.sunrise,
            solar_day.date.weekday(),
            self.engine,
            context.ayanamsa,
            include_transitions=False,
        )
        events.sort(key=lambda item: datetime.fromisoformat(item["at"]))
        payload = self._base(context, solar_day)
        payload.update(self._solar_payload(solar_day))
        payload["panchanga_at_sunrise"] = self._panchanga_payload(snapshot)[
            "panchanga"
        ]
        payload["events"] = events
        payload["meta"] = self._meta(snapshot.positions)
        return localize_payload(payload, context.lang)

    def matchmaking(
        self,
        groom_context: RequestContext,
        groom_name: str,
        bride_context: RequestContext,
        bride_name: str,
        include_manglik: bool = True,
    ) -> dict[str, Any]:
        groom_kundali = calculate_kundali(
            groom_context.instant,
            groom_context.latitude,
            groom_context.longitude,
            self.engine,
            groom_context.ayanamsa,
        )
        bride_kundali = calculate_kundali(
            bride_context.instant,
            bride_context.latitude,
            bride_context.longitude,
            self.engine,
            bride_context.ayanamsa,
        )

        groom_loc = f"{groom_context.latitude:.4f}, {groom_context.longitude:.4f}"
        bride_loc = f"{bride_context.latitude:.4f}, {bride_context.longitude:.4f}"

        res = calculate_match_making(
            groom_kundali=groom_kundali,
            bride_kundali=bride_kundali,
            groom_name=groom_name,
            bride_name=bride_name,
            groom_datetime_str=isoformat(groom_context.instant),
            bride_datetime_str=isoformat(bride_context.instant),
            groom_location_str=groom_loc,
            bride_location_str=bride_loc,
            include_manglik=include_manglik,
        )

        from hora_server.astrology.constants import DASHA_LORDS
        g_nak_idx = res.groom_info.nakshatra_number - 1
        b_nak_idx = res.bride_info.nakshatra_number - 1
        g_nak_lord = DASHA_LORDS[g_nak_idx % 9]
        b_nak_lord = DASHA_LORDS[b_nak_idx % 9]

        payload: dict[str, Any] = {
            "ayanamsa": groom_context.ayanamsa.display_name,
            "groom_info": {
                "name": res.groom_info.name,
                "datetime": res.groom_info.datetime,
                "location": res.groom_info.location,
                "moon_rasi": res.groom_info.moon_rasi,
                "moon_rasi_lord": res.groom_info.moon_rasi_lord,
                "nakshatra": res.groom_info.nakshatra,
                "nakshatra_number": res.groom_info.nakshatra_number,
                "nakshatra_lord": g_nak_lord,
                "pada": res.groom_info.pada,
                "varna": res.groom_info.varna,
                "vashya": res.groom_info.vashya,
                "yoni": res.groom_info.yoni,
                "gana": res.groom_info.gana,
                "nadi": res.groom_info.nadi,
            },
            "bride_info": {
                "name": res.bride_info.name,
                "datetime": res.bride_info.datetime,
                "location": res.bride_info.location,
                "moon_rasi": res.bride_info.moon_rasi,
                "moon_rasi_lord": res.bride_info.moon_rasi_lord,
                "nakshatra": res.bride_info.nakshatra,
                "nakshatra_number": res.bride_info.nakshatra_number,
                "nakshatra_lord": b_nak_lord,
                "pada": res.bride_info.pada,
                "varna": res.bride_info.varna,
                "vashya": res.bride_info.vashya,
                "yoni": res.bride_info.yoni,
                "gana": res.bride_info.gana,
                "nadi": res.bride_info.nadi,
            },
            "guna_milan": {
                "total_points": res.total_points,
                "max_points": res.max_points,
                "percentage": res.percentage,
                "result": res.result,
                "is_recommended": res.is_recommended,
                "summary_message": res.summary_message,
            },
            "kootas": {
                k_name: {
                    "name": k.name,
                    "obtained_points": k.obtained_points,
                    "max_points": k.max_points,
                    "groom_attribute": k.groom_attribute,
                    "bride_attribute": k.bride_attribute,
                    "is_favorable": k.is_favorable,
                    "dosha": k.dosha,
                    "parihara_applied": k.parihara_applied,
                    "description": k.description,
                }
                for k_name, k in res.kootas.items()
            },
            "doshas_summary": res.doshas_summary,
        }

        if res.manglik_analysis is not None:
            payload["manglik_analysis"] = {
                "groom_manglik": {
                    "is_manglik": res.manglik_analysis.groom_manglik.is_manglik,
                    "status": res.manglik_analysis.groom_manglik.status,
                    "mars_house_lagna": res.manglik_analysis.groom_manglik.mars_house_lagna,
                    "mars_house_moon": res.manglik_analysis.groom_manglik.mars_house_moon,
                },
                "bride_manglik": {
                    "is_manglik": res.manglik_analysis.bride_manglik.is_manglik,
                    "status": res.manglik_analysis.bride_manglik.status,
                    "mars_house_lagna": res.manglik_analysis.bride_manglik.mars_house_lagna,
                    "mars_house_moon": res.manglik_analysis.bride_manglik.mars_house_moon,
                },
                "manglik_compatibility": res.manglik_analysis.manglik_compatibility,
                "description": res.manglik_analysis.description,
            }

        return localize_payload(payload, groom_context.lang)

