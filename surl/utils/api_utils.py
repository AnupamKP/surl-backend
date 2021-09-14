from flask import (
    request,
    current_app,
    jsonify
)
from marshmallow import ValidationError
from functools import wraps


def validate_input(schema_obj, input_type):
    def decorator(func):
        @wraps(func)
        def deserialize_and_validate_input(*args, **kwargs):
            try:
                if input_type == 'payload':
                    request_json = request.get_json()
                else:
                    request_json = request.view_args
                current_app.logger.info(f'raw request json: {request_json}')
                schema_obj.load(request_json)
                current_app.logger.info(f'validated request json: {request_json}')
                return func(*args, **kwargs)
            except ValidationError as err:
                err_response = {
                    "message": "Validation Error",
                    "errors": err.normalized_messages()
                }
                current_app.logger.error(f'request validation Error: {err}, status_code: 400')
                return jsonify(err_response), 400
        return deserialize_and_validate_input
    return decorator
