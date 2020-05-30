from app.utils.extensions import db
import datetime


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    body = db.Column(db.Text(), nullable=False)
    username = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)
    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'), nullable=False)
    time = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow)
    # 用于判断是否显示此评论
    is_show = db.Column(db.Boolean(), default=True)
