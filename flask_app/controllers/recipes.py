from flask_app.__init__ import app
from flask_app.models import recipe as ratcipe
from flask_app.models import user as luser
from flask import render_template, request, flash, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
# user switch to luser and recipe module switcht to ratcipe
@app.route('/recipes')
def recipes():
    if session:
        user = luser.User.getUserById(session['user'])
        recipes = ratcipe.Recipe.get_all()
        return(render_template('recipes.html', recipes = recipes, user = user))
    else:
        return(redirect('/'))

@app.route('/new_recipe')
def recipe_form():
    user = luser.User.getUserById(session['user'])
    return(render_template('new_recipe.html',user = user))

@app.route('/new_recipe_submit', methods = ['POST'])
def new_recipe():
    data = request.form.to_dict()
    if session:
        if ratcipe.Recipe.validate_recipe(data):
            data['user_id']=session['user']
            ratcipe.Recipe.create_recipe(data)
            return(redirect('/recipes'))
    return(redirect('/new_recipe'))

@app.route('/edit/<int>')
def edit_recipe(int):
    if session:
        data = {'id': int}
        recipe = ratcipe.Recipe.get_recipe_by_id(data)
        return(render_template('edit_recipe.html',recipe = recipe))
    else:
        return(redirect('/'))

@app.route('/update_recipe', methods = ['POST'])
def update():
    data = request.form
    if ratcipe.Recipe.validate_recipe(data):
        ratcipe.Recipe.update_recipe(data)
        return(redirect('/recipes'))
    else:
        id = data['id']
        string = f'/edit/{id}'
        return(redirect(string))


@app.route('/view_recipe/<int>')
def view_recipe(int):
    if session:
        data = {'id': int}
        recipe = ratcipe.Recipe.get_recipe_by_id(data)
        return(render_template('view_recipe.html', recipe = recipe, current = luser.User.getUserById(session['user'])))
    else:
        return(redirect('/'))

@app.route('/delete/<int>')
def delete(int):
    data = {'id': int}
    print(data)
    ratcipe.Recipe.delete_recipe(data)
    return(redirect('/recipes'))



