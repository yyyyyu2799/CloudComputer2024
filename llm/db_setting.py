from langchain_community.utilities import SQLDatabase

# 连接本地MySQL数据库
# 数据库连接配置
db_user = "root"  # 用户名
db_password = "Zsy19838232580"  # 密码
db_host = "localhost"  # 主机地址
db_port = 3306  # 端口
db_name = "education"  # 数据库名称

# 拼接连接字符串
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLDatabase.from_uri(
    connection_string,
    sample_rows_in_table_info=0
)


def get_schema(_):
    return db.get_table_info()


# 查询语句
def run_query(query):
    return db.run(query)


if __name__ == "__main__":
    print(get_schema(None))
