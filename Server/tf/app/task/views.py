import json
import logging
from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from mongoengine.errors import ValidationError, FieldDoesNotExist, NotUniqueError, DoesNotExist
from pymongo.errors import DuplicateKeyError, BulkWriteError
from app.common.error import InternalServerError, ValidationError as AppValidationError
from app.common.constant import CONSTRAIN_VIOLATION

from .models import Task, JOB_MAPS


def validate_job_data(value):
    if not value:
        raise ValidationError("Field cannot be null or empty")
    if value.get('data') is None:
        raise ValidationError("Invalid Job")
    if value.get('type') not in JOB_MAPS:
        raise ValidationError("Invalid Job Type")


class TasksApi(Resource):

    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args', default=1)
        parser.add_argument('limit', type=int, location='args', default=1000)
        parser.add_argument('name', type=str, location='args', default=None)

        args = parser.parse_args()
        job = Task.objects
        if args.get('name'):
            job = job.filter(name__contains=args.get('name'))
        job = job.paginate(page=args['page'], per_page=args['limit'])
        response = [json.loads(obj.to_json(use_db_field=False)) for obj in job.items]
        return {
            "data": response, "hasNext": job.has_next,
            "hasPrev": job.has_prev, "total": job.total
        }

    def post(self):
        try:
            request_body = request.get_json(force=True)
            validate_job_data(request_body)
            job_data = request_body.get('data')
            job_type = request_body.get('type')
            task_id = Task.launch_task(request_body.get('name', job_type), request_body.get('description'),
                                       job_type, job_data)
            return {"jobId": task_id}, 200
        except AppValidationError as _e:
            return {"error": _e.args}, 400
        except ValidationError as _e:
            return _e.to_dict(), 400
        except (FieldDoesNotExist, NotUniqueError, DuplicateKeyError) as _e:
            return {"error": _e.args}, 400
        except BulkWriteError as _e:
            return {"error": CONSTRAIN_VIOLATION}, 400
        except DoesNotExist:
            return {"error": "Training dataset missing"}, 404
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError


class TaskApi(Resource):

    @staticmethod
    def get(job_id):
        try:
            job = json.loads(Task.objects.get(job_id=job_id).to_json(use_db_field=False))
            return job, 200
        except DoesNotExist:
            return {"error": "Item or Parent item doesn't exist"}, 404
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError
