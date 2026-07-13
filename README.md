# 智慧物业 (Smart Property)

物业管理系统毕业设计项目 — Spring Boot 后端 + 纯静态 HTML/JS 前端。

## 技术栈

- **后端**：Java 8 / Spring Boot 2.7 / MyBatis / Druid / MySQL 8.0
- **前端**：原生 HTML + CSS + JavaScript（无构建工具，Axios CDN）
- **认证**：JWT Bearer Token
- **AI**：可选 DeepSeek API 催缴提醒（默认关闭）

## 快速开始

```bash
# 1. 数据库初始化
# 创建数据库 property_management，执行 src/main/resources/db_init.sql

# 2. 编译运行
mvn clean compile
mvn spring-boot:3

# 4. 访问 http://localhost:8080
# 默认账号：admin / 123456
```

## 项目结构

```
src/main/
├── java/com/wygl/
│   ├── controller/    # REST 控制器（15 个）
│   ├── service/       # 业务逻辑接口 + 实现
│   ├── dao/           # MyBatis Mapper 接口
│   ├── pojo/          # 实体类
│   ├── config/        # WebConfig / AiConfig
│   ├── interceptor/   # JWT 认证拦截器
│   ├── result/        # Result / PageResult 统一响应
│   └── util/          # JWT / MD5 工具类
├── resources/
│   ├── mapper/        # MyBatis XML 映射文件
│   ├── static/        # 前端静态资源
│   │   ├── css/       # 公共样式
│   │   ├── js/        # api.js / page-common.js / sidebar.js
│   │   └── pages/     # 19 个业务页面
│   └── db_init.sql    # 数据库初始化脚本
└── ...
```

## 功能模块

| 模块 | 页面 | 说明 |
|------|------|------|
| 用户管理 | user.html | 系统用户、角色权限 |
| 业主管理 | owner.html | 业主档案 |
| 租户管理 | tenant.html | 租户档案、退租办理 |
| 房屋管理 | house.html | 房屋档案、状态 |
| 楼栋管理 | building.html | 楼栋信息 |
| 商铺管理 | shop.html | 商铺档案 |
| 停车位管理 | parking.html | 车位档案 |
| 租赁管理 | rental.html | 租赁合同、续签、终止 |
| 访客管理 | visitor.html | 访客登记、核验、取消 |
| 报修服务 | repair.html | 报修工单、派单、评价 |
| 收费管理 | payment.html | 账单管理、AI 催缴 |
| 设施管理 | facility.html | 公共设施 |
| 门禁管理 | access.html | 门禁记录 |
| 公告管理 | notice.html | 物业公告 |
| 仪表盘 | dashboard.html | 数据概览统计 |

## API 规范

所有响应统一使用 `Result` 格式：

```json
{
  "flag": true,
  "message": "操作成功",
  "data": { ... }
}
```

分页使用 `PageResult`：

```json
{
  "total": 100,
  "rows": [ ... ]
}
```

## 数据库表

所有表以 `t_` 前缀命名：`t_user`, `t_owner`, `t_house`, `t_building`, `t_rental`, `t_payment` 等。

## License

仅供毕业设计使用。
