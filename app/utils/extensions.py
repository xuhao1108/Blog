from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager

# 创建相关扩展对象
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()


def config_extendsions(app):
    """
    初始化相关扩展
    :param app:
    :return:
    """
    # 初始化相关扩展
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    # 会话保护级别:None:,basic,strong......strong:用户信息改变时立即退出用户
    login_manager.session_protection = 'strong'
    # 用户未登录时重定向的页面
    login_manager.login_view = 'user.login'
    # 用户未登录时提示信息
    login_manager.login_message = '请先登录才能才问此页面！'
