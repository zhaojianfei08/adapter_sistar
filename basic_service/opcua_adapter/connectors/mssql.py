"""
用于连接tdengine
"""
import time
#from basic_service.opcua_adapter.get_logger import logger
from basic_service.opcua_adapter.config import mysql_connection_params, mssql_connection_params

from sqlalchemy import create_engine, text

engine = create_engine(
    f'mssql+pyodbc://sa:Zhaojianfei0820#@127.0.0.1:1433/sistarData?driver=ODBC+Driver+17+for+SQL+Server')


def get_mssql_connection():
    while True:
        try:
            conn = engine.connect()
            return conn
        except Exception:
            logger.error(
                f"MSSQL连接建立失败,请检查网络是否畅通(ping {mssql_connection_params['host']}),服务器是否正常,是否开启远程连接")
            time.sleep(3)
            continue


conn = get_mssql_connection()

result = conn.execute(text("SELECT TABLE_NAME,COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sistar_eng_areas';"))

print(result.fetchall())