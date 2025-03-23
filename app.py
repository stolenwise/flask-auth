from flask import Flask, render_template, redirect, session, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_auth.models import db, User, Feedback, connect_db  # Keep db import here
from flask_auth.forms import UserForm, LoginForm, FeedbackForm
from flask_session import Session
from datetime import timedelta

# Initialize the migration extension
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Flask app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_auth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'
    app.config["SESSION_TYPE"] = "filesystem"  # Store sessions in a file
    app.config["SESSION_PERMANENT"] = True
    Session(app)
    app.permanent_session_lifetime = timedelta(days=1)  # Sessions will last 1 day.
    
    # Initialize the database and migration extensions with the app
    db.init_app(app)  # Initialize db with app
    migrate.init_app(app, db)

    # Create the tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/')
def home():
    return redirect("/login")

@app.route('/register', methods=['GET'])
def register():
    form = UserForm() #Create the instance for the UserForm
    return render_template("register_form.html", form=form)

@app.route('/register', methods=['POST'])
def process_register():
    form = UserForm(request.form)
    if form.validate_on_submit():
        print("Form validated successfully!")
        hashed_password = generate_password_hash(form.password.data)  # This hashes the password

        new_user = User(
            username=form.username.data,
            password=hashed_password,  # Save the hashed password
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )

        db.session.add(new_user)
        db.session.commit()
        print("User created successfully!")

        return redirect("/secret")
    else:
        print(f"Form errors: {form.errors}")  # Print form validation errors for debugging
        return render_template("register_form.html", form=form)

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm() #Create the instance for the Login Form
    return render_template("login_form.html", form=form)

@app.route('/login', methods=['POST'])
def process_login():
    form = LoginForm()
    print(f"Entered username: {form.username.data}")
    print(f"Entered password: {form.password.data}")

    if form.validate_on_submit():
        # Make sure the current app is the one initialized with the db instance
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            print(f"Stored hash: {user.password}") 
            session.permanent = True
            session['user_id'] = user.id  # Store user_id in session after login
            session['username'] = user.username
            print(f"User {user.username} logged in successfully.")
            return redirect(url_for('user_profile', username=user.username))  # Redirect to user page after login
        else:
            print("Invalid username or password")
            return redirect("/login")  # Redirect back to login if invalid credentials
    else:
        print("Form validation failed")
        return render_template("login_form.html", form=form)  # Render login form if not submitted


@app.route('/secret', methods=['GET'])
def secret():
    # Check if the user is logged in by checking session for a username
    print(f"Session: {session}")
    if 'user_id' not in session:
        print("Redirecting: user_id is missing in session")
        return redirect('/login')  # If not logged in, redirect to login page
    print("User is authenticated, rendering secret page")
    return render_template("secret.html")  # Show the secret page

@app.route('/logout')
def logout():
    session.pop('username', None)  # Pop removes the username from session
    return redirect('/')  # Redirect to homepage

@app.route('/users/<username>')
def user_profile(username):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/login')

    # Get the current logged-in user's details
    user = User.query.filter_by(id=session['user_id']).first()

    # Check if the logged-in user matches the username from the URL
    if user.username != username:
        return redirect('/login')

    # Query the feedback from the current user by user_id (NOT by username)
    feedback_list = Feedback.query.filter_by(user_id=user.id).all()

    return render_template('user_profile.html', user=user, feedback_list=feedback_list)


    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Ensure that the logged-in user is the one attempting to delete the user
    if 'username' not in session or session['username'] != username:
        return redirect('/login') # Redirect to login page
    
    user = User.query.filter_by(username=username).first()
    if not user or user.id != session ["user_id"]:
        flash("You are not authorized to delete this account.", "danger")
        return redirect("/")
    
    # Delete feedback
    Feedback.query.filter_by(user_id=user.id).delete()

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    session.clear() # Log the user out
    flash("Account successfully deleted.", "success")
    return redirect("/")


    

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback_form(username):
    form = FeedbackForm()

    if 'user_id' not in session or session.get('username') != username:
        flash("You must be logged in as this user to add feedback", "danger")
        return redirect("/login")

    if form.validate_on_submit():
        new_feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            user_id=session['user_id']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for('user_profile', username=username))

    return render_template("feedback_form.html", form=form, username=username)




@app.route('/feedback/<int:feedback_id>/update', methods=['GET'])
def edit_feedback_form(feedback_id):
    """Show update feedback form."""
    feedback = Feedback.query.get_or_404(feedback_id)

    if "user_id" not in session or feedback.user_id != session["user_id"]:
        flash("You are not authorized to edit this feedback", "danger")
        return redirect("/")
    
    form = FeedbackForm(obj=feedback)
    return render_template("feedback_form.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/update', methods=['POST'])
def update_feedback(feedback_id):
    """Handle Feedback Update."""
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "user_id" not in session or feedback.user_id != session["user_id"]:
        flash("Youare not authorized to edit this feedback", "danger")
        return redirect("/")
    
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash("Feedback updated!", "success")
        return redirect("user_profile", username=feedback.user.username)
    
    return render_template("feedback_form.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback and redirect to user profile."""
    feedback = Feedback.query.get_or_404(feedback_id)

    if "user_id" not in session or feedback.user_id != session["user_id"]:
        flash("You are not authorized to delete this feedback.", "danger")
        return redirect(url_for("home"))
    
    username = feedback.user.username

    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted!", "success")

    return redirect(url_for("user_profile", username=feedback.user.username))