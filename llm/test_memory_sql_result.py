# Prompt
import re

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from db_setting import db
from llm_setting import llm
from db_setting import get_schema


from flask_cors import CORS  # 允许跨域请求
from flask import Flask, render_template, request, jsonify


# 启用跨域支持
app = Flask(__name__)
CORS(app)

# 内存缓存
memory = ConversationBufferMemory(return_messages=True)



def get_sql_chain():
    template = """根据下表架构，编写一个 SQL 查询来回答用户的问题: 

            问题:{question} SQL 查询:"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "给定一个输入问题，将其转换为 SQL 查询。数据库架构为:\n{schema}\n。直接返回査询语句,不需要markdwon代码格式返回"),
            MessagesPlaceholder(variable_name="history"),
            ("human", template),
        ]
    )

    sql_response = (
            RunnablePassthrough.assign(
                schema=get_schema,
                history= lambda x: memory.load_memory_variables(x)["history"])
            | prompt
            | llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
    )
    return sql_response


def process_resp_to_sql(query):
    sql_query = re.search(r"SELECT.*?;", query, re.DOTALL)
    return sql_query.group()


memory = ConversationBufferMemory(return_messages=True)

def get_sql_result_chain():

    # Chain to answer
    template = """根据下表问题、SQL查询和 SQL响应, 编写问题答案, 只返回答案, 不需要返回响应的格式前言,问题里没问具体分数等细节就给大概评价，大概评价根据评分转化成自然语言而不是数字，平均分体现了考试难度，如果数据库查不到就说“不好意思，没有查询到相关信息”，请用流畅的像真实的助手的语言回答，不要像机器人一样单纯的列出来:

    问题:{question}
    SQL 查询:{query}
    SQL 响应:{response}
    答案:"""

    prompt_response = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "给定一个输入问题和 SQL 响应，将其转换为自然语言答案。无前言。数据库架构为:\n{schema}\n。",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", template),
        ]
    )

    sql_response = get_sql_chain()

    full_chain = (
            RunnablePassthrough.assign(query=sql_response)
            | RunnablePassthrough.assign(
                schema=get_schema,
                response=lambda x: db.run(process_resp_to_sql(x["query"])),
                history=lambda x: memory.load_memory_variables(x)["history"],
            )
            | prompt_response
            | llm
            | StrOutputParser()
    )
    return full_chain

def save(input_output):
    output = {"output":input_output.pop("output")}
    memory.save_context(input_output, output)
    return output["output"]

@app.route('/')
def index():
    return render_template('index.html')  # Flask 会查找 templates/index.html

# 后端路由：接收问题并返回答案
@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # 获取前端传来的问题
        user_message = request.json.get('question')

        if not user_message:
            return jsonify({"error": "No question provided"}), 400

        # 执行查询链
        full_chain = get_sql_result_chain()
        full_chain_memory = RunnablePassthrough.assign(output=full_chain) | save
        result1 = full_chain_memory.invoke({"question": user_message})

        # 返回处理后的答案
        return jsonify({"answer": result1})

    except Exception as e:
        # 错误处理
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

   