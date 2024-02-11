from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hospital.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data['name'], specialization=data['specialization'])
    db.session.add(new_doctor)
    db.session.commit()
    
    # Retrieve the newly created doctor from the database to include its ID in the response
    new_doctor_data = {'id': new_doctor.id, 'name': new_doctor.name, 'specialization': new_doctor.specialization}
    
    return jsonify(new_doctor_data), 201

@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization} for doctor in doctors])

@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
