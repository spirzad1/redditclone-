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
        if top_posts is None:
            return render_template('index.html')
        return render_template('index.html', posts=top_posts)
    if request.method == 'POST':
        
        return render_template('write.html')


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
    return render_template('tags.html', tag=tag_name, posts=posts)


@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_tag = request.form.get('tag')
        post = PostDB(title=title, author=current_user.username, content=content,num_likes=0, time=datetime.now())
        db.session.add(post)
        tag = TagDB(name=new_tag)
        db.session.add(tag)

        db.session.commit()
        print post.id
        return redirect(url_for('post', post_id=str(post.id)))


@app.route('/posts/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'GET':
        post = PostDB.query.filter_by(id=post_id).first()
        if post is None:
            return render_template('error.html')
        comments = CommentDB.query.filter_by(post_id=post_id).all()

        return render_template('post.html', post_title=post.title, author=post.author, content=post.content, comments=comments)
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
            return render_template('profile.html')
        return render_template('profile.html')
        #return str("User is " + user.username + "\nMail is " + user.email + "\nPassword is" + user.pass_hash)
    if request.method == 'POST':
        selection = request.form['selection']
        if selection == 'likes':
            post_ids = map(lambda x: x['post_id'], LikeDB.query.filter_by(username=username).all())
            if post_ids is None:
                return "No posts liked"
            posts = map(lambda x: PostDB.query.filter_by(x), post_ids)
            return render_template('profile.html', posts=posts) #returns the list of all the posts that the current user has liked

        if selection == 'posts':
            posts = PostDB.query.filter_by(author=username).all()
            if posts is None:
                return "No posts exist"
            return render_template('profile.html', posts=posts)

        if selection == 'comments':
            comments = CommentDB.query.filter_by(author=username).all()
            return render_template('profile.html', posts=comments) #returns the list of all the comments that the current user has written


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


