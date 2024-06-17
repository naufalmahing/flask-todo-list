from flask import Flask, render_template, request, redirect, url_for
from models import (
    db, 
    User, 
    Task, 
    TaskGroup, 
    user_task_m2m,
)

app = Flask(__name__)

# TODO: update database to postgresql
# initialize sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project1.db'
db.init_app(app)

with app.app_context():
    db.create_all()

# TODO: update routes to not include index parameter
@app.route('/')
def index():
    """
    get users
    get tasks
    get taskgroups
    """
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    todos = db.session.execute(db.select(Task).order_by(Task.id)).scalars()
    # TODO: get taskgroups
    # TODO: link user and task
    print(users)

    return render_template('index.html', todos=todos, users=users)

@app.route('/add-task', methods=['POST'])
def add_task():
    text = request.form['task']
    task = Task(
        task=text
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit-task/<int:index>')
def edit_task(index):
    todos = db.session.execute(db.select(Task).order_by(Task.id)).scalars()
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()

    return render_template('index.html', todos=todos, users=users, edit_index=index)

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
@app.route('/add-user/<int:index>')
def add_user(index):
    todos = db.session.execute(db.select(Task).order_by(Task.id)).scalars()
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()

    return render_template('index.html', todos=todos, users=users, adduser_index=index)

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