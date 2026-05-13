"""Enums + type-id↔type-code mappings used across the dumper."""

from enum import Enum


class DumpStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class DumpPhase(str, Enum):
    IDLE = "idle"
    REFERENCE = "reference"
    MANUFACTURERS = "manufacturers"
    MODELS = "models"
    VEHICLES = "vehicles"
    CATEGORIES = "categories"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class CursorKey(str, Enum):
    MODELS = "models"
    VEHICLES = "vehicles"
    CATEGORIES = "categories"


class VehicleTypeCode(str, Enum):
    """Our short code for each RapidAPI vehicle type id."""

    PC = "PC"
    CV = "CV"
    MOTO = "MOTO"
    LCV = "LCV"
    DCAB = "DCAB"
    AXLE = "AXLE"
    ENG = "ENG"
    BUS = "BUS"
    AFT = "AFT"
    TRAC = "TRAC"
    VOEM = "VOEM"


# Map the API's numeric `type id` (1..11) to our short code.
# This is the only place this mapping lives — everything else looks it up here.
TYPE_ID_TO_CODE: dict[int, str] = {
    1: VehicleTypeCode.PC.value,
    2: VehicleTypeCode.CV.value,
    3: VehicleTypeCode.MOTO.value,
    4: VehicleTypeCode.LCV.value,
    5: VehicleTypeCode.DCAB.value,
    6: VehicleTypeCode.AXLE.value,
    7: VehicleTypeCode.ENG.value,
    8: VehicleTypeCode.BUS.value,
    9: VehicleTypeCode.AFT.value,
    10: VehicleTypeCode.TRAC.value,
    11: VehicleTypeCode.VOEM.value,
}

CODE_TO_TYPE_ID: dict[str, int] = {v: k for k, v in TYPE_ID_TO_CODE.items()}


# API-name as returned by `GET /types/list-vehicles-type` → our short code.
# Useful when we receive the API's `vehicleType` string and want our code.
API_NAME_TO_CODE: dict[str, str] = {
    "PC": "PC",
    "CV": "CV",
    "Motorcycle": "MOTO",
    "LCV": "LCV",
    "DriverCab": "DCAB",
    "Axle": "AXLE",
    "Engine": "ENG",
    "Bus": "BUS",
    "Aftermarket": "AFT",
    "Tractor": "TRAC",
    "Virtual OEM": "VOEM",
}
