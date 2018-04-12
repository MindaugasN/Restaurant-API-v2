# from flask_api import FlaskAPI
from flask_restful import Api
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from logging.handlers import RotatingFileHandler
import logging
import traceback
from time import strftime

from app.config import app_config


db = SQLAlchemy()

def create_app(config_name):
    from app.resources import Employee, EmployeeList
    from app.resources import Restaurant, RestaurantList
    from app.resources import Menu, TodayMenu
    from app.resources import GiveVote, Vote


    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.add_resource(Restaurant, '/restaurants') # POST
    api.add_resource(RestaurantList, '/restaurants/<int:id>') # GET
    api.add_resource(Employee, '/employees') # POST
    api.add_resource(EmployeeList, '/employees/<int:id>') # GET   
    api.add_resource(Menu, '/restaurants/menus') # POST
    api.add_resource(TodayMenu, '/menus') # GET
    api.add_resource(GiveVote, '/menus/<int:id>/votes') # PUT
    api.add_resource(Vote, '/votes') # GET

    # logging

    @app.after_request
    def after_request(response):
        ''' Logging after every request. '''
        # This avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler.
        if response.status_code != 500:
            ts = strftime('[%Y-%b-%d %H:%M]')
            logger.error('%s %s %s %s %s %s',
                        ts,
                        request.remote_addr,
                        request.method,
                        request.scheme,
                        request.full_path,
                        response.status)
        return response


    @app.errorhandler(Exception)
    def exceptions(e):
        ''' Logging after every Exception. '''
        ts = strftime('[%Y-%b-%d %H:%M]')
        tb = traceback.format_exc()
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                    ts,
                    request.remote_addr,
                    request.method,
                    request.scheme,
                    request.full_path,
                    tb)
        return 'Internal Server Error', 500

    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)

    return app