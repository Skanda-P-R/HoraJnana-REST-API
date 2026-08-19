"""Matchmaking (Ashtakoota Guna Milan) API routes."""

from __future__ import annotations

from typing import Any
from flask import Blueprint, jsonify, request

from hora_server.auth import require_session
from hora_server.extensions import cache, limiter
from hora_server.utils.errors import ApiError

from .common import service


blueprint = Blueprint("matchmaking", __name__)


def _parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    val_str = str(value).strip().lower()
    if val_str in ("true", "1", "yes"):
        return True
    if val_str in ("false", "0", "no"):
        return False
    return default


@blueprint.post("/matchmaking")
@require_session
@limiter.limit("60 per minute")
def post_matchmaking():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError(
            "Invalid JSON payload. Request body must be a JSON object.",
            code="invalid_payload",
            status_code=400,
        )

    srv = service()
    global_ayanamsa = data.get("ayanamsa") or data.get("ayanamsha")
    global_lang = data.get("lang", "en")
    include_manglik = _parse_bool(data.get("include_manglik", True))

    # Groom profile
    groom_data = data.get("groom") if isinstance(data.get("groom"), dict) else data
    groom_prefix = "" if isinstance(data.get("groom"), dict) else "groom"
    groom_context, groom_name = srv.parse_profile_context(
        groom_data,
        prefix=groom_prefix,
        default_ayanamsa=global_ayanamsa,
        default_lang=global_lang,
    )

    # Bride profile
    bride_data = data.get("bride") if isinstance(data.get("bride"), dict) else data
    bride_prefix = "" if isinstance(data.get("bride"), dict) else "bride"
    bride_context, bride_name = srv.parse_profile_context(
        bride_data,
        prefix=bride_prefix,
        default_ayanamsa=global_ayanamsa,
        default_lang=global_lang,
    )

    result = srv.matchmaking(
        groom_context=groom_context,
        groom_name=groom_name,
        bride_context=bride_context,
        bride_name=bride_name,
        include_manglik=include_manglik,
    )
    return jsonify(result)


@blueprint.get("/matchmaking")
@require_session
@limiter.limit("60 per minute")
@cache.cached(timeout=60, query_string=True)
def get_matchmaking():
    query = request.args
    srv = service()

    global_ayanamsa = query.get("ayanamsa") or query.get("ayanamsha")
    global_lang = query.get("lang", "en")
    include_manglik = _parse_bool(query.get("include_manglik", "true"))

    groom_context, groom_name = srv.parse_profile_context(
        query,
        prefix="groom",
        default_ayanamsa=global_ayanamsa,
        default_lang=global_lang,
    )

    bride_context, bride_name = srv.parse_profile_context(
        query,
        prefix="bride",
        default_ayanamsa=global_ayanamsa,
        default_lang=global_lang,
    )

    result = srv.matchmaking(
        groom_context=groom_context,
        groom_name=groom_name,
        bride_context=bride_context,
        bride_name=bride_name,
        include_manglik=include_manglik,
    )
    return jsonify(result)
