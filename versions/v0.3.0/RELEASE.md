# 版本 v0.3.0 — 前后端真实连通

> 日期: 2026-07-13  
> Commit: 050bd9a
> 目标: 改造前端使用真实 API，实现数据持久化

---

## 📋 变更摘要

| 类型 | 数量 | 说明 |
|------|------|------|
| 新增功能 | 0 | — |
| Bug 修复 | 0 | — |
| 重构优化 | 14 | page-common.js 重写 + 13 个 HTML 页面适配 |
| 文档更新 | 1 | 版本记录 |

---

## ✅ 详细变更

### page-common.js 重写
- 新增 API 模式：传入 `api` 配置（findPage/findById/add/edit/delete）和 `renderRow` 回调
- 保持向后兼容：不传 `api` 配置时保持原有静态数据行为
- 实现真正的 CRUD：数据加载、搜索、删除、分页全部调用后端 API
- 统一弹窗、Toast、Hash 深度链接等基础能力

### 13 个 HTML 页面适配
- 移除所有静态 `<tbody>` 硬编码数据，替换为动态渲染
- 各页面配置 `api` 对象和 `renderRow` 回调
- 已适配：building、owner、tenant、employee、visitor、rental、payment、repair、notice、user、access

### API 字段对齐
- 修复 owner 字段 `name`/`ownerName` 映射
- 修复 tenant 字段 `name`/`tenantName` 映射

---

## 📊 代码 Diff 摘要

```diff
page-common.js: 重写（支持 API 模式 + 静态模式）
building.html: 移除静态数据，接入 building API
owner.html: 移除静态数据，接入 owner API
tenant.html: 移除静态数据，接入 tenant API
employee.html: 移除静态数据，接入 employee API
visitor.html: 移除静态数据，接入 visitor API
rental.html: 移除静态数据，接入 rental API
payment.html: 移除静态数据，接入 payment API
repair.html: 移除静态数据，接入 repair API
notice.html: 移除静态数据，接入 notice API
user.html: 移除静态数据，接入 user API
access.html: 移除静态数据，接入 access API
```

---

## 📁 受影响文件列表

**新增文件:**
- `versions/v0.3.0/RELEASE.md`

**修改文件:**
- `src/main/resources/static/js/page-common.js`
- `src/main/resources/static/pages/building.html`
- `src/main/resources/static/pages/owner.html`
- `src/main/resources/static/pages/tenant.html`
- `src/main/resources/static/pages/employee.html`
- `src/main/resources/static/pages/visitor.html`
- `src/main/resources/static/pages/rental.html`
- `src/main/resources/static/pages/payment.html`
- `src/main/resources/static/pages/repair.html`
- `src/main/resources/static/pages/notice.html`
- `src/main/resources/static/pages/user.html`
- `src/main/resources/static/pages/access.html`

---

## 🧪 测试结果

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 编译 | ✅ | mvn clean compile |
| 启动 | ✅ | Tomcat started on port 8080 |
| building API | ✅ | 返回 5 条数据，含关联字段 |
| owner API | ✅ | 返回 100 条数据 |
| tenant API | ✅ | 返回 15 条数据 |
| 登录页 | ✅ | 页面加载正常 |
| JWT 拦截 | ✅ | 未认证返回 401 |

---

## 📝 遗留问题

1. **AI 催缴仍为模拟**：需配置 DeepSeek API Key
2. **部分弹窗缺失表单**：facility 等页面需补全
3. **未测试模块**：shop、parking、facility 使用独立 axios 代码，需验证
4. **业务方法不完整**：退租、到期预警、派单功能待后端补充
5. **未执行测试**：需全模块功能测试

---

## 🔧 技术说明

### page-common.js v3 使用方式

```javascript
initPage({
  name: '模块名称',
  api: {
    findPage: API.moduleFindPage,
    findById: API.moduleFindById,
    add: API.moduleAdd,
    edit: API.moduleEdit,
    delete: API.moduleDelete
  },
  renderRow: function(item, index) {
    return '<td>' + item.field1 + '</td><td>' + item.field2 + '</td>';
  },
  hashActions: { add: function(){ openAddModal(); } }
});
```

