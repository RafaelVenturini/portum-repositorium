from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class NewsLetterForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar Mensagem')
