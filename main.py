from flask import Flask, render_template, request, redirect, url_for
from models import (
    db, 
    User, 
    Task, 
    TaskGroup, 
    user_task_m2m,
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# TODO: update database to postgresql
# initialize sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    get users
    get tasks
    get taskgroups
    """
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    taskgroups = db.session.execute(db.select(TaskGroup).order_by(TaskGroup.id)).scalars()

    return render_template('index.html', users=users, taskgroups=taskgroups)

@app.route('/add-task', methods=['POST'])
def add_task():
    text = request.form['task']
    task = Task(
        task=text
    )
    
    """
    get the taskgroup input
    add task to taskgroup
    display

    input: taskgroup index
    output: none

    index = 1
    output = none
    """
    index = request.form['taskgroup_id']
    taskgroup = db.session.get(TaskGroup, index)
    taskgroup.tasks.append(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit-task/<int:index0>/<int:index>')
def edit_task(index0, index):
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    taskgroups = db.session.execute(db.select(TaskGroup).order_by(TaskGroup.id)).scalars()

    return render_template('index.html', users=users, taskgroups=taskgroups, edit_index=(index0, index))

@app.route('/save-task', methods=['POST'])
def save_task():
    text = request.form['task']
    done = request.form['done']
    
    task = db.session.get(Task, request.form['id'])
    task.task = text
    task.done = True if done=='on' else False

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-task', methods=['POST'])
def delete_task():
    db.session.delete(db.get_or_404(Task, request.form['id']))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/check-task', methods=['POST'])
def check_task():
    task = db.session.get(Task, request.form['id'])
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index'))

"""function to show input form for adding user"""
@app.route('/add-user/<int:index0>/<int:index>')
def add_user(index0, index):
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    taskgroups = db.session.execute(db.select(TaskGroup).order_by(TaskGroup.id)).scalars()

    return render_template('index.html', users=users, taskgroups=taskgroups, adduser_index=(index0, index))

@app.route('/save-user', methods=['POST'])
def save_user():
    if request.method == 'POST':
        name = request.form['name']

        # get task
        task = db.session.get(Task, request.form['id'])

        # find user if there is
        try:
            user = db.session.execute(db.select(User).filter_by(name=name)).scalar_one()
        except:
            user = User(
                name = name
            )
        print(user)

        # add user to task
        task.users.add(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-user', methods=['POST'])
def delete_user():
    db.session.delete(db.session.get(User, request.form['id']))
    db.session.commit()
    return redirect(url_for('index'))

# APIs
@app.route('/api/createtask', methods=['POST'])
def createtask():
    if request.method == 'POST':
        task = Task(
            text=request.json['task']
        )
        db.session.add(task)
        db.session.commit()
        return {'code': 200}

@app.route('/api/createuser', methods=['POST'])
def createuser():
    if request.method == 'POST':
        user = User(
            name=request.json['name']
        )
        db.session.add(user)
        db.session.commit()
        return {'code': 200}
    
@app.route('/api/link-user-task', methods=['POST'])
def link_user_task():
    if request.method == 'POST':
        """
        get user
        get task
        link user and task
        commit

        how to get user and get task

        """
        pass
        return {'code': 200}
    pass

    
if __name__ == '__main__':
    app.run(debug=True)