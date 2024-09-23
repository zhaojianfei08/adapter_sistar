"""
用于初始化，创建数据库，创建数据库表
"""
import random

import pandas as pd
from sqlalchemy import text
from connectors.tdengine import get_tdengine_connection
from get_logger import logger

xlsx = r'E:\TH\core\basic_service\opcua_adapter\static\opcua_template.xlsx'

connection = get_tdengine_connection()

db_name = 'test'
stable = 'meters'

df = pd.read_excel(xlsx, sheet_name='device1')

tag_uuid = df.loc[:, ['tag_uuid', 'unit']]

create_table_sql = ''

for item in tag_uuid.values:
    _sql = f"""CREATE TABLE IF NOT EXISTS {db_name}.{item[0]} USING {db_name}.{stable} TAGS ('{item[1]}', '{random.randint(1, 10)}');"""
    create_table_sql += _sql

create_db_stable_sql = f"""CREATE DATABASE IF NOT EXISTS {db_name} KEEP 3650;
use {db_name};
CREATE STABLE IF NOT EXISTS {db_name}.{stable} (ts TIMESTAMP, val FLOAT) TAGS ( unit BINARY(20),   s_type BINARY(20));
"""
total_sql = create_db_stable_sql + create_table_sql
print(total_sql)
try:
    connection.execute(text(total_sql))
    connection.commit()
    logger.info('init success')
except Exception as e:
    print(str(e))
    connection.rollback()
    logger.error('init failed')
