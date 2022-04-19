from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    team = StringField('Название команды', validators=[DataRequired()])
    school = StringField('Номер школы', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TaskForm(FlaskForm):
    part1_answer = StringField('Введите код первого раздела')
    part2_answer = StringField('Введите код второго раздела')
    part3_answer = StringField('Введите код третьего раздела')
    part4_answer = StringField('Введите код четвертого раздела')
    submit = SubmitField('Отправить')
