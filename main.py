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
    return render_template('index.html', todos=todos, edit_index=index)

@app.route('/save-task/<int:index>', methods=['POST'])
def save_task(index):
    text = request.form['task']
    done = request.form['done']
    
    task = db.session.get(Task, index+1)
    task.task = text
    task.done = True if done=='on' else False

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-task/<int:index>')
def delete_task(index):
    db.session.delete(db.get_or_404(Task, index+1))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/check-task/<int:index>', methods=['POST'])
def check_task(index):
    task = db.session.get(Task, index+1)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add-user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        user = User(
            name = name
        )
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-user/<int:index>')
def delete_user(index):
    db.session.delete(db.session.get(User, index+1))
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