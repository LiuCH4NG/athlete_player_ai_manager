# AI助手/聊天调用流程图

```mermaid
sequenceDiagram
    participant Client as HTTP客户端
    participant FastAPI as FastAPI服务器<br/>/chat/
    participant Agent as AI代理创建<br/>create_agent()
    participant LLM as LLM提供商<br/>Ollama/OpenAI
    participant MCP as MCP客户端<br/>MultiServerMCPClient
    participant Tools as MCP工具<br/>运动员API
    participant DB as 数据库<br/>SQLite

    Note over Client,DB: 步骤1: 创建AI代理

    FastAPI->>Agent: create_agent()
    activate Agent

    Agent->>Agent: get_llm()
    activate Agent
    Note right of Agent: 读取环境变量<br/>LLM_SERVE=OLLAMA/OpenAI
    alt OLLAMA模式
        Agent->>Agent: ChatOllama(<br/>model=OLLAMA_MODEL,<br/>base_url=OLLAMA_BASE_URL,<br/>temperature=0.7)
    else OpenAI模式
        Agent->>Agent: ChatOpenAI(<br/>model=OPENAI_MODEL,<br/>base_url=OPENAI_BASE_URL,<br/>temperature=0.7)
    end
    Agent-->>Agent: 返回llm实例
    deactivate Agent

    Agent->>MCP: get_mcp_tools(base_url)
    activate MCP
    Note right of MCP: 创建MCP客户端<br/>配置: athletes服务<br/>URL: http://localhost:8001/mcp/
    MCP-->>MCP: 返回client实例
    deactivate MCP

    Agent->>MCP: await get_tools()
    activate MCP
    MCP-->>Agent: 返回可用工具列表<br/>• create_athlete<br/>• get_athletes<br/>• get_athlete<br/>• update_athlete<br/>• delete_athlete<br/>• search_athletes
    deactivate MCP

    Agent->>Agent: create_react_agent(llm, tools, SystemMessage)
    activate Agent
    Note right of Agent: 创建LangGraph React代理<br/>系统提示: 你是帮助用户<br/>查询运动员信息的助手
    Agent-->>Agent: 返回agent实例
    deactivate Agent

    FastAPI-->>FastAPI: 返回agent
    deactivate Agent

    Note over Client,DB: 步骤2: 执行聊天查询

    Client->>FastAPI: GET /chat/?message=找一个北京的运动员
    FastAPI->>FastAPI: run_agent(agent, message)
    activate FastAPI

    FastAPI->>Agent: agent.ainvoke({"messages": message})
    activate Agent

    Note over Agent,LLM: 代理推理过程 (LangGraph)

    Agent->>LLM: llm.invoke(message)
    activate LLM
    Note right of LLM: LLM分析用户意图<br/>"找一个北京的运动员"<br/>需要搜索 hometown=北京
    LLM-->>Agent: 决定调用search_athletes工具
    deactivate LLM

    Agent->>Tools: search_athletes(search_params)<br/>{hometown: "北京"}
    activate Tools
    Note right of Tools: 通过HTTP调用<br/>http://localhost:8001/mcp/search_athletes
    Tools->>FastAPI: HTTP POST /athletes/search/
    activate FastAPI

    FastAPI->>FastAPI: search_athletes(search_params, skip=0, limit=10)
    activate FastAPI
    FastAPI->>FastAPI: get_db() [依赖注入]
    activate FastAPI

    FastAPI->>FastAPI: crud.search_athletes(db, search_params)
    activate FastAPI

    FastAPI->>FastAPI: 构建SQLAlchemy查询<br/>SELECT * FROM athletes<br/>WHERE is_deleted=false<br/>AND hometown ILIKE '%北京%'
    activate FastAPI
    FastAPI->>DB: EXECUTE query
    activate DB
    DB-->>FastAPI: 返回匹配运动员列表
    deactivate DB

    FastAPI-->>FastAPI: 返回运动员列表
    deactivate FastAPI
    FastAPI-->>FastAPI: 返回athletes JSON
    deactivate FastAPI
    Tools-->>Agent: 返回运动员查询结果
    deactivate Tools

    Agent->>LLM: llm.invoke(results + 原始查询)
    activate LLM
    Note right of LLM: LLM将运动员数据<br/>格式化为自然语言回复
    LLM-->>Agent: 生成友好回复
    deactivate LLM

    Agent-->>FastAPI: 返回最终消息
    deactivate Agent

    FastAPI-->>FastAPI: 返回 {"info": response}
    deactivate FastAPI

    FastAPI-->>Client: HTTP 200<br/>{"info": "找到3位来自北京的运动员..."}
    deactivate FastAPI

    Client-->>Client: 显示AI回复
```

## 关键组件说明

### 1. LLM提供商 (get_llm)
```python
# 环境变量配置
LLM_SERVE=OLLAMA  # 或 OPENAI
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:4b
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 2. MCP工具集成
- **协议**: Model Context Protocol (MCP)
- **传输**: streamable_http
- **URL**: http://localhost:8001/mcp/
- **服务名**: athletes

### 3. LangGraph React代理
- 使用预构建的 `create_react_agent`
- 思维链: Thought → Action → Observation
- 自动工具选择和调用
- 支持多轮对话

### 4. 数据流程
1. **用户输入** → 自然语言查询
2. **LLM分析** → 理解意图，提取参数
3. **工具调用** → 转换为结构化查询
4. **数据库查询** → 执行SQLAlchemy操作
5. **结果处理** → LLM格式化自然语言回复

### 5. 工具列表 (MCP)
| 工具名 | 功能 | 参数 |
|--------|------|------|
| create_athlete | 创建运动员 | AthleteCreate |
| get_athletes | 获取运动员列表 | skip, limit |
| get_athlete | 获取单个运动员 | athlete_id |
| update_athlete | 更新运动员 | athlete_id, AthleteUpdate |
| delete_athlete | 删除运动员 | athlete_id |
| search_athletes | 搜索运动员 | AthleteSearch, skip, limit |

### 6. 查询示例

**用户查询**: "找一个北京的运动员"

**解析过程**:
1. LLM识别意图: search
2. 提取参数: hometown="北京"
3. 调用工具: search_athletes({"hometown": "北京"})
4. 执行SQL: `WHERE hometown ILIKE '%北京%'`
5. LLM生成回复: "找到3位来自北京的运动员: ..."

**更复杂查询**: "找20岁以下，身高180以上的篮球运动员"
- 参数: min_age=20, max_age=inf, min_height=180, sport_event="篮球"
- 构建复合查询条件
