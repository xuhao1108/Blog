from flask import Blueprint, render_template, flash, url_for, redirect, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import RegisterForm, LoginForm, IgnorePasswordForm, ProfileForm, EditPasswordForm
from app.models import User
from app.utils import db, send_mail
import uuid
import os

# 创建user蓝本对象
user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册页面
    :return:
    """
    # 创建表单对象
    form = RegisterForm()
    # 判断表单是否提交
    if form.validate_on_submit():
        if not User.query.filter_by(username=form.username.data).first():
            # 创建user模型对象
            u = User(username=form.username.data, password=form.password.data, email=form.email.data)
            # 提交到数据库中
            db.session.add(u)
            db.session.commit()
            # 发送邮箱用于账户激活
            send_mail(u.email, '账户激活', 'mail/active_account', token=u.generate_token())
            flash('邮件已发送，请到邮箱中查看邮件并激活！')
        else:
            flash('用户已存在！')
        # 重定向到主页面
        return redirect(request.args.get('next') or url_for('.login'))
    return render_template('user/register.html', form=form)


@user.route('/confirm/<token>')
def confirm(token):
    # 校验token是否有效
    u = User.check_token(token)
    # 若数据有效并且处于未激活状态，则激活用户
    if u and not u.confirm:
        # 激活用户，并提交到数据库
        u.confirm = True
        db.session.add(u)
        db.session.commit()
        flash('账户激活成功！')
        return redirect(url_for('user.login'))
    else:
        flash('账户激活失败！token无效或过期，请重新发送邮箱激活账户！')
        return redirect(url_for('main.index'))


@user.route('/ignore_password', methods=['GET', 'POST'])
def ignore_password():
    # 创建表单对象
    form = IgnorePasswordForm()
    if form.validate_on_submit():
        # 获取用户信息
        u = User.query.filter_by(email=form.email.data).first()
        # 判断旧密码是否输入正确
        if u:
            send_mail(u.email, '重置密码', 'mail/reset_password', token=u.generate_token(use_username=0, use_email=1))
            flash('邮件已发送，请到邮箱中查看邮件并重置密码！')
            # 重定向到登录页面
            return redirect(url_for('user.login'))
        else:
            flash('请输入正确的邮箱！')
    return render_template('user/edit_password.html', form=form)


@user.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # 校验token是否有效
    u = User.check_token(token, use_username=0, use_email=1)
    if u:
        # 创建表单对象
        form = ResetPassword()
        if form.validate_on_submit():
            # 保存新密码，并提交到数据库
            u.password = form.password.data
            db.session.add(u)
            db.session.commit()
            flash('密码修改成功！')
            return redirect(url_for('user.login'))
        return render_template('user/reset_password.html', form=form)
    else:
        flash('无法重置密码！token无效或过期，请重新发送邮箱重置密码！')
        return redirect(url_for('main.index'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    # 创建表单对象
    form = LoginForm()
    # 判断表单是否提交
    if form.validate_on_submit():
        # 判断登录方式
        if LoginForm.is_username_or_email(form.username.data):
            # 创建user模型对象
            u = User.query.filter_by(username=form.username.data).first()
        else:
            # 创建user模型对象
            u = User.query.filter_by(email=form.username.data).first()
        # 校验密码正确性
        if u.check_password(form.password.data):
            # 登录用户
            login_user(u, remember=form.remember.data)
            # 重定向到next页面或主页面
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码不正确')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # 创建表单对象
    form = ProfileForm()
    # 获取用户信息
    u = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        # 判断头像是否修改
        if form.protrait.data:
            # 图片根路径
            base_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'static\image\\')
            # 若不是默认头像，则删除旧头像
            if u.protrait != 'default.jpg':
                # 删除原图像
                try:
                    # 若不存在则会报错
                    os.remove(os.path.join(base_dir, u.protrait))
                except:
                    pass
            # 生成新图像名称
            u.protrait = uuid.uuid4().hex + '.' + form.protrait.data.filename.split('.')[-1].lower()
            # 保存图片到本地
            form.protrait.data.save(os.path.join(base_dir, u.protrait))
        # 保存更新后的数据
        u.nickname = form.nickname.data
        u.sex = dict(form.sex.choices).get(form.sex.data)
        u.info = form.info.data
        # 提交到数据库
        db.session.add(u)
        db.session.commit()
        flash('保存成功')
    else:
        form.username.data = u.username
        form.email.data = u.email
        form.nickname.data = u.nickname
        if u.sex:
            form.sex.data = dict(zip(dict(form.sex.choices).values(), dict(form.sex.choices).keys())).get(u.sex)
        form.info.data = u.info
    return render_template('user/profile.html', form=form, filename=u.protrait)


@user.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    # 创建表单对象
    form = EditPasswordForm()
    # 获取用户信息
    u = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        # 判断旧密码是否输入正确
        if u.check_password(form.old_password.data):
            # 保存新密码
            u.password = form.new_password.data
            # 提交到数据库
            db.session.add(u)
            db.session.commit()
            flash('请记住新密码！')
            # 重定向到主页面
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的原密码！')
    return render_template('user/edit_password.html', form=form)


@user.route('/<username>')
def info(username):
    u = User.query.filter_by(username=username).first()
    return render_template('user/user.html', user=u)
