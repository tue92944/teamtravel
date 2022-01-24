from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
from time import time
from flask_app.models import user
import math


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
        self.users_who_rsvpd=[]
        self.creator={}

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
            
    @classmethod
    def save(cls,data):
        query = "INSERT INTO trips (location,description,startdate,enddate,user_id) VALUES (%(location)s,%(description)s,%(startdate)s,%(enddate)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def opentrips(cls,data):
        query="SELECT * FROM trips WHERE trips.id NOT IN (SELECT trip_id FROM rsvps WHERE user_id=%(id)s);"
        results=connectToMySQL(cls.db).query_db(query,data)
        trips=[]
        for row in results:
            trips.append(cls(row))
        print(trips)
        return trips

    @classmethod
    def update(cls, data):
        query = "UPDATE trips SET location=%(location)s, description=%(description)s, startdate=%(startdate)s, enddate=%(enddate)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM trips WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM trips WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_trips_with_user(cls):
        query="SELECT * FROM trips LEFT JOIN users ON trips.user_id=users.id;"
        results=connectToMySQL(cls.db).query_db(query)
        all_trips=[]
        for one_trip in results:
            trip_data={
                "id":one_trip['id'],
                "location":one_trip['location'],
                "description":one_trip['description'],
                "startdate":one_trip['startdate'],
                "enddate":one_trip['enddate'],
                "user_id":one_trip['user_id'],
                "created_at":one_trip['created_at'],
                "updated_at":one_trip['updated_at']
            }
            single_trip=cls(trip_data)
            user_data={
                "id":one_trip['users.id'],
                "first_name":one_trip['first_name'],
                "last_name":one_trip['last_name'],
                "email":one_trip['email'],
                "password":one_trip['password'],
                "created_at":one_trip['users.created_at'],
                "updated_at":one_trip['users.updated_at']
            }

            single_user=user.User(user_data)
            single_trip.creator=single_user
            all_trips.append(single_trip)
        return all_trips


    @classmethod
    def get_one_with_user(cls,data):
        query="SELECT * FROM trips LEFT JOIN users ON trips.user_id=users.id WHERE trips.id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_trips=[]
        for one_user in results:
            tripdata={
                "id":one_user['id'],
                "location":one_user['location'],
                "description":one_user['description'],
                "startdate":one_user['startdate'],
                "enddate": one_user['enddate'],
                "user_id":one_user['user_id'],
                "created_at":one_user['created_at'],
                "updated_at":one_user['updated_at']
            }
            trips=cls(tripdata)
            
            userdata={
                "id":one_user['users.id'],
                "first_name":one_user['first_name'],
                "last_name":one_user['last_name'],
                "email":one_user['email'],
                "password":one_user['password'],
                "created_at":one_user['users.created_at'],
                "updated_at":one_user['users.updated_at']
            }
            user_obj=user.User(userdata)
            rsvp_obj=user.User(userdata)
            trips.creator=user_obj
            trips.users_who_rsvpd=rsvp_obj
            all_trips.append(trips)
        return all_trips

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM trips LEFT JOIN rsvps ON trips.id = rsvps.trip_id LEFT JOIN users ON users.id = rsvps.user_id WHERE trips.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)

        trip = cls(results[0])

        for row in results:
            if row['users.id'] == None:
                break
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            trip.users_who_rsvpd.append(user.User(data))
        return trip



    @staticmethod
    def validate_trip(trip):
        is_valid = True
        startdate=datetime.strptime(trip['startdate'],"%Y-%m-%d")
        enddate=datetime.strptime(trip['enddate'],"%Y-%m-%d")
        
        if len(trip['location']) < 3:
            flash("Location must be at least 3 characters","trip")
            is_valid = False
        if len(trip['description']) < 3:
            flash("Description must be at least 3 characters","trip")
            is_valid = False
        if trip['startdate'] == " ":
            flash("Please enter a start date","trip")
            is_valid = False
        if trip['enddate'] == " ":
            flash("Please enter an end date","trip")
            is_valid = False
        if startdate<datetime.now():
            flash("Start date must be today or in the future","trip")
            is_valid=False
        if enddate<startdate:
            flash("End date cannot be before start date","trip")
            is_valid=False
        return is_valid


