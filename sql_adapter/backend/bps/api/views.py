import time
import json
import datetime
from multiprocessing import Value, Process
from threading import Thread, Event
import config
from connector import get_mysql_connection, get_mssql_connection
from . import api_bp
from helpers import success_response, error_response
from flask_apispec import doc, use_kwargs
from marshmallow import Schema, fields
from sqlalchemy import text, Row
from create_app import db
from . import _sql as custom_sql
from get_logger import logger

# 创建后台任务线程和停止事件
background_thread = None
stop_event = Event()
# 全局变量，用于管理多进程任务
task_process = None  # 存储当前进程
is_running = Value('b', False)  # 共享布尔值，指示任务运行


# 定义后台任务函数
def _background_task():
    global stop_event
    while not stop_event.is_set():
        try:
            fetch_incremental_data()
        except Exception as e:
            logger.error(str(e))
            time.sleep(1)
        finally:
            time.sleep(5)  # 模拟任务执行周期
    return


# 后台任务函数
def background_task(is_running):
    while is_running.value:
        # 模拟长时间运行的任务
        try:
            fetch_incremental_data()
        except Exception as e:
            logger.error(str(e))
            time.sleep(1)
        finally:
            time.sleep(1)  # 模拟任务执行周期
    return


# 定义输入参数模式
class HelloSchema(Schema):
    name = fields.String(required=True, description='Name of the person')  #
    # 判断输入的元素是数组中的某一个 validate=validate.OneOf(['active', 'inactive', 'pending'])
    #  status = fields.String(required=True, validate=validate.OneOf(['active', 'inactive', 'pending']))


@api_bp.route('/test', methods=['POST'])
@doc(description="Returns a personalized greeting message")  # 注释生成文档
@use_kwargs(HelloSchema, location='json')  # 验证输入数据
def test(name):
    try:
        data = {'a': 1, 'b': 2, 'name': name}
        return success_response(data=data)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/mssql_tables', methods=['POST'])
@doc(description="Returns braumat mssql tables contains 'eng'&'rt'")
def get_mssql_tables():
    try:
        with db.get_engine('db2').connect() as connection:
            data = [row[0] for row in connection.execute(text(custom_sql.BRAUMAT_ENG_RT_Table_SQL)).fetchall()]
            return success_response(data=data)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/mysql_tables', methods=['POST'])
@doc(description="Returns IOT Mysql tables contains 'eng'&'rt'")
def get_mysql_tables():
    try:
        with db.engine.connect() as connection:
            data = [row[0] for row in connection.execute(text(custom_sql.IOT_BRAUMAT_Table_SQL)).fetchall()]
            return success_response(data=data)
    except Exception as e:
        return error_response(message=str(e))


class TableNameSchema(Schema):
    table_name = fields.String(required=True, description='Name of the table')


def build_dict(columns, result):
    """
    将 sqlalchemy 返回的数据转成包含多个字典的列表，其中每个字典对应数据库的一行数据
    """
    if result is None:
        return None
    columns = list(map(str, columns))
    if isinstance(result, Row):
        return dict(zip(columns, result))
    return [dict(zip(columns, r)) for r in result]


