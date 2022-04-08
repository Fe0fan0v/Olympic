from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class RegisterForm(FlaskForm):
    team = StringField('Название команды')
    school = StringField('Название школы')
    submit = SubmitField('Зарегистрироваться')
