# 运动员管理后端开发计划

## 目标
使用 FastAPI 和 SQLite 创建一个运动员管理模块的后端 API，支持增删改查和分页功能。

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

## 功能
- [x] 1. 初始化项目，安装 FastAPI, Uvicorn, SQLAlchemy
- [x] 2. 配置数据库连接和模型
- [x] 3. 创建运动员数据模型 (Athlete)
- [x] 4. 创建数据库表
- [x] 5. 实现运动员 CRUD API
  - [x] 5.1 创建运动员 (POST /athletes)
  - [x] 5.2 获取运动员列表 (GET /athletes) - 支持分页
  - [x] 5.3 获取单个运动员 (GET /athletes/{id})
  - [x] 5.4 更新运动员 (PUT /athletes/{id})
  - [x] 5.5 删除运动员 (DELETE /athletes/{id}) - 软删除
- [x] 6. 添加 Pydantic 模型用于请求和响应
- [ ] 7. 测试 API
- [x] 8. 更新 README.md
- [ ] 9. 最终审查和提交代码

## 审查
- [ ] 确保所有功能按要求实现
- [ ] 代码符合 Python 最佳实践
- [ ] 添加了必要的注释和文档