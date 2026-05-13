"""Feature-specific request/response schemas and enums for the RapidAPI POC.

Models mirror the Auto Parts Catalog API's JSON shapes so responses can be
passed through without lossy transformation.
"""

from enum import Enum
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, ConfigDict, Field


# ==================== ENUMS ====================

class ArticleSearchType(str, Enum):
    ARTICLE_NUMBER = "ArticleNumber"
    OE_NUMBER = "OENumber"
    EAN = "EAN"
    IAM_NUMBER = "IAMNumber"


# ==================== LANGUAGES (API #1) ====================

class LanguageItem(BaseModel):
    lngId: str = Field(..., description="Numeric language ID (as string)", examples=["4"])
    lngIso2: Optional[str] = Field(None, description="ISO 639-1 two-letter code", examples=["en"])
    lngDescription: str = Field(..., description="Native language name", examples=["English (GB)"])


class LanguagesResponse(BaseModel):
    success: bool = Field(default=True, description="Whether the request succeeded")
    message: str = Field(..., description="Status message")
    data: List[LanguageItem] = Field(..., description="List of supported catalog languages")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Fetched 42 languages",
                "data": [
                    {"lngId": "4", "lngIso2": "en", "lngDescription": "English (GB)"},
                    {"lngId": "42", "lngIso2": "ar", "lngDescription": "عربي"},
                    {"lngId": "37", "lngIso2": "qa", "lngDescription": "English (USA)"},
                ],
            }
        }
    )


# ==================== COUNTRIES (API #2) ====================

class CountryItem(BaseModel):
    id: int = Field(..., description="Numeric country ID (use in country_id params)", examples=[63])
    couCode: str = Field(..., description="Catalog country code (not always ISO 3166)", examples=["D"])
    countryName: str = Field(..., description="Country or region name (English)", examples=["Germany"])


class CountriesData(BaseModel):
    countries: List[CountryItem] = Field(..., description="List of countries and regional groupings")


class CountriesResponse(BaseModel):
    success: bool = Field(default=True, description="Whether the request succeeded")
    message: str = Field(..., description="Status message")
    data: CountriesData = Field(..., description="Countries wrapper")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Fetched 283 countries",
                "data": {
                    "countries": [
                        {"id": 63, "couCode": "D", "countryName": "Germany"},
                        {"id": 261, "couCode": "USA", "countryName": "United States of America"},
                        {"id": 259, "couCode": "UAE", "countryName": "United Arab Emirates"},
                    ]
                },
            }
        }
    )


# ==================== VEHICLE TYPES (API #5) ====================

class VehicleTypeItem(BaseModel):
    id: int = Field(..., description="Numeric vehicle type ID", examples=[1])
    vehicleType: str = Field(..., description="Short type name (PC, CV, LCV, etc.)", examples=["PC"])


class VehicleTypesResponse(BaseModel):
    success: bool = Field(default=True, description="Whether the request succeeded")
    message: str = Field(..., description="Human-readable status message")
    data: List[VehicleTypeItem] = Field(..., description="List of vehicle types from the catalog")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Fetched 11 vehicle types",
                "data": [
                    {"id": 1, "vehicleType": "PC"},
                    {"id": 2, "vehicleType": "CV"},
                    {"id": 3, "vehicleType": "Motorcycle"},
                ],
            }
        }
    )


# ==================== MANUFACTURERS (API #6) ====================

class ManufacturerItem(BaseModel):
    manufacturerId: int = Field(..., description="Manufacturer ID", examples=[111])
    manufacturerName: str = Field(..., description="Brand name (uppercase)", examples=["TOYOTA"])


class ManufacturersData(BaseModel):
    countManufactures: int = Field(..., description="Total number of manufacturers", examples=[698])
    manufacturers: List[ManufacturerItem] = Field(..., description="List of manufacturers")


class ManufacturersResponse(BaseModel):
    success: bool = Field(default=True)
    message: str = Field(..., description="Status message")
    data: ManufacturersData = Field(..., description="Manufacturers wrapper")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Fetched 698 manufacturers",
                "data": {
                    "countManufactures": 698,
                    "manufacturers": [
                        {"manufacturerId": 111, "manufacturerName": "TOYOTA"},
                        {"manufacturerId": 183, "manufacturerName": "HYUNDAI"},
                    ],
                },
            }
        }
    )


# ==================== MODELS (API #8) ====================

class ModelItem(BaseModel):
    modelId: int = Field(..., description="Model ID", examples=[5626])
    modelName: str = Field(..., description="Full model name", examples=["CEE'D Hatchback (ED)"])
    modelYearFrom: Optional[str] = Field(None, description="Production start (YYYY-MM-DD)", examples=["2006-12-01"])
    modelYearTo: Optional[str] = Field(None, description="Production end (YYYY-MM-DD); null if still in production", examples=["2012-12-01"])


