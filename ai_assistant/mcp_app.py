import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage


def get_llm():
    llm = ChatOllama(
        model="qwen3:4b",
        base_url="http://172.16.34.247:11434",
        temperature=0.7,
        reasoning=True,
    )
    return llm


def get_mcp_tools(base_url: str = "http://localhost:8001/mcp/"):
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
            1. 如果输入的查询条件无法满足，请返回: 无法满足查询条件
            2. 如果输入的问题与运动员无关，请返回: 对不起，仅支持运动员信息查询"
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
