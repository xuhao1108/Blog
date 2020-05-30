from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app.models import Article, Comment, User, Role
from app.forms import ArticleForm, CommentForm
from app.utils import db
import datetime

# 创建article蓝本对象
comment = Blueprint('comment', __name__)


@comment.route('/all/<username>')
def all(username):
    """
    获取某用户的所有评论
    :param username: 用户名
    :return:
    """
    # 获取页码
    page = int(request.args.get('page', 1))
    # 获取每页的大小
    per_page = int(request.args.get('per_page', 20))
    # 获取评论的模型对象
    u = User.query.filter_by(username=username).first()
    # 获取评论模型的分页对象，按照时间降序
    pagination = Comment.query.filter_by(username=username). \
        order_by(Comment.time.desc()). \
        paginate(page=page, per_page=per_page, error_out=False)
    # 获取分页对象的所有评论模型
    comments = pagination.items
    return render_template('comment/comments.html', user=u, comments=comments, pagination=pagination)


@comment.route('/delete/<int:id>')
@login_required
def delete(id):
    """
    删除评论
    :param id: 评论id
    :return:
    """
    # 获取此评论id的模型对象
    c = Comment.query.filter_by(id=id).first()
    # 获取管理员身份
    admin = Role.query.filter_by(name=current_app.config['FLASK_ADMIN_ROLE']).first()
    # 判断当前用户是否发表评论的用户或者是管理员用户
    if current_user == c.user or current_user.role == admin:
        # 将数据从数据库中删除
        db.session.delete(c)
        db.session.commit()
        flash('删除成功！')
        return redirect(request.args.get('next') or url_for('.all', username=current_user.username))
    else:
        abort(404)


@comment.route('/set_show/<int:id>')
@login_required
def set_show(id):
    """
    设置评论的可见性
    :param id: 评论id
    :return:
    """
    # 获取管理员身份
    admin = Role.query.filter_by(name=current_app.config['FLASK_ADMIN_ROLE']).first()
    # 判断当前用户是否是管理员
    if current_user.role == admin:
        # 获取此评论id的模型对象
        c = Comment.query.filter_by(id=id).first()
        # 修改此评论可见性
        c.is_show = bool(1 - c.is_show)
        # 提交到数据库中
        db.session.add(c)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('comment.all', username=current_user.username))
    else:
        abort(404)
