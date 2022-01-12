from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Trip:
    db = "teamtravel"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.startdate = data['startdate']
        self.enddate = data['enddate']
        self.user_id=data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator={}

    @classmethod
    def save(cls,data):
        query = "INSERT INTO trips (location,description,startdate,enddate,user_id) VALUES (%(location)s,%(description)s,%(startdate)s,%(enddate)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_trip(trip):
        is_valid = True
        if len(trip['location']) < 3:
            flash("Location must be at least 3 characters","trip")
            is_valid = False
        if len(trip['description']) < 3:
            flash("Description must be at least 3 characters","trip")
            is_valid = False
        if trip['startdate'] == "":
            flash("Please enter a start date","trip")
            is_valid = False
        if trip['enddate'] == "":
            flash("Please enter an end date","trip")
            is_valid = False
        return is_valid


