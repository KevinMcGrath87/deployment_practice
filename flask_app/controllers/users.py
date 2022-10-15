from flask_app.__init__ import app
from flask import render_template, request, flash, redirect, session
from flask_app.models import user

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/register', methods = ['POST'])
def register():
    data = request.form.to_dict()
    if user.User.validate(data):
        newUser = user.User.insertUser(data)
        session['user'] = newUser
        return(redirect('/recipes'))
    else:
        return(redirect('/'))

@app.route('/login', methods = ['POST'])
def login():
    data = request.form.to_dict()
    if user.User.validate_login(data):
        newUser = user.User.getUserByEmail(data['email'])
        session['user'] = newUser.id
        return(redirect('/recipes'))
    else:
        return(redirect('/'))

@app.route('/logout')
def logout():
    session.clear()
    return(redirect('/'))


