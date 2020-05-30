from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app.utils.extensions import db, login_manager
from .role import Role


class User(UserMixin, db.Model):
    # 表名
    __tablename__ = 'user'
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    # 字段名：用户名，密码（加密的），邮箱，昵称，头像（路径），性别，简介
    username = db.Column(db.String(32), primary_key=True, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32), unique=True, index=True)
    nickname = db.Column(db.String(32))
    protrait = db.Column(db.String(64), default='default.jpg')
    sex = db.Column(db.String(4))
    info = db.Column(db.Text())
    # 用于判断用户是否验证
    confirm = db.Column(db.Boolean, default=False)
    # 用户文章
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    # 用户评论
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.role:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='SuperAdministrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('该属性不可读')

    @password.setter
    def password(self, password):
        """
        对密码进行加密
        :param password: 未加密的密码
        :return:
        """
        # 对密码进行加密
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        校验密码是否正确
        :param password: 要校验的密码
        :return:
        """
        # 校验密码是否正确
        return check_password_hash(self.password_hash, password)

    def generate_token(self, use_username=1, use_email=0, expires_in=60 * 60 * 2):
        """
        生成用户唯一标识符token
        :param use_username: 是否序列化username
        :param use_email: 是否序列化email
        :param expires_in: 有效时间，默认为2小时
        :return:
        """
        data = {}
        if use_username:
            data['username'] = self.username
        if use_email:
            data['email'] = self.email
        # 创建序列化对象
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        # 返回序列化后的信息作为token
        return serializer.dumps(data)

    @staticmethod
    def check_token(token, use_username=1, use_email=0):
        """
        校验token是否正确
        :param token: 用户唯一标识符
        :param use_username: 是否反序列化username
        :param use_email: 是否反序列化username
        :return:
        """
        # 创建序列化对象
        serializer = Serializer(current_app.config['SECRET_KEY'])
        # 判断校验的token是否正确，若不正确，则loads失败
        try:
            # 反序列化token信息，获取原信息
            data = serializer.loads(token)
            print(data)
            # 判断信息是否有效
            if use_username:
                return User.query.filter_by(username=data['username']).first()
            if use_email:
                return User.query.filter_by(email=data['email']).first()
        except:
            return False

    # 若无此方法则会报错 NotImplementedError: No `id` attribute - override `get_id`
    def get_id(self):
        """
        flask-login登录用户后，返回一个能唯一标识用户的
        :return:
        """
        return self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()
