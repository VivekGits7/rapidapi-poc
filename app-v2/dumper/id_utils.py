"""Sequential type-coded ID generator. See DUMP_PLAN §2.

Format:
    {ENTITY}_{TYPE_CODE}_{seq:NNN}    ← type-scoped tables
    {ENTITY}_{seq:NNN}                ← type-agnostic tables

Backed by Postgres SEQUENCEs declared in `database/rapid_api_query.sql`.
"""

from typing import Optional

from services.db import execute_scalar


# Per-table config: entity prefix, padding width, type-scoping, sequence base name.
# For type-scoped tables the actual sequence is `{seq_base}_{type_code.lower()}`
# (e.g. `seq_models_pc`, `seq_vehicles_moto`).
ENTITY_CONFIG: dict[str, dict] = {
    "languages":     {"entity": "LNG", "pad": 3, "type_scoped": False, "seq_base": "seq_languages"},
    "countries":     {"entity": "COU", "pad": 3, "type_scoped": False, "seq_base": "seq_countries"},
    "vehicle_types": {"entity": "VTY", "pad": 3, "type_scoped": False, "seq_base": "seq_vehicle_types"},
    "manufacturers": {"entity": "MFG", "pad": 5, "type_scoped": False, "seq_base": "seq_manufacturers"},
    "mvt":           {"entity": "MVT", "pad": 5, "type_scoped": True,  "seq_base": "seq_mvt"},
    "models":        {"entity": "MOD", "pad": 6, "type_scoped": True,  "seq_base": "seq_models"},
    "vehicles":      {"entity": "VEH", "pad": 7, "type_scoped": True,  "seq_base": "seq_vehicles"},
    "categories":    {"entity": "CAT", "pad": 4, "type_scoped": True,  "seq_base": "seq_categories"},
    "vca":           {"entity": "VCA", "pad": 8, "type_scoped": True,  "seq_base": "seq_vca"},
    "dump_jobs":     {"entity": "JOB", "pad": 3, "type_scoped": False, "seq_base": "seq_dump_jobs"},
}


def format_id(entity: str, type_code: Optional[str], seq: int, pad: int) -> str:
    parts = [entity]
    if type_code:
        parts.append(type_code)
    parts.append(str(seq).zfill(pad))
    return "_".join(parts)


async def _next_seq(sequence_name: str) -> int:
    """Pull the next value from a Postgres sequence. Atomic."""
    return await execute_scalar(f"SELECT nextval('{sequence_name}')")


async def new_id(table: str, type_code: Optional[str] = None) -> str:
    """Generate a fresh ID for the given table.

    For type-scoped tables, `type_code` is required (e.g. "PC", "CV", "MOTO").
    """
    cfg = ENTITY_CONFIG.get(table)
    if not cfg:
        raise ValueError(f"Unknown table for id_utils: {table!r}")

    if cfg["type_scoped"]:
        if not type_code:
            raise ValueError(f"{table} is type-scoped — type_code is required")
        seq_name = f"{cfg['seq_base']}_{type_code.lower()}"
    else:
        seq_name = cfg["seq_base"]

    seq_value = await _next_seq(seq_name)
    return format_id(
        entity=cfg["entity"],
        type_code=type_code if cfg["type_scoped"] else None,
        seq=seq_value,
        pad=cfg["pad"],
    )
