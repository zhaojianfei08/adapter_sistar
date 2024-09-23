"""
用于连接tdengine
"""
import time
from basic_service.opcua_adapter.get_logger import logger
from basic_service.opcua_adapter.config import mysql_connection_params

from sqlalchemy import create_engine

engine = create_engine(
    f"mysql+pymysql://{mysql_connection_params['username']}:{mysql_connection_params['password']}@{mysql_connection_params['host']}:{mysql_connection_params['port']}/{mysql_connection_params['database']}")


def get_mysql_connection():
    while True:
        try:
            conn = engine.connect()
            return conn
        except Exception:
            logger.error(
                f"MySQL连接建立失败,请检查网络是否畅通(ping {mysql_connection_params['host']}),服务器是否正常,是否开启远程连接")
            time.sleep(3)
            continue


get_mysql_connection()
