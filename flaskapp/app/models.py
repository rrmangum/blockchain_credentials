from datetime import datetime
from .extensions import db
from flask_appbuilder import Model
from flask_login import UserMixin
from flask_appbuilder.models.mixins import ImageColumn

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    profile_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Wallet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(100), unique=True, nullable=False)
    last_connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    role_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Issuance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credential_id = db.Column(db.Integer, db.ForeignKey('credential.id'), nullable=False)
    expires_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)