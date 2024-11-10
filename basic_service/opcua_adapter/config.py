import random

tdengine_connection_params = {
    'username': 'root',
    'password': 'taosdata',
    'host': '127.0.0.1',
    'port': 6030,
    'database': 'test'
}

mysql_connection_params = {
    'username': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'th'
}

mssql_connection_params = {
    'username': 'sa',
    'password': 'Zhaojianfei0820#',
    'host': '127.0.0.1',
    'port': 1433,
    'database': 'SistarData',
    'driver': 'ODBC+Driver+17+for+SQL+Server'
}

redis_connection_params = {
    'host': 'localhost',  # Redis 服务器的地址
    'port': 6379,  # Redis 服务器的端口
    'db': 0,  # 使用的 Redis 数据库编号
    'max_connections': 10,  # 连接池的最大连接数
    'decode_responses': True
}

emqx_connection_params = {
    'broker': '127.0.0.1',
    'port': 1883,
    'client_id': f'python_mqtt_client_{random.randint(1, 10)}',
    'keep_alive_interval': 60,
    'password': None,
    'username': None,
    'topic_sub': None,
    'topic_pub': None
}

logger_params = {
    "logger_name": "opcua_adapter_logger",
    "total_level": 20,
    "file_handler_level": 10,
    "control_handler_level": 20,
    "file_name": r"E:\TH\core\basic_service\opcua_adapter\logs\opcua_adapter_logger.txt",
    "mode": "a",
    "max_bytes": 10485760,
    "backup_count": 10,
    "encoding": "UTF-8",
    "format": "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
}


opcua_adapter_params = {
    'alarm_consumer_queue_length': 100,
    'archive_consumer_queue_length': 100,
    'emqx_consumer_queue_length': 100,
    'acquisition_frequency':1, # 采集周期
    'monitor_frequency': 2, # 监控周期
    'alarm_table_name': 'alarm', # 报警的表格
    'archive_table_name': 'test', # 归档的数据库名称
    'emqx_worker': 1,
    'alarm_worker': 5,
    'archive_worker':5
}