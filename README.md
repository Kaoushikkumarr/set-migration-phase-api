# Database Migration Project Phase API

This solution provides an API to allow for the update of phases during a given database migration.
It is implemented in Python using Flask, Flask-RESTful, and Google Cloud's BigQuery service.

## Functionality

The solution provides endpoints for creating, updating, and deleting Phases, Progress, Entities, and Entity Objects. It also provides an endpoint for retrieving a list of available phases.

## Dependencies

The following Python packages are required to run this solution:
* Flask
* Flask-RESTful
* google-cloud-bigquery
* pydantic

## Endpoints

The following endpoints are available:

* /api/v1/phase-table - Create, update, or delete a Phase.
* /api/v1/process-table - Create, update, or delete a Progress.
* /api/v1/entity-table - Create, update, or delete an Entity.
* /api/v1/entity-object-table - Create, update, or delete an Entity Object.

## Models

The following models are used in this solution:

### Phase(Enum)

Represents a Enum for class Phase.

* NOT_STARTED (str)
* DEV_SCHEMA_CONVERSION (str)
* DEV_SCHEMA_BEFORE_CONSTRAINTS (str)
* DEV_DATA_MOVEMENT (str)
* DEV_SCHEMA_AFTER_CONSTRAINTS (str)
* DEV_DATA_VALIDATION (str)
* DEV_APPLICATION_CONVERSION (str)
* DEV_DATA_MIGRATION (str)
* DEV_CUT_OVER (str)
*
* PROD_SCHEMA_CONVERSION (str)
* PROD_SCHEMA_BEFORE_CONSTRAINTS (str)
* PROD_DATA_MOVEMENT (str)
* PROD_SCHEMA_AFTER_CONSTRAINTS (str)
* PROD_DATA_VALIDATION (str)
* PROD_APPLICATION_CONVERSION (str)
* PROD_DATA_MIGRATION (str)
* PROD_CUT_OVER (str)

### PhaseModel

Represents a phase.

* step_id (int) - The phase's unique identifier.
* name (Phase) - The phase's name. One of: NOT_STARTED, SCHEMA_CONVERSION_DEV, DATA_MOVEMENT_DEV.
* description (str) - A description of the phase.
* orders (int) - The rank of the phase.
* optional (bool, optional) - Whether the phase is optional.
* parent_id (int, optional) - The ID of the parent phase.

### ProgressModel

Represents the progress of an entity in a phase.

* step_id (int) - The ID of the phase.
* entity_id (int) - The ID of the entity.
* start_date_time (datetime) - The start date and time of the progress.
* end_date_time (datetime, optional) - The end date and time of the progress.
* is_successful (bool, optional) - Whether the progress was successful.

### EntityModel

Represents an entity.

* entity_id (int) - The entity's unique identifier.
* application_name (str) - The name of the application.
* source_server (str) - The source server.
* source_database_name (str) - The name of the source database.
* target_server (str) - The target server.
* target_database_name (str, optional) - The name of the target database.
* is_spdb (bool, optional) - Whether the entity is an SPDB.
* migration_type (str) - Type of migration
* env (str, optional) - Env type, default will be Development

### EntityObjectModel

Represents an object associated with an entity.

* object_id (int) - The object's unique identifier.
* entity_id (int) - The ID of the entity.
* name (str) - The object's name.
* size_in_mb (int) - The size of the object in MB.

## Example Payloads

### Phase Table
POST /api/v1/phase-table
```json
{
    "step_id": 2,
    "name": "Dev Data Movement",
    "description": "Dev Data Movement Testing 1",
    "orders": 2,
    "is_optional": false,
    "parent_step_id": 2
}
```

PUT /api/v1/phase-table
```json
{
    "step_id": 2,
    "name": "Not Started",
    "description": "Sample Not Started",
    "orders": 2,
    "is_optional": false,
    "parent_step_id": 2
}
```

DELETE api/v1/phase-table?step_id=2
```json
{}
```

### Progress Table
POST /api/v1/process-table
```json
{
    "step_id": 2,
    "entity_id": 2,
    "start_date_time": "2023-05-04 11:00:00",
    "end_date_time": "2023-05-04 12:00:00",
    "is_successful": true
}
```

PUT /api/v1/process-table
```json
{
    "step_id": 2,
    "entity_id": 2,
    "start_date_time": "2023-05-04 11:00:00",
    "end_date_time": "2023-05-04 12:00:00",
    "is_successful": false
}
```

DELETE /api/v1/process-table?step_id=2&entity_id=2
```json
{}
```

### Entity Table
POST /api/v1/entity-table
```json
{
    "entity_id": 2,
    "application_name": "striim",
    "source_server": "MSSQL",
    "source_database": "adventure-works-2019",
    "target_server": "Postgres",
    "target_database": "postgres",
    "is_spdb": false,
    "migrator": "In-progress"
}
```

PUT /api/v1/entity-table
```json
{
    "entity_id": 2,
    "application_name": "striim",
    "source_server": "MSSQL",
    "source_database": "adventure-works-2019",
    "target_server": "Postgres",
    "target_database": "postgres",
    "is_spdb": true,
    "migrator": "Completed"
}
```

DELETE /api/v1/entity-table?entity_id=2
```json
{}
```

### Entity Object Table
POST /api/v1/entity-object-table
```json
{
    "entity_id": 2,
    "object_id": 2,
    "name": "PostgreSQL",
    "size_in_mb": 30
}
```

PUT /api/v1/entity-object-table
```json
{
    "entity_id": 2,
    "object_id": 2,
    "name": "Postgres",
    "size_in_mb": 31
}
```

DELETE /api/v1/entity-object-table?object_id=2
```json
{}
```
