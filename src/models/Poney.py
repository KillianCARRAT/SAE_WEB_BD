from src.app import db
from datetime import datetime, date

class Poney(db.Model):
    __tablename__ = "PONEY"

    id_poney = db.Column(db.Integer, primary_key=True)
    nom_poney = db.Column(db.Text)
    capacite_poney = db.Column(db.Integer)

    les_reservations = db.relationship('Reservation', back_populates='poney', lazy=True)

    def getPoney(poids, seance):
        poneys = Poney.query.all()
        for poney in poneys:
            if int(poney.capacite_poney) >= int(poids) and poney.getPause(seance):
                return poney
        return None
    
    def getPause(self, seance):
        for res in self.les_reservations:
            for s in res.seance:
                # Combiner les heures avec une date fictive
                heure_fin_s = datetime.combine(date.today(), s.seance.heure_fin_seance)
                heure_debut_seance = datetime.combine(date.today(), seance.heure_debut_seance)
                heure_fin_seance = datetime.combine(date.today(), seance.heure_fin_seance)
                heure_debut_s = datetime.combine(date.today(), s.seance.heure_debut_seance)

                # Calculer les différences et appliquer les conditions
                if (heure_fin_s - heure_debut_seance).total_seconds() > -2 * 3600 or (heure_fin_seance - heure_debut_s).total_seconds() > -2 * 3600:
                    return False
        return True

