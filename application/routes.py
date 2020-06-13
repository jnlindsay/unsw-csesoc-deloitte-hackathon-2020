from datetime import datetime
from flask import request, render_template, url_for, redirect, json

''' Import functions'''
from application import app
from application.models import Task, Covid, Suburb
from application.functions.task_funcs import tasks

from application import db

#######################################################
#                  HEALTH RISKS                       #
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

        #turn data into day/month 




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
        '''

        print("Redirected with the following"
                "request data: " + request.form['suburb'])
        try:
            return redirect('/')
        except:
            return "There was an issue with the POST request."
        '''

@app.route('/suburb/australia')
def suburb_australia():
    return render_template('suburb_australia.html')

@app.route('/suburb/brazil')    
def suburb_brazil():
    return render_template('suburb_brazil.html')

@app.route('/city/sydney')    
def city_sydney():
    return render_template('city_sydney.html')

@app.route('/city/sao-paulo')    
def city_sao_paulo():
    return render_template('city_sao-paulo.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        data = request.form
        suburb = data.get('suburb')
        date_str = data.get('date')
        num_cases = data.get('num_cases')
        # find suburb in database and get suburb id
        suburb_data = Suburb.query.filter_by(name=suburb).all()
        if suburb_data is None:
            return "invalid suburb or suburb doesnt exist"
        try:
            suburb_id = suburb_data[0].id
        except IndexError:
            return "invalid suburb or suburb doesnt exist"

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
        print("get")

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
            print(new_covid.suburb_id, date_created, num_cases)
            return "There was an issue assing your task"
    else:
        print("get")
        suburb = Suburb.query.filter_by().all()
        return render_template('suburb.html', suburb=suburb)


#######################################################

# @app.route('/task', methods=['POST', 'GET'])
# def taskPage():
#     if request.method == "POST":
#         task_content = request.form['content']
#         new_task = Task(content=task_content)
#         print("post")
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/task')
#         except:
#             return "There was an issue assing your task"
#     else:
#         print("get")
#         u_tasks = Task.query.filter_by(completed=0).all()
#         c_tasks = Task.query.filter_by(completed=1).all()
#         return render_template('task.html', u_tasks=u_tasks, c_tasks=c_tasks)

# @app.route('/task/delete/<int:id>')
# def delete(id):
#     task_to_delete = Task.query.get_or_404(id)
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/task')
#     except:
#         return "There was a problem deleting that task"

# @app.route('/task/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task_to_update = Task.query.get_or_404(id)
#     if request.method == 'POST':
#         task_to_update.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/task')
#         except:
#             return "There was a problem deleting that task"
#     else:
#         return render_template('update.html', task=task_to_update)

# @app.route('/task/complete/<int:id>')
# def complete(id):
#     task_to_complete = Task.query.get_or_404(id)
#     task_to_complete.completed = 1
#     try:
#         db.session.commit()
#         return redirect('/task')
#     except:
#         return "There was a problem completing that task"


# @app.route('/task/uncomplete/<int:id>')
# def uncomplete(id):
#     task_to_complete = Task.query.get_or_404(id)
#     task_to_complete.completed = 0
#     try:
#         db.session.commit()
#         return redirect('/task')
#     except:
#         return "There was a problem completing that task"

# @app.route('/about')
# def about():
#     return render_template('about.html')
