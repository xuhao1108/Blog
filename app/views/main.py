from flask import Blueprint, render_template, request, current_app
from app.models import Article, Role
import datetime

# 创建main蓝本对象
main = Blueprint('main', __name__)


@main.route('/')
def index():
    # 获取页码
    page = int(request.args.get('page', 1))
    # 获取每页的大小
    per_page = int(request.args.get('per_page', 20))
    # 获取atricles模型的分页对象，按照时间降序
    pagination = Article.query.order_by(Article.last_modify.desc(), Article.time.desc()). \
        paginate(page=page, per_page=per_page, error_out=False)
    # 获取分页对象的atricles
    articles = pagination.items
    # 获取管理员角色名字
    return render_template('main/index.html', articles=articles, pagination=pagination)


@main.app_context_processor
def main_role():
    admin = Role.query.filter_by(name=current_app.config['FLASK_ADMIN_ROLE']).first()
    current_time = datetime.datetime.utcnow()
    return dict(admin=admin, current_time=current_time)
