from flask import Flask, render_template, redirect, jsonify, request, send_file
from forms import RegisterForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models import Task, Part
from data import db_session
from data.models import Team, Task
import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_duper_secret_key'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
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
                    if team.tasks_done:
                        return render_template('login.html', title='Вход', form=form, message='Вы уже сдали задание')
                    time = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=30)
                    team.deadline = list(map(int, time.strftime("%Y-%m-%d-%H-%M-%S").split("-")))
                    team.timer_started = True
                    team.tasks_done = False
                    db_sess.add(team)
                    db_sess.commit()
                    login_user(team)
                    return redirect('/download')
                else:
                    login_user(team)
                    return redirect('/tasks')
            else:
                return render_template('login.html', title='Вход', form=form,
                                       message='Неверный номер школы')
        else:
            return render_template('login.html', title='Вход', form=form, message='Такой команды не зарегистрировано')
    return render_template('login.html', title='Вход', form=form)


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        if request.data:
            team = current_user
            data = request.get_json()
            if data['block_number'] == 1:
                team.first_task_complete = True
            elif data['block_number'] == 2:
                team.second_task_complete = True
            elif data['block_number'] == 3:
                team.third_task_complete = True
            elif data['block_number'] == 4:
                team.fourth_task_complete = True
            db_sess = db_session.create_session()
            team = db_sess.merge(team)
            db_sess.add(team)
            db_sess.commit()
            return redirect('/tasks')
        else:
            team = current_user
            return render_template('tasks.html', title='Задания', team=team)
    else:
        team = current_user
        return render_template('tasks.html', title='Задания', team=team)


@app.route('/stop_time')
def stop_time():
    db_sess = db_session.create_session()
    team = db_sess.query(Team).filter(Team.name == current_user.name).first()
    team.timer_started = False
    team.deadline = None
    team.tasks_done = True
    db_sess.add(team)
    db_sess.commit()
    print(f'team {team.name} stopped')
    return jsonify({'success': 'OK'})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/download', methods=['GET'])
def download():
    if request.method == 'GET':
        file_path = 'files/tasks.zip'
        return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run()
