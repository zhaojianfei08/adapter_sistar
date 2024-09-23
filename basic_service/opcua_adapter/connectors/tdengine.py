"""
用于连接tdengine
"""
import time
from basic_service.opcua_adapter.get_logger import logger
from basic_service.opcua_adapter.config import tdengine_connection_params

from sqlalchemy import create_engine

engine = create_engine(
    f"taos://{tdengine_connection_params['username']}:{tdengine_connection_params['password']}@{tdengine_connection_params['host']}:{tdengine_connection_params['port']}/{tdengine_connection_params['database']}")


def get_tdengine_connection():
    while True:
        try:
            conn = engine.connect()
            return conn
        except Exception:
            logger.error(
                f"TDEngine连接建立失败,请检查网络是否畅通(ping {tdengine_connection_params['host']}),服务器是否正常,是否开启远程连接,是否安装与服务器相同版本的客户端")
            time.sleep(3)
            continue
