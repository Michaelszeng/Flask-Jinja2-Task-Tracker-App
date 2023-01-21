"""
Use Powershell Terminal.

ACTIVATE VIRTUALENV:
>.\env\Scripts\activate

RUN SERVER:
>flask run
"""

import os
from datetime import datetime

# import flask
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

#Define and initialize database test.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]   #Placing the database URI in .env so it is secure (things in .env get but in OS environment variables); .env is in gitignore
db = SQLAlchemy(app)
CORS(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['new_task_content']  #Get content of form with id 'content'
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'The website did an oopsie'
    else:
        #Just render page
        tasks = Todo.query.order_by(Todo.date_created).all()    #Get all the existing tasks
        return render_template('index.html', tasks=tasks)    #Automatically looks for a 'templates' folder

# if __name__ == "__main__":
#     app.run(debug=True, port=8888)