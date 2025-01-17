from src.app import db

class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    id_reservation = db.Column(db.Integer, primary_key=True)
    id_poney = db.Column(db.Integer, db.ForeignKey('PONEY.id_poney'))
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))
    id_seance = db.Column(db.Integer, db.ForeignKey('SEANCE.id_seance'))

    poney = db.relationship("Poney", back_populates="les_reservations", lazy=True)
    utilisateur = db.relationship("Utilisateur", lazy=True)
    seance = db.relationship("Seance", lazy=True)
