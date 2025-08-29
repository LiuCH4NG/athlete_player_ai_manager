# 运动员智能管理助手

这是一个基于 FastAPI 和 SQLite 构建的运动员管理后端，并搭配现代化的 HTML、CSS 和 JavaScript 前端界面。
系统旨在提供一个全面的运动员信息管理解决方案，并集成智能对话助手功能。

**本项目是基于 [fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) 和 LangChain 的实践项目。**

## 功能

### 后端 (FastAPI)

- **运动员信息管理**: 支持对运动员的 `id`, `姓名`, `身高`, `体重`, `描述`, `创建时间`, `更新时间`, `删除时间`, `删除标记`, `项目`, `年龄`, `籍贯`, `备注` 等字段进行管理。
- **RESTful API**: 提供标准的增、删、改、查 (CRUD) API 接口。
- **分页支持**: 获取运动员列表时支持分页，优化数据加载性能。
- **搜索功能**: 支持根据关键词搜索运动员信息。
- **智能对话助手集成**: 提供 `/chat` 接口，与前端对话助手进行交互。

### 前端 (HTML, CSS, JavaScript)

- **现代化用户界面**: 采用简洁、美观的设计，提供良好的用户体验。
- **运动员列表展示**: 清晰展示运动员信息列表，支持搜索和操作。
- **模态框操作**: 新增和编辑运动员信息均通过独立的模态框完成，界面整洁。
- **空值友好显示**: 备注等可选字段为空时，显示为空白而非 `undefined`。
- **智能对话助手**: 
    - 页面右下角浮动按钮，点击可打开/关闭对话窗口。
    - 支持 Markdown 格式渲染，使助手回复内容更具可读性。
    - 优化了等待回复时的动画效果，更合理美观。
    - 初始对话欢迎语，引导用户开始交互。
    - 用户消息和助手消息位置对调，更符合常见聊天应用习惯。
- **全中文界面**: 所有界面元素和提示信息均为中文。

## 技术栈

- **后端**: FastAPI, SQLAlchemy (异步), SQLite
- **前端**: HTML5, CSS3, JavaScript (ES6+), Showdown.js (Markdown 渲染)
- **包管理**: uv

## 字段

- `id` (主键, 自增)
- `姓名` (name)
- `身高` (height)
- `体重` (weight)
- `描述` (description)
- `创建时间` (created_at)
- `更新时间` (updated_at)
- `删除时间` (deleted_at)
- `删除标记` (is_deleted)
- `项目` (sport_event)
- `年龄` (age)
- `籍贯` (hometown)
- `备注` (remarks)

## 安装

确保你已经安装了 `uv` 工具。

```bash
# 复制环境变量文件
cp .env.example .env

# 克隆项目
git clone <repository-url>
cd athlete_player_ai_manager

# 安装后端依赖
uv sync
```

## 运行

1.  **启动后端服务**:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
    ```
    (注意：如果前端 `script.js` 中配置的 API 端口是 8001，请将此处的端口改为 8001，或修改 `script.js` 中的 `apiUrl`)

2.  **访问前端界面**:
    在浏览器中打开 `http://127.0.0.1:8000` (或您后端运行的对应端口)。

## API 文档

访问 `http://127.0.0.1:8000/docs` 查看自动生成的 API 文档。

## 许可证

MIT
