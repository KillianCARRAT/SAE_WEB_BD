from src.app import db
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = 'ROLE'
    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    users = db.relationship('Utilisateur', backref='role')