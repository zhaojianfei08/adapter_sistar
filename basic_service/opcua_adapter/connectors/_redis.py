import redis

from basic_service.opcua_adapter.get_logger import logger
from basic_service.opcua_adapter.config import redis_connection_params

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


conn = get_redis_connection()


