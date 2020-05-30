from .main import main
from .user import user
from .article import article
from .comment import comment
from .errors import *

blueprints = [
    (main, ''),
    (user, '/user'),
    (article, '/article'),
    (comment, '/comment'),
]
errorhandlers = [
    (404, page_not_found),
    (500, server_inner_error),
]


def config_blueprints(app):
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def config_errorhandlers(app):
    for error_code, error_func in errorhandlers:
        app.register_error_handler(error_code, error_func)
