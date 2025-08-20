# 使用官方 Python 运行时作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装 uv 工具
# 这里使用 pip 安装 uv，因为它比从源码编译更快
RUN pip install uv

# 将 requirements.txt 复制到容器中
# 注意：uv 不直接使用 requirements.txt，但我们可以用它来安装依赖
# 为了利用 Docker 的层缓存，我们先复制 pyproject.toml 和 uv.lock (如果存在)
# 但 uv sync 通常直接使用 pyproject.toml
COPY pyproject.toml ./
# 如果有 uv.lock 文件，也复制它以确保依赖版本锁定
COPY uv.lock ./ 
# uv.lock 是可选的，但推荐用于生产环境以确保可重现的构建

# 安装项目依赖
# 使用 uv sync 来安装所有依赖，包括开发依赖 (dev group)
# 如果你只想安装运行时依赖，可以使用 `uv sync --no-dev`
# 这里我们安装所有依赖，因为构建过程可能需要它们 (例如, for running scripts)
# 但是，为了减小生产镜像的大小，最好只安装运行时需要的依赖。
# 因此，我们使用 --no-dev 来排除开发依赖。
RUN uv sync --no-dev

# 将项目源代码复制到容器中
# 使用 .dockerignore 文件来排除不需要的文件（如 .git, __pycache__, .venv 等）
COPY . .

# 暴露应用运行的端口
# FastAPI 默认运行在 8000 端口，但你的 README 中提到了 8001
# 我们使用 8000 作为默认端口，可以通过环境变量或命令行参数更改
EXPOSE 8000

# 定义环境变量
# 这些可以在运行容器时被覆盖
# 数据库文件路径
ENV DATABASE_URL=sqlite+aiosqlite:///./athlete.db
# Uvicorn host 和 port
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000
# 允许的 CORS 源，生产环境应设置为具体的域名
ENV ALLOWED_ORIGINS=*
# MCP 工具基地址，这里假设后端 API 和此应用在同一容器或通过网络访问
# 如果 MCP 工具指向的是容器内的另一个服务，需要相应调整
ENV MCP_TOOLS_BASE_URL=http://localhost:8000/mcp/

# 运行应用
# 使用 uv run 来执行 uvicorn 命令
# 注意：移除了 --reload 选项，因为这是生产环境
# --host 和 --port 从环境变量获取
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]