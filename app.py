from flask import Flask, render_template, redirect, jsonify, request, send_file, make_response
from forms import RegisterForm, Task1, Task2, Task3, Task4
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from data.models import Team
import datetime
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_duper_secret_key'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)


def create_table():
    sess = db_session.create_session()
    teams = [['admin', 'itcube'], ['Prosti esli', '4'], ['Za Россию', '6'], ['Минус три богатыря', '7'],
             ['Комби', '10'],
             ['Отряд Страуструпа', '16'], ['Стрела', '17'], ['Питекантропы', '18'], ['Победа', '19']]
    for name, school in teams:
        if not sess.query(Team).filter(Team.name == name).first():
            team = Team(name=name, school=school)
            sess.add(team)
    sess.commit()


ANSWERS = {'first': {'cltkfkltkjuekzqcvtkj': 1, '13240': 2, '57.92.113.225': 3, '2_3_5_7_11_12_13': 4, '249': 5},
           'second': {r'E:\\VitalikRogalik\important\secret.png': 1, 'algoritm': 2, 'CHALLENGE': 3, '5RGB': 4,
                      '10101': 5},
           'third': {'Scientia potentia est': 1, '2640': 2, '49837': 3, '1961': 4, '141,43': 5},
           'fourth': {'224': 1, '11:40': 2, 'journey': 3, '7_1010100': 4, '3336': 5}
           }


def check_progress(team):
    if team.first_block_answer:
        team.scores += ANSWERS['first'][team.first_block_answer]
    if team.second_block_answer:
        team.scores += ANSWERS['second'][team.second_block_answer]
    if team.third_block_answer:
        team.scores += ANSWERS['third'][team.third_block_answer]
    if team.fourth_block_answer:
        team.scores += ANSWERS['fourth'][team.fourth_block_answer]
    return team.scores if team.scores else 0


def save(team):
    db_sess = db_session.create_session()
    team = db_sess.merge(team)
    db_sess.add(team)
    db_sess.commit()


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
        if name == 'admin' and school == 'itcube':
            login_user(team)
            return redirect('/get_results')
        if team:
            if team.school == school:
                if not team.timer_started:
                    if team.tasks_done:
                        return render_template('login.html', title='Вход', form=form, message='Вы уже сдали задание')
                    time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                    team.deadline = list(map(int, time.strftime("%Y-%m-%d-%H-%M-%S").split("-")))
                    team.timer_started = True
                    team.tasks_done = False
                    db_sess.add(team)
                    db_sess.commit()
                    login_user(team)
                    return redirect('/tasks')
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
    task1, task2, task3, task4 = Task1(), Task2(), Task3(), Task4()
    team = current_user
    if task1.validate_on_submit():
        answer = task1.answer1.data
        if answer in ANSWERS['first']:
            if ANSWERS['first'][answer] > ANSWERS['first'].get(team.first_block_answer, 0):
                team.first_block_answer = answer
                message = 'Ответ принят'
                team.scores = check_progress(team)
                team.last_answer = datetime.datetime.now()
                task1.clear()
                save(team)
            else:
                message = 'Такой ответ уже принят'
                task1.clear()
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            task1.clear()
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
    if task2.validate_on_submit():
        answer = task2.answer2.data
        if answer in ANSWERS['second']:
            if ANSWERS['second'][answer] > ANSWERS['second'].get(team.second_block_answer, 0):
                team.second_block_answer = answer
                message = 'Ответ принят'
                team.scores = check_progress(team)
                team.last_answer = datetime.datetime.now()
                task2.clear()
                save(team)
            else:
                message = 'Такой ответ уже принят'
                task2.clear()
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            task2.clear()
        return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                               task3=task3, task4=task4)
    if task3.validate_on_submit():
        answer = task3.answer3.data
        if answer in ANSWERS['third']:
            if ANSWERS['third'][answer] > ANSWERS['third'].get(team.third_block_answer, 0):
                team.third_block_answer = answer
                message = 'Ответ принят'
                team.scores = check_progress(team)
                team.last_answer = datetime.datetime.now()
                task3.clear()
                save(team)
            else:
                message = 'Такой ответ уже принят'
                task3.clear()
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            task3.clear()
        return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                               task3=task3, task4=task4)

    if task4.validate_on_submit():
        answer = task4.answer4.data
        if answer in ANSWERS['fourth']:
            if ANSWERS['fourth'][answer] > ANSWERS['fourth'].get(team.fourth_block_answer, 0):
                team.fourth_block_answer = answer
                message = 'Ответ принят'
                team.scores = check_progress(team)
                team.last_answer = datetime.datetime.now()
                task4.clear()
                save(team)
            else:
                message = 'Такой ответ уже принят'
                task4.clear()
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            task4.clear()
        return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                               task3=task3, task4=task4)

    return render_template('tasks.html', title='Задания', team=team, task1=task1, task2=task2,
                           task3=task3, task4=task4)


@app.route('/stop_time')
def stop_time():
    db_sess = db_session.create_session()
    team = db_sess.query(Team).filter(Team.name == current_user.name).first()
    team.timer_started = False
    team.deadline = None
    team.tasks_done = True
    team.scores = check_progress(team)
    save(team)
    return make_response(jsonify({'success': 'OK'}), 200)


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


@app.route('/get_results', methods=['POST', 'GET'])
@login_required
def get_results():
    if current_user.name == 'admin' and current_user.school == 'itcube':
        db_sess = db_session.create_session()
        team_list = sorted(filter(lambda x: x.last_answer, db_sess.query(Team).all()),
                           key=lambda x: (-x.scores, x.last_answer))
        return render_template('results.html', team_list=team_list, title='Результаты')


if __name__ == '__main__':
    db_session.global_init('base.db')
    create_table()
    serve(app, host='0.0.0.0', port=5000)
