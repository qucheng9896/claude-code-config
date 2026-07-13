# 变更日志 (Change Log)

本文档记录智慧物业管理系统的所有迭代变更，包括版本号、变更内容、代码 diff 摘要和日期。

---

## 版本规范

采用语义化版本号：`MAJOR.MINOR.PATCH`

- **MAJOR**: 重大功能变更（如架构调整）
- **MINOR**: 新功能模块增加
- **PATCH**: Bug 修复、小改动

---

## 迭代记录

### [v0.2.0] - 2026-07-13 — 环境配置与数据库初始化

#### 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 文档更新 | 1 | 环境配置与运行记录 |

#### ✅ 已完成

- **环境配置**: 确认 JAVA_HOME (Corretto 1.8.0_492) + Maven 3.9.5 + MySQL 8.0.19
- **数据库初始化**: `db_init.sql` 执行成功，18 张表 + 3 视图 + 完整初始数据
- **编译验证**: `mvn clean compile` 通过，102 个 .class 文件
- **启动验证**: `mvn spring-boot:run` 成功，端口 8080
- **接口验证**: 登录 / 房屋分页 / Dashboard 统计 / JWT 拦截 全部通过

#### 📊 验证结果

```
登录接口:  POST /user/login       → ✅ 返回 JWT Token
房屋接口:  POST /house/findPage   → ✅ 460 条数据，含关联名称
统计接口:  GET  /dashboard/overview → ✅ 真实统计数据
JWT拦截:   未认证访问              → ✅ 返回 401
```

##### 数据库状态

| 表 | 记录数 | 表 | 记录数 |
|------|--------|------|--------|
| t_house | 460 | t_shop | 36 |
| t_owner | 100 | t_parking | 580 |
| t_tenant | 15 | t_rental | 386 |
| t_payment | 2316 | t_building | 5 |
| t_employee | 16 | t_user | 1 |
| t_visitor | 20 | t_notice | 9 |
| t_repair_order | 30 | t_facility | 24 |
| t_ai_remind_log | 0 | t_access_record | 0 |

#### 📁 新增文件

```
versions/v0.2.0/RELEASE.md
```

#### 🔗 Git 信息

```
Tag: v0.2.0
Commit: [待提交]
```

---

### [v0.1.0] - 2026-07-13 — 项目基线版本

#### 📋 项目状态快照

| 组件 | 状态 | 说明 |
|------|------|------|
| 数据库 | ✅ 100% | 18 张表 + 3 视图 + 初始化数据 |
| 后端骨架 | ✅ 85% | Controller/Service/Dao 已建 |
| 前端页面 | ✅ 90% | 23 个页面框架完成 |
| **前后端真实对接** | **~20%** | **大部分页面使用静态数据** |
| 业务功能 | ⚠️ 60% | 缺少退租、派单等功能 |

#### ✅ 已完成

- **数据库设计**: 完整的 `db_init.sql`，包含 18 张业务表、3 个视图、索引/外键、初始化数据
- **后端基础框架**: 泛型继承体系 `BaseDao → BaseService → BaseServiceImpl → BaseController`
- **用户认证**: JWT 登录、拦截器、MD5 加密
- **CRUD 模块**: 业主、房屋、楼栋、商铺、车位、租户、员工、访客、租赁、缴费、报修、公告（各 5 个基础接口）
- **缴费管理**: 批量生成账单、缴费、确认到账、逾期查询
- **AI 催缴**: 基础框架完成（当前为模拟输出，预留 DeepSeek API 接入）
- **数据概览**: 4 个统计接口（overview/payment/repair/ai）
- **前端页面**: 23 个 HTML 页面 + 公共样式 + 侧边栏导航

#### ⚠️ 已知问题

1. **前后端未真正连通**: `page-common.js` 使用内存静态数据，搜索/删除/编辑不会持久化
2. **业务方法不完整**: 缺少退租处理、到期预警、派单、评价等功能
3. **AI 催缴为模拟**: 使用 `simulateAiCall()` 字符串拼接，未调用真实 API
4. **弹窗缺失**: `facility.html` 等页面缺少 `addModal`/`editModal` 表单
5. **前端静态数据**: 各页面表格行硬编码在 HTML 中

#### 📊代码 Diff 摘要

```
项目基线统计:
- Java 文件: 80+ 个
- XML Mapper: 15 个
- 前端页面: 23 个 HTML + 4 个 JS 模块 + 1 个 CSS
- 数据库表: 18 个
- 视图: 3 个
```

#### 📁 文件清单

**后端核心:**
- `controller/` — 15 个控制器 + BaseController
- `service/` — 15 个 Service 接口 + 实现
- `service/ai/` — AI 催缴服务
- `dao/` — 15 个 Mapper 接口 + BaseDao
- `pojo/` — 18 个实体类
- `config/` — WebConfig, AiConfig, AiService
- `interceptor/` — AuthInterceptor
- `util/` — JwtUtil, MD5Util

**前端核心:**
- `css/common.css` — 全局样式系统
- `js/api.js` — API 接口定义
- `js/axios-config.js` — HTTP 配置
- `js/page-common.js` — 通用 CRUD 逻辑
- `js/sidebar.js` — 侧边栏导航
- `pages/*.html` — 23 个业务页面

---

## 后续迭代计划

### 第一阶段: 前后端真实连通
- [ ] 改造 `page-common.js` 调用后端 API
- [ ] 各模块实现真正的数据持久化
- [ ] 环境配置与数据库初始化

### 第二阶段: 补齐业务功能
- [ ] 租户退租处理
- [ ] 租赁到期预警
- [ ] 报修派单/评价
- [ ] 缺失弹窗修复

### 第三阶段: 完善与测试
- [ ] AI 催缴功能完善
- [ ] 全模块功能测试
- [ ] 系统联调
- [ ] 打包部署验证

---

> 📝 **记录规范**: 每次迭代需更新版本号、记录变更内容、列出受影响文件、保存关键代码 diff 片段。

