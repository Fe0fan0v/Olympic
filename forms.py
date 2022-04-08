from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    team = StringField('Название команды', validators=[DataRequired()])
    school = StringField('Название школы', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