class ModelsData(BaseModel):
    countModels: int = Field(..., description="Total models", examples=[130])
    models: List[ModelItem] = Field(..., description="List of models")


class ModelsResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: ModelsData

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Fetched 130 models",
                "data": {
                    "countModels": 130,
                    "models": [
                        {
                            "modelId": 5626,
                            "modelName": "CEE'D Hatchback (ED)",
                            "modelYearFrom": "2006-12-01",
                            "modelYearTo": "2012-12-01",
                        }
                    ],
                },
            }
        }
    )


# ==================== ENGINE VARIANTS (API #12) ====================

class EngineVariant(BaseModel):
    vehicleId: int = Field(..., description="Vehicle ID for this trim", examples=[19942])
    manufacturerName: str = Field(..., description="Brand name", examples=["KIA"])
    modelName: str = Field(..., description="Model name", examples=["CEE'D Hatchback (ED)"])
    typeEngineName: str = Field(..., description="Engine/trim label", examples=["1.6 CRDi 115"])
    constructionIntervalStart: Optional[str] = Field(None, description="Start date")
    constructionIntervalEnd: Optional[str] = Field(None, description="End date")
    powerKw: Optional[str] = Field(None, description="Power in kW (decimal string)")
    powerPs: Optional[str] = Field(None, description="Power in PS (decimal string)")
    capacityTax: Optional[str] = Field(None, description="Tax displacement")
    fuelType: Optional[str] = Field(None, description="Fuel type", examples=["Diesel"])
    bodyType: Optional[str] = Field(None, description="Body style", examples=["Hatchback"])
    numberOfCylinders: Optional[int] = Field(None, description="Cylinder count")
    capacityLt: Optional[str] = Field(None, description="Displacement in litres (decimal string)")
    capacityTech: Optional[str] = Field(None, description="Exact displacement in cc (decimal string)")
    engineCodes: Optional[str] = Field(None, description="OEM engine codes", examples=["D4FB"])
    engId: Optional[int] = Field(None, description="Catalog engine ID")


class EngineVariantsData(BaseModel):
    modelType: str = Field(..., description="Vehicle type name", examples=["PC"])
    countModelTypes: int = Field(..., description="Total engine variants")
    modelTypes: List[EngineVariant] = Field(..., description="List of engine variants")


class EngineVariantsResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: EngineVariantsData


# ==================== VEHICLE VARIANTS (API #14 — light) ====================

class VehicleVariantLight(BaseModel):
    vehicleId: int = Field(..., description="Vehicle ID for this trim", examples=[19942])
    manufacturerName: str = Field(..., description="Brand name")
    modelName: str = Field(..., description="Model name")
    typeEngineName: str = Field(..., description="Engine/trim label")


class VehicleVariantsData(BaseModel):
    modelType: str = Field(..., description="Vehicle type name")
    countModelTypes: int = Field(..., description="Total variants")
    modelTypes: List[VehicleVariantLight] = Field(..., description="Lightweight variant list")


class VehicleVariantsResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: VehicleVariantsData


# ==================== CATEGORIES (API #27, #28) ====================
# The category tree is deeply nested with inconsistent children types
# (object at non-leaf, empty array at leaf). Use permissive typing for passthrough.

class CategoriesAllResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: Dict[str, Any] = Field(..., description="Raw nested category tree keyed by name")


class CategoryBreadcrumbRow(BaseModel):
    level: int = Field(..., description="Depth of this row (1-4)", examples=[3])
    categoryName1: Optional[str] = Field(None, description="Level 1 name")
    categoryId1: Optional[int] = Field(None, description="Level 1 ID")
    categoryName2: Optional[str] = Field(None, description="Level 2 name")
    categoryId2: Optional[int] = Field(None, description="Level 2 ID")
    categoryName3: Optional[str] = Field(None, description="Level 3 name")
    categoryId3: Optional[int] = Field(None, description="Level 3 ID")
    categoryName4: Optional[str] = Field(None, description="Level 4 name")
    categoryId4: Optional[int] = Field(None, description="Level 4 ID")


class CategoriesByVehicleData(BaseModel):
    categories: List[CategoryBreadcrumbRow] = Field(..., description="Flat breadcrumb rows")


class CategoriesByVehicleResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: CategoriesByVehicleData


# ==================== ARTICLE LIST (API #41) ====================

