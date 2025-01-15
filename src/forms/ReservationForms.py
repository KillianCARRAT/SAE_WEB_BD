from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SelectField, DateField, FloatField, IntegerField, TextAreaField, SubmitField, TimeField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

class AjoutSeance(FlaskForm):
    id = HiddenField('id')
    semaine_seance = DateField('Jour exact', format='%Y-%m-%d')
    jour_seance = SelectField('Jour de la semaine', choices=[(1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi'), (7, 'Dimanche')], coerce=int)
    heure_debut_seance = TimeField('Heure de début', validators=[DataRequired()])
    heure_fin_seance = TimeField('Heure de fin', validators=[DataRequired()])
    nb_places_seance = IntegerField('Nombre de places', validators=[DataRequired()])
    moniteur_id = SelectField('Moniteur', coerce=int, validators=[DataRequired()])
    hebdomadaire_seance = BooleanField('Hebdomadaire')
    date_debut_seance = DateField('Date de début', format='%Y-%m-%d')
    date_fin_seance = DateField('Date de fin', format='%Y-%m-%d')
    submit = SubmitField('Ajouter')
    def validate(self, extra_validators = None):
        return True