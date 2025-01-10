from src.app import db

class Reservation_Seance(db.Model):
    __tablename__ = "RESERVATION_SEANCE"
    id_seance = db.Column(db.Integer, db.ForeignKey('SEANCE.id_seance'), primary_key=True)
    id_reservation = db.Column(db.Integer, db.ForeignKey('RESERVATION.id_reservation'), primary_key=True)
    
    seance = db.relationship('Seance', back_populates='les_reservations', lazy=True)
    reservation = db.relationship("Reservation", back_populates="seance", lazy=True, overlaps="reservation")