import time
import redis
from sqlalchemy import create_engine

from connector_config import redis_connection_params, mssql_connection_params, mysql_connection_params
from get_logger import logger

pool = redis.ConnectionPool(host=redis_connection_params['host'],
                            port=redis_connection_params['port'],
                            db=redis_connection_params['db'],
                            max_connections=redis_connection_params['max_connections'],
                            decode_responses=redis_connection_params['decode_responses'],
                            )


# 获取连接对象
def get_redis_connection():
    while True:
        try:
            redis_conn = redis.Redis(connection_pool=pool)
            response = redis_conn.ping()
            if response:
                return redis_conn
            else:
                continue
        except Exception as e:
            logger.error(str(e))


mssql_engine = create_engine(
    f"mssql+pyodbc://{mssql_connection_params['username']}:{mssql_connection_params['password']}@{mssql_connection_params['host']}:{mssql_connection_params['port']}/{mssql_connection_params['database']}?driver={mssql_connection_params['driver']}")


def get_mssql_connection():
    while True:
        try:
            conn = mssql_engine.connect()
            return conn
        except Exception as e:
            logger.error(
                f"MSSQL连接建立失败,请检查网络是否畅通(ping {mssql_connection_params['host']}),服务器是否正常,是否开启远程连接,{str(e)}")
            time.sleep(3)
            continue


mysql_engine = create_engine(
    f"mysql+pymysql://{mysql_connection_params['username']}:{mysql_connection_params['password']}@{mysql_connection_params['host']}:{mysql_connection_params['port']}/{mysql_connection_params['database']}")


def get_mysql_connection():
    while True:
        try:
            conn = mysql_engine.connect()
            return conn
        except Exception:
            logger.error(
                f"MySQL连接建立失败,请检查网络是否畅通(ping {mysql_connection_params['host']}),服务器是否正常,是否开启远程连接")
            time.sleep(3)
            continue
