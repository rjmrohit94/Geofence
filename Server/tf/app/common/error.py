
class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class MultiValidationError(Exception):
    pass


class ValidationError(Exception):
    pass


class ExternalApiCallError(Exception):
    pass


class MLCallBackValidationError(Exception):
    pass


errors = {
    "mongoengine.errors.FieldDoesNotExist": {
        "message": "Something went wrong",
        "status": 500
    },
    "app.error.error.InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    }
}