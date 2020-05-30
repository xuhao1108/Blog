from flask import Flask
from .config import config
from .utils import config_extendsions, db, add_users, add_articles, add_comments
from .views import config_blueprints, config_errorhandlers
from .models import Role


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])
    # 初始化配置参数
    config[config_name].init_app(app)
    # 配置扩展
    config_extendsions(app)
    # 配置蓝本
    config_blueprints(app)
    # 配置错误码
    config_errorhandlers(app)
    # 需要在上下文中进行
    # with app.app_context():
    #     # 删除原有数据库
    #     db.drop_all()
    #     # 创建数据库
    #     db.create_all()
    #     # 插入默认角色
    #     Role.insert_roles()
    #     # 随机添加100个普通用户，1个超级管理员
    #     add_users(100)
    #     # 随机添加100篇文章
    #      add_articles(100)
    #     # # 随机添加1000条评论
    #     add_comments(1000)
    return app
