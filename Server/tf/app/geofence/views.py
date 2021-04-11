import uuid
import json
import logging
from flask_restful import Resource
from flask_restful import reqparse
from flask import request, Response
from pymongo import UpdateOne

from app.common.constant import APPLICATION_JSON, ITEM_DOES_NOT_EXIST, CONSTRAIN_VIOLATION
from app.geofence.models import Geofence, GeoCoordinate
from mongoengine.errors import ValidationError, FieldDoesNotExist, DoesNotExist, NotUniqueError
from app.common.error import InternalServerError
from pymongo.errors import DuplicateKeyError, BulkWriteError


parser = reqparse.RequestParser()
parser.add_argument('page', type=int, location='args', default=1)
parser.add_argument('limit', type=int, location='args', default=1000)
parser.add_argument('status', type=bool, location='args', default=True)


class GeoFencesApi(Resource):

    @staticmethod
    def get():
        args = parser.parse_args()
        geo_fence = Geofence.objects
        # if args.get('status') is not None:
        #     geo_fence = geo_fence.filter(status=args.get('status'))
        geo_fence = geo_fence.paginate(page=args['page'], per_page=args['limit'])
        response = [json.loads(obj.to_json(use_db_field=False)) for obj in geo_fence.items]
        return {
            "data": response, "hasNext": geo_fence.has_next,
            "hasPrev": geo_fence.has_prev, "total": geo_fence.total
        }

    @staticmethod
    def post():
        try:
            request_body = request.get_json(force=True)
            geo_fence = Geofence(**request_body)
            geo_fence.uu_id = str(uuid.uuid4())
            geo_fence = geo_fence.save(validate=True)
            request_body['uu_id'] = geo_fence.uu_id
            return request_body, 200
        except ValidationError as _e:
            return _e.to_dict(), 400
        except (FieldDoesNotExist, NotUniqueError, DuplicateKeyError) as _e:
            return {"error": _e.args}, 400
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError


class GeoFenceApi(Resource):

    @staticmethod
    def patch(fence_id):
        try:
            request_body = request.get_json(force=True)
            geo_fence = Geofence.objects.get(uu_id=fence_id)
            current_obj = json.loads(geo_fence.to_json(use_db_field=False))
            for key in request_body:
                current_obj[key] = request_body[key]
            geo_fence.uu_id = fence_id
            geo_fence.validate()
            geo_fence.update(**request_body)
            return Response(geo_fence.to_json(use_db_field=False), mimetype=APPLICATION_JSON, status=200)
        except ValidationError as _e:
            return _e.to_dict(), 400
        except (FieldDoesNotExist, NotUniqueError) as _e:
            return {"error": _e.args}, 400
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError

    @staticmethod
    def put(fence_id):
        try:
            request_body = request.get_json(force=True)
            geo_fence = Geofence.objects.get(uu_id=fence_id)
            if not geo_fence:
                geo_fence = Geofence(**request_body)
                geo_fence.uu_id = fence_id
                geo_fence.save(validate=True)
            else:
                geo_fence = Geofence(**request_body)
                geo_fence.uu_id = fence_id
                geo_fence.validate()
                Geofence._get_collection().replace_one({"_id": fence_id}, request_body)
            return Response(geo_fence.to_json(use_db_field=False), mimetype=APPLICATION_JSON, status=200)
        except ValidationError as _e:
            return _e.to_dict(), 400
        except (FieldDoesNotExist, NotUniqueError) as _e:
            return {"error": _e.args}, 400
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError

    @staticmethod
    def delete(fence_id):
        try:
            geo_fence = Geofence.objects.get(uu_id=fence_id)
            geo_fence.delete()
            return None, 204
        except DoesNotExist:
            return {"error": ITEM_DOES_NOT_EXIST}, 404
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError

    @staticmethod
    def get(fence_id):
        try:
            geo_fence = Geofence.objects.get(uu_id=fence_id).to_json(use_db_field=False)
            return Response(geo_fence, mimetype=APPLICATION_JSON, status=200)
        except DoesNotExist:
            return {"error": ITEM_DOES_NOT_EXIST}, 404
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError


class GeoFenceCollectionApi(Resource):

    @staticmethod
    def post():
        try:
            request_body = request.get_json(force=True)
            bulk_operations = []
            error_list = []
            response_list = []
            for item in request_body:
                uu_id = item.get('uu_id', str(uuid.uuid4()))
                geo_fence = Geofence(**item)
                geo_fence.uu_id = uu_id
                try:
                    geo_fence.validate()
                    bulk_operations.append(
                        UpdateOne({'_id': uu_id}, {'$set': item}, upsert=True))
                    item['uu_id'] = uu_id
                    response_list.append(item)
                except ValidationError as _e:
                    item["error"] = _e.to_dict()
                    error_list.append(item)
            if error_list:
                return error_list, 400
            else:
                Geofence._get_collection().bulk_write(bulk_operations, ordered=False)
                return response_list, 207
        except ValidationError as _e:
            return _e.to_dict(), 400
        except BulkWriteError as _e:
            return {"error": CONSTRAIN_VIOLATION}, 400
        except FieldDoesNotExist as _e:
            return {"error": _e.args}, 400
        except Exception as _e:
            logging.error(_e)
            raise InternalServerError
