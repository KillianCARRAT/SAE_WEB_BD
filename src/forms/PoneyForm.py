from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class PoneyForm(FlaskForm):
    id = HiddenField('id')
    nom = StringField('Nom', validators=[DataRequired()])
    capacite = IntegerField('Capacité', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
