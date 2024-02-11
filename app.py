from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['login_name']
    password = request.form['login_password']
    user = User.query.filter_by(name=name).first()
    if user and user.password == password:
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Incorrect username or password', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form['register_name']
    password = request.form['register_password']
    confirm_password = request.form['register_confirm_password']
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('index'))
    else:
        user = User.query.filter_by(name=name).first()
        if user:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('index'))
        else:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
