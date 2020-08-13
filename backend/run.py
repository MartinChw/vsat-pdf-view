from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.db import db, reset_database
from app.views.admin_views import ns as admin_view

app = Flask(__name__)

cors = CORS(app,
            supports_credentials=True,
            resources={
                r'/api/*': {
                    'origins': '*',
                    'allow_headers': ['Content-Type', 'Authorization']
                }
            })
app.register_blueprint(admin_view)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)
with app.app_context():
    reset_database()
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
