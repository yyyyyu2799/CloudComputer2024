# README

该项目实现了一个基于DeepSeek的自然语言查询数据库的系统，用于学生询问教师教学相关信息，帮助其进行课程选择，使用Flask和LangChain构建。通过此系统，用户可以向数据库提问并获取自然语言的答案。

## 环境配置

1. **克隆仓库** ：

   `git clone https://github.com/OpenEduTech/CloudComputer2024/tree/017  `

`  cd llm`

1. **安装依赖** ：
   安装项目依赖：

```bash
   pip install -r requirements.txt
```

1. **数据库配置** ：
   在 `db_setting.py` 文件中配置本地MySQL数据库连接：

```python
   db_user = "root"  # 数据库用户名
   db_password = "your_password"  # 数据库密码
   db_host = "localhost"  # 数据库主机
   db_port = 3306  # MySQL端口
   db_name = "education"  # 数据库名称
```

1. **数据库初始化** ：
   运行 `create_table.sql` 来初始化数据库表：

```bash
   mysql -u root -p < create_table.sql
```

1. **运行项目** ：
   启动Flask应用：

```bash
   python test_memory_sql_result.py
```

1. **API接口** ：

* `GET /`：返回主页面（`index.html`）。
* `POST /get_answer`：接收问题并返回答案。

---

## 代码结构

```
|-- static/
    |-- images/
        |-- OIP.jpg  # 静态资源中的图片
|-- templates/
    |-- index.html  # 渲染应用UI的模板文件
|-- db_setting.py  # 数据库连接配置文件
|-- llm_setting.py  # 语言模型配置文件
|-- requirements.txt  # Python依赖库列表
|-- test_memory_sql_result.py  # 启动Flask应用的脚本
```

### 主要模块：

1. **db_setting.py** ：

* 配置MySQL数据库连接并提供查询接口。

1. **llm_setting.py** ：

* 配置与DeepSeek API的连接，初始化语言模型。

1. **test_memory_sql_result.py** ：

* Flask应用入口文件，处理前端请求、查询数据库并生成自然语言回答。

---

## 运行示例

### 启动Flask应用

1. 配置好数据库和环境后，运行以下命令启动应用：
   ```bash
   python test_memory_sql_result.py
   ```
2. 应用将在 `http://localhost:5000` 启动，您可以通过浏览器访问。

### 调用API接口

1. **获取答案** ：

* `POST /get_answer` 接口用于接收用户问题，并返回自然语言答案。
* 请求示例：
  ```json
  {
    "question": "赵明昊老师的评价怎么样？"
  }
  ```
* 响应示例：
  ```json
  {
    "answer": "赵明昊老师风趣幽默，但是给分较低"
  }
  ```
