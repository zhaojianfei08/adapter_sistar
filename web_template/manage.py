import redis
from flask import g

from app import create_app

app = create_app()


# 创建 Redis 连接池的函数
def get_redis_pool():
    if 'redis_pool' not in g:
        # 如果 `g` 中还没有 redis_pool，则创建一个新的连接池
        g.redis_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=0,
            max_connections=10,  # 连接池最大连接数
            decode_responses=True  # 自动将 byte 转换为 str
        )
    return g.redis_pool


# 创建 Redis 客户端
def get_redis_client():
    pool = get_redis_pool()
    return redis.Redis(connection_pool=pool)


# 在请求之前初始化 Redis 连接池
@app.before_request
def before_request():
    # 初始化 Redis 客户端，保存在 `g` 对象中，以便在请求处理时复用
    g.redis_client = get_redis_client()


# 在请求结束时释放 Redis 连接池
@app.teardown_appcontext
def teardown_redis_pool(exception):
    redis_pool = g.pop('redis_pool', None)
    if redis_pool is not None:
        redis_pool.disconnect()


if __name__ == '__main__':
    app.run(debug=True)
