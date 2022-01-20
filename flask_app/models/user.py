from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import trip

class User:
    db = "teamtravel"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trips=[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def rsvpd_trips(cls,data):
        query="SELECT * FROM users LEFT JOIN rsvps ON users.id=rsvps.user_id LEFT JOIN trips ON trips.id=rsvps.trip_id WHERE users.id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        user=cls(results[0])
        for row in results:
            if row['trips.id']==None:
                break
            data={
                "id":row['trips.id'],
                "location":row['location'],
                "description":row['description'],
                "startdate":row['startdate'],
                "enddate":row['enddate'],
                "created_at":row['trips.created_at'],
                "updated_at":row['trips.updated_at'],
                "user_id":row['trips.user_id']
            }
            user.trips.append(trip.Trip(data))
        return user

    @classmethod
    def add_rsvp(cls,data):
        query="INSERT INTO rsvps (user_id,trip_id) VALUES (%(user_id)s, %(trip_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['password_confirmation']:
            flash("Passwords don't match","register")
            is_valid=False
        return is_valid