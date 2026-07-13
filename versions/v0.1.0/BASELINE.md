# 版本 v0.1.0 — 项目基线版本

> 日期: 2026-07-13  
> 目标: 建立项目基线，记录初始状态

---

## 📋 项目状态快照

### 后端模块完成度

| 模块 | Controller | Service | Dao | XML | 业务方法 | 状态 |
|------|-----------|---------|-----|-----|----------|------|
| 基础框架 | ✅ BaseController | ✅ BaseService | ✅ BaseDao | — | ✅ 5个通用CRUD | ✅ |
| 用户认证 | ✅ UserController | ✅ UserServiceImpl | ✅ UserDao | ✅ | ✅ 登录/改密/信息 | ✅ |
| 房产-楼栋 | ✅ BuildingController | ✅ BuildingServiceImpl | ✅ BuildingDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 房产-房屋 | ✅ HouseController | ✅ HouseServiceImpl | ✅ HouseDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 房产-商铺 | ✅ ShopController | ✅ ShopServiceImpl | ✅ ShopDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 房产-车位 | ✅ ParkingController | ✅ ParkingServiceImpl | ✅ ParkingDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 房产-设施 | ✅ FacilityController | ✅ FacilityServiceImpl | ✅ FacilityDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 人员-业主 | ✅ OwnerController | ✅ OwnerServiceImpl | ✅ OwnerDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 人员-租户 | ✅ TenantController | ✅ TenantServiceImpl | ✅ TenantDao | ✅ | ❌ 缺退租 | ❌ |
| 人员-员工 | ✅ EmployeeController | ✅ EmployeeServiceImpl | ✅ EmployeeDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 人员-访客 | ✅ VisitorController | ✅ VisitorServiceImpl | ✅ VisitorDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 租赁 | ✅ RentalController | ✅ RentalServiceImpl | ✅ RentalDao | ✅ | ❌ 缺到期预警 | ❌ |
| 收费 | ✅ PaymentController | ✅ PaymentServiceImpl | ✅ PaymentDao | ✅ | ✅ 批量生成/缴费/确认 | ✅ |
| 报修 | ✅ RepairController | ✅ RepairServiceImpl | ✅ RepairOrderDao | ✅ | ❌ 缺派单/评价 | ❌ |
| 公告 | ✅ NoticeController | ✅ NoticeServiceImpl | ✅ NoticeDao | ✅ | ⚠️ 仅基础CRUD | ⚠️ |
| 数据概览 | ✅ DashboardController | ✅ DashboardServiceImpl | — | — | ✅ 4个统计接口 | ✅ |
| AI催缴 | — | ✅ IAiRemindServiceImpl | ✅ AiRemindLogDao | ✅ | ⚠️ 模拟输出 | ⚠️ |

### 前端模块完成度

| 页面 | 结构 | 样式 | 静态交互 | API对接 | 状态 |
|------|------|------|----------|---------|------|
| index.html | ✅ | ✅ | ✅ | — | ✅ |
| landing.html | ✅ | ✅ | ✅ | — | ✅ |
| login.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| dashboard.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| building.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| house.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| shop.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| parking.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| facility.html | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| owner.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| tenant.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| employee.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| visitor.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| rental.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| payment.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| access.html | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| repair.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| notice.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| report.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| user.html | ✅ | ✅ | ✅ | ❌ | ⚠️ |

### 数据库完成度

| 项目 | 状态 | 说明 |
|------|------|------|
| 18 张表建表 SQL | ✅ | 完整 |
| 3 个视图 | ✅ | 租户缴费/月度收缴/租赁状态 |
| 初始化数据 | ✅ | 460户房屋 + 390合同 + 2760账单 |
| 索引/外键 | ✅ | 完整 |

---

## ⚠️ 关键问题清单

### P0 — 前后端未真正连通
- `page-common.js` 使用内存静态数据 `var tableData = opts.data || []`
- 搜索/删除/编辑只在浏览器内存中操作，刷新即丢失
- 所有 API 调用函数已在 `api.js` 定义但未使用

### P1 — 业务方法缺失
- 租户退租处理 (`tenant/checkout`)
- 租赁到期预警 (`rental/expire`)
- 报修派单 (`repair/dispatch`)
- 报修评价 (`repair/evaluate`)

### P2 — AI 催缴为模拟
- `simulateAiCall()` 只是简单字符串拼接
- DeepSeek API Key 未配置

### P3 — 前端弹窗缺失
- `facility.html` 缺少 addModal/editModal
- 部分页面弹窗表单字段不完整

---

## 📊 代码统计

```
后端:
- Java 源文件: 80+ 个
- MyBatis XML: 15 个
- 包层级: com.wygl (controller/service/dao/pojo/config/util/interceptor/exception/result)

前端:
- HTML 页面: 23 个
- JS 模块: 4 个 (api.js/axios-config.js/page-common.js/sidebar.js)
- CSS: 1 个 (common.css)

数据库:
- 表: 18 个
- 视图: 3 个
```

---

## 🔄 Git 状态

```
分支: master
最新提交: [待确认]
工作区: 干净
```

---

## 📁 关键文件路径

```
f:\毕业资料\毕业项目\
├── src/main/java/com/wygl/
│   ├── Application.java              # 启动类
│   ├── controller/                   # 15 个控制器
│   ├── service/                      # 业务层
│   ├── service/ai/                   # AI 催缴服务
│   ├── dao/                          # 持久层
│   ├── pojo/                         # 实体类
│   ├── config/                       # 配置类
│   ├── interceptor/                  # JWT 拦截器
│   ├── util/                         # 工具类
│   └── result/                       # 统一返回结果
├── src/main/resources/
│   ├── mapper/                       # MyBatis XML
│   ├── static/                       # 前端资源
│   │   ├── css/common.css            # 全局样式
│   │   ├── js/api.js                 # API 定义
│   │   ├── js/page-common.js         # 通用逻辑 ⚠️ 需改造
│   │   ├── js/sidebar.js             # 侧边栏
│   │   └── pages/*.html              # 23 个页面
│   ├── application.properties        # 配置
│   └── db_init.sql                   # 数据库脚本
├── pom.xml                           # Maven 配置
├── 设计文档.md                        # 设计文档
└── 开发进度.md                        # 进度跟踪
```

