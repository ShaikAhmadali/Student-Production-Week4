from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
#create Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "student_week3_secret_key"

#configure the SqLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

#Home Route
@app.route('/')
def home():
    return "Student REST API is Running"

@app.route('/home')
@login_required
def index():
    return render_template("index.html", username=current_user.username)

#-------signup Route-------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            error = "Username already exists!"
            return render_template("signup.html", error=error)

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html", error=error)

#-------login Route-------
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("index"))

        error = "Invalid username or password!"

    return render_template("login.html", error=error)

#-------dashboard Route-------
@app.route("/dashboard")
@login_required
def dashboard():

    return f"""
    <h1>Welcome {current_user.username}</h1>

    <h3>You are successfully logged in.</h3>

    <a href='/logout'>Logout</a>
    """

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

# Create Student (POST API)
@app.route('/students', methods=['POST'])
@login_required
def add_student():

    # Receive JSON data from Postman
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "No data received"}), 400

    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    if not data.get("age"):
        return jsonify({"error": "Age is required"}), 400

    if not data.get("course"):
        return jsonify({"error": "Course is required"}), 400

    # Create Student object
    student = Student(
        name=data["name"],
        age=data["age"],
        course=data["course"]
    )

    # Save into database
    db.session.add(student)
    db.session.commit()

    # Return success response
    return jsonify({
        "message": "Student added successfully!"
    }), 201

#-----------GET API for all Students-----------
@app.route('/students', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()

    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course
        })

    return jsonify(student_list)

#-----GET API for specific Student-----
@app.route('/students/<int:id>', methods=['GET'])
@login_required
def get_student(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify({
    "id": student.id,
    "name": student.name,
    "age": student.age,
    "course": student.course
})

#----------PUT API----------
@app.route('/students/<int:id>', methods=['PUT'])
@login_required
def update_student(id):

    student = Student.query.get(id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json()
    student.name = data["name"]
    student.age = data["age"]
    student.course = data["course"]

    db.session.commit()

    return jsonify({
        "message": "student updated successfully!"
    })

#---------DELETE API---------
@app.route('/students/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({
        "message": "Student deleted successfully!"
    })


# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)