

"""
Linux 安装odbc
# Import the public repository GPG keys
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# Register the Microsoft repository
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Update the list of available packages
sudo apt-get update

# Install the Microsoft ODBC driver for SQL Server
sudo ACCEPT_EULA=Y apt-get install msodbcsql17

# Optional: Install mssql-tools and unixodbc-dev
sudo ACCEPT_EULA=Y apt-get install mssql-tools unixodbc-dev
"""
mysql_connection_params = {
    'username': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'braumat'
}

mssql_connection_params = {
    'username': 'sa',
    'password': 'Zhaojianfei0820#',
    'host': '127.0.0.1',
    'port': 1433,
    'database': 'sistarData',
    'driver': 'ODBC+Driver+17+for+SQL+Server'
}
# "Brumat 数据库	10.116.29.26	172.20.1.38	1433	21433	MES_NAJ_USER	Mesnajuser123"
# mssql_connection_params = {
#     'username': 'MES_NAJ_USER',
#     'password': 'Mesnajuser123',
#     'host': '172.20.1.38',
#     'port': 1433,
#     'database': 'sistarData',
#     'driver': 'ODBC+Driver+17+for+SQL+Server'
# }

redis_connection_params = {
    'host': '127.0.0.1',  # Redis 服务器的地址
    'port': 6379,  # Redis 服务器的端口
    'db': 0,  # 使用的 Redis 数据库编号
    'max_connections': 10,  # 连接池的最大连接数
    'decode_responses': True
}