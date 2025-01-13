from src.app import db

class Poney(db.Model):
    __tablename__ = "PONEY"

    id_poney = db.Column(db.Integer, primary_key=True)
    nom_poney = db.Column(db.Text)
    capacite_poney = db.Column(db.Integer)

    les_reservations = db.relationship('Reservation', back_populates='poney', lazy=True)

    def getPoney(poids, jour, heure, duree):
        poneys = Poney.query.all()
        for poney in poneys():
            if poney.capacite_poney >=poids and poney.getPause(jour, heure, duree):
                return poney
        return None
    
    def getPause(self, jour, heure, duree):
        for res in self.les_reservations:
            if res.seance.jour_seance == jour:
                if (res.seance.heure_fin_seance - heure) > -2 or ((heure+duree) - res.seance.heure_debut_seance) > -2:
                    return False
        return True

