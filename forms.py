from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    team = StringField('Название команды', validators=[DataRequired()])
    school = StringField('Номер школы', validators=[DataRequired()])
    submit = SubmitField('Войти')


class Task1(FlaskForm):
    answer1 = StringField('Ответ 1 блока', validators=[DataRequired()])
    submit1 = SubmitField('Отправить')

    def clear(self):
        self.answer1.data = ''


class Task2(FlaskForm):
    answer2 = StringField('Ответ 2 блока', validators=[DataRequired()])
    submit2 = SubmitField('Отправить')

    def clear(self):
        self.answer2.data = ''


class Task3(FlaskForm):
    answer3 = StringField('Ответ 3 блока', validators=[DataRequired()])
    submit3 = SubmitField('Отправить')

    def clear(self):
        self.answer3.data = ''


class Task4(FlaskForm):
    answer4 = StringField('Ответ 4 блока', validators=[DataRequired()])
    submit4 = SubmitField('Отправить')

    def clear(self):
        self.answer4.data = ''

