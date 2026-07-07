function initSidebar(activeKey) {
  // 从 sessionStorage 读取上次展开的组，新页面 HTML 直接带 open 类 → 不闪烁
  var lastGroup = '';
  try { lastGroup = sessionStorage.getItem('sidebar_group') || ''; } catch(e) {}
  // 如果当前 activeKey 属于某个组，也记录下来
  var currentGroup = activeKey.split(':')[0];

  // 构建 menu 时用 lastGroup / currentGroup 判断 open
  var isOpen = function(key) {
    return key === currentGroup || key === lastGroup;
  };

  var menu = [
    {
      key: 'dashboard', label: '数据概览', href: 'dashboard.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
      children: [
        { key: 'dashboard:view', label: '综合统计', href: 'dashboard.html' },
        { key: 'dashboard:payment', label: '收缴分析', href: 'dashboard.html#payment' },
        { key: 'dashboard:repair', label: '工单分析', href: 'dashboard.html#repair' },
        { key: 'dashboard:ai', label: 'AI催缴统计', href: 'dashboard.html#ai' }
      ]
    },
    {
      key: 'property', label: '房产管理', href: 'building.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
      children: [
        { key: 'building:list', label: '楼栋管理', href: 'building.html' },
        { key: 'house:list', label: '住宅管理', href: 'house.html' },
        { key: 'shop:list', label: '商铺管理', href: 'shop.html' },
        { key: 'parking:list', label: '车位管理', href: 'parking.html' },
        { key: 'facility:list', label: '公共设施', href: 'facility.html' }
      ]
    },
    {
      key: 'people', label: '人员管理', href: 'owner.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
      children: [
        { key: 'owner:list', label: '业主管理', href: 'owner.html' },
        { key: 'tenant:list', label: '租户管理', href: 'tenant.html' },
        { key: 'employee:list', label: '物业员工', href: 'employee.html' },
        { key: 'visitor:list', label: '访客管理', href: 'visitor.html' }
      ]
    },
    {
      key: 'rental', label: '租赁管理', href: 'rental.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      children: [
        { key: 'rental:house', label: '住宅合同', href: 'rental.html#house' },
        { key: 'rental:shop', label: '商铺合同', href: 'rental.html#shop' },
        { key: 'rental:parking', label: '车位租赁', href: 'rental.html#parking' },
        { key: 'rental:expire', label: '到期预警', href: 'rental.html#expire' }
      ]
    },
    {
      key: 'payment', label: '收费管理', href: 'payment.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
      children: [
        { key: 'payment:property', label: '住宅物业费', href: 'payment.html#property' },
        { key: 'payment:shop_fee', label: '商铺物业费', href: 'payment.html#shop_fee' },
        { key: 'payment:shared', label: '公摊水电分摊', href: 'payment.html#shared' },
        { key: 'payment:shop_util', label: '商铺水电代收', href: 'payment.html#shop_util' },
        { key: 'payment:parking_fee', label: '停车费', href: 'payment.html#parking_fee' },
        { key: 'payment:charging', label: '充电桩服务费', href: 'payment.html#charging' },
        { key: 'payment:deposit', label: '装修押金', href: 'payment.html#deposit' },
        { key: 'payment:latefee', label: '滞纳金管理', href: 'payment.html#latefee' },
        { key: 'payment:ai_remind', label: 'AI智能催缴', href: 'payment.html#ai' }
      ]
    },
    {
      key: 'security', label: '安防门禁', href: 'access.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
      children: [
        { key: 'access:records', label: '门禁记录', href: 'access.html#records' },
        { key: 'access:face', label: '人脸管理', href: 'access.html#face' },
        { key: 'visitor:reserve', label: '访客预约', href: 'visitor.html#reserve' },
        { key: 'monitor:list', label: '监控中心', href: 'access.html#monitor' },
        { key: 'alarm:list', label: '报警中心', href: 'access.html#alarm' }
      ]
    },
    {
      key: 'repair', label: '报修服务', href: 'repair.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
      children: [
        { key: 'repair:list', label: '工单列表', href: 'repair.html' },
        { key: 'repair:pending', label: '待派单', href: 'repair.html#pending' },
        { key: 'repair:processing', label: '维修中', href: 'repair.html#processing' },
        { key: 'repair:done', label: '已完成', href: 'repair.html#done' },
        { key: 'repair:material', label: '物料管理', href: 'repair.html#material' }
      ]
    },
    {
      key: 'community', label: '社区服务', href: 'notice.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>',
      children: [
        { key: 'notice:list', label: '公告发布', href: 'notice.html' },
        { key: 'holiday:list', label: '节假日福利', href: 'notice.html#holiday' },
        { key: 'complaint:list', label: '投诉建议', href: 'notice.html#complaint' },
        { key: 'vote:list', label: '在线投票', href: 'notice.html#vote' }
      ]
    },
    {
      key: 'report', label: '经营报表', href: 'report.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
      children: [
        { key: 'report:payment', label: '收缴明细表', href: 'report.html#payment' },
        { key: 'report:rental', label: '租赁报表', href: 'report.html#rental' },
        { key: 'report:repair', label: '工单报表', href: 'report.html#repair' },
        { key: 'report:year', label: '年度汇总', href: 'report.html#year' }
      ]
    },
    {
      key: 'system', label: '系统管理', href: 'user.html',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
      children: [
        { key: 'user:list', label: '用户管理', href: 'user.html' },
        { key: 'role:list', label: '角色管理', href: 'user.html#role' },
        { key: 'perm:list', label: '权限管理', href: 'user.html#permission' },
        { key: 'log:list', label: '操作日志', href: 'user.html#log' },
        { key: 'backup', label: '数据备份', href: 'user.html#backup' }
      ]
    }
  ];

  var html = '<aside class="sidebar">';
  html += '<div class="sidebar-logo"><div class="sidebar-logo-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div><span>智慧物业</span></div>';
  html += '<nav class="sidebar-nav">';

  menu.forEach(function(item) {
    var hasChildren = item.children && item.children.length > 0;
    var open = isOpen(item.key);
    var subActive = activeKey && activeKey.indexOf(item.key + ':') === 0;

    if (hasChildren) {
      html += '<div class="sidebar-group ' + (open ? 'open' : '') + (subActive ? ' active' : '') + '" data-key="' + item.key + '">';
      html += '<div class="sidebar-group-title" onclick="toggleGroup(this)">';
      html += item.icon + '<span class="sidebar-group-label">' + item.label + '</span>';
      html += '<svg class="sidebar-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>';
      html += '</div><div class="sidebar-submenu">';
      item.children.forEach(function(sub) {
        var sActive = activeKey === sub.key ? 'active' : '';
        // 同页面锚点：不刷新页面
        var hrefParts = sub.href.split('#');
        var samePage = (hrefParts[0] === window.location.pathname.split('/').pop());
        if (samePage && hrefParts[1]) {
          html += '<a href="javascript:void(0)" class="' + sActive + '" onclick="handleSubClick(event,\'' + hrefParts[0] + '\',\'' + hrefParts[1] + '\',\'' + item.key + '\')">' + sub.label + '</a>';
        } else {
          html += '<a href="' + sub.href + '" class="' + sActive + '" onclick="saveGroup(\'' + item.key + '\')">' + sub.label + '</a>';
        }
      });
      html += '</div></div>';
    } else {
      html += '<a href="' + item.href + '" class="' + (activeKey === item.key ? 'active' : '') + '">' + item.icon + item.label + '</a>';
    }
  });

  html += '</nav>';
  html += '<div class="sidebar-footer"><a href="login.html"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>退出登录</a></div>';
  html += '</aside>';

  document.getElementById('sidebar-placeholder').innerHTML = html;
}

