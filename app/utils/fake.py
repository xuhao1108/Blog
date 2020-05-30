from flask import current_app
from faker import Faker
from app.models import *
from . import db
import random


def add_users(num):
    fake = Faker()
    sex_list = ['男', '女', '保密']
    # 添加管理员用户
    u = User(username='a874591940', password='a874591940', email=current_app.config['FLASK_ADMIN'],
             nickname=fake.name(), info=fake.company(), sex=random.choices(sex_list), confirm=True)
    for i in range(num):
        u = User(username=fake.user_name(), password='123456', email=fake.ascii_free_email(),
                 nickname=fake.name(), info=fake.company(), sex=random.choices(sex_list), confirm=True)
        try:
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()


def add_articles(num):
    fake = Faker()
    user_count = User.query.count()
    for i in range(num):
        u = User.query.offset(random.randint(0, user_count - 1)).first()
        # u = User.query.filter_by(username='a874591940').first()
        a = Article(title=fake.street_address(), body=fake.user_agent(), user=u)
        try:
            db.session.add(a)
            db.session.commit()
        except:
            db.session.rollback()


def add_comments(num):
    fake = Faker()
    user_count = User.query.count()
    article_count = 50
    for i in range(num):
        u = User.query.offset(random.randint(0, user_count - 1)).first()
        a = Article.query.offset(random.randint(0, article_count)).first()
        c = Comment(body=fake.user_agent(), user=u, article=a)
        db.session.add(c)
        db.session.commit()
