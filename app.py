from flask import Flask, render_template, redirect, jsonify, request, send_file
from forms import RegisterForm, Task1, Task2, Task3, Task4
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from data.models import Team
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
           'second': {'E:\\VitalikRogalik\important\secret.png': 1, 'algoritm': 2, 'CHALLENGE': 3, '5RGB': 4,
                      '10101': 5},
           'third': {'Scientia potentia est': 1, '2640': 2, '49837': 3, '1961': 4, '141,43': 5},
           'fourth': {'224': 1, '11:40': 2, 'journey': 3, '7_1010100': 4, '3336': 5}
           }


def save(team):
    db_sess = db_session.create_session()
    team = db_sess.merge(team)
    db_sess.add(team)
    db_sess.commit()


def clear_inputs(tasks):
    for i in tasks:
        i.answer.data = ''


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
    all_tasks = (task1, task2, task3, task4)
    team = current_user
    if task1.validate_on_submit():
        answer = task1.answer.data
        if answer in ANSWERS['first']:
            team.first_block_answer = answer
            message = 'Ответ принят'
            clear_inputs(all_tasks)
            save(team)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            clear_inputs(all_tasks)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
    if task2.validate_on_submit():
        answer = task2.answer.data
        if answer in ANSWERS['second']:
            team.second_block_answer = answer
            message = 'Ответ принят'
            clear_inputs(all_tasks)
            save(team)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            clear_inputs(all_tasks)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
    if task3.validate_on_submit():
        answer = task3.answer.data
        if answer in ANSWERS['third']:
            team.third_block_answer = answer
            message = 'Ответ принят'
            clear_inputs(all_tasks)
            save(team)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            clear_inputs(all_tasks)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
    if task4.validate_on_submit():
        answer = task4.answer.data
        if answer in ANSWERS['fourth']:
            team.fourth_block_answer = answer
            message = 'Ответ принят'
            clear_inputs(all_tasks)
            save(team)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
        else:
            message = 'Ответ неверный'
            clear_inputs(all_tasks)
            return render_template('tasks.html', title='Задания', team=team, message=message, task1=task1, task2=task2,
                                   task3=task3, task4=task4)
    return render_template('tasks.html', title='Задания', team=team, task1=task1, task2=task2, task3=task3, task4=task4)


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