def function_of_migrate(table_name):
    try:
        # 获取到传递过来表的mssql数据库的表结构
        columns_info_of_mssql = []
        try:
            with db.get_engine('db2').connect() as connection:
                result = connection.execute(custom_sql.COLUMNS_INFO_OF_MSSQL, {'table_name': table_name})
                keys = result.keys()
                rows = result.fetchall()
                columns_info_of_mssql = [row for row in rows]
                result_dict = build_dict(keys, rows)
        except Exception:
            return error_response(message='get column info from mssql failed!')
        # 拼接在mysql创建表的sql语句
        try:
            create_mysql_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            for column in columns_info_of_mssql:
                # 涉及到
                column_name = column[0]
                data_type = column[1]
                max_length = column[2]
                is_nullable = column[3]
                default_value = column[4]
                # 转换数据类型
                mysql_data_type = config.SQL_SERVER_TO_MYSQL_TYPE.get(data_type.lower(), "VARCHAR")
                # 如果有字符长度限制，处理 VARCHAR 类型
                if mysql_data_type in ["VARCHAR", "varchar"] and max_length:
                    mysql_data_type = f"{mysql_data_type}({max_length})"
                # 拼接列定义
                column_sql = f"  `{column_name}` {mysql_data_type}"
                # 处理是否为 NULL
                if is_nullable == "NO":
                    column_sql += " NOT NULL"
                else:
                    column_sql += " NULL"
                # 处理默认值
                if default_value is not None:
                    column_sql += f" DEFAULT {default_value}"
                create_mysql_table_sql += column_sql + ",\n"
            # 移除最后一个逗号
            create_mysql_table_sql = create_mysql_table_sql.rstrip(",\n") + "\n);"
            # print(create_mysql_table_sql)
        except Exception:
            return error_response(message='concat mysql create table sql failed!')
        try:
            with db.engine.connect() as connection:
                connection.execute(text(create_mysql_table_sql))
        except Exception:
            return error_response(message='create mysql table failed!')
    except Exception as e:
        return error_response(message=str(e))
    else:
        return success_response(message='migrate success', data=result_dict)


@api_bp.route('/migrate_mssql_to_mysql', methods=['POST'])
@doc(description="migrate mssql table schame to mysql")
@use_kwargs(TableNameSchema, location='json')
def migrate_mssql_to_mysql(table_name):
    return function_of_migrate(table_name)


@api_bp.route('/force_migrate_mssql_to_mysql', methods=['POST'])
@doc(description="force migrate mssql table schame to mysql")
@use_kwargs(TableNameSchema, location='json')
def force_migrate_mssql_to_mysql(table_name):
    try:
        # 首先强制删除mysql数据库中的数据表
        with db.engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
    except Exception as e:
        return error_response(message=str(e))
    else:
        return function_of_migrate(table_name)


class DBInfoSchema(Schema):
    exclude_tables = fields.List(fields.String(), description='不处理的表数据',
                                 missing=['sistar_rt_batch_params', 'sistar_rt_changelog', 'sistar_rt_matmovs',
                                          'sistar_rt_messages',
                                          'sistar_rt_tag_values', 'sistar_rt_tank_history', 'sistar_rt_unit_history'])


@api_bp.route('/get_db_schema', methods=['POST'])
@use_kwargs(DBInfoSchema, location="json")
def get_db_schema(exclude_tables):
    table_schema = {}
    try:
        with db.get_engine('db2').connect() as connection:
            ms_table_list = [row[0] for row in connection.execute(text(custom_sql.BRAUMAT_ENG_RT_Table_SQL)).fetchall()]
            for table_name in ms_table_list:
                result = connection.execute(custom_sql.COLUMNS_INFO_OF_MSSQL, {'table_name': table_name})
                result_dict = build_dict(result.keys(), result.fetchall())
                table_schema[table_name] = result_dict
        # 封装数据 到 json文件
        json_str_dict = {}
        # 处理数据转换成tree_data类型
        tree_table_schema = []
        tree_node_start_id = 1
        for k, v in table_schema.items():
            p_node = {'id': tree_node_start_id, 'data': k, 'children': [], 'label': k}
            tree_table_schema.append(p_node)
            tree_node_start_id += 1
            for item in v:
                c_node = {'id': tree_node_start_id, 'data': item,
                          'label': f"{item['COLUMN_NAME']}<{item['DATA_TYPE']}>"}
                tree_node_start_id += 1
                p_node['children'].append(c_node)
        for k, v in table_schema.items():
            if k in exclude_tables:
                continue
            json_str_dict[k] = {'columns': [], 'select_column': '', 'last_time': '2000-01-01 00:00:00'}
            for item in v:
                json_str_dict[k]['columns'].append((item['COLUMN_NAME'], item['DATA_TYPE']))
                if item['DATA_TYPE'] == 'datetime':
                    json_str_dict[k]['select_column'] = item['COLUMN_NAME']
        with open('./last_sync_time.json', 'w') as f:
            f.write(json.dumps(json_str_dict))
        return success_response(data=tree_table_schema)
    except Exception as e:
        return error_response(message=str(e))


