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
    userDelete: function(id) { return axios.delete('/user/delete/' + id); }
};
