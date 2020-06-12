from datetime import datetime
from flask import request, render_template, url_for, redirect

''' Import functions'''
from application import app
from application.models import Task, Covid, Country
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
    # dummy data structure; will be implemented in database
    data = {
        'successful_result': True,
        'country': 'Country Name',
        'population': 123456789,
        'covid_19_cases': 12345,
    }


    if request.method == "GET":
        try:
            return render_template('home.html', data=data)
        except:
            return "There was an issue loading the page."

    elif request.method == "POST":

        data = request.form
        country = data.country
        




        print("Redirected with the following"
                "request data: " + request.form['content'])
        try:
            return redirect('/')
        except:
            return "There was an issue with the POST request."

@app.route('/country/australia')
def country_australia():
    return render_template('country_australia.html')

@app.route('/country/brazil')    
def country_brazil():
    return render_template('country_brazil.html')

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
        country = data.get('country')
        date_str = data.get('date')
        num_cases = data.get('num_cases')
        # find country in database and get country id
        country_data = Country.query.filter_by(name=country).all()

        if country_data is []:
            return "invalid country"
        try:
            country_id = country_data[0].id
        except IndexError:
            return "invalid country"


        date_created = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(date_created)
        new_covid = Covid(country_id=country_id, date_created=date_created, num_cases=num_cases)
        try:
            db.session.add(new_covid)
            db.session.commit()
            return redirect('/admin')
        except:
            return "There was an issue assing your task"

    else:
        print("get")

        covid = Covid.query.filter_by().all()
        print(covid)
        return render_template('admin.html', covid=covid)
    return render_template('admin.html')


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
