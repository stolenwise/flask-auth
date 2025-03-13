# from flask import Flask, render_template, redirect, session, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_auth.models import db, User, Feedback, connect_db

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_auth.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'supersecretkey'

# db.init_app(app)
# migrate = Migrate(app, db)

# # Routes go here


# app = create_app()

# @app.route('/')
# def home():
#     """Homepage redirect to /register"""
#     return redirect("/register")

from flask import Flask, render_template, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_auth.models import db, User, Feedback, connect_db
from flask_auth.forms import UserForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/register', methods=['GET'])
def register():
    form = UserForm() #Create the instance for the UserForm
    return render_template("register_form.html", form=form)

# @app.route('/register', methods=['POST'])
# def process_register():
#     form = UserForm(request.form)
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data)  # Hash the password

#         new_user = User(
#             username=form.username.data,
#             password=hashed_password,  # Save the hashed password
#             email=form.email.data,
#             first_name=form.first_name.data,
#             last_name=form.last_name.data,
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return redirect("/secret")
#     else:
#         return render_template("register_form.html", form=form)

    

# @app.route('/login', methods=['GET'])
# def login():
#     form = LoginForm() #Create the instance for the Login Form
#     return redirect("/secret", User=User)

# @app.route('/login', methods=['POST'])
# def process_login():
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()

#         if user and check_password_hash(user.password, form.password.data):  # Check hashed password
#             session['user_id'] = user.id  # Store user id in the session
#             return redirect("/secret")
#         else:
#             return redirect("/login")  # Redirect back to login if invalid credentials

#     return render_template("login_form.html", form=form)  # If form is invalid, stay on the login page



# @app.route('/secret', methods=['GET'])
# def secret():
#     if 'user_id' not in session:
#         return redirect("/login")
#     return render_template("secret.html")