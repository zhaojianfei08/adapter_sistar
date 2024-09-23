import os

import redis


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Zhaojianfei0820#@39.96.77.96:3306/th?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/th?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False  # 设置 session 非永久
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask-session:'  # Redis 中 session 的前缀
    SESSION_REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)  # Redis 配置


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')
