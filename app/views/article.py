from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app.models import Article, Comment, User, Role
from app.forms import ArticleForm, CommentForm
from app.utils import db
import datetime

# 创建article蓝本对象
article = Blueprint('article', __name__)


@article.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """
    添加文章
    :return:
    """
    form = ArticleForm()
    if form.validate_on_submit():
        # 创建文章的模型对象
        a = Article(title=form.title.data, body=form.body.data, username=current_user.username)
        # 添加到数据库中
        db.session.add(a)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('.all', username=current_user.username))
    return render_template('article/write.html', form=form)


@article.route('/delete/<int:id>')
@login_required
def delete(id):
    """
    删除文章
    :param id: 文章id
    :return:
    """
    # 获取此id的文章模型对象
    a = Article.query.filter_by(id=id).first()
    # 获取管理员身份
    admin = Role.query.filter_by(name=current_app.config['FLASK_ADMIN_ROLE']).first()
    # 判断当前用户是否发表文章的用户或者是管理员用户
    if current_user == a.user or current_user.role == admin:
        # 将数据从数据库中删除
        db.session.delete(a)
        db.session.commit()
        flash('删除成功！')
        return redirect(request.args.get('next') or url_for('.all', username=current_user.username))
    else:
        abort(404)


@article.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    """
    删除文章
    :param id: 文章id
    :return:
    """
    # 获取此id的文章模型对象
    a = Article.query.filter_by(id=id).first()
    # 判断当前用户是否发表文章的用户
    if current_user == a.user:
        # 创建文章表单对象
        form = ArticleForm()
        if form.validate_on_submit():
            # 获取修改后的数据
            a.title = form.title.data
            a.body = form.body.data
            a.last_modify = datetime.datetime.utcnow()
            # 提交到数据库中
            db.session.add(a)
            db.session.commit()
            flash('修改成功！')
            return redirect(request.args.get('next') or url_for('.all', username=current_user.username))
        else:
            # 将原数据填充到表单中
            form.title.data = a.title
            form.body.data = a.body
        return render_template('article/write.html', form=form)
    else:
        abort(404)


@article.route('/<int:id>', methods=['GET', 'POST'])
def get(id):
    """
    文章详情页面
    :param id: 文章id
    :return:
    """
    # 获取页码
    page = int(request.args.get('page', 1))
    # 获取每页的大小
    per_page = int(request.args.get('per_page', 20))
    # 获取此id的文章模型对象
    a = Article.query.filter_by(id=id).first()
    # 获取此id的文章模型对象下的评论模型的分页对象，按照时间降序
    pagination = Comment.query.filter_by(article=a). \
        order_by(Comment.time.desc()). \
        paginate(page=page, per_page=per_page, error_out=False)
    # 获取分页对象的所有评论模型对象
    comments = pagination.items
    # 创建评论的表单
    form = CommentForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            # 创建评论的模型对象
            c = Comment(body=form.body.data, user=current_user, article=a)
            # 将评论添加到数据库中
            db.session.add(c)
            db.session.commit()
            flash('评论成功')
            # 重定向到最后一页
            return redirect(url_for('.get', id=id, page=pagination.pages))
        else:
            flash('请先登录才能评论')
            # 重定向到登录页面
            return redirect(url_for('user.login', next=request.url))
    return render_template('article/article.html', article=a, comments=comments, pagination=pagination, form=form)


@article.route('/all/<username>')
def all(username):
    """
    获取某用户的所有文章
    :param username: 用户名
    :return:
    """
    # 获取页码
    page = int(request.args.get('page', 1))
    # 获取每页的大小
    per_page = int(request.args.get('per_page', 20))
    # 获取用户的模型对象
    u = User.query.filter_by(username=username).first()
    # 获取文章模型的分页对象，按照修改时间和发布时间的降序
    pagination = Article.query.filter_by(username=username). \
        order_by(Article.last_modify.desc(), Article.time.desc()). \
        paginate(page=page, per_page=per_page, error_out=False)
    # 获取分页对象的所以文章模型
    articles = pagination.items
    return render_template('article/articles.html', user=u, articles=articles, pagination=pagination)
