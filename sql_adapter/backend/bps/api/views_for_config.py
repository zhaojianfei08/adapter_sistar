from flask import request
from sqlalchemy import text

from create_app import db
from helpers import error_response, success_response
from . import api_bp


@api_bp.route('/get_mysql_columns', methods=['POST'])
def get_mysql_columns():
    table_name = request.json.get('table_name')
    try:
        # 首先强制删除mysql数据库中的数据表
        with db.engine.connect() as connection:
            sql = f"""SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'braumat' AND TABLE_NAME = '{table_name}';"""
            result = [row[0] for row in connection.execute(text(sql)).fetchall()]
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/run_sql', methods=['POST'])
def run_sql():
    sql = request.json.get('sql')
    try:
        # 首先强制删除mysql数据库中的数据表
        with db.engine.connect() as connection:
            result = [row for row in connection.execute(text(sql)).fetchall()]
            print(result)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))









