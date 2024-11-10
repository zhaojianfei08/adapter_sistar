from flask import Flask
from web_template.extensions import db, api, session
from web_template.apps.one_model_app import task_app
from web_template.apps.student_app import student_app
from web_template.apps.one_to_many_model_app import author_book_app
from web_template.apps.opcua_point_app import opcua_app
from web_template.apps.many_to_many_model_app import user_role_app
from web_template.apps.user_role_permission_app import user_role_permisson_app
from web_template.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # 初始化扩展
    db.init_app(app)
    api.init_app(app)
    session.init_app(app)
    # 注册蓝图
    app.register_blueprint(task_app, url_prefix='/task')
    app.register_blueprint(student_app,  url_prefix='/student')
    app.register_blueprint(author_book_app,  url_prefix='/ab')
    app.register_blueprint(opcua_app, url_prefix='/opcua')
    app.register_blueprint(user_role_app, url_prefix='/ur')
    app.register_blueprint(user_role_permisson_app, url_prefix='/rbac')
    return app



