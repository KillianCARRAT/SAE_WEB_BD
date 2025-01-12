from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SelectField, DateField, FloatField, IntegerField, TextAreaField, SubmitField, TimeField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

class AjoutSeance(FlaskForm):
    id = HiddenField('id')
    jour_seance = SelectField('Jour de la semaine', choices=[(1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi'), (7, 'Dimanche')], coerce=int, validators=[DataRequired()])
    heure_debut_seance = TimeField('Heure de début', validators=[DataRequired()])
    heure_fin_seance = TimeField('Heure de fin', validators=[DataRequired()])
    nb_places_seance = IntegerField('Nombre de places', validators=[DataRequired()])
    moniteur_id = SelectField('Moniteur', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ajouter')

