from flask import render_template


def page_not_found(e):
    """
    错误码404页面
    :param e: 错误信息
    :return:
    """
    return render_template('error/404.html'), 404


def server_inner_error(e):
    """
    错误码500页面
    :param e: 错误信息
    :return:
    """
    return render_template('error/500.html'), 500
