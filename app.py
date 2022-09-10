from flask import Flask, render_template, url_for, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Job %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        job_content = request.form['content']
        new_job = Todo(content = job_content)

        try:
            db.session.add(new_job)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue with adding your job app"

    else:
        jobs = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', jobs = jobs)

@app.route('/delete/<int:id>')
def delete(id):
    job_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue with deleting the job app'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    job = Todo.query.get_or_404(id)

    if request.method == 'POST':
        job.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your job application"
    else:
        return render_template('update.html', job = job)

if __name__ == "__main__":
    app.run(debug=True)