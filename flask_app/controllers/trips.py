from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_app.models.trip import Trip


@app.route('/newtrip')
def createpage():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('createpage.html',user=User.get_by_id(data))

@app.route('/create', methods=['POST'])
def newtrip():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trip.validate_trip(request.form):
        return redirect('/newtrip')
    data ={ 
        "location": request.form['location'],
        "description": request.form['description'],
        "startdate": request.form['startdate'],
        "enddate": request.form['enddate'],
        "user_id":session['user_id']
    }
    trip_id = Trip.save(data)

    return redirect('/confirmed')

@app.route('/confirmed')
def confirm():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('confirmed.html')

@app.route('/mytripspage')
def mytrips():
    return render_template("mytrips.html")