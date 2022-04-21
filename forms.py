from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    team = StringField('Название команды', validators=[DataRequired()])
    school = StringField('Номер школы', validators=[DataRequired()])
    submit = SubmitField('Войти')


class Task1(FlaskForm):
    answer = StringField('Ответ 1 блока', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class Task2(FlaskForm):
    answer = StringField('Ответ 2 блока', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class Task3(FlaskForm):
    answer = StringField('Ответ 3 блока', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class Task4(FlaskForm):
    answer = StringField('Ответ 4 блока', validators=[DataRequired()])
    submit = SubmitField('Отправить')


