from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Phase(Enum):
    NOT_STARTED = "Not Started"

    DEV_SCHEMA_CONVERSION = "Dev Schema Conversion"
    DEV_SCHEMA_BEFORE_CONSTRAINTS = "Dev Schema Before Constraints"
    DEV_DATA_MOVEMENT = "Dev Data Movement"
    DEV_SCHEMA_AFTER_CONSTRAINTS = "Dev Schema After Constraints"
    DEV_DATA_VALIDATION = "Dev Data Validation"
    DEV_APPLICATION_CONVERSION = "Dev Application Conversion"
    DEV_DATA_MIGRATION = "Dev Data Migration"
    DEV_CUT_OVER = "Dev Cutover"

    PROD_SCHEMA_CONVERSION = "Prod Schema Conversion"
    PROD_SCHEMA_BEFORE_CONSTRAINTS = "Prod Schema Before Constraints"
    PROD_DATA_MOVEMENT = "Prod Data Movement"
    PROD_SCHEMA_AFTER_CONSTRAINTS = "Prod Schema After Constraints"
    PROD_DATA_VALIDATION = "Prod Data Validation"
    PROD_APPLICATION_CONVERSION = "Prod Application Conversion"
    PROD_DATA_MIGRATION = "Prod Data Migration"
    PROD_CUT_OVER = "Prod Cutover"


class PhaseModel(BaseModel):
    step_id: int
    name: Phase
    description: str
    orders: int
    is_optional: bool
    parent_step_id: int


class ProgressModel(BaseModel):
    step_id: int
    entity_id: int
    start_date_time: Optional[datetime] = Field(default_factory=datetime.now)
    end_date_time: Optional[datetime] = Field(default_factory=datetime.now)
    is_successful: Optional[bool] = False


class EntityModel(BaseModel):
    entity_id: int
    application_name: str
    source_server: str
    source_database: str
    target_server: str
    target_database: Optional[str] = None
    is_spdb: Optional[bool] = False
    migration_type: Optional[str] = 'Downtime'
    migrator: str
    env: Optional[str] = 'Development'


class EntityObjectModel(BaseModel):
    object_id: int
    entity_id: int
    name: str
    size_in_mb: int
