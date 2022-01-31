from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask_app.models import model_magazines
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []
    
    # C - Create methods / INSERT a new entry into a table
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # R - Read methods / return data from table
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL(DATABASE).query_db(query)
        users = [] 
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_last_one(cls):
        query = "SELECT * FROM user ORDER BY id DESC LIMIT 1;"
        result = connectToMySQL(DATABASE).query_db(query)
        return cls(result)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_one_email(cls, data):
        print("this is the data that was input to get_one_email", data)
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False # This should return an instance of the class

    @classmethod
    def get_user_magazines(cls, data):
        query = "SELECT * FROM users LEFT JOIN magazines ON users.id = magazines.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(results[0])
        for magazine in results:
            magazine_data = {
                "id": magazine['magazines.id'],
                "title": magazine['title'],
                "description": magazine['description'],
                "first_name": user.first_name,
                "last_name": user.last_name,
                "created_at": magazine['magazines.created_at'],
                "updated_at": magazine["magazines.updated_at"],
                "user_id": magazine["user_id"]
            }
            user.magazines.append(model_magazines.Magazine(magazine_data))
        return user

    # U - Update methods / UPDATE existing entries with new values
    @classmethod
    def update_one(cls, data):
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    # D - Delete methods / DELETE existing entries from table
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id= %(id)s;"
        return connectTomMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First name must be 3 characters", "err_users_first_name")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be 3 characters", "err_users_last_name")
            is_valid = False
        if len(data['email']) < 3:
            flash("Email must be at least 3 characters", "err_users_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "err_users_email")
            is_valid = False  
        else:
            user = User.get_one_email(data)
            if user:
                flash("Email account already in use", "err_users_email")
                is_valid = False  
        if len(data['password']) < 8:
            flash("Your password needs to be at least 8 characters", "err_users_password")
            is_valid = False
        if data['password'] != data['confirmation_password']:
            flash("Your passwords do not match", "err_password_match")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_user_update(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First name must be 3 characters", "err_users_first_name")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be 3 characters", "err_users_last_name")
            is_valid = False
        if len(data['email']) < 3:
            flash("Email must be at least 3 characters", "err_users_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "err_users_email")
            is_valid = False  

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        
        if len(data['email']) < 2:
            flash("Email must be at least 2 characters", "err_users_email_login")
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Must enter a valid email address", "err_users_email_login")
            is_valid = False  

        else:
            user = User.get_one_email(data)
            print(data, "this is the data in the else clause")
            print(type(user), "this is the type of user")
            if user:
                if not bcrypt.check_password_hash(user.password, data['password']):
                    flash("Invalid credentials", "err_users_password_login")
                    print(data['password'], "is datapassword")
                    print(user.password, "is user.password")
                    is_valid = False
                else:
                    session['user_id'] = user.id

        print(is_valid, "IS_VALID LOGIN")
        return is_valid




