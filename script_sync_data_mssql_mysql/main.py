import json
import time
from typing import Union, Sequence, Optional, List, Dict

import redis
import datetime

from sqlalchemy import create_engine, text, Row
from sqlalchemy.engine.result import RMKeyView

from connector_config import redis_connection_params, mssql_connection_params, mysql_connection_params
from get_logger import logger


def build_dict(columns: RMKeyView,
               result: Union[Row, Sequence[Row]]) -> Optional[Union[Dict, List[Dict]]]:
    """
    将 sqlalchemy 返回的数据转成包含多个字典的列表，其中每个字典对应数据库的一行数据
    """
    if result is None:
        return None
    columns = list(map(str, columns))
    if isinstance(result, Row):
        return dict(zip(columns, result))
    return [dict(zip(columns, r)) for r in result]


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
                f"MSSQL连接建立失败,请检查网络是否畅通(ping {mssql_connection_params['host']}),服务器是否正常,是否开启远程连接")
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


def get_last_sync_time():
    """
    从文件或数据库获取上次同步的时间戳。可以根据实际场景调整存储方式。
    这里简单地使用一个文件保存时间戳。
    """
    try:
        with open('last_sync_time.json', 'r') as f:
            last_sync_time = f.read()
            last_sync_obj = json.loads(last_sync_time)
            for k, v in last_sync_obj.items():
                if v['last_time'] == '':
                    v['last_time'] = '2000-01-01 00:00:00'
        # return datetime.datetime.strptime(last_sync_time, '%Y-%m-%d %H:%M:%S')
        return last_sync_obj
    except FileNotFoundError:
        # 如果文件不存在，返回一个很早的时间
        return datetime.datetime(2000, 1, 1)


def update_last_sync_time(sync_time):
    """
    更新最后的同步时间戳。
    """
    with open('last_sync_time.json', 'w') as f:
        sync_str = json.dumps(sync_time)
        # f.write(sync_time.strftime('%Y-%m-%d %H:%M:%S'))
        f.write(sync_str)


def insert_into_mysql(table, result_dict):
    """
    将增量数据插入 MySQL。
    """
    mysql_connect = get_mysql_connection()

    # 假设你有一个与 SQL Server 结构相同的 MySQL 表
    columus = [key for key in result_dict[0].keys()]
    rows = [tuple(item.values()) for item in result_dict]
    columus_str = str(columus).replace('[', '(').replace(']', ')').strip().replace("'", "")
    rows_str = str(rows).replace('[', '').replace(']', '').strip()[:-1]
    insert_query = f"""
        INSERT INTO {table} {columus_str}
        VALUES {rows_str}"""
    print(insert_query)
    mysql_connect.execute(text(insert_query))


def fetch_incremental_data():
    """
    从 SQL Server 获取增量数据，根据时间戳进行过滤。
    """
    factor = 2000
    last_sync_obj = get_last_sync_time()
    if not isinstance(last_sync_obj, dict):
        return

    for k, v in last_sync_obj.items():
        mssql_conn = get_mssql_connection()
        try:
            count = mssql_conn.execute(text(f"select count(*) from {k}")).fetchall()[0][0]
            for i in range(0, int(count) // factor + 1):
                try:
                    result = mssql_conn.execute(text(
                        f"select * from {k} where {v['columns']} > '{v['last_time']}' ORDER BY {v['columns']} OFFSET {i * factor} ROWS FETCH NEXT {factor} ROWS ONLY;"))
                    result_dict = build_dict(result.keys(), result.fetchall())
                except Exception as e:
                    logger.error(f'读取数据失败:{str(e)}')
                else:
                    try:
                        if result_dict:
                            insert_into_mysql(k, result_dict)
                            v['last_time'] = result_dict[-1][v['columns']]
                    except Exception as e:
                        logger.error(f'写入数据失败:{str(e)}')
                    else:
                        # 更新最后的时间
                        update_last_sync_time(last_sync_obj)
        except Exception as e:
            logger.error(f'未捕获到的错误:{str(e)}')


def main():
    fetch_incremental_data()


if __name__ == '__main__':
    main()
