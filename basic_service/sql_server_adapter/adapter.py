

"""
pip install pyodbc
"""
import time
import pyodbc


"""
part 1 建立连接
"""

# 定义连接字符串
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server_name;"
    "DATABASE=your_database_name;"
    "UID=your_username;"
    "PWD=your_password;"
)

# 连接到数据库
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()



"""
part 2：检查连接
"""
def check_table_changes(cursor, table_name, last_count):
    # 查询表的行数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    current_count = cursor.fetchone()[0]

    # 比较行数是否发生变化
    if current_count != last_count:
        print(f"Table {table_name} has changed. Previous count: {last_count}, Current count: {current_count}")
        # 执行某个函数
        your_function()
        return current_count  # 更新最新的行数

    return last_count  # 未发生变化，保持原来的行数


def your_function():
    print("Data has changed, executing your function!")


# 初始化
table_name = "your_table_name"
last_count = -1  # 初始设置为-1以确保第一次总是执行

# 循环检测表变化
while True:
    last_count = check_table_changes(cursor, table_name, last_count)
    time.sleep(10)  # 每10秒检查一次


"""
part 3 断开连接
"""

cursor.close()
connection.close()


"""
part 4 断线重连机制，保证连接一直处于活跃状态
"""

def connect_to_sql_server(connection_string):
    """
    连接到SQL Server数据库，失败时进行重连。
    """
    while True:
        try:
            # 尝试连接到数据库
            connection = pyodbc.connect(connection_string, timeout=10)
            print("Successfully connected to the database.")
            return connection
        except pyodbc.Error as e:
            # 如果连接失败，输出错误信息并等待重试
            print(f"Failed to connect to the database: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def execute_query(cursor, query):
    """
    执行SQL查询，捕获异常并进行重连。
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Query failed: {e}")
        return None


def main():
    # 定义连接字符串
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server_name;"
        "DATABASE=your_database_name;"
        "UID=your_username;"
        "PWD=your_password;"
    )

    connection = None

    while True:
        try:
            if connection is None or connection.closed:
                connection = connect_to_sql_server(connection_string)

            cursor = connection.cursor()

            # 你的查询
            query = "SELECT TOP 1 * FROM your_table_name"
            result = execute_query(cursor, query)

            if result:
                print("Query result:", result)

            time.sleep(10)  # 设置你的查询间隔

        except pyodbc.Error as e:
            print(f"Database operation failed: {e}")
            connection = None  # 强制重新连接

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # 对于其他类型的异常，退出循环

        finally:
            if cursor:
                cursor.close()


"""
connect_to_sql_server函数: 该函数尝试连接到SQL Server数据库。如果连接失败，它将捕获pyodbc.Error异常，等待5秒钟后重试。成功连接后返回数据库连接对象。

execute_query函数: 该函数执行SQL查询，处理查询过程中可能出现的异常。如果查询失败，会返回None。

main函数: 包含了主逻辑。在主循环中，它检查连接是否存在或已关闭，必要时重新连接数据库。然后，使用execute_query函数执行查询。查询间隔由time.sleep(10)控制，可以根据需要调整。

断线重连: 如果数据库操作失败或连接被关闭，程序会捕获异常，并在下一次循环时尝试重新连接。

异常处理: 除了pyodbc.Error外，其他的异常也会被捕获并处理。对于非数据库相关的异常，程序会打印错误信息并退出循环。

在实际使用中，记得在程序结束时关闭数据库连接，释放资源。通常情况下，在finally块中确保cursor和connection被关闭。

通过这种方式，你可以确保在网络问题或SQL Server重启等情况下，Python程序能够自动恢复连接并继续运行。
"""



if __name__ == "__main__":
    main()

