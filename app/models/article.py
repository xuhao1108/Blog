from app.utils.extensions import db
import datetime


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
    last_modify = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
    username = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)
    comments = db.relationship('Comment', backref='article', lazy='dynamic', cascade='all, delete-orphan')
