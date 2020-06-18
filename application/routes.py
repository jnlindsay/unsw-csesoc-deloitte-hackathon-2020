from datetime import datetime
from flask import request, render_template, url_for, redirect, json

''' Import functions'''
from application import app
from application.models import Covid, Suburb


from application import db

#######################################################
#                 HealthView Routes                   #
#######################################################

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/', methods=['POST', 'GET'])
def home():

    if request.method == "GET":
        try:
            return render_template('home.html', empty=-1)
        except:
            return "There was an issue loading the page."

    elif request.method == "POST":
        
        data = request.form
        suburb = data.get('suburb')
        suburb_data = Suburb.query.filter_by(name=suburb).first()
        print(suburb_data)
        if suburb_data is None:
            return render_template('home.html', suburb_name=suburb, empty = 0)
        
        # get all data related to given suburb
        all_data = Covid.query.filter_by(suburb_id=suburb_data.id).order_by(Covid.date_created).all()
        # Get most recent data
        recent_data = all_data[:14]
        # calculate sum of recent data
        sum = 0
        dates = []
        data = []
        for i in recent_data:
            string = i.date_created.date().strftime("%d/%m")
            data.append(i.num_cases)
            dates.append(string)
            sum += i.num_cases

        population = {
            'bondi': 15000,
            'maroubra': 31000
        }
        rate = "{0:.4%}".format(sum / population['bondi'])
        return render_template('home.html', sum=sum, suburb_name=suburb.title(), empty=1, labels=dates, data=data, rate=rate)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        data = request.form
        suburb = data.get('suburb')
        date_str = data.get('date')
        num_cases = data.get('num_cases')
        # find suburb in database and get suburb id
        suburb_data = Suburb.query.filter_by(name=suburb).all()

        '''
        Error Checking 
        '''
        if suburb_data is None:
            return "invalid suburb or suburb doesnt exist"
        try:
            suburb_id = suburb_data[0].id
        except IndexError:
            return "invalid suburb or suburb doesnt exist"
        '''
        Turn string into datetime object
        '''
        date_created = datetime.strptime(date_str, '%Y-%m-%d').date()
        new_covid = Covid(suburb_id=suburb_id, date_created=date_created, num_cases=num_cases)
        try:
            db.session.add(new_covid)
            db.session.commit()
            return redirect('/admin')
        except:
            print(new_covid.suburb_id, date_created, num_cases)

            return "There was an issue assing your task"
    else:
        covid = Covid.query.filter_by().all()
        suburb = Suburb.query.filter_by().all()
        print(covid)
        return render_template('admin.html', covid=covid, suburb=suburb)

    return render_template('admin.html')

@app.route('/suburb', methods=['POST', 'GET'])
def suburb():
    if request.method == "POST":
        data = request.form
        suburb = data.get('suburb')

        suburb_data = Suburb.query.filter_by(name=suburb).first()
        if suburb_data is not None:
            return "this suburb already exists"
    
        new_suburb = Suburb(name=suburb)
        try:
            db.session.add(new_suburb)
            db.session.commit()
            return redirect('/suburb')
        except:
            return "There was an issue assing your task"
    else:
        suburb = Suburb.query.filter_by().all()
        return render_template('suburb.html', suburb=suburb)