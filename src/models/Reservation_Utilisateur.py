from src.app import db

class Reservation_Utilisateur(db.Model):
    __tablename__ = "RESERVATION_UTILISATEUR"
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'), primary_key=True)
    id_reservation = db.Column(db.Integer, db.ForeignKey('RESERVATION.id_reservation'), primary_key=True)

    utilisateur = db.relationship('Utilisateur', back_populates='les_reservations', lazy=True)
    reservation = db.relationship("Reservation", back_populates="les_reservations", lazy=True, overlaps="utilisateur")