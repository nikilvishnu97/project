from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .signup_form import SignUpForm
from .models import User
from flask_bcrypt import Bcrypt



#!py
@lm.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve
    """
    return User.query.get(user_id)


@app.before_request
def before_request():
    g.user = current_user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignUpForm()
    if form.validate_on_submit():
        user = User(name=form.name.data ,age= form.age.data ,username= form.username.data ,password= form.password.data ,email= form.email.data ,)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html",form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
    user = current_user
    logout_user()
    return render_template("home.html")
    

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    print(db)
    form = LoginForm()
    bcrypt = Bcrypt(app)
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        password=bcrypt.generate_password_hash(user.password)
        if user:
            if bcrypt.check_password_hash(password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("index"))
        else:
            print("invalid")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")

#!py
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)
