import os
import flask
import logging
import traceback
import json_log_formatter
from flask import request, jsonify
from flask_log_request_id import RequestID, RequestIDLogFilter, current_request_id
from prometheus_flask_exporter import PrometheusMetrics
from logging.handlers import RotatingFileHandler
from mongoengine import connect
from .logic import TwittCLogic


app = flask.Flask(__name__)


# Configuração de request uuid para rastreio de requisições
RequestID(app)


# Configuração de exporter de métricas para prometheus
metrics = PrometheusMetrics(app)
metrics.info("info", "twitterapi", version="1.0.0")


# Configuração da aplicação a partir de variáveis de ambiente
app.config['MONGO_DB_HOST']=os.environ.get("MONGO_DB_HOST")
app.config['MONGO_DB_PORT']=os.environ.get("MONGO_DB_PORT")


# Configuração de LOG da
applog = logging.getLogger(__name__)
applog.setLevel(logging.DEBUG)

formatter_json =  json_log_formatter.JSONFormatter()

file_handler = RotatingFileHandler('/app/logs/twitterapi.log', maxBytes=104857600, backupCount=10)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter_json)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter_json)

applog.addHandler(file_handler)
applog.addHandler(stream_handler)

applog.debug("config", extra=app.config)


try:

    applog.debug("connect mongodb...", extra={'host':app.config['MONGO_DB_HOST'], 'port':app.config['MONGO_DB_PORT']})
    
    connect('twittes', host=app.config['MONGO_DB_HOST'], port=int(app.config['MONGO_DB_PORT']))

except Exception as e:

    tb = traceback.format_exc()

    applog.error("Fail connect mongodb", extra={'host':app.config['MONGO_DB_HOST'], 'port':app.config['MONGO_DB_PORT'], 'trace': tb})


twittcl = TwittCLogic()


applog.debug("Twitter API startup", extra={'status': 'success', 'event':'start-api'})


@app.route('/', methods=['GET'])
def index():
    
    applog.debug("List endpoints", extra={'method':'GET', 'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'endpoint': request.path })
    
    endpoints = { 'info': 'Twitter API', 
                    'version':'1.0.0', 
                    'endpoints': [
                        {'url':'/twitter/api/v1/publish/posts', 'method':'POST'},
                        {'url':'/twitter/api/v1/users/followers', 'method':'GET'}, 
                        {'url':'/twitter/api/v1/posts/hour', 'method':'GET'}, 
                        {'url':'/twitter/api/v1/posts/tags/location', 'method':'GET'},
                        {'url':'/twitter/api/v1/posts/tags/lang', 'method':'GET'}
                    ]
                }

    return jsonify(endpoints), 200


@app.route('/twitter/api/v1/users/followers', methods=['GET'])
def user_followers():

    applog.debug("Listing users with more followers", extra={'method':'GET', 'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'endpoint': request.path })
    
    result = None

    try:

        result = twittcl.list_users_by_followers('DESC')

    except Exception as e:

        tb = traceback.format_exc()

        applog.error("Error when listing users with more followers", extra={'method':'GET', 'logger': __name__, 'level': 'error', 'uuid': current_request_id(), 'endpoint': request.path, 'trace': tb})
        
        return '{ "status": "500", "message": "Internal Server Error" }', 500

    return jsonify(result)


@app.route('/twitter/api/v1/publish/posts', methods=['POST'])
def publish_post():

    applog.debug("Publish new tweetts..", extra={'method':'POST', 'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'endpoint': request.path })

    result = None

    data = request.json

    try:

        if twittcl.publish(data):
            retult = "{ 'status': 'success' }"
        else:
            retult = "{ 'status': 'failed' }"

    except Exception as e:

        tb = traceback.format_exc()

        applog.error("Error when publish new tweets", extra={'method':'POST', 'logger': __name__, 'level': 'error', 'uuid': current_request_id(), 'endpoint': request.path, 'trace': tb })
        
        return jsonify('{ "status": "500", "message": "Internal Server Error" }'), 500

    return jsonify(result)


@app.route('/twitter/api/v1/posts/hour', methods=['GET'])
def posts_hour():

    applog.debug("List posts per hour", extra={'method':'GET', 'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'endpoint': request.path })
    
    result = None

    try:

        result = twittcl.total_posts_by_hour()

    except Exception as e:

        tb = traceback.format_exc()

        applog.error("Error when listing posts by time of publication", extra={'method':'GET', 'logger': __name__, 'level': 'error', 'uuid': current_request_id(), 'endpoint': request.path, 'trace': tb })
        
        return '{ "status": "500", "message": "Internal Server Error" }', 500

    return jsonify(result)


@app.route('/twitter/api/v1/posts/tags/<group>', methods=['GET'])
def posts_tags(group):

    applog.debug("List posts group %s" % group, extra={'method':'GET', 'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'endpoint': request.path })
    
    result = None

    if group == "location" or  group == "lang":

        applog.info("get total post by tag", extra={'logger': __name__, 'level': 'info', 'uuid': current_request_id(), 'endpoint': request.path })
        
        try:

            result = twittcl.total_posts_by_tag(group)

        except Exception as e:

            tb = traceback.format_exc()

            applog.error("Error when listing posts by time of publication", extra={'method':'GET', 'logger': __name__, 'level': 'error', 'uuid': current_request_id(), 'endpoint': request.path , 'trace': tb})
            
            return '{ "status": "500", "message": "Internal Server Error" }', 500

        return jsonify(result)

    else:

        applog.warning("Invalid group %s" % group, extra={'method':'GET', 'logger': __name__, 'level': 'warning', 'uuid': current_request_id(), 'endpoint': request.path })
        
        return '{ "status": "400", "message": "Bad request!" }', 400


@app.after_request
def after_request(response):

    response.headers.add('x-request-id', current_request_id())

    applog.info("Request", extra={'method':request.method, 'logger': __name__, 'level': 'info', 'uuid': current_request_id(), 'endpoint': request.path, 'status_code': response.status_code })
    
    return response


if __name__ == "__main__":

    app.run(host='0.0.0.0')