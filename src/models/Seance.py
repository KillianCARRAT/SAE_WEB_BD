from src.app import db

class Seance(db.Model):
    __tablename__ = "SEANCE"
    id_seance = db.Column(db.Integer, primary_key=True)
    jour_seance = db.Column(db.Integer)
    heure_debut_seance = db.Column(db.Time)
    heure_fin_seance = db.Column(db.Time)
    nb_places_seance = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    moniteur_id = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))
    
    # Pour un moniteur
    moniteur = db.relationship("Utilisateur", back_populates="les_seances")
    
    # Pour un élève
    les_reservations = db.relationship("Reservation_Seance", back_populates="seance", lazy=True)