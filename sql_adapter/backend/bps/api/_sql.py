from sqlalchemy import text

# 返回braumat数据库中所有包含eng的基础表和包含rt的运行表
BRAUMAT_ENG_RT_Table_SQL = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where table_name like 'sistar_rt%' or table_name like 'sistar_eng%';"""
IOT_BRAUMAT_Table_SQL = """SELECT table_name as table_name FROM information_schema.tables WHERE table_schema = 'braumat' and (table_name like 'sistar_rt%' or table_name like 'sistar_eng%');"""
COLUMNS_INFO_OF_MSSQL = text("""SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    CHARACTER_MAXIMUM_LENGTH, 
    IS_NULLABLE, 
    COLUMN_DEFAULT 
FROM 
    INFORMATION_SCHEMA.COLUMNS 
WHERE 
    TABLE_NAME = :table_name;
""")
