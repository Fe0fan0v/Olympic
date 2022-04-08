from flask import Flask, render_template, redirect
from forms import RegisterForm
from flask_login import LoginManager, login_user, current_user
from models import Team, Task, Part

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_duper_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Team.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = RegisterForm()
    if form.validate_on_submit():
        team = form.team.data
        school = form.school.data
        team = Team(team, school)
        login_user(team, remember=True)
        print('User logined')
        return redirect('/tasks')
    return render_template('register.html', title='Регистрация', form=form)


app.run()