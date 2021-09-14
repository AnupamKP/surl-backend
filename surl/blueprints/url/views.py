import shortuuid
from flask import (
    Blueprint,
    request,
    redirect,
    jsonify,
    current_app
)
from surl.blueprints.url.schemas import (
    URLSchema,
    IdSchema,
    Surl_IDSchema
)
from surl.blueprints.url.models import Surl_ID
from surl.utils.api_utils import validate_input

url = Blueprint('url', __name__)
url_schema = URLSchema()
id_schema = IdSchema()
surl_id_schema = Surl_IDSchema()


@url.route('/', methods=['POST', 'PUT'])
@validate_input(url_schema, input_type='payload')
def create_url():
    short_id = shortuuid.uuid()
    response_from_db = Surl_ID.create_url(short_id, request.get_json()['url'])
    current_app.logger.info(f'response from db: {response_from_db}')
    formatted_response = surl_id_schema.dump(response_from_db)
    return jsonify(formatted_response), 201


@url.route('/', methods=['GET'])
def get_url_all():
    response_from_db = Surl_ID.get_url_all()
    current_app.logger.info(f'response from db: {response_from_db}')
    formatted_response = [surl_id_schema.dump(row) for row in response_from_db]
    return jsonify(formatted_response), 200


@url.route('/<string:url_id>', methods=['GET'])
@validate_input(id_schema, input_type='arg')
def get_url_from_id(url_id):
    response_from_db = Surl_ID.get_url_from_id(request.view_args['url_id'])
    current_app.logger.info(f'response from db: {response_from_db}')
    if response_from_db:
        redirect_url = surl_id_schema.dump(response_from_db)['url']
        return redirect(redirect_url, 302)
    return jsonify('{"message": "Data Not Found", "errors": "url id doesnt exists"}'), 403


@url.route('/<string:url_id>', methods=['DELETE'])
@validate_input(id_schema, input_type='arg')
def delete_url_from_id(url_id):
    response_from_db = Surl_ID.delete_url_from_id(request.view_args['url_id'])
    current_app.logger.info(f'response from db: {response_from_db}')
    return jsonify(''), 202