class JsonSchema(Schema):
    json_str = fields.String(required=True, description='json')


@api_bp.route('/save_json_file', methods=['POST'])
@use_kwargs(JsonSchema, location='json')
def save_json_file(json_str):
    try:
        with open('./last_sync_time.json', 'w') as f:
            f.write(json_str)
        return success_response(message='save success')
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_json_file', methods=['POST'])
def get_json_file():
    try:
        with open('./last_sync_time.json', 'r') as f:
            last_sync_time_str = f.read()
        last_sync_time_obj = json.loads(last_sync_time_str)
        return success_response(data=last_sync_time_obj)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/task/start', methods=['POST'])
def start_background_task():
    try:
        # global background_thread
        # global stop_event
        # if background_thread and background_thread.is_alive():
        #     return error_response(message=f'{background_thread.name} is running!')
        # # 重置停止事件并启动新线程
        # stop_event.clear()
        # background_thread = Thread(target=background_task, name='task')
        # background_thread.start()
        global task_process
        if is_running.value:
            return error_response(message=f'task is running!')
        is_running.value = True  # 设置任务状态为运行
        task_process = Process(target=background_task, args=(is_running,))
        task_process.start()
        return success_response(message=f'task started; pid:{task_process.pid}')
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/task/stop', methods=['POST'])
def stop_background_task():
    try:
        # global background_thread
        # global stop_event
        # if not background_thread or not background_thread.is_alive():
        #     return error_response(message='thread is not running!')
        # # 触发停止事件
        # stop_event.set()
        # background_thread.join()  # 等待线程停止
        # return success_response()
        global task_process
        if not is_running.value:
            return error_response(message="No task is running")

        is_running.value = False  # 设置任务状态为停止
        task_process.join()  # 等待任务结束
        task_process = None
        return success_response(message="Task stopped")
    except Exception as e:
        return error_response(message=str(e))


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
    try:
        # 假设你有一个与 SQL Server 结构相同的 MySQL 表
        columus = [key for key in result_dict[0].keys()]
        rows = [tuple(item.values()) for item in result_dict]
        columus_str = str(columus).replace('[', '(').replace(']', ')').strip().replace("'", "")
        rows_str = str(rows).replace('[', '').replace(']', '').replace('None', 'null').strip()
        insert_query = f"""INSERT INTO {table} {columus_str} VALUES {rows_str}"""
        mysql_connect.execute(text(insert_query))
        mysql_connect.commit()
    except Exception as e:
        mysql_connect.rollback()
        logger.error(str(e))
    finally:
        try:
            mysql_connect.close()
        except Exception:
            pass


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
                    column_sql_str = ''
                    for column_name, column_type in v['columns']:
                        if column_type == 'datetime':
                            column_sql_str += f'CONVERT(VARCHAR, {column_name}, 120) AS {column_name},'
                        elif column_type == 'datetimeoffset':
                            column_sql_str += f"""CONVERT(VARCHAR(19), SWITCHOFFSET({column_name}, '+08:00'), 120) AS {column_name},"""
                        else:
                            column_sql_str += f'{column_name},'
                    column_sql_str = column_sql_str.strip()[:-1]
                    total_sql = f"select {column_sql_str} from {k} where {v['select_column']} > '{v['last_time']}' ORDER BY {v['select_column']} OFFSET {i * factor} ROWS FETCH NEXT {factor} ROWS ONLY;"
                    result = mssql_conn.execute(text(total_sql))
                    result_dict = build_dict(result.keys(), result.fetchall())
                except Exception as e:
                    logger.error(f'读取数据失败:{str(e)}')
                else:
                    try:
                        if result_dict:
                            insert_into_mysql(k, result_dict)
                            v['last_time'] = result_dict[-1][v['select_column']]
                    except Exception as e:
                        logger.error(f'写入数据失败:{str(e)}')
                    else:
                        # 更新最后的时间
                        update_last_sync_time(last_sync_obj)
        except Exception as e:
            logger.error(f'未捕获到的错误:{str(e)}')
        finally:
            try:
                mssql_conn.close()
            except Exception:
                pass
