from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    id = HiddenField('id')
    concerne = SelectField('Personne à contacter', choices=[(1,"Moniteur"), (2, "Administrateur")], coerce=int, validators=[DataRequired()])
    sujet = StringField('Sujet', validators=[DataRequired()])
    contenu = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField('Envoyer')
    
