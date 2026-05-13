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
    ENGINE_VARIANTS = "engine_variants"
    CATEGORIES = "categories"
    ARTICLES = "articles"
    ARTICLE_DETAILS = "article_details"
    ARTICLE_MEDIA = "article_media"
    OEM_BATCH = "oem_batch"
    FITMENT = "fitment"
    CROSS_REFS = "cross_refs"
    SEARCH = "search"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
