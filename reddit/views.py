#!venv/bin/python
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import request, render_template,redirect, url_for
from reddit import app, db, lm
from models import *
from datetime import datetime
from sqlalchemy import desc

@lm.user_loader
def load_user(id):
    return UserDB.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        top_posts = PostDB.query.order_by(desc(PostDB.num_likes)).limit(50).all()
        return render_template('index.html', posts=top_posts)
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
            user = UserDB.query.filter_by(email=email).first()
            if user is not None:
                return "email already exists.. pls no"
            user = UserDB.query.filter_by(username=username).first()
            if user is not None:
                return "username is already taken. pls die"
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

            login_user(user, True)
            print "user successfully logged in"
            return redirect(url_for('home'))


@app.route('/tags/<tag_name>')
def tag(tag_name):
    tag = TagDB.query.filter_by(name=tag_name).first()
    if tag is None:
        return render_template('error.html')
    post_ids = map(lambda x: x['post_id'], PostTagDB.query.filter_by(tag_id=tag.id).all())
    posts = map(lambda x: PostDB.query.filter_by(x), post_ids)
    return str(posts)


@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = PostDB(title=title, author=current_user.username, content=content,num_likes=0, time=datetime.now())
        db.session.add(post)
        db.session.commit()
        print post.id
        return redirect(url_for('post', post_id=str(post.id)))


@app.route('/posts/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'GET':
        post = PostDB.query.filter_by(id=post_id).first()
        if post is None:
            return render_template('error.html')

        return str("Post is " + post.title + "Message : " + post.content)
    if request.method == 'POST':
        # User wants to add a comment. Assume user is logged in
        content = request.form.get('content')
        if content is None:
            return render_template('error.html')
        author = current_user.username
        time = datetime.now()
        comment = CommentDB(content=content, author=author, post_id=post_id, num_likes=0, time=time)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))


@app.route('/users/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == 'GET':
        user = UserDB.query.filter_by(username=username).first()
        if user is None:
            return "hah. you suck. try again"
        return str("User is " + user.username + "\nMail is " + user.email + "\nPassword is" + user.pass_hash)
    if request.method == 'POST':
        selection = request.form['selection']
        if selection == 'likes':
            post_ids = map(lambda x: x['post_id'], LikeDB.query.filter_by(username=username).all())
            if post_id is None:
                return "No posts liked"
            posts = map(lambda x: PostDB.query.filter_by(x), post_ids)
            return str(posts) #returns the list of all the posts that the current user has liked
        if selection == 'posts':
            posts = PostDB.query.filter_by(author=username).all()
            if posts is None:
                return "No posts exist"
            return str(posts)
        if selection == 'comments':
            comment_ids = map(lambda x: x['comment_id'], LikeDB.query.filter_by(username=username).all())
            if comment_ids is None:
                return "No comments made"
            comments = map(lambda x: CommentDB.query.filter_by(x), comment_ids)
            return str(comments) #returns the list of all the comments that the current user has written


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


