# 版本 v0.4.0 — 补齐业务方法与前端弹窗

> 日期: 2026-07-13  
> Commit: 744b861  
> 目标: 补充退租、到期预警、派单、评价业务方法

---

## 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 新增功能 | 4 | 退租、到期预警、派单、评价 |
| 重构优化 | 1 | page-common.js 支持业务 API 调用 |
| 文档更新 | 1 | 版本记录 |

---

## ✅ 详细变更

### 后端新增 4 个业务接口

#### 1. 租户退租 `PUT /tenant/checkout/{id}`
- 事务操作：清空房屋租户 → 终止合同 → 更新租户状态
- 校验：租户是否存在、是否已退租、是否有有效合同

#### 2. 租赁到期预警 `GET /rental/expire?days=30`
- 查询 N 天内到期的合同（默认 30 天）
- 返回字段：合同信息 + 业主名 + 租户名 + 房屋地址 + 剩余天数

#### 3. 报修派单 `PUT /repair/dispatch/{id}?workerId=&workerName=`
- 校验工单状态必须为待派单(0)
- 更新维修工信息、状态改为维修中(1)、记录派单时间

#### 4. 报修评价 `PUT /repair/evaluate/{id}?evaluation=`
- 校验工单状态必须为维修中(1)
- 更新评价星级、状态改为已完成(2)、记录完成时间

### DAO 层扩展
- HouseDao: clearTenantId, updateStatus
- RentalDao: findExpiring, findActiveByTenantId, terminate
- RepairOrderDao: dispatch, evaluate
- TenantDao: updateStatus

### Service 层扩展
- TenantServiceImpl: checkout (事务方法)
- RentalServiceImpl: findExpiring, findActiveByTenantId
- RepairServiceImpl: dispatch, evaluate

### Controller 层扩展
- TenantController: checkout
- RentalController: expire
- RepairController: dispatch, evaluate

### 前端适配
- page-common.js: 支持 api.dispatch/api.checkout/api.evaluate 调用
- tenant.html: 配置 checkout API
- repair.html: 配置 dispatch/evaluate API
- rental.html: 配置 expire hashAction
- api.js: 统一 API 接口定义（314 行）

---

## 📊 代码 Diff 摘要

```diff
+ 新增文件:
  src/main/resources/static/js/api.js (314 行)
  versions/v0.4.0/RELEASE.md

~ 修改文件 (22 个):
  MessageConstant.java, HouseDao.xml, RentalDao.xml, RepairOrderDao.xml, TenantDao.xml,
  TenantDao.java, RentalDao.java, RepairOrderDao.java, HouseDao.java,
  ITenantService.java, IRentalService.java, IRepairService.java,
  TenantServiceImpl.java, RentalServiceImpl.java, RepairServiceImpl.java,
  TenantController.java, RentalController.java, RepairController.java,
  page-common.js, tenant.html, repair.html, rental.html
```

---

## 📁 受影响文件列表

**新增文件:**
- `src/main/resources/static/js/api.js`
- `versions/v0.4.0/RELEASE.md`

**修改文件:**
- `src/main/java/com/wygl/constant/messageConstant.java`
- `src/main/java/com/wygl/dao/HouseDao.java`
- `src/main/java/com/wygl/dao/RentalDao.java`
- `src/main/java/com/wygl/dao/RepairOrderDao.java`
- `src/main/java/com/wygl/dao/TenantDao.java`
- `src/main/java/com/wygl/service/IRentalService.java`
- `src/main/java/com/wygl/service/IRepairService.java`
- `src/main/java/com/wygl/service/ITenantService.java`
- `src/main/java/com/wygl/service/impl/RentalServiceImpl.java`
- `src/main/java/com/wygl/service/impl/RepairServiceImpl.java`
- `src/main/java/com/wygl/service/impl/TenantServiceImpl.java`
- `src/main/java/com/wygl/controller/RentalController.java`
- `src/main/java/com/wygl/controller/RepairController.java`
- `src/main/java/com/wygl/controller/TenantController.java`
- `src/main/resources/mapper/HouseDao.xml`
- `src/main/resources/mapper/RentalDao.xml`
- `src/main/resources/mapper/RepairOrderDao.xml`
- `src/main/resources/mapper/TenantDao.xml`
- `src/main/resources/static/js/page-common.js`
- `src/main/resources/static/pages/repair.html`
- `src/main/resources/static/pages/rental.html`
- `src/main/resources/static/pages/tenant.html`

---

## 🧪 测试结果

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 编译 | ✅ | mvn clean compile |
| 启动 | ✅ | 端口 8080 |
| `/tenant/checkout/1` | ✅ | 退租办理成功 |
| `/rental/expire?days=365` | ✅ | 返回多份到期合同 |
| `/repair/dispatch/1` | ✅ | 状态校验正确（非待派单拒绝） |
| `/repair/evaluate/1` | ✅ | 评价成功 |

---

## 📝 遗留问题

1. **AI 催缴仍为模拟**：需配置 DeepSeek API Key
2. **部分弹窗缺失表单**：facility 等页面需补全
3. **shop/parking/facility 页面**：使用独立 axios 代码，需验证
4. **系统全模块测试**：需完整功能测试

---

## 🔧 技术说明

### 退租事务流程
```
1. 校验租户是否存在且状态为在租(1)
2. 查询租户的有效合同(status=1)
3. 更新房屋：tenant_id=NULL, status=0（空闲）
4. 更新合同：status=0（已终止）
5. 更新租户：status=0（已退租）
```

### 到期预警 SQL 逻辑
```sql
WHERE r.status = 1 
  AND r.end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL #{days} DAY)
```

