from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 16, message='标题不能太长')])
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('评论')
