from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from .extensions import mail


def async_task(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    message.html = render_template(template + '.html', **kwargs)
    message.body = render_template(template + '.txt', **kwargs)
    # 因为flask的上下文特性，如果没有这一句会造成邮件无法发送
    app = current_app._get_current_object()
    thread = Thread(target=async_task, args=[app, message])
    thread.start()
    return thread
