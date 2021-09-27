from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import show
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows = []


    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        results = connectToMySQL('tv_shows').query_db(query,data)
        return results



    @classmethod
    def choose_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('tv_shows').query_db(query,data)
        print(results[0])
        return cls(results[0])


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('tv_shows').query_db(query)
        return results

    @classmethod
    def one_user(cls):
        query = "SELECT first_name FROM users WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query)
        return results


    @classmethod
    def display_shows(cls,data):
        query = "SELECT * FROM shows LEFT JOIN users ON user_id = users.id WHERE user_id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query, data)
        print(results)


        for db_row in results:
            show_data = {
                "id": db_row["id"],
                "title": db_row["title"],
                "network": db_row["network"],
                "release_date": db_row["release_date"],
                "description": db_row["description"],
                "user_id": db_row["user_id"],
                "created_at": db_row["created_at"],
                "updated_at": db_row["updated_at"]
            }

            

        return results


    @staticmethod
    def validate_user(data):
        is_legit = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_legit = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_legit = False
        if len(data['email']) < 7:
            flash("Email must be at least 7 characters ")
            is_legit = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is not valid')
            is_legit = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_legit = False
        if not data['password'] == data['confirm_password']:
            flash('Passwords do not match')
            is_legit = False
        return is_legit
