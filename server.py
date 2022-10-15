from flask_app.__init__ import app
from flask import render_template, request, session, flash, redirect
from flask_app.controllers import users, recipes


if __name__=='__main__':
    app.run(debug = True)
