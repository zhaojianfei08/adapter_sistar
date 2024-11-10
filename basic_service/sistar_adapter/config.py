

mysql_connection_params = {
    'username': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'braumat'
}


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_connection_params['username']}:{mysql_connection_params['password']}@{mysql_connection_params['host']}:{mysql_connection_params['port']}/{mysql_connection_params['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REQUEST_TIMEOUT = 5

class TestConfig(Config):
    pass


class ProductConfig(Config):
    pass


config_dict = {
    "config": Config(),
    "test_config": TestConfig(),
    "product_config": ProductConfig()
}
