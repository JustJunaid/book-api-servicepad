from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
import json


# ....getting data from config.json file.... #
with open('config.json','r') as config:
    fConfig= json.load(config)

BASE_URL = fConfig["BASE_URL"]

app = Flask(__name__)
app.config['SECRET_KEY'] = fConfig.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']= fConfig['PARAMS']['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# .....swagger conf.....#
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book Management API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



from bookAPI import routes
