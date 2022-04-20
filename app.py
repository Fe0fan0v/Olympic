from flask import Flask, render_template, redirect, jsonify, request, send_file, url_for
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
ANSWERS = {'first': {'cltkfkltkjuekzqcvtkj': 1, '13240': 2, '57.92.113.225': 3, '2_3_5_7_11_12_13': 4, '249': 5},
           'second': {'E:\\VitalikRogalik\important\secret.png': 1, 'algoritm': 2, 'CHALLENGE': 3, '5RGB': 4, '10101': 5},
           'third': {'Scientia potentia est': 1, '2640': 2, '49837': 3, '1961': 4, '141,43': 5},
           'fourth': {'224': 1, '11:40': 2, 'journey': 3, '7_1010100': 4, '3336': 5}
           }


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
            block_number = data['block_number']
            answer = data['answer']
            if (block_number == 'first') and (answer in ANSWERS[block_number]):
                team.first_block_answer = answer
            elif block_number == 'second' and answer in ANSWERS[block_number]:
                team.second_block_answer = answer
            elif block_number == 'third' and answer in ANSWERS[block_number]:
                team.third_block_answer = answer
            elif block_number == 'fourth' and answer in ANSWERS[block_number]:
                team.fourth_block_answer = answer
            else:
                message = 'Неверный ответ!'
                return redirect(url_for('/tasks', message=message))
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


@app.route('/tasks/<message>', methods=['GET'])
def get_message(message):
    print(message)
    team = current_user
    return render_template('tasks.html', title='Задания', team=team, message=message)


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
