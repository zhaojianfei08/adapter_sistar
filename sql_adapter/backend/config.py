SQL_SERVER_TO_MYSQL_TYPE = {
    'bit': 'tinyint(1)',  # 布尔值（0 或 1）
    'tinyint': 'tinyint',  # 0 到 255 的整数
    'smallint': 'smallint',  # -32, 768到32, 767的整数
    'int': 'int',  # -2 ^ 31到2 ^ 31 - 1的整数
    'bigint': 'bigint',  # -2 ^ 63到2 ^ 63 - 1的整数
    'decimal': 'decimal',  # (p, s)	定点数，精度和标度（p 和 s）可以自定义
    'numeric': 'decimal',  # (p, s)	同 decimal，SQL Server 的别名
    'money': 'decimal',  # (19, 4)	货币类型，-922,337,203,685,477.5808 到 922,337,203,685,477.5807
    'smallmoney': 'decimal',  # (10, 4)	货币类型，-214,748.3648 到 214,748.3647
    'float': 'float',  # 浮点数，SQL Server n 决定精度
    'real': 'float',  # float 或 double	精度较低的浮点数
    'char': 'char',  # 固定长度字符，最多 255 个字符
    'varchar': 'varchar',  # (n)	可变长度字符，最多 65,535 个字符
    'text': 'text',  # 可变长度字符，最多 65,535 个字符
    'nchar': 'char',  # 固定长度 Unicode 字符串，最多 255 个字符
    'nvarchar': 'varchar',  # 可变长度 Unicode 字符串，最多 65,535 个字符
    'ntext': 'text',  # 可变长度 Unicode 字符串，最多 65,535 个字符
    'binary': 'binary',  # 固定长度二进制数据
    'varbinary': 'varbinary',  # 可变长度二进制数据，最多 65,535 个字节
    'image': 'blob',
    'datetime': 'datetime',  # 日期和时间，范围为 1000-01-01 到 9999-12-31
    'datetime2': 'datetime(6)',  # 扩展的 datetime，带有纳秒精度
    'smalldatetime': 'datetime',  # 日期和时间，范围为 1900-01-01 到 2079-06-06
    'date': 'date',  # 日期（不包含时间），范围为 1000-01-01 到 9999-12-31
    'time': 'time',  # 时间（不包含日期），范围为 00:00:00 到 23:59:59
    'datetimeoffset': 'datetime',  # 或 timestamp	带有时区的日期和时间
    'timestamp': 'timestamp',  # 自动生成的时间戳，MySQL 具有更新特性
    'uniqueidentifier': 'char(36)',  # 或 binary(16)	全局唯一标识符（GUID/UUID）
    'rowversion': 'timestamp',  # 自动生成的二进制编号
    'xml': 'text',  # XML 数据类型
    'sql_variant': '不支持',  # 存储不同数据类型的值
    'cursor': '不支持',  # 游标类型
    'table': '不支持',  # 表变量，用于存储表结构的数据
}

mysql_connection_params = {
    'username': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'braumat'
}


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_connection_params['username']}:{mysql_connection_params['password']}@{mysql_connection_params['host']}:{mysql_connection_params['port']}/{mysql_connection_params['database']}"
    SQLALCHEMY_BINDS = {
        #"Brumat 数据库	10.116.29.26	172.20.1.38	1433	21433	MES_NAJ_USER	Mesnajuser123"
        #'db2': 'mssql+pyodbc://sa:Zhaojianfei0820#@127.0.0.1:1433/sistarData?driver=ODBC+Driver+17+for+SQL+Server'}
        'db2': 'mssql+pyodbc://MES_NAJ_USER:Mesnajuser123@172.20.1.38:1433/sistarData?driver=ODBC+Driver+17+for+SQL+Server'}
        #'db2': 'mssql+pyodbc://MES_NAJ_USER:Mesnajuser123@10.116.29.26:21433/sistarData?driver=ODBC+Driver+17+for+SQL+Server'}
    # 禁用修改跟踪功能
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    pass


class ProductConfig(Config):
    pass


config_dict = {
    "config": Config(),
    "test_config": TestConfig(),
    "product_config": ProductConfig()
}
