import os
from flask import Flask
from flask_mail import Mail
from zksync_sdk import ZkSyncLibrary

## initialize ZKsync SDK
lib = ZkSyncLibrary()

### Flask extension objects instantiation ###
mail = Mail()

### Application Factory ###
def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app

### Helper Functions ###
def register_blueprints(app):
    from app.auth import auth_blueprint
    from app.main import main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/users')
    app.register_blueprint(main_blueprint)

def initialize_extensions(app):
    mail.init_app(app)

def register_error_handlers(app):
  pass

def configure_logging(app):
  pass