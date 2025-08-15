# 运动员管理后端

这是一个使用 FastAPI 和 SQLite 构建的运动员管理后端 API，支持增删改查和分页功能。

## 功能

- 创建运动员信息
- 获取运动员列表（支持分页）
- 获取单个运动员信息
- 更新运动员信息
- 删除运动员信息（软删除）

## 字段

- id (主键, 自增)
- 姓名 (name)
- 身高 (height)
- 体重 (weight)
- 描述 (description)
- 创建时间 (created_at)
- 更新时间 (updated_at)
- 删除时间 (deleted_at)
- 删除标记 (is_deleted)
- 项目 (sport_event)
- 年龄 (age)
- 籍贯 (hometown)
- 备注 (remarks)

## 安装

确保你已经安装了 `uv` 工具。

```bash
# 克隆项目
git clone <repository-url>
cd athlete-player-ai-manager

# 安装依赖
uv sync
```

## 运行

```bash
# 启动服务器
uv run main.py
```

服务器将在 `http://localhost:8000` 上运行。

## API 文档

访问 `http://localhost:8000/docs` 查看自动生成的 API 文档。

## 许可证

MIT