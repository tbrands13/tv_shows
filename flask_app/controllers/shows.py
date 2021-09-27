from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.show import Show
from flask_app.models.user import User


@app.route('/new')
def add():
    return render_template('newshow.html')


@app.route('/show/add', methods=['POST'])
def add_show():
    if not Show.validate_show(request.form):
        return redirect('/new')
    data = {
        "title" : request.form['title'],
        "network" : request.form['network'],
        "release_date" : request.form['release_date'],
        "description" : request.form['description'],
        "user_id" : session['user_id'],
    }
    print(request.form)
    Show.create_show(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def display_show(id):
    data = {
        'id' : id
    }
    user = User.one_user()
    show= Show.one_show(data)
    return render_template('display.html', show = show)


@app.route('/update/show', methods=['POST'])
def update_show():
    if not Show.validate_show(request.form):
        return redirect(f"/edit/shows/{request.form['id']}")
    data = {
        'id' : request.form['id'],
        'title' : request.form['title'],
        'network' : request.form['network'],
        'release_date' : request.form['release_date'],
        'description' : request.form['description'],
        'updated_at' : request.form['updated_at']
    }
    show = Show.update_show(data)
    return redirect(f"/show/{data['id']}")


@app.route('/edit/shows/<int:id>')
def edit_show(id):
    data = {
        'id' : id
    }
    show = Show.one_show(data)
    return render_template('editshow.html', show = show)

@app.route('/shows/<id>/destroy')
def delete_show(id):
    data = {
        'id' : id
    }
    Show.delete_show(data)
    return redirect('/dashboard')
