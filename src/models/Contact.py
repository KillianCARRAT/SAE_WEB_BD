from src.app import db

class Contact(db.Model):
    __tablename__ = "CONTACT"

    id_contact = db.Column(db.Integer, primary_key=True)
    concerne = db.Column(db.Text)
    sujet = db.Column(db.Text)
    contenu = db.Column(db.Text)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))

    utilisateur = db.relationship("Utilisateur", back_populates="les_contacts", lazy=True)
    
