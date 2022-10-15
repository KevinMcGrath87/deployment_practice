from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.__init__ import app
from flask import flash
from flask_bcrypt import Bcrypt
import re
REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
REGEX_PASSWORD   = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{5,}$')
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []

    @classmethod
    def getUserByEmail(cls,email):
        query = 'SELECT * FROM users WHERE users.email = %(email)s'
        data = {'email': email}
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return(cls(result[0]))
        else:
            return(False)

    @classmethod
    def getUserById (cls,id):
        query = 'SELECT * FROM users WHERE users.id = %(id)s'
        data = {'id': id}
        result = connectToMySQL('recipes').query_db(query, data)
        return(cls(result[0]))

    @classmethod
    def insertUser(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s, %(password)s)'
        data['password']= bcrypt.generate_password_hash(data['password'])
        user = connectToMySQL('recipes').query_db(query,data)
        return(user)

    @classmethod
    def getall(cls):
        query = 'SELECT * FROM users'
        result = connectToMySQL('recipes').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return(users)

# data returns a dictionary from request form
    @staticmethod
    def validate(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        if len(data['first_name'])< 2:
            flash('first name must have more than 2 characters')
            is_valid = False
        if len(data['last_name'])<2:
            flash('last name must have more than 2 characters')
            is_valid = False
        if len(data['password']) < 5:
            flash('password must be at least 5 characters long')
            is_valid = False
        if not REGEX_EMAIL.match(data['email']):
            flash('invalid email format')
            is_valid = False
        if not REGEX_PASSWORD.match(data['password']):
            flash('password must not contain spaces and must contain both alpha and numeric characters and at least one ! @ # $, or ? * symbol')
            is_valid = False
        if  User.getUserByEmail(data['email']):
            flash('that email is already registered to another account')
            is_valid = False
        return(is_valid)
        
    @staticmethod
    def validate_login(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        user = User.getUserByEmail(data['email'])
        if user:
            if not bcrypt.check_password_hash(user.password, data['password']):
                flash("YOUR ARE A HACKER AND I AM CALLING THE POLICE THE PASSWORD DOESNT MATCH!!!")
                is_valid = False
        else:
            flash('information does not match an existing user')
            is_valid = False
        return(is_valid)
            
        




