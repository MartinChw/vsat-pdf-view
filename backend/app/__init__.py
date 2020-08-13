import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import ProductionConfig
from app.db import db, reset_database


jwt = JWTManager()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__)

    cors = CORS(app,
                supports_credentials=True,
                resources={
                    r'/api/*': {
                        'origins': '*',
                        'allow_headers': ['Content-Type', 'Authorization']
                    }
                })
    from app.views.admin_views import ns as admin_view
    app.register_blueprint(admin_view)
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    UPLOAD_FOLDER = '/uploads'
    app.config.from_object(ProductionConfig)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.getcwd()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    scheduler.init_app(app)
    scheduler.start()
    return app
