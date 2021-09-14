from flask import Flask, jsonify, request
import logging
from logging.handlers import RotatingFileHandler
from surl.utils.db import db
from surl.blueprints.url import url


def create_app(env: str = 'local') -> object:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config.from_pyfile(f'{env}_settings.py', silent=True)
    register_logger(app)
    app.logger.info(f'Application Worker Started: {app}')
    db.init_app(app)
    exception_handler(app)
    app.register_blueprint(url)
    db.create_all(app=app)
    register_each_request(app)

    return app


def exception_handler(app):
    def render_error_404(error_message):
        app.logger.error(f'Global exception: {error_message}')
        response = {
            "message": "Page not Found",
            "errors": "/path doesnt exists"
        }
        return jsonify(response), 404

    def render_error_400(error_message):
        app.logger.error(f'Global exception: {error_message}')
        response = {
            "message": "Invalid inputs",
            "errors": "invalid format of input sent"
        }
        return jsonify(response), 400

    def render_error_500(error_message):
        app.logger.error(f'Global exception: {error_message}')
        response = {
            "message": "Internal Server Error",
            "errors": "triggered global exception"
        }
        return jsonify(response), 500

    app.errorhandler(404)(render_error_404)
    app.errorhandler(400)(render_error_400)
    app.errorhandler(Exception)(render_error_500)


def register_each_request(app):
    def execute_before_each_request():
        app.logger.debug(f'Got Request Type: '
                         f'URL_FOR<{request.endpoint}>, '
                         f'PATH<{request.path}>, '
                         f'METHOD<{request.method}>, '
                         f'MIME<{request.mimetype}>')
        app.logger.debug(f'Got Request Data: '
                         f'ARGS<{request.view_args}>, '
                         f'PAYLOAD<{request.get_json()}>')

    def execute_after_each_response(response):
        app.logger.debug(f'Sent Response: '
                         f'DATA<{response.get_data()}>'
                         f'MIME<{response.mimetype}>')
        return response

    app.before_request(execute_before_each_request)
    app.after_request(execute_after_each_response)


def register_logger(app):
    logger_conf = {
        "backupCount": 20,
        "log_format": "[%(asctime)s]\t[%(name)s]\t[%(levelname)s]\t[%(pathname)s]\t[%(funcName)s]\t[%(message)s]",
        "log_level": 10,
        "log_path": "log/app.log",
        "maxBytes": 10240000,
        "mode": "a",
    }

    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logger_conf["log_level"])

    console_handler = RotatingFileHandler(filename=logger_conf["log_path"], mode=logger_conf["mode"],
                                          maxBytes=logger_conf["maxBytes"], backupCount=logger_conf["backupCount"],
                                          encoding=None)
    console_handler.setLevel(logger_conf["log_level"])

    formatter = logging.Formatter(logger_conf["log_format"])
    console_handler.setFormatter(formatter)

    app.logger.addHandler(console_handler)