/**
 * Axios 全局配置 — 前后端接口统一规范
 * 部署时修改 BASE_URL 为后端服务地址
 */
axios.defaults.baseURL = 'http://localhost:8080';
axios.defaults.timeout = 15000;

// 请求拦截器 — 自动注入 Token
axios.interceptors.request.use(function(config) {
    var token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
}, function(error) {
    return Promise.reject(error);
});

// 响应拦截器 — 统一错误处理
axios.interceptors.response.use(function(response) {
    var data = response.data;
    // 后端返回格式：{ flag: true/false, message: "...", data: ... }
    if (data && data.flag === false) {
        if (data.message && (data.message.indexOf('登录') >= 0 || data.message.indexOf('Token') >= 0 || data.message.indexOf('token') >= 0)) {
            localStorage.clear();
            window.location.href = 'login.html';
            return Promise.reject(new Error(data.message));
        }
        alert(data.message || '操作失败');
        return Promise.reject(new Error(data.message));
    }
    return data;
}, function(error) {
    if (error.response && error.response.status === 401) {
        localStorage.clear();
        window.location.href = 'login.html';
        return;
    }
    alert('网络错误，请检查服务是否启动');
    return Promise.reject(error);
});
