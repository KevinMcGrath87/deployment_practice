from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.db = 'recipes'
        self.id = data['id']
        self.under = data['under']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = None
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id'
        result = connectToMySQL('recipes').query_db(query)
        recipe_list = []
        for recipe in result:
            print(recipe)
            recipeObj = cls(recipe)
            recipeObj.user_name = recipe['first_name']
            recipe_list.append(recipeObj)
        return (recipe_list)

    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s'
        result = connectToMySQL('recipes').query_db(query, data)
        recipeObj = cls(result[0])
        recipeObj.user_name = result[0]['first_name']
        return(recipeObj)
        

    @classmethod
    def create_recipe(cls,data):
        query = 'INSERT INTO recipes (recipe_name,instructions,description,user_id, under) VALUES(%(recipe_name)s,%(instructions)s, %(description)s,%(user_id)s, %(under)s)'
        result = connectToMySQL('recipes').query_db(query, data)
        return(result)
    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET recipe_name = %(recipe_name)s, instructions = %(instructions)s, description = %(description)s,user_id = %(user_id)s, created_at = %(created_at)s, under = %(under)s WHERE recipes.id = %(id)s'
        result =connectToMySQL('recipes').query_db(query,data)
        return(result)
    @classmethod
    def delete_recipe(cls,data):
        query = 'DELETE FROM recipes WHERE recipes.id = %(id)s'
        result = connectToMySQL('recipes').query_db(query,data)
        return(result)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        if len(data['description']) < 3:
            flash('description must be at least 3 characters')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('instructions must be at least three characters')
            is_valid = False
        if len(data['recipe_name']) < 3:
            flash('recipe name must be at least 3 characters')
            is_valid = False
        return(is_valid)



