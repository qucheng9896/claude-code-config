/**
 * API 接口定义 — 与后端 Controller 一一对应
 * 所有方法返回 Promise，响应格式: { flag: boolean, message: string, data: any }
 */
var API = (function() {

  function findPage(url, params) {
    return axios.post(url + '/findPage', params);
  }

  function findById(url, id) {
    return axios.get(url + '/findById/' + id);
  }

  function add(url, data) {
    return axios.post(url + '/add', data);
  }

  function edit(url, data) {
    return axios.put(url + '/edit', data);
  }

  function remove(url, id) {
    return axios.delete(url + '/delete/' + id);
  }

  return {

    // ==================== 用户认证 ====================
    userLogin: function(data) {
      return axios.post('/user/login', data);
    },
    userFindPage: function(params) {
      return findPage('/user', params);
    },
    userFindById: function(id) {
      return findById('/user', id);
    },
    userAdd: function(data) {
      return add('/user', data);
    },
    userEdit: function(data) {
      return edit('/user', data);
    },
    userDelete: function(id) {
      return remove('/user', id);
    },

    // ==================== 业主管理 ====================
    ownerFindPage: function(params) {
      return findPage('/owner', params);
    },
    ownerFindById: function(id) {
      return findById('/owner', id);
    },
    ownerAdd: function(data) {
      return add('/owner', data);
    },
    ownerEdit: function(data) {
      return edit('/owner', data);
    },
    ownerDelete: function(id) {
      return remove('/owner', id);
    },

    // ==================== 租户管理 ====================
    tenantFindPage: function(params) {
      return findPage('/tenant', params);
    },
    tenantFindById: function(id) {
      return findById('/tenant', id);
    },
    tenantAdd: function(data) {
      return add('/tenant', data);
    },
    tenantEdit: function(data) {
      return edit('/tenant', data);
    },
    tenantDelete: function(id) {
      return remove('/tenant', id);
    },
    tenantCheckout: function(id) {
      return axios.put('/tenant/checkout/' + id);
    },

    // ==================== 房屋管理 ====================
    houseFindPage: function(params) {
      return findPage('/house', params);
    },
    houseFindById: function(id) {
      return findById('/house', id);
    },
    houseAdd: function(data) {
      return add('/house', data);
    },
    houseEdit: function(data) {
      return edit('/house', data);
    },
    houseDelete: function(id) {
      return remove('/house', id);
    },

    // ==================== 楼栋管理 ====================
    buildingFindPage: function(params) {
      return findPage('/building', params);
    },
    buildingFindById: function(id) {
      return findById('/building', id);
    },
    buildingAdd: function(data) {
      return add('/building', data);
    },
    buildingEdit: function(data) {
      return edit('/building', data);
    },
    buildingDelete: function(id) {
      return remove('/building', id);
    },

    // ==================== 商铺管理 ====================
    shopFindPage: function(params) {
      return findPage('/shop', params);
    },
    shopFindById: function(id) {
      return findById('/shop', id);
    },
    shopAdd: function(data) {
      return add('/shop', data);
    },
    shopEdit: function(data) {
      return edit('/shop', data);
    },
    shopDelete: function(id) {
      return remove('/shop', id);
    },

    // ==================== 停车位管理 ====================
    parkingFindPage: function(params) {
      return findPage('/parking', params);
    },
    parkingFindById: function(id) {
      return findById('/parking', id);
    },
    parkingAdd: function(data) {
      return add('/parking', data);
    },
    parkingEdit: function(data) {
      return edit('/parking', data);
    },
    parkingDelete: function(id) {
      return remove('/parking', id);
    },

    // ==================== 租赁管理 ====================
    rentalFindPage: function(params) {
      return findPage('/rental', params);
    },
    rentalFindById: function(id) {
      return findById('/rental', id);
    },
    rentalAdd: function(data) {
      return add('/rental', data);
    },
    rentalEdit: function(data) {
      return edit('/rental', data);
    },
    rentalDelete: function(id) {
      return remove('/rental', id);
    },
    rentalExpire: function(days) {
      return axios.get('/rental/expire?days=' + (days || 30));
    },
    rentalRenew: function(id) {
      return axios.put('/rental/renew/' + id);
    },
    rentalTerminate: function(id) {
      return axios.put('/rental/terminate/' + id);
    },

    // ==================== 设施管理 ====================
    facilityFindPage: function(params) {
      return findPage('/facility', params);
    },
    facilityFindById: function(id) {
      return findById('/facility', id);
    },
    facilityAdd: function(data) {
      return add('/facility', data);
    },
    facilityEdit: function(data) {
      return edit('/facility', data);
    },
    facilityDelete: function(id) {
      return remove('/facility', id);
    },

    // ==================== 员工管理 ====================
    employeeFindPage: function(params) {
      return findPage('/employee', params);
    },
    employeeFindById: function(id) {
      return findById('/employee', id);
    },
    employeeAdd: function(data) {
      return add('/employee', data);
    },
    employeeEdit: function(data) {
      return edit('/employee', data);
    },
    employeeDelete: function(id) {
      return remove('/employee', id);
    },

    // ==================== 访客管理 ====================
    visitorFindPage: function(params) {
      return findPage('/visitor', params);
    },
    visitorFindById: function(id) {
      return findById('/visitor', id);
    },
    visitorAdd: function(data) {
      return add('/visitor', data);
    },
    visitorEdit: function(data) {
      return edit('/visitor', data);
    },
    visitorDelete: function(id) {
      return remove('/visitor', id);
    },
    visitorVerify: function(id) {
      return axios.put('/visitor/verify/' + id);
    },
    visitorCancel: function(id) {
      return axios.delete('/visitor/cancel/' + id);
    },

    // ==================== 报修服务 ====================
    repairFindPage: function(params) {
      return findPage('/repair', params);
    },
    repairFindById: function(id) {
      return findById('/repair', id);
    },
    repairAdd: function(data) {
      return add('/repair', data);
    },
    repairEdit: function(data) {
      return edit('/repair', data);
    },
    repairDelete: function(id) {
      return remove('/repair', id);
    },
    repairDispatch: function(id, workerId, workerName) {
      return axios.put('/repair/dispatch/' + id + '?workerId=' + workerId + '&workerName=' + encodeURIComponent(workerName));
    },
    repairEvaluate: function(id, evaluation) {
      return axios.put('/repair/evaluate/' + id + '?evaluation=' + evaluation);
    },

    // ==================== 收费管理 ====================
    paymentFindPage: function(params) {
      return findPage('/payment', params);
    },
    paymentFindById: function(id) {
      return findById('/payment', id);
    },
    paymentAdd: function(data) {
      return add('/payment', data);
    },
    paymentEdit: function(data) {
      return edit('/payment', data);
    },
    paymentDelete: function(id) {
      return remove('/payment', id);
    },

    // ==================== 公告管理 ====================
    noticeFindPage: function(params) {
      return findPage('/notice', params);
    },
    noticeFindById: function(id) {
      return findById('/notice', id);
    },
    noticeAdd: function(data) {
      return add('/notice', data);
    },
    noticeEdit: function(data) {
      return edit('/notice', data);
    },
    noticeDelete: function(id) {
      return remove('/notice', id);
    },

    // ==================== 门禁管理 ====================
    accessFindPage: function(params) {
      return findPage('/access', params);
    },
    accessFindById: function(id) {
      return findById('/access', id);
    },
    accessAdd: function(data) {
      return add('/access', data);
    },
    accessEdit: function(data) {
      return edit('/access', data);
    },
    accessDelete: function(id) {
      return remove('/access', id);
    },

    // ==================== 仪表盘 ====================
    dashboardOverview: function() {
      return axios.get('/dashboard/overview');
    },
    dashboardPayment: function() {
      return axios.get('/dashboard/payment');
    },
    dashboardRepair: function() {
      return axios.get('/dashboard/repair');
    },
    dashboardAi: function() {
      return axios.get('/dashboard/ai');
    }
  };
})();
