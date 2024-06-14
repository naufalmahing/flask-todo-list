from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = []

todos.append({
    'task': 'sample', 'done': False
})

todos.append({
    'task': 'sample', 'done': True
})

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['task']
    todos.append({'task': todo, 'done': False})
    return redirect(url_for('index'))

@app.route('/edit/<int:index>')
def edit(index):
    return render_template('index.html', todos=todos, edit_index=index)

@app.route('/save/<int:index>', methods=['POST'])
def save(index):
    pass
    todo = request.form['task']
    done = request.form['done']
    # print(done)
    todos[index] = {'task': todo, 'done': True if done=='on' else False}
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    del todos[index]
    return redirect(url_for('index'))

@app.route('/check/<int:index>', methods=['POST'])
def check(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

"""
Features
create
read 
update 
delete

check to strikethrough the text
- gotta check flask documentation
edit in same page

later after first commit
use database

additionals
use owner
use datetime
"""