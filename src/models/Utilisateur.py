from src.app import db, login_manager
from flask_security import UserMixin
import uuid

class Utilisateur(db.Model, UserMixin):
    __tablename__ = "UTILISATEUR"

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(50))
    prenom_utilisateur = db.Column(db.String(50))
    tel_utilisateur = db.Column(db.Text)
    poids_utilisateur = db.Column(db.Integer)
    email_utilisateur = db.Column(db.String(120), unique=True)
    mdp_utilisateur = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE.id_role'))
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, default=lambda: str(uuid.uuid4()))
    
    # Pour un élève
    les_reservations = db.relationship("Reservation", back_populates="utilisateur", lazy=True)
    
    # Pour un moniteur
    les_seances = db.relationship("Seance", back_populates="moniteur", lazy=True)

    les_contacts = db.relationship('Contact', back_populates='utilisateur', lazy=True)
    
    def is_admin(self):
        return self.role.name == 'Administrateur'
    
    def is_moniteur(self):
        return self.role.name == 'Moniteur'
    
    def is_adhérent(self):
        return self.role.name == 'Adhérent'

    @classmethod
    def get_by_fs_uniquifier(cls, fs_uniquifier):
        return cls.query.filter_by(fs_uniquifier=fs_uniquifier).first()

    def get_last_id():
        id = 0
        users = Utilisateur.query.all()
        for user in users:
            if user.id_utilisateur > id:
                id = user.id_utilisateur
        return id