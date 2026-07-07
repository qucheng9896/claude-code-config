/**
 * API 接口统一管理
 * 对应后端 Controller 路由
 */
var API = {
    // 用户认证
    login: function(data) { return axios.post('/user/login', data); },
    logout: function() { return axios.post('/user/logout'); },
    userInfo: function() { return axios.get('/user/info'); },
    changePassword: function(data) { return axios.put('/user/password', data); },

    // 业主管理
    ownerFindPage: function(data) { return axios.post('/owner/findPage', data); },
    ownerFindById: function(id) { return axios.get('/owner/findById/' + id); },
    ownerAdd: function(data) { return axios.post('/owner/add', data); },
    ownerEdit: function(data) { return axios.put('/owner/edit', data); },
    ownerDelete: function(id) { return axios.delete('/owner/delete/' + id); },

    // 房屋管理
    houseFindPage: function(data) { return axios.post('/house/findPage', data); },
    houseFindById: function(id) { return axios.get('/house/findById/' + id); },
    houseAdd: function(data) { return axios.post('/house/add', data); },
    houseEdit: function(data) { return axios.put('/house/edit', data); },
    houseDelete: function(id) { return axios.delete('/house/delete/' + id); },

    // 缴费管理
    paymentFindPage: function(data) { return axios.post('/payment/findPage', data); },
    paymentOverdue: function() { return axios.get('/payment/overdue'); },
    paymentGenerate: function(data) { return axios.post('/payment/generateBills', data); },
    paymentPay: function(id) { return axios.put('/payment/pay/' + id); },
    paymentConfirm: function(id) { return axios.put('/payment/confirm/' + id); },
    paymentDelete: function(id) { return axios.delete('/payment/delete/' + id); },

    // AI催缴（新功能）
    aiPreviewRemind: function(ownerId) { return axios.post('/payment/ai/preview', { ownerId: ownerId }); },
    aiBatchPreview: function() { return axios.post('/payment/ai/batchPreview'); },
    aiSendRemind: function(logId) { return axios.post('/payment/ai/send/' + logId); },
    aiRemindLogs: function(data) { return axios.post('/payment/ai/logs', data); },

    // 用户管理
    userFindPage: function(data) { return axios.post('/user/findPage', data); },
    userAdd: function(data) { return axios.post('/user/add', data); },
    userEdit: function(data) { return axios.put('/user/edit', data); },
    userDelete: function(id) { return axios.delete('/user/delete/' + id); },

    // 数据概览
    dashboardOverview: function() { return axios.get('/dashboard/overview'); },
    dashboardPayment: function() { return axios.get('/dashboard/payment'); },
    dashboardRepair: function() { return axios.get('/dashboard/repair'); },
    dashboardAi: function() { return axios.get('/dashboard/ai'); },

    // 房产管理
    buildingFindPage: function(data) { return axios.post('/building/findPage', data); },
    buildingAdd: function(data) { return axios.post('/building/add', data); },
    buildingEdit: function(data) { return axios.put('/building/edit', data); },
    buildingDelete: function(id) { return axios.delete('/building/delete/' + id); },

    // 商铺管理
    shopFindPage: function(data) { return axios.post('/shop/findPage', data); },
    shopAdd: function(data) { return axios.post('/shop/add', data); },
    shopEdit: function(data) { return axios.put('/shop/edit', data); },
    shopDelete: function(id) { return axios.delete('/shop/delete/' + id); },

    // 车位管理
    parkingFindPage: function(data) { return axios.post('/parking/findPage', data); },
    parkingAdd: function(data) { return axios.post('/parking/add', data); },
    parkingEdit: function(data) { return axios.put('/parking/edit', data); },
    parkingDelete: function(id) { return axios.delete('/parking/delete/' + id); },

    // 公共设施
    facilityFindPage: function(data) { return axios.post('/facility/findPage', data); },
    facilityAdd: function(data) { return axios.post('/facility/add', data); },
    facilityEdit: function(data) { return axios.put('/facility/edit', data); },
    facilityDelete: function(id) { return axios.delete('/facility/delete/' + id); },

    // 租户管理
    tenantFindPage: function(data) { return axios.post('/tenant/findPage', data); },
    tenantAdd: function(data) { return axios.post('/tenant/add', data); },
    tenantEdit: function(data) { return axios.put('/tenant/edit', data); },
    tenantDelete: function(id) { return axios.delete('/tenant/delete/' + id); },

    // 租赁管理
    rentalFindPage: function(data) { return axios.post('/rental/findPage', data); },
    rentalAdd: function(data) { return axios.post('/rental/add', data); },
    rentalEdit: function(data) { return axios.put('/rental/edit', data); },
    rentalDelete: function(id) { return axios.delete('/rental/delete/' + id); },

    // 报修管理
    repairFindPage: function(data) { return axios.post('/repair/findPage', data); },
    repairAdd: function(data) { return axios.post('/repair/add', data); },
    repairEdit: function(data) { return axios.put('/repair/edit', data); },
    repairDelete: function(id) { return axios.delete('/repair/delete/' + id); },

    // 公告管理
    noticeFindPage: function(data) { return axios.post('/notice/findPage', data); },
    noticeAdd: function(data) { return axios.post('/notice/add', data); },
    noticeEdit: function(data) { return axios.put('/notice/edit', data); },
    noticeDelete: function(id) { return axios.delete('/notice/delete/' + id); },

    // 员工管理
    employeeFindPage: function(data) { return axios.post('/employee/findPage', data); },
    employeeAdd: function(data) { return axios.post('/employee/add', data); },
    employeeEdit: function(data) { return axios.put('/employee/edit', data); },
    employeeDelete: function(id) { return axios.delete('/employee/delete/' + id); },

    // 访客管理
    visitorFindPage: function(data) { return axios.post('/visitor/findPage', data); },
    visitorAdd: function(data) { return axios.post('/visitor/add', data); },
    visitorEdit: function(data) { return axios.put('/visitor/edit', data); },
    visitorDelete: function(id) { return axios.delete('/visitor/delete/' + id); }
};
