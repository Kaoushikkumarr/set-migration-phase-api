"""
This file will be used for performing the DML operations over the BigQuery.
"""
from google.cloud import bigquery
from API.pydantics import (
    EntityModel,
    EntityObjectModel,
    PhaseModel,
    ProgressModel
)
from constants import (
    DATASET_NAME,
    PROJECT_ID,
    TBL_MIGRATION_ENTITY,
    TBL_MIGRATION_ENTITY_OBJECTS,
    TBL_MIGRATION_STEP,
    TBL_MIGRATION_PROGRESS
)

# Accessing the PROJECT_ID from constants.
client = bigquery.Client(project=PROJECT_ID)


class BigQueryTable:
    """
    This Big Query Class will contain all the function to perform CRUD operation using Bigquery API.
    """
    def __init__(self, table_name):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance variables for that particular object.

        :param self: Represent the instance of the class
        :param table_name: Set the name of the table
        :return: Nothing
        :doc-author: Kaoushik Kumar
        """
        self.table_name = table_name

    def _get_table(self):
        """
        The _get_table function is a helper function that returns the table object from BigQuery.

        :param self: Represent the instance of the class
        :return: A table object from the bigquery api
        :doc-author: Kaoushik Kumar
        """
        table_ref = client.dataset(DATASET_NAME).table(self.table_name)
        return client.get_table(table_ref)

    def insert_row(self, row):
        """
        The insert_row function takes a row of data and inserts it into the BigQuery table.
            Args:
                row (dict): A dictionary containing the column names and values to be inserted into the table.

        :param self: Represent the instance of the class
        :param row: Insert a row into the table
        :return: A dictionary with a key 'response' and value 'success'
        :doc-author: Kaoushik Kumar
        """
        table = self._get_table()
        client.insert_rows(table, [row])
        return {'response': 'Success'}

    def update_row(self, query):
        """
        The update_row function takes a query as an argument and updates the row in the database.
            Args:
                query (str): The SQL update statement to be executed.

        :param self: Represent the instance of the class
        :param query: Specify the query to be executed
        :return: The string 'updated'
        :doc-author: Kaoushik Kumar
        """
        query_job = client.query(query)
        query_job.result()
        return {'response': 'Updated'}

    def delete_row(self, query):
        """
        The delete_row function deletes a row from the table.
            Args:
                query (str): The Bigquery to delete a row from the table.

        :param self: Represent the instance of the class
        :param query: Specify the query to be executed
        :return: A dictionary with a key of response and a value of 'deleted'
        :doc-author: Kaoushik Kumar
        """
        query_job = client.query(query)
        query_job.result()
        return {'response': 'Deleted'}


class PhaseTable(BigQueryTable):
    """
    This PhaseTable Class will contain all the function to perform CRUD operation using Bigquery API.
    """
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        The __init__ function can take arguments, but self must be included as an argument to every
        __init__ function in a class.

        :param self: Represent the instance of the class
        :return:  instance
        :doc-author: Kaoushik Kumar
        """
        super().__init__(TBL_MIGRATION_STEP)

    def insert_phase(self, phase: PhaseModel):
        """
        The insert_phase function takes a PhaseModel object and inserts it into the database.

        :param self: Represent the instance of the class
        :param phase: PhaseModel: Pass in the phase object that is being inserted into the database
        :return: The id of the phase inserted into the database
        :doc-author: Kaoushik Kumar
        """
        row = (
            phase.step_id,
            phase.name.value,
            phase.description,
            phase.orders,
            phase.is_optional,
            phase.parent_step_id,
        )
        return self.insert_row(row)

    def update_phase(self, phase: PhaseModel):
        """
        The update_phase function updates the phase table in BigQuery with a new PhaseModel object.

        :param self: Reference the object that is calling the function
        :param phase: PhaseModel: Pass the phase object to the function
        :return: A boolean value
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            UPDATE 
                `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            SET 
                name = '{phase.name.value}', 
                description = '{phase.description}',
                orders = {phase.orders},
                is_optional = {phase.is_optional},
                parent_step_id = {phase.parent_step_id}
            WHERE 
                step_id = {phase.step_id}
            """
        return self.update_row(query)

    def delete_phase(self, step_id: int):
        """
        The delete_phase function deletes a phase from the database.

        :param self: Represent the instance of the class
        :param step_id: int: Specify the phase_id of the row to be deleted
        :return: The number of rows deleted
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            DELETE 
                FROM `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            WHERE 
                step_id = {step_id}
            """
        return self.delete_row(query)


class ProgressTable(BigQueryTable):
    """
    This ProgressTable Class will contain all the function to perform CRUD operation using Bigquery API.
    """
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        The __init__ function takes in arguments that are passed to it by whoever creates an instance of this class,
        and assigns them to self.&lt;attribute name&gt; so that they can be accessed
        by other functions within this class.

        :param self: Represent the instance of the class
        :return: The following:
        :doc-author: Kaooushik Kumar
        """
        super().__init__(TBL_MIGRATION_PROGRESS)

    def insert_progress(self, progress: ProgressModel):
        """
        The insert_progress function inserts a new row into the Progress table.

        :param self: Represent the instance of the class
        :param progress: ProgressModel: Pass the progress object to the function
        :return: The row data of the progress that was inserted into the database
        :doc-author: Kaoushik Kumar
        """
        row = (
            progress.step_id,
            progress.entity_id,
            progress.start_date_time,
            progress.end_date_time,
            progress.is_successful,
        )
        return self.insert_row(row)

    def update_progress(self, progress: ProgressModel):
        """
        The update_progress function updates the progress table with a new ProgressModel.
            Args:
                progress (ProgressModel): The ProgressModel to be updated in the database.

        :param self: Refer to the current instance of a class
        :param progress: ProgressModel: Update the progress table in bigquery
        :return: A boolean value
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            UPDATE 
                `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            SET 
                start_date_time = '{progress.start_date_time}',
                end_date_time = '{progress.end_date_time}',
                is_successful = {progress.is_successful}
            WHERE 
                step_id = {progress.step_id} 
            AND 
                entity_id = {progress.entity_id}
            """
        return self.update_row(query)

    def delete_progress(self, step_id: int, entity_id: int):
        """
        The delete_progress function deletes a row from the progress table.

        :param self: Refer to the class itself
        :param step_id: int: Specify the phase_id of the row to be deleted
        :param entity_id: int: Specify the entity that is being deleted
        :return: A boolean value
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            DELETE 
                FROM `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            WHERE 
                step_id = {step_id} 
            AND 
                entity_id = {entity_id}
            """
        return self.delete_row(query)


class EntityTable(BigQueryTable):
    """
    This EntityTable Class will contain all the function to perform CRUD operation using Bigquery API.
    """
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        The __init__ function takes in arguments that are passed to it by whoever creates an instance of this class,
        and assigns them to self.TBL_MIGRATION_ENTITY; so that they can be accessed by other functions within the class.

        :param self: Represent the instance of the class
        :return: The object itself
        :doc-author: Kaoushik Kumar
        """
        super().__init__(TBL_MIGRATION_ENTITY)

    def insert_entity(self, entity: EntityModel):
        """
        The insert_entity function inserts a new entity into the database.

        :param self: Represent the instance of the class
        :param entity: EntityModel: Pass in the entity object
        :return: The primary key of the row that was inserted
        :doc-author: Kaoushik Kumar
        """
        row = (
            entity.entity_id,
            entity.application_name,
            entity.source_server,
            entity.source_database,
            entity.target_server,
            entity.target_database,
            entity.is_spdb,
            entity.migration_type,
            entity.migrator,
            entity.env
        )
        return self.insert_row(row)

    def update_entity(self, entity: EntityModel):
        """
        The update_entity function updates an existing entity in the entities table.

        :param self: Bind the method to the object
        :param entity: EntityModel: Pass in the entity object that is to be updated
        :return: A boolean value
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            UPDATE 
                `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            SET 
                application_name = '{entity.application_name}',
                source_server = '{entity.source_server}',
                source_database = '{entity.source_database}',
                target_server = '{entity.target_server}',
                target_database = '{entity.target_database}',
                is_spdb = {entity.is_spdb},
                migration_type = '{entity.migration_type}',
                migrator = '{entity.migrator}',
                env = '{entity.env}'
            WHERE 
                entity_id = {entity.entity_id}
            """
        return self.update_row(query)

    def delete_entity(self, entity_id: int):
        """
        The delete_entity function deletes a row from the table.

        :param self: Refer to the object itself
        :param entity_id: int: Identify the row to be deleted
        :return: The number of rows deleted
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            DELETE 
                FROM `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            WHERE 
                entity_id = {entity_id}
            """
        return self.delete_row(query)


class EntityObjectTable(BigQueryTable):
    """
    This EntityObjectTable Class will contain all the function to perform CRUD operation using Bigquery API.
    """
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        The __init__ function can take any number of arguments, but they must have default values
        if you want to be able to create objects without passing in any values.

        :param self: Represent the instance of the class
        :return: The object itself
        :doc-author: Kaoushik Kumar
        """
        super().__init__(TBL_MIGRATION_ENTITY_OBJECTS)

    def insert_entity_object(self, entity_object: EntityObjectModel):
        """
        The insert_entity_object function inserts a new row into the entity_object table.

        :param self: Access the attributes and methods of the class
        :param entity_object: EntityObjectModel: Pass in the entityobjectmodel object
        :return: The object_id of the inserted row
        :doc-author: Kaoushik Kumar
        """
        row = (
            entity_object.object_id,
            entity_object.entity_id,
            entity_object.name,
            entity_object.size_in_mb,
        )
        return self.insert_row(row)

    def update_entity_object(self, entity_object: EntityObjectModel):
        """
        The update_entity_object function updates an existing entity object in the database.

        :param self: Keep track of the instance of the class
        :param entity_object: EntityObjectModel: Pass the object to be updated
        :return: The number of rows that were updated
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            UPDATE 
                `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            SET 
                entity_id = {entity_object.entity_id}, 
                name = '{entity_object.name}',
                size_in_mb = {entity_object.size_in_mb}
            WHERE 
                object_id = {entity_object.object_id}
            """
        return self.update_row(query)

    def delete_entity_object(self, object_id: int):
        """
        The delete_entity_object function deletes a row from the entity table.

        :param self: Refer to the object itself
        :param object_id: int: Identify the row to be deleted
        :return: The number of rows deleted
        :doc-author: Kaoushik Kumar
        """
        query = f"""
            DELETE 
                FROM `{PROJECT_ID}.{DATASET_NAME}.{self.table_name}`
            WHERE 
                object_id = {object_id}
            """
        return self.delete_row(query)
