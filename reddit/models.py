from reddit import app, db

class UserDB(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), primary_key=True,nullable=False)
    email = db.Column(db.String(48), nullable=False)
    pass_hash = db.Column(db.String(128), nullable=False)

class PostDB(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    context = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class CommentDB(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class LikeDB(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    postorcomment = db.Column(db.Integer, nullable=False) 
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    type_like = db.Column(db.String(1), nullable=False)

class TagDB(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

class PostTagDB(db.Model):
    __tablename__ = 'posts_tags' 
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class UserTagDB(db.Model):
    __tablename__ = 'users_tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    username = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
