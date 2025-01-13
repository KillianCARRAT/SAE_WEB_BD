from flask_wtf import FlaskForm
from flask_security import current_user
from wtforms import StringField, HiddenField, FileField, PasswordField, RadioField
from wtforms.validators import DataRequired
from hashlib import sha256
from src.models.Role import Role
from src.models.Utilisateur import Utilisateur
from flask import current_app


class InscriptionForm(FlaskForm):
    id = HiddenField('id')
    nom_user = StringField('Nom', validators=[DataRequired()])
    prenom_user = StringField('Prenom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    confirmation_mot_de_passe = PasswordField('Confirmation mot de passe', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired()])
    role = RadioField('Role')
    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self, extra_validators=extra_validators):
            return False
        if self.mot_de_passe.data != self.confirmation_mot_de_passe.data:
            self.confirmation_mot_de_passe.errors.append('Les mots de passe ne correspondent pas')
            return False
        if Utilisateur.query.filter_by(email_utilisateur=self.email.data).first():
            self.email.errors.append('Un utilisateur existe déjà avec cette adresse mail')
            return False
        return True

class ConnexionForm(FlaskForm):
    id=HiddenField('id')
    email=StringField('Adresse mail', validators=[DataRequired()])
    mot_de_passe=PasswordField('Mot de passe', validators=[DataRequired()])
    def get_authenticated_user(self):
        u = Utilisateur.query.filter_by(email_utilisateur=self.email.data).first()
        if u and u.mdp_utilisateur == sha256(self.mot_de_passe.data.encode()).hexdigest():
            return u
        return None
    
class UpdateUser(FlaskForm):
    id =HiddenField('id')
    nom_user = StringField("Nom", validators=[DataRequired()])
    prenom_user = StringField('Prenom', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired()])
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        user = current_user
        if user.email_utilisateur != self.email.data and Utilisateur.query.filter_by(email_utilisateur=self.email.data).first():
            self.email.errors.append('Un utilisateur existe déjà avec cette adresse mail')
            return False
        return True

class UpdatePassword(FlaskForm):
    id = HiddenField('id')
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmation mot de passe', validators=[DataRequired()])
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        user = current_user
        if sha256(self.current_password.data.encode()).hexdigest() != user.mdp_utilisateur:
            self.current_password.errors.append("Le mot de passe actuel ne correspond pas")
            return False
        if self.confirm_password.data != self.new_password.data:
            self.new_password.errors.append("Le nouveau mot de passe ne correspond pas à la confirmation")
            return False
        if self.current_password.data == self.new_password.data:
            self.new_password.errors.append("Le nouveau mot de passe est le même le l'ancien")
            return False
        return True
