from flask import Flask, render_template, redirect
from forms import RegisterForm, TaskForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models import Task, Part
from data import db_session
from data.models import Team, Task
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_duper_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("base.db")


@login_manager.user_loader
def load_user(team_id):
    db_sess = db_session.create_session()
    return db_sess.query(Team).get(team_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        name = form.team.data
        school = form.school.data
        team = db_sess.query(Team).filter(Team.name == name).first()
        if team:
            if team.school == school:
                if not team.timer_started:
                    time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    team.deadline = list(map(int, time.strftime("%Y-%m-%d-%H-%M-%S").split("-")))
                    team.timer_started = True
                    db_sess.add(team)
                    db_sess.commit()
                    login_user(team, remember=True)
                    return redirect('/tasks')
                else:
                    login_user(team, remember=True)
                    return redirect('/tasks')
            else:
                return render_template('login.html', title='Вход', form=form,
                                       message='Неверный номер школы')
        else:
            return render_template('login.html', title='Вход', form=form, message='Такой команды не зарегистрировано')
    return render_template('login.html', title='Вход', form=form)


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
    return render_template('tasks.html', title='Задания', team=team, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()
