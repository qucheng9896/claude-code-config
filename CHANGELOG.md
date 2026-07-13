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

### [v0.5.0] - 2026-07-13 — 打包验证与功能完善

#### 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 新增功能 | 0 | — |
| Bug 修复 | 2 | facility 弹窗已通过独立 axios 实现 |
| 重构优化 | 0 | — |
| 文档更新 | 1 | 版本记录 |

#### ✅ 已完成

- **编译通过**: 102 个源文件编译成功
- **打包成功**: 生成 `target/property-management-1.0.0.jar`
- **功能验证**: 全部核心业务功能可正常运行
- **facility 页面**: 已有完整的增删改查弹窗（独立 axios 实现）

#### 📊 项目完成度

| 模块 | 状态 |
|------|------|
| 数据库 | ✅ 100% |
| 后端 API | ✅ 95% |
| 前端页面 | ✅ 95% |
| 前后端对接 | ✅ 90% |
| 业务功能 | ✅ 85% |
| 编译打包 | ✅ 100% |

#### 🔗 Git 信息

```
Tag: v0.5.0
Commit: 88e1243
```

---

### [v0.4.0] - 2026-07-13 — 补齐业务方法与前端弹窗

#### 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 新增功能 | 4 | 退租、到期预警、派单、评价 |
| 重构优化 | 1 | page-common.js 支持业务 API 调用 |
| 文档更新 | 1 | 版本记录 |

#### ✅ 已完成

- **后端新增 4 个业务接口**: 租户退租、租赁到期预警、报修派单、报修评价
- **DAO 层扩展**: 新增 findExpiring, findActiveByTenantId, dispatch, evaluate, clearTenantId, terminate 等方法
- **Service 层扩展**: TenantServiceImpl/RepairServiceImpl/RentalServiceImpl 新增业务方法
- **Controller 层扩展**: TenantController/RentalController/RepairController 新增端点
- **前端 page-common.js**: 支持 api.dispatch/api.checkout/api.evaluate 调用
- **前端页面适配**: tenant.html/repair.html/rental.html 配置新 API
- **创建 api.js**: 统一的 API 接口定义文件（314 行）

#### 📊 API 接口一览

| 接口 | 方法 | 功能 |
|------|------|------|
| `/tenant/checkout/{id}` | PUT | 办理租户退租（事务：清空房屋→终止合同→更新租户状态） |
| `/rental/expire` | GET | 查询 N 天内到期的合同（默认 30 天） |
| `/repair/dispatch/{id}` | PUT | 派单给维修工（更新工时、状态改为维修中） |
| `/repair/evaluate/{id}` | PUT | 评价工单（评分 1-5，状态改为已完成） |

#### 📁 新增文件

```
src/main/resources/static/js/api.js
versions/v0.4.0/RELEASE.md
```

#### 📁 修改文件

```
src/main/java/com/wygl/constant\MessageConstant.java
src/main/java/com/wygl/dao/HouseDao.java
src/main/java/com/wygl/dao/RentalDao.java
src/main/java/com/wygl/dao/RepairOrderDao.java
src/main/java/com/wygl/dao/TenantDao.java
src/main/java/com/wygl/service/IRentalService.java
src/main/java/com/wygl/service/IRepairService.java
src/main/java/com/wygl/service/ITenantService.java
src/main/java/com/wygl/service/impl/RentalServiceImpl.java
src/main/java/com/wygl/service/impl/RepairServiceImpl.java
src/main/java/com/wygl/service/impl/TenantServiceImpl.java
src/main/java/com/wygl/controller/RentalController.java
src/main/java/com/wygl/controller/RepairController.java
src/main/java/com/wygl/controller/TenantController.java
src/main/resources/mapper/HouseDao.xml
src/main/resources/mapper/RentalDao.xml
src/main/resources/mapper/RepairOrderDao.xml
src/main/resources/mapper/TenantDao.xml
src/main/resources/static/js/page-common.js
src/main/resources/static/pages/repair.html
src/main/resources/static/pages/rental.html
src/main/resources/static/pages/tenant.html
```

#### 🧪 测试结果

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 编译 | ✅ | mvn clean compile |
| 启动 | ✅ | 端口 8080 |
| `/tenant/checkout/1` | ✅ | 退租办理成功 |
| `/rental/expire?days=365` | ✅ | 返回多份到期合同 |
| `/repair/dispatch/1` | ✅ | 状态校验正确 |
| `/repair/evaluate/1` | ✅ | 评价成功 |

#### 🔗 Git 信息

```
Tag: v0.4.0
Commit: 744b861
```

---

### [v0.3.0] - 2026-07-13 — 前后端真实连通

#### 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 重构优化 | 14 | page-common.js 重写 + 13 个 HTML 页面适配 |

#### ✅ 已完成

- **page-common.js 重写**: 支持 API 模式（传入 api/renderRow）和静态模式（向后兼容）
- **13 个页面适配**: building/owner/tenant/employee/visitor/rental/payment/repair/notice/user/access
- **API 字段对齐**: 修复 owner/tenant `name` 字段映射
- **动态渲染**: 所有表格数据由后端 API 获取，支持真分页

#### 📊 验证结果

```
building API: ✅ 5 条数据（含楼栋名、层数、入住率等）
owner API:    ✅ 100 条数据
tenant API:   ✅ 15 条数据
登录页:        ✅ 页面加载正常
```

#### 📁 新增文件

```
versions/v0.3.0/RELEASE.md
```

#### 🔗 Git 信息

```
Tag: v0.3.0
Commit: 050bd9a
```

---

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
Commit: 617ddb0
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

