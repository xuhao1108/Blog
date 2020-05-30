import os


class Config(object):
    # 配置秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    # 配置bootstrap
    # 默认为False:从网络加载bootsrap，True:从本地加载bootsrap
    BOOTSTRAP_SERVE_LOCAL = True
    # 配置数据库
    # 默认为True，会追踪对象的修改并发送信息，会消耗额外内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置邮件
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 465
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '874591940@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'kmiifmkgirwxbbbc'
    # 文件上传路径
    UPLOAD_FOLDER = os.environ.get('MAIL_PASSWORD') or os.path.abspath(os.path.dirname(__file__))
    # 管理员
    FLASK_ADMIN_ROLE = os.environ.get('FLASK_ADMIN_ROLE') or 'SuperAdministrator'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'a874591940@163.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/blog_dev'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/blog_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/blog'


# 配置字典
config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
}
