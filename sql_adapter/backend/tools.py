
import pymssql
import pymysql

# SQL Server连接信息
sql_server_conn_info = {
    'server': '127.0.0.1',
    'user': 'sa',
    'password': 'Zhaojianfei0820#',
    'database': 'SistarData'
}

# MySQL连接信息
mysql_conn_info = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'braumat'
}

# 连接SQL Server
sql_server_conn = pymssql.connect(**sql_server_conn_info)
sql_server_cursor = sql_server_conn.cursor()

# 连接MySQL
mysql_conn = pymysql.connect(**mysql_conn_info)
mysql_cursor = mysql_conn.cursor()

# 查询SQL Server表结构
sql_server_cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sistar_eng_areas'")
columns = sql_server_cursor.fetchall()
print(columns)

# 创建MySQL表的SQL语句
create_table_sql = "CREATE TABLE IF NOT EXISTS `sistar_eng_areas` ("
for column in columns:
    create_table_sql += f"{column[3]} {column[6]},"
create_table_sql = create_table_sql.rstrip(',') + ');'

print(create_table_sql)

# 在MySQL中执行创建表的SQL语句
mysql_cursor.execute(create_table_sql)

# 关闭MySQL和SQL Server的连接
mysql_conn.commit()
mysql_conn.close()
mysql_cursor.close()
sql_server_conn.close()
sql_server_cursor.close()