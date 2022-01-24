from flask_app import app
from datetime import datetime
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
    print("startdate")

    return redirect('/confirmed')

@app.route('/confirmed')
def confirm():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('confirmed.html')

@app.route('/mytripspage')
def mytrips():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data ={
        'id': session['user_id']
    }
    data = {
        "id":id
    }
    return render_template("mytrips.html",user=User.get_by_id(user_data),trips=Trip.get_trips_with_user(),now=datetime.now())

@app.route('/showrsvptrips')
def show_triprsvp():
    data = {
        "id": id
    }
    return render_template('rsvptrips.html',user=Trip.get_by_id(data))


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("updatepage.html",edit=Trip.get_one(data),user=User.get_by_id(user_data))

@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trip.validate_trip(request.form):
        return redirect('/edit/<int:id>')

    data={
        "location": request.form['location'],
        "description": request.form['description'],
        "startdate": request.form['startdate'],
        "enddate": request.form['enddate'],
        "id":request.form['id']
    }

    Trip.update(data)
    return redirect ('/mytripspage')

@app.route('/view/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("viewtrip.html",trip=Trip.get_one_with_user(data),user=User.get_by_id(user_data))
    

@app.route('/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data={
        "id":id
    }
    Trip.destroy(data)
    return redirect('/mytripspage')


@app.route('/rsvp',methods=['POST'])
def user_rsvp():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'user_id': request.form['user_id'],
        'trip_id': request.form['trip_id']
    }
    User.add_rsvp(data)
    return redirect(f"/rsvp/{request.form['trip_id']}")

@app.route('/rsvp/<int:id>')
def show_rsvp(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template('confirmrsvp.html',trip=Trip.get_one_with_user(data), rsvp=Trip.get_by_id(data),user=User.get_by_id(data))

@app.route('/showrsvptrips/<int:id>')
def show_rsvp_trip(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    user_data={
        "id":session['user_id']
    }
    return render_template('rsvptrips.html', rsvp=User.get_by_tripid(data),users=User.get_by_id(user_data))