"""
This file will be used for Registering the Blueprint for the Flask Application. It will Flask Restful APIs,
to perform the CRUD Operations on the various BigQuery Tables.
Also, it will be logging the error to the error.log file.
"""
from flask import Blueprint, request
from flask_restful import Resource, Api
from loggers.logger import Logger
from API import pydantics
from utils import bq_client


# Registering the Flask Restful API Blueprint.
bp = Blueprint("API", __name__, url_prefix='/')
apps = Api(bp)


class PhaseTable(Resource):
    """
    This PhaseTable Class will behave as a container which will be used for creating, updating
    and deleting BigQuery's table records.
    """
    def post(self):
        """
        The post function will be used to insert the data into Phase table.
            ---
            tags:
              - Phase Table

        :param self: Represent the instance of a class
        :return: The response from the BigQuery
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.PhaseModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.PhaseTable().insert_phase(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def put(self):
        """
        The put function will be used to update the phase details in BigQuery.
            The below function will take the request payload and send that to BigQuery.
            If any exception will be occurred in payload, it will return through exception.

        :param self: Represent the instance of the class
        :return: The response in the form of dictionary
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.PhaseModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.PhaseTable().update_phase(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def delete(self):
        """
        The delete function will delete the phase from the BigQuery table records.
            ---
            tags:
              - Phase Table

        :param self: Represent the instance of the class
        :return: The response of the BigQuery
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            step_id = request.args.get('step_id')
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.PhaseTable().delete_phase(int(step_id))
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}


class ProgressTable(Resource):
    """
    This ProgressTable Class will behave as a container which will be used for creating, updating
    and deleting BigQuery's table records.
    """
    def post(self):
        """
        The post function will be used to insert the data into BigQuery table.
            The below function will take the request payload and send that to BigQuery.

        :param self: Represent the instance of a class
        :return: The response in the form of dictionary
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.ProgressModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.ProgressTable().insert_progress(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def put(self):
        """
        The put function will be used to update the progress of a particular user.
            The request payload should contain the following fields:
                - phase_id (int): This is a unique identifier for each user.
                - progress (str): This field contains the current status of a particular user.

        :param self: Represent the instance of the class
        :return: A json object with the following fields:
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.ProgressModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.ProgressTable().update_progress(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def delete(self):
        """
        The delete function will be used to delete the progress of a particular phase for an entity.
            The below function will take two parameters as input:
                1) Step ID - This is the unique identifier of a phase.
                2) Entity ID - This is the unique identifier of an entity.

        :param self: Represent the instance of the class
        :return: The following:
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            step_id = request.args.get('step_id')
            entity_id = request.args.get('entity_id')
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.ProgressTable().delete_progress(int(step_id), int(entity_id))
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}


class EntityTable(Resource):
    """
    This EntityTable Class will behave as a container which will be used for creating, updating
    and deleting BigQuery's table records.
    """
    def post(self):
        """
        The post function will be used to insert the data into BigQuery table.
            The below function will take the request payload and send that to BigQuery.
            If any exception will be occurred in payload, it will return through exception.

        :param self: Represent the instance of the class
        :return: A dictionary with two keys: response and result
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.EntityModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityTable().insert_entity(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def put(self):
        """
        The put function will be used to update the entity in BigQuery.
            The below function will take the request payload and send that to BigQuery.
            If any exception will be occurred in payload, it will return through exception.

        :param self: Represent the instance of the class
        :return: The following:
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.EntityModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityTable().update_entity(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def delete(self):
        """
        The delete function will delete the entity from the database.
            ---
            tags:
              - EntityTable

        :param self: Represent the instance of a class
        :return: A response which is in the form of a dictionary
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            entity_id = request.args.get('entity_id')
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityTable().delete_entity(int(entity_id))
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}


class EntityObjectTable(Resource):
    """
    This EntityObjectTable Class will behave as a container which will be used for creating, updating
    and deleting BigQuery's table records.
    """
    def post(self):
        """
        The post function will be used to insert the data into Entity Object Table.
            ---
            tags:
              - Entity Object Table

        :param self: Represent the instance of a class
        :return: The below response
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.EntityObjectModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityObjectTable().insert_entity_object(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def put(self):
        """
        The put function will be used to update the entity object in BigQuery.
            The below function will take the request payload and send that to BigQuery Dataset.
            If any exception will be occurred in payload, it will return through exception.

        :param self: Represent the instance of the class
        :return: The below payload
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = pydantics.EntityObjectModel(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityObjectTable().update_entity_object(payload)
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}

    def delete(self):
        """
        The delete function will delete the entity object from the database.
            ---
            tags:
              - Entity Object Table API

        :param self: Represent the instance of a class
        :return: The response from the wrapper
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            object_id = request.args.get('object_id')
            # The below will take the request payload and send that to dvt-wrapper.
            response = bq_client.EntityObjectTable().delete_entity_object(int(object_id))
            return response
        except Exception as e:
            Logger().logging().error(f'{str(e)}')
            # If any exception will be occurred in payload, will be returned through exception.
            return {'response': False, 'result': str(e)}


class HealthCheck(Resource):
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        In this case, we are setting up a Success object that will have one attribute: message.

        :param self: Represent the instance of the class
        :return: The instance of the class
        :doc-author: Kaoushik Kumar
        """
        self.message = 'Success'

    def get(self) -> str:
        """
        The health_check function is a simple function that returns the message 'I am healthy!'
            This can be used to test if the server is running and responding.

        :param self: Refer to the class instance
        :return: A string
        :doc-author: Kaoushik Kumar
        """
        return self.message


#  Registering End-Points
apps.add_resource(PhaseTable, '/api/v1/phase-table')
apps.add_resource(ProgressTable, '/api/v1/process-table')
apps.add_resource(EntityTable, '/api/v1/entity-table')
apps.add_resource(EntityObjectTable, '/api/v1/entity-object-table')

# Health Check API
apps.add_resource(HealthCheck, '/health-check')
