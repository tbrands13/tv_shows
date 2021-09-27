from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import user
from flask import flash

class Show:
    def __init__(self,data):
            self.id = data['id']
            self.title = data['title']
            self.network = data['network']
            self.release_date = data['release_date']
            self.description = data['description']
            self.user_id = data['user_id']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']

    @classmethod
    def create_show(cls,data):
        query = 'INSERT INTO shows (title, network, release_date, description, user_id, created_at, updated_at) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s, NOW(), NOW())'
        results = connectToMySQL('tv_shows').query_db(query, data)
        return results


    @classmethod
    def all_shows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL('tv_shows').query_db(query)

        shows = []
        for show in results:
            shows.append(cls(show))
        return shows


    @classmethod
    def one_show(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query, data)
        return cls(results[0])



    @classmethod
    def update_show(cls,data):
        query = 'UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s'
        results = connectToMySQL('tv_shows').query_db(query, data)
        return results


    @classmethod
    def delete_show(cls, data):
        query = 'DELETE FROM shows WHERE id = %(id)s'
        results = connectToMySQL('tv_shows').query_db(query, data)
        return results



    @staticmethod
    def validate_show(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if len(data['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid = False
        if len(data['release_date']) < 3:
            flash("Date field required.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description field required")
            is_valid = False
        return is_valid