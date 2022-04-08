from flask import Flask, render_template, redirect
from forms import RegisterForm, TaskForm
from flask_login import LoginManager, login_user, current_user, login_required
from models import Task, Part
from data import db_session
from data.models import Team, Task


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_duper_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(team_id):
    db_sess = db_session.create_session()
    return db_sess.query(Team).get(team_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    db_session.global_init("base.db")
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        team = form.team.data
        school = form.school.data
        team = Team(name=team, school=school)
        db_sess.add(team)
        db_sess.commit()
        login_user(team, remember=True)
        return redirect('/tasks')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/tasks')
@login_required
def tasks():
    team = current_user
    form = TaskForm()
    if form.validate_on_submit():
        answer1 = form.part1_answer.data
        answer2 = form.part2_answer.data
        answer3 = form.part3_answer.data
        answer4 = form.part4_answer.data
        db_sess = db_session.create_session()
        
    return render_template('tasks.html', title='Задания', team=team, form=form)


app.run()