class ArticleListItem(BaseModel):
    articleId: int = Field(..., description="Article ID", examples=[5522538])
    articleNo: str = Field(..., description="Supplier part number", examples=["A63193"])
    supplierName: str = Field(..., description="Supplier brand", examples=["1A FIRST AUTOMOTIVE"])
    supplierId: int = Field(..., description="Supplier ID")
    articleProductName: str = Field(..., description="Product type name", examples=["Air Filter"])
    productId: Optional[int] = Field(None, description="Generic article/product group ID")
    articleMediaType: Optional[str] = Field(None, description="Declared media type")
    articleMediaFileName: Optional[str] = Field(None, description="Image filename (.webp)")
    s3image: Optional[str] = Field(None, description="Direct S3 image URL")


class ArticleListData(BaseModel):
    vehicleId: str = Field(..., description="Echoed vehicle ID (as string)")
    categoryId: str = Field(..., description="Echoed category ID (as string)")
    countArticles: int = Field(..., description="Total matched articles")
    articles: List[ArticleListItem] = Field(..., description="Matching articles")


class ArticleListResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: ArticleListData


# ==================== ARTICLE DETAILS (API #36) ====================

class ArticleSpecification(BaseModel):
    criteriaName: str = Field(..., description="Spec label with unit", examples=["Weight [kg]"])
    criteriaValue: str = Field(..., description="Spec value (may be empty string)", examples=["9,20"])


class OEMReference(BaseModel):
    oemBrand: str = Field(..., description="OEM manufacturer", examples=["HYUNDAI"])
    oemDisplayNo: str = Field(..., description="OEM part number", examples=["28113-2H000"])


class CompatibleVehicle(BaseModel):
    vehicleId: int = Field(..., description="Vehicle ID")
    modelId: int = Field(..., description="Model ID")
    manufacturerName: str = Field(..., description="Manufacturer name")
    modelName: str = Field(..., description="Model name")
    typeEngineName: str = Field(..., description="Engine name")
    constructionIntervalStart: Optional[str] = Field(None, description="Production start")
    constructionIntervalEnd: Optional[str] = Field(None, description="Production end (null if current)")


class EANNumber(BaseModel):
    eanNumbers: Optional[str] = Field(None, description="EAN barcode(s)")


class ArticleInfo(BaseModel):
    articleId: int
    articleNo: str
    supplierId: int
    supplierName: str
    isAccessory: int = Field(..., description="0 = main article, 1 = accessory")
    articleProductName: str


class ArticleFullDetails(BaseModel):
    articleId: int = Field(..., description="Article ID")
    articleNo: str = Field(..., description="Supplier part number")
    articleProductName: str = Field(..., description="Product type name")
    supplierName: str
    supplierId: int
    articleMediaType: Optional[str] = None
    articleMediaFileName: Optional[str] = None
    articleInfo: Optional[ArticleInfo] = None
    allSpecifications: Optional[List[ArticleSpecification]] = None
    eanNo: Optional[EANNumber] = None
    oemNo: Optional[List[OEMReference]] = None
    s3image: Optional[str] = None
    compatibleCars: Optional[List[CompatibleVehicle]] = None


class ArticleDetailsData(BaseModel):
    article: ArticleFullDetails = Field(..., description="Full article record")


class ArticleDetailsResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: ArticleDetailsData


class ArticleDetailsRequest(BaseModel):
    articleId: int = Field(..., gt=0, description="Article ID", examples=[131540])
    langId: Optional[int] = Field(None, description="Language ID (defaults to config)", examples=[4])
    typeId: Optional[int] = Field(None, description="Vehicle type ID (defaults to config)", examples=[1])
    countryFilterId: Optional[int] = Field(None, description="Country filter ID (defaults to config)", examples=[63])


# ==================== ARTICLE MEDIA (API #48) ====================

class ArticleMediaItem(BaseModel):
    articleMediaType: str = Field(..., description="Declared media type (JPEG/JPG/PNG/GIF)")
    articleMediaFileName: str = Field(..., description="Filename with .webp extension")
    supplierId: int = Field(..., description="Supplier who provided the media")
    mediaInformation: str = Field(..., description="Media purpose label", examples=["Picture"])
    s3image: str = Field(..., description="Full S3 URL")


class ArticleMediaResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: List[ArticleMediaItem] = Field(..., description="List of media assets")


# ==================== OEM NUMBERS (API #26) ====================

class OEMByArticleItem(BaseModel):
    articleId: int = Field(..., description="Article ID")
    oemNo: List[OEMReference] = Field(..., description="OEM cross-references")


class OEMNumbersData(BaseModel):
    count: int = Field(..., description="Number of articles in response")
    articles: List[OEMByArticleItem] = Field(..., description="OEM data per article")


class OEMNumbersResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: OEMNumbersData


class OEMNumbersRequest(BaseModel):
    articleIds: List[int] = Field(..., min_length=1, max_length=100, description="Article IDs to fetch OEM for", examples=[[5522538, 6822931]])


# ==================== FITMENT / COMPATIBLE VEHICLES (API #43) ====================

class FitmentArticleItem(BaseModel):
    articleId: int
    articleNo: str
    articleProductName: str
    supplierName: str
    supplierId: int
    compatibleCars: List[CompatibleVehicle] = Field(..., description="Vehicles this article fits")


class FitmentData(BaseModel):
    countArticles: int = Field(..., description="Total matched articles")
    articles: List[FitmentArticleItem] = Field(..., description="Articles with fitment data")


class FitmentResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: FitmentData


# ==================== CROSS-REFERENCES (API #50) ====================

class CrossReferencesResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: Any = Field(..., description="Raw cross-references response from the catalog")


# ==================== ARTICLE SEARCH (API #19, #20) ====================

class ArticleSearchItem(BaseModel):
    articleSearchNo: str = Field(..., description="Article number as matched")
    articleId: int = Field(..., description="Article ID")
    articleNo: str = Field(..., description="Canonical article number")
    articleProductName: str = Field(..., description="Generic product name")
    supplierName: str = Field(..., description="Supplier brand")
    supplierId: int = Field(..., description="Supplier ID")
    articleMediaType: Optional[str] = Field(None, description="Declared image format")
    articleMediaFileName: Optional[str] = Field(None, description="Image filename")
    s3image: Optional[str] = Field(None, description="Direct S3 image URL")


class ArticleSearchData(BaseModel):
    countArticles: int = Field(..., description="Total matches")
    articles: List[ArticleSearchItem] = Field(..., description="Matched articles")


class ArticleSearchResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: ArticleSearchData


# ==================== DUMP ====================

class DumpCountsData(BaseModel):
    languages: int = Field(default=0)
    countries: int = Field(default=0)
    vehicle_types: int = Field(default=0)
    manufacturers: int = Field(default=0)
    models: int = Field(default=0)
    vehicles: int = Field(default=0)
    engine_variants: int = Field(default=0)
    vehicle_categories: int = Field(default=0)
    articles: int = Field(default=0)
    article_details: int = Field(default=0)
    article_media: int = Field(default=0)
    oem_refs: int = Field(default=0)
    fitment: int = Field(default=0)
    cross_refs: int = Field(default=0)
    search: int = Field(default=0)


class DumpPhasesDoneData(BaseModel):
    reference: bool = Field(default=False)
    manufacturers: bool = Field(default=False)
    models: bool = Field(default=False)
    vehicles: bool = Field(default=False)
    engine_variants: bool = Field(default=False)
    categories: bool = Field(default=False)
    articles: bool = Field(default=False)
    article_details: bool = Field(default=False)
    article_media: bool = Field(default=False)
    oem_batch: bool = Field(default=False)
    fitment: bool = Field(default=False)
    cross_refs: bool = Field(default=False)
    search: bool = Field(default=False)


class DumpStatusData(BaseModel):
    job_id: Optional[int] = Field(None, description="Dump job ID")
    status: str = Field(..., description="idle | running | paused | completed | failed")
    current_phase: str = Field(..., description="Current crawl phase")
    budget_limit: int = Field(..., description="Total API call budget")
    total_api_calls: int = Field(..., description="API calls used so far")
    remaining_budget: int = Field(..., description="Calls remaining in budget")
    calls_per_key: Dict[str, int] = Field(..., description="Calls used per key")
    counts: DumpCountsData = Field(..., description="Row counts per table")
    phases_done: DumpPhasesDoneData = Field(..., description="Phase completion flags")
    started_at: Optional[str] = Field(None, description="ISO timestamp when dump started")
    completed_at: Optional[str] = Field(None, description="ISO timestamp when dump finished")
    error_message: Optional[str] = Field(None, description="Error detail if failed")


class DumpStatusResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: DumpStatusData


class DumpStartResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: Optional[Dict[str, Any]] = None


# ==================== VIN DECODE ====================

class VinDecodeResponse(BaseModel):
    success: bool = Field(default=True)
    message: str
    data: Any = Field(..., description="Parsed VIN decoder payload (v1, v2, v3 subsections)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "VIN decoded successfully",
                "data": {
                    "vin-data-1": {"vin": "WDBFA68F42F202731", "manufacturer": "Mercedes-Benz"},
                    "vin-data-2": {"make": "MERCEDES-BENZ", "model": "SL-Class", "trim": "SL500"},
                },
            }
        }
    )