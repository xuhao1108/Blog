from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import User
import re


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Regexp('^\w{5,14}\w$', message='用户名必须是数字、字母或下划线'),
                                              Length(6, 15, message='用户名必须在6-10位之间！')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18, message='密码必须在6-18位之间！')])
    confirm_passowrd = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次密码输入不一致！')])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法邮箱！')])
    submit = SubmitField('注册')

    def validate_username(self, field):
        """
        验证用户名合法性
        :param field:
        :return:
        """
        # 判断用户名是否存在
        user = User.query.filter_by(username=field.data).first()
        if user and user.confirm:
            raise ValidationError('用户名已存在！')

    def validate_email(self, field):
        """
        验证邮箱合法性
        :param field:
        :return:
        """
        # 判断邮箱是否存在
        user = User.query.filter_by(email=field.data).first()
        if user and user.comfirm:
            raise ValidationError('邮箱已被使用！')


class ResetPassword(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18, message='密码必须在6-18位之间！')])
    confirm_passowrd = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次密码输入不一致！')])
    submit = SubmitField('重置密码')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Regexp('^\w{5,14}\w$', message='用户名必须是数字、字母或下划线'),
                                              Length(6, 15, message='用户名必须在6-10位之间！')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18, message='密码必须在6-18位之间！')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self, field):
        """
        判断输入的是用户名还是邮箱
        :param field:
        :return:
        """
        # 输入的是用户名
        if LoginForm.is_username_or_email(field.data) and not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名未注册！')
        elif User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册！')

    @staticmethod
    def is_username_or_email(data):
        """
        判断登录方式
        :param data: 登录的数据
        :return: 返回True则为用户名登录，False则为邮箱登录
        """
        return True if re.findall(r'^\w{5,14}\w$', data) else False


class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Regexp('^\w{5,14}\w$', message='用户名必须是数字、字母或下划线'),
                                              Length(6, 15, message='用户名必须在6-10位之间！')], render_kw={'readonly': True})
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法邮箱！')], render_kw={'readonly': True})
    nickname = StringField('昵称')
    protrait = FileField('头像', validators=[FileAllowed(['jpg', 'png'], message='请选择图片文件')])
    sex = SelectField('性别', choices=[(0, '保密'), (1, '男'), (2, '女')], default=0,
                      coerce=int)
    info = TextAreaField('简介')
    submit = SubmitField('保存')


class EditPasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired(), Length(6, 18, message='密码必须在6-18位之间！')])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(6, 18, message='密码必须在6-18位之间！')])
    confirm_passowrd = PasswordField('确认密码', validators=[DataRequired(), EqualTo('new_password', message='两次密码输入不一致！')])
    submit = SubmitField('保存')


class IgnorePasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法邮箱！')])
    submit = SubmitField('发送邮件')
