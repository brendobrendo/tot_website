from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Magazine:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # C - Create methods / INSERT a new entry into a table
    @classmethod
    def save(cls, data):
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # R - Read methods / return data from table
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        magazines = [] 
        for magazine in results:
            magazines.append( cls(magazine) )
        return magazines  # Returns list of classes or False

    @classmethod
    def get_last_one(cls):
        query = "SELECT * FROM magazines ORDER BY id DESC LIMIT 1;"
        result = connectToMySQL(DATABASE).query_db(query)
        return cls(result)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])


    # U - Update methods / UPDATE existing entries with new values
    @classmethod
    def update_one(cls, data):
        query = 'UPDATE magaziness SET title=%(title)s, description=%(description)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    # D - Delete methods / DELETE existing entries from table
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM magazines WHERE id= %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_magazine_update(data):
        is_valid = True

        if len(data['title']) < 3:
            flash("First name must be 3 characters", "err_users_first_name")
            is_valid = False
        if len(data['description']) < 3:
            flash("Last name must be 3 characters", "err_users_last_name")
            is_valid = False

        return is_valid