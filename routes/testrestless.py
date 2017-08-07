#!/bin/python
#-*- coding:utf-8 -*-

from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from flask import send_file
from flask_restless import APIManager

# restless = APIManager(app, flask_sqlalchemy_db=db)
from app import restless
from models.topic import Topic

# _url_prefix = '/topic/show'

customer_info_export_bp = Blueprint('topic', __name__)


customer_info_export_bp = restless.create_api_blueprint(Topic
                    , collection_name="show"
                    , methods=['GET']
                    , exclude_columns=['']
                    , url_prefix='/rest'
                    , preprocessors={"GET_MANY": []}
                    , postprocessors={"GET_MANY": []}
                )


import json
def add(response):
    data = response.data.decode()
    topics = json.loads(data).get('objects')
    return send_file('a.txt',as_attachment=True, attachment_filename='customer')


customer_info_export_bp.after_request(add)