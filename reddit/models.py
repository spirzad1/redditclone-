from reddit import app, db


class UserDB(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(48), nullable=False)
    pass_hash = db.Column(db.String(128), nullable=False)
