
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    classes = db.relationship('Class', backref='student', lazy=True)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/<int:id>')
def student_detail(id):
    student = Student.query.get_or_404(id)
    return render_template('student_detail.html', student=student)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_student = Student(name=name, email=email)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/add_class/<int:student_id>', methods=['GET', 'POST'])
def add_class(student_id):
    if request.method == 'POST':
        name = request.form['name']
        time = datetime.datetime.strptime(request.form['time'], '%H:%M').time()
        building = request.form['building']
        floor = request.form['floor']
        new_class = Class(name=name, time=time, building=building, floor=floor, student_id=student_id)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('student_detail', id=student_id))
    return render_template('add_class.html', student_id=student_id)

@app.route('/map/<string:building>')
def map_view(building):
    google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    return render_template('map.html', api_key=google_maps_api_key, building=building)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
