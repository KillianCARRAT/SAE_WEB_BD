from src.app import db

class Poney(db.Model):
    __tablename__ = "PONEY"

    id_poney = db.Column(db.Integer, primary_key=True)
    nom_poney = db.Column(db.Text)
    capacite_poney = db.Column(db.Integer)

    les_reservations = db.relationship('Reservation', back_populates='poney', lazy=True)