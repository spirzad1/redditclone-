#!venv/bin/python
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import request, render_template,redirect, url_for
from reddit import app, db, lm
from models import *

@lm.user_loader
def load_user(id):
    return UserDB.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if request.form.get('login_or_signup') == 'signup': #signup
            user = UserDB.query.filter_by(email=email, username=username).first()
            if user is not None:
                return "user already exists"
            else:
                user = UserDB.query.filter_by(email=email).first()
                if user is not None:
                    return "email already exists.. pls no"
                user = UserDB.query.filter_by(username=username).first()
                if user is not None:
                    return "username is already taken. pls be more creative"
                user = UserDB(email=email, username=username, pass_hash=password)
                db.session.add(user)
                db.session.commit()
                login_user(user, True)
                print "user successfully added"
                return redirect(url_for('home'))
            
        else: #login
            user = UserDB.query.filter_by(username=username, pass_hash=password).first()
            if user is None:
                return "user doesnt exist"
            else:
                login_user(user, True)
                print "user successfully logged in"
                return redirect(url_for('home'))

        return render_template('register.html')


@app.route('/tags/<tag>')
def tag(tag):
    first_tag= TagDB.query.filter_by(name=tag).first()
    if tag_list is None:
        return render_template('error.html')
    #try to get id of the tag
    #posts_list = PostTagDB.query(TagDB,UserTagDB).join(TagDB).join(UserTagDB)).filter(tag_id=first_tag.id).all()

    return str("Tag is " + tag)


@app.route('/tags')
def get_tag(tag):
    return str("Tag page!")


@app.route('/posts/<post>')
def post(post):
    return str("Post is " + post)


@app.route('/profile/<username>')
def profile(username):
    user = UserDB.query.filter_by(username=username).first()
    if user is None:
        return "hah. you suck. try again"
    return str("User is " + user.username + "\nMail is " + user.email + "\nPassword is" + user.pass_hash)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


