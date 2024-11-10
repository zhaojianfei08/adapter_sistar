from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_apispec import FlaskApiSpec


from helpers import error_response

db = SQLAlchemy()
cors = CORS()
docs = FlaskApiSpec()


# # 设置 Swagger UI 的 URL
# SWAGGER_URL = '/api/docs'
# # 设置 Swagger JSON 的路径，假设放在 static 目录下
# API_URL = '/static/swagger.json'

# 使用 get_swaggerui_blueprint 方法创建 Swagger UI
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,  # Swagger UI 访问的 URL
#     API_URL,  # Swagger 文档的 JSON 路径
#     config={  # 可选的 Swagger UI 配置
#         'app_name': "Flask API"
#     }
# )


def create_app(config_obj) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # 加载全局跨域
    cors.init_app(app)
    # 初始化db
    db.init_app(app)
    # 加载蓝图
    # 注册 Swagger UI 蓝图
    # app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    from bps.api import api_bp
    app.register_blueprint(api_bp)
    docs.init_app(app)
    gen_api_doc()
    # 定义异常的处理方式
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """处理 HTTP 异常"""
        return error_response(message=str(e), code=e.code)

    return app


def gen_api_doc():
    from bps.api import views
    docs.register(views.test,blueprint='api_bp')
