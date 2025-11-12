# 运动员CRUD API调用流程图

```mermaid
graph TD
    A[HTTP客户端请求] --> B{FastAPI路由匹配}
    B -->|POST /athletes/| C[create_athlete]
    B -->|GET /athletes/| D[read_athletes<br/>分页: skip, limit]
    B -->|GET /athletes/{id}| E[read_athlete<br/>ID: athlete_id]
    B -->|PUT /athletes/{id}| F[update_athlete<br/>ID: athlete_id]
    B -->|DELETE /athletes/{id}| G[delete_athlete<br/>ID: athlete_id]
    B -->|POST /athletes/search/| H[search_athletes<br/>搜索参数]

    %% 创建流程
    C --> C1[校验请求体<br/>schemas.AthleteCreate]
    C1 --> C2[依赖注入: get_db<br/>获取 AsyncSession]
    C2 --> C3[调用 crud.create_athlete]
    C3 --> C4[SQLAlchemy ORM:<br/>db_athlete = Athlete(**data)]
    C4 --> C5[db.add(db_athlete)]
    C5 --> C6[db.commit()]
    C6 --> C7[db.refresh(db_athlete)]
    C7 --> C8[返回 schemas.AthleteInDB]

    %% 读取列表流程
    D --> D1[依赖注入: get_db]
    D1 --> D2[调用 crud.get_athletes<br/>skip, limit]
    D2 --> D3[SQLAlchemy查询:<br/>SELECT * FROM athletes<br/>WHERE is_deleted=false<br/>OFFSET skip LIMIT limit]
    D3 --> D4[返回运动员列表]

    %% 读取单个流程
    E --> E1[依赖注入: get_db]
    E1 --> E2[调用 crud.get_athlete<br/>athlete_id]
    E2 --> E3[SQLAlchemy查询:<br/>SELECT * FROM athletes<br/>WHERE id=id AND is_deleted=false]
    E3 --> E4{运动员存在?}
    E4 -->|是| E5[返回运动员信息]
    E4 -->|否| E6[抛出 404 异常<br/>Athlete not found]

    %% 更新流程
    F --> F1[校验请求体<br/>schemas.AthleteUpdate]
    F1 --> F2[依赖注入: get_db]
    F2 --> F3[调用 crud.update_athlete<br/>athlete_id, athlete]
    F3 --> F4[SQLAlchemy查询:<br/>WHERE id=id AND is_deleted=false]
    F4 --> F5{运动员存在?}
    F5 -->|是| F6[更新字段<br/>setattr]
    F6 --> F7[db.commit()]
    F7 --> F8[返回更新后数据]
    F5 -->|否| F9[抛出 404 异常]

    %% 删除流程（软删除）
    G --> G1[依赖注入: get_db]
    G1 --> G2[调用 crud.delete_athlete<br/>athlete_id]
    G2 --> G3[SQLAlchemy查询:<br/>WHERE id=id AND is_deleted=false]
    G3 --> G4{运动员存在?}
    G4 -->|是| G5[设置 is_deleted=true<br/>deleted_at=now()]
    G5 --> G6[db.commit()]
    G6 --> G7[返回删除结果]
    G4 -->|否| G8[抛出 404 异常]

    %% 搜索流程
    H --> H1[校验请求体<br/>schemas.AthleteSearch]
    H1 --> H2[依赖注入: get_db]
    H2 --> H3[调用 crud.search_athletes<br/>search_params, skip, limit]
    H3 --> H4[构建SQLAlchemy查询:<br/>WHERE is_deleted=false]
    H4 --> H5{添加搜索条件}
    H5 -->|name| H6[AND name ILIKE %name%]
    H5 -->|sport_event| H7[AND sport_event ILIKE %event%]
    H5 -->|hometown| H8[AND hometown ILIKE %hometown%]
    H5 -->|min_age/max_age| H9[AND age BETWEEN min_age AND max_age]
    H5 -->|min_height/max_height| H10[AND height BETWEEN min_height AND max_height]
    H5 -->|min_weight/max_weight| H11[AND weight BETWEEN min_weight AND max_weight]
    H6 --> H12[EXECUTE query<br/>OFFSET skip LIMIT limit]
    H7 --> H12
    H8 --> H12
    H9 --> H12
    H10 --> H12
    H11 --> H12
    H12 --> H13[返回匹配运动员列表]

    %% 响应
    C8 --> R1[HTTP 201 Created<br/>响应体: AthleteInDB]
    D4 --> R2[HTTP 200 OK<br/>响应体: List[AthleteInDB]]
    E5 --> R3[HTTP 200 OK<br/>响应体: AthleteInDB]
    F8 --> R4[HTTP 200 OK<br/>响应体: AthleteInDB]
    G7 --> R5[HTTP 200 OK<br/>响应体: AthleteInDB]
    H13 --> R6[HTTP 200 OK<br/>响应体: List[AthleteInDB]]
    E6 --> R7[HTTP 404 Not Found]
    F9 --> R8[HTTP 404 Not Found]
    G8 --> R9[HTTP 404 Not Found]
```

## API端点总览

| 方法 | 路径 | 描述 | 响应状态 |
|------|------|------|----------|
| POST | `/athletes/` | 创建新运动员 | 201 |
| GET | `/athletes/` | 获取运动员列表 | 200 |
| GET | `/athletes/{id}` | 获取单个运动员 | 200/404 |
| PUT | `/athletes/{id}` | 更新运动员信息 | 200/404 |
| DELETE | `/athletes/{id}` | 删除运动员 | 200/404 |
| POST | `/athletes/search/` | 搜索运动员 | 200 |

## 关键特性

### 1. 软删除机制
- 删除操作设置 `is_deleted=true` 而非物理删除
- 查询时自动过滤 `is_deleted=false` 的记录

### 2. 分页支持
- `GET /athletes/` 支持 `skip` 和 `limit` 参数
- 默认 limit=10

### 3. 灵活搜索
- 支持多字段模糊搜索（name, sport_event, hometown, description, remarks）
- 支持数值范围搜索（age, height, weight）
- 支持 min/max 组合查询

### 4. 异步数据库
- 使用 AsyncSQLAlchemy
- 所有数据库操作都是异步的
