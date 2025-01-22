#调用了DeepSeek的API
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

deepseek_key = "sk-b1f8fec4d39c4096bf8b248102cd5055"      #替换为自己的deepseek密钥（API KEY）
print(deepseek_key)

#大语言模型，下面都要用这个llm来回答
llm = ChatOpenAI(
    temperature=0.95,      #多样性
    model="deepseek-chat",
    openai_api_key=deepseek_key,
    openai_api_base="https://api.deepseek.com"
)

if __name__ == "__main__":
    prompt = ChatPromptTemplate.from_template("请根据下面的主题写一篇小红书营销的短文：{topic}")
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    result = chain.invoke({"topic": "华东师范大学"})
    print(result)
