from flask import request, render_template, redirect
from application.models import Task

def tasks(request, db):
    if request == "POST":
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/task')
        except:
            return "There was an issue assing your task"
    else:
        u_tasks = Task.query.filter_by(completed=0).all()
        c_tasks = Task.query.filter_by(completed=1).all()
        return render_template('task.html', u_tasks=u_tasks, c_tasks=c_tasks)
    