function saveGroup(key) {
  try { sessionStorage.setItem('sidebar_group', key); } catch(e) {}
}

function toggleGroup(el) {
  var group = el.parentElement;
  var isOpen = group.classList.contains('open');
  // 手风琴：收起其他组
  document.querySelectorAll('.sidebar-group.open').forEach(function(g) { g.classList.remove('open'); });
  if (!isOpen) {
    group.classList.add('open');
    saveGroup(group.getAttribute('data-key'));
  } else {
    saveGroup('');
  }
}

/**
 * 子菜单点击 — 同页面不刷新，跨页面保存组状态
 */
function handleSubClick(e, page, hash, groupKey) {
  e.preventDefault();
  saveGroup(groupKey);
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  if (currentPage === page || currentPage === 'index.html' || currentPage === '') {
    history.pushState(null, '', '#' + hash);
    document.querySelectorAll('.sidebar-submenu a').forEach(function(a) { a.classList.remove('active'); });
    e.currentTarget.classList.add('active');
    if (window.__hashActions && window.__hashActions[hash]) {
      window.__hashActions[hash]();
    } else if (typeof switchTab === 'function') {
      var tabKey = hash.replace('dashboard:', '');
      switchTab(tabKey);
    } else {
      showToast('功能开发中：' + hash);
    }
  } else {
    window.location.href = page + '#' + hash;
  }
}

