from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/trip')
def createpage():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('createpage.html',user=User.get_by_id(data))

@app.route('/create/trip', methods=['POST'])
def newtrip():
    if not Trip.validate_trip(request.form):
        return redirect('/new/trip')
    data ={ 
        "location": request.form['location'],
        "description": request.form['description'],
        "startdate": request.form['startdate'],
        "enddate": request.form['enddate'],
        "user_id":session['user_id']
    }
    trip_id = Trip.save(data)

    return redirect('/dashboard')

