from src.app import db

class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    id_poney = db.Column(db.Integer, db.ForeignKey('PONEY.id_poney'), primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'), primary_key=True)

    poney = db.relationship("Poney", back_populates="les_utilisateurs", lazy=True)
    utilisateur = db.relationship("Utilisateur", back_populates="les_poneys", lazy=True)