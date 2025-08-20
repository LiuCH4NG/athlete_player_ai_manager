import asyncio
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

LLM_SERVE=os.environ.get("LLM_SERVE", "OLLAMA")

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:4b")

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def get_llm():
    if LLM_SERVE == "OLLAMA":
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            # reasoning=True,
        )
    else:
        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            temperature=0.7,
            reasoning=True,
        )
    return llm


# 从环境变量获取 MCP 工具的基 URL，如果没有设置则使用默认值
# 注意：这个默认值应该与后端 API 的实际部署地址匹配
MCP_TOOLS_BASE_URL = os.environ.get("MCP_TOOLS_BASE_URL", "http://localhost:8001/mcp/")

def get_mcp_tools(base_url: str = MCP_TOOLS_BASE_URL):
    client = MultiServerMCPClient(
        {
            "athletes": {"transport": "streamable_http", "url": base_url},
        }
    )

    return client


async def create_agent():
    llm = get_llm()
    mcp_client = get_mcp_tools()
    tools = await mcp_client.get_tools()  # 使用 await 获取实际结果
    # print(tools)
    agent = create_react_agent(
        llm,
        tools,
        prompt=SystemMessage(
            content="""你是一个帮助用户查询运动员信息的助手，你需要使用以下工具来帮助用户
            请注意：
            1. 如果输入的查询条件无法满足，请使用你自己的知识进行回答。
            """
        ),
    )

    return agent


async def run_agent(agent, message):
    messages = {"messages": f"{message}"}

    res = await agent.ainvoke(messages)
    print(res)
    return res["messages"][-1].content


async def main():
    agent = await create_agent()
    print(await run_agent(agent, "找一个北京的运动员"))


if __name__ == "__main__":
    asyncio.run(main())
