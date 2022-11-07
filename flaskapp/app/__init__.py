import os
from flask import Flask
from flask_mail import Mail
from zksync_sdk import ZkSyncLibrary
from datetime import datetime
from .extensions import db, migrate

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
    
    
    with app.app_context():
      db.init_app(app)
      db.create_all()
        
    # migrate.init_app(app, db)

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
    from app.user import user_blueprint
    from app.main import main_blueprint
    from app.register_wallet import register_wallet_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(register_wallet_blueprint, url_prefix="/register-wallet")
    app.register_blueprint(main_blueprint)

def initialize_extensions(app):
    mail.init_app(app)

def register_error_handlers(app):
  pass

def configure_logging(app):
  pass