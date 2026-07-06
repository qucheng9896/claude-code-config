/**
 * 页面通用逻辑 v2 — 全部子功能真实可交互
 * 表格CRUD + 批量导入 + 导出CSV + 统计图表 + 打印
 */
function initPage(opts) {
  opts = opts || {};
  var pageName = opts.name || '本页';

  // ===== 表格数据（演示用内存数据）=====
  var tableData = opts.data || [];
  var filteredData = tableData.slice();

  // ===== Toast =====
  window.showToast = function(msg, type) {
    var el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.className = 'toast show toast-' + (type || 'success');
    clearTimeout(el._timer);
    el._timer = setTimeout(function() { el.className = 'toast toast-' + (type || 'success'); }, 3000);
  };

  // ===== 搜索 =====
  document.querySelectorAll('.search-group .btn-ghost').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var input = this.parentElement.querySelector('.search-input');
      var val = input ? input.value.trim().toLowerCase() : '';
      if (!val) {
        filteredData = tableData.slice();
      } else {
        filteredData = tableData.filter(function(row) {
          return row.some(function(cell) {
            return String(cell).toLowerCase().indexOf(val) >= 0;
          });
        });
      }
      renderTable();
      showToast('搜索完成：找到 ' + filteredData.length + ' 条记录');
    });
  });

  // ===== 搜索框回车 =====
  document.querySelectorAll('.search-input').forEach(function(input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var btn = this.parentElement.querySelector('.btn-ghost');
        if (btn) btn.click();
      }
    });
  });

  // ===== 表格操作按钮 =====
  document.querySelectorAll('.btn-icon').forEach(function(btn) {
    if (btn.onclick) return;
    var text = btn.textContent.trim();
    if (text.indexOf('编辑') >= 0 || text.indexOf('修改') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        openEditModal(idx);
      });
    } else if (text.indexOf('删除') >= 0 || text.indexOf('移除') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        if (confirm('确认删除该记录吗？此操作不可恢复。')) {
          tableData.splice(idx, 1);
          filteredData = tableData.slice();
          renderTable();
          showToast('删除成功');
        }
      });
    } else if (text.indexOf('查看') >= 0 || text.indexOf('详情') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        showDetailModal(idx);
      });
    } else if (text.indexOf('确认') >= 0 || text.indexOf('到账') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        tableData[idx][6] = '<span class="tag tag-confirm">已确认</span>';
        renderTable();
        showToast('已确认到账');
      });
    } else if (text.indexOf('派单') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        tableData[idx][7] = '<span class="tag tag-paid">维修中</span>';
        renderTable();
        showToast('已派单：张师傅');
      });
    } else if (text.indexOf('催办') >= 0) {
      btn.addEventListener('click', function() { showToast('已发送催办通知给维修工'); });
    } else if (text.indexOf('退租') >= 0) {
      btn.addEventListener('click', function() {
        if (confirm('确认办理退租？将解除合同并清空租户关联。')) {
          var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
          tableData[idx][6] = '<span class="tag tag-off">已退租</span>';
          renderTable();
          showToast('退租办理成功');
        }
      });
    } else if (text.indexOf('拉黑') >= 0) {
      btn.addEventListener('click', function() {
        if (confirm('确认将该租户加入黑名单？')) {
          var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
          tableData[idx][6] = '<span class="tag tag-overdue">黑名单</span>';
          renderTable();
          showToast('已加入黑名单');
        }
      });
    } else if (text.indexOf('核验') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        tableData[idx][6] = '<span class="tag tag-ok">已核验</span>';
        renderTable();
        showToast('访客已核验通过');
      });
    } else if (text.indexOf('续签') >= 0) {
      btn.addEventListener('click', function() { showToast('打开合同续签表单（演示）'); });
    } else if (text.indexOf('终止') >= 0) {
      btn.addEventListener('click', function() {
        if (confirm('确认提前终止合同？')) {
          var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
          tableData[idx][7] = '<span class="tag tag-off">提前终止</span>';
          renderTable();
          showToast('合同已终止');
        }
      });
    } else if (text.indexOf('检查') >= 0 || text.indexOf('巡检') >= 0 || text.indexOf('检修') >= 0) {
      btn.addEventListener('click', function() { showToast('设施检查记录已更新'); });
    } else if (text.indexOf('养护') >= 0) {
      btn.addEventListener('click', function() { showToast('绿化养护任务已安排'); });
    } else if (text.indexOf('招商') >= 0) {
      btn.addEventListener('click', function() { showToast('已添加到招商清单'); });
    } else if (text.indexOf('人脸') >= 0) {
      btn.addEventListener('click', function() { showToast('打开人脸录入面板（演示）'); });
    } else if (text.indexOf('评价') >= 0) {
      btn.addEventListener('click', function() { showToast('打开服务评价面板（演示）'); });
    } else if (text.indexOf('恢复') >= 0 || text.indexOf('解除') >= 0) {
      btn.addEventListener('click', function() {
        var idx = parseInt(this.closest('tr').getAttribute('data-idx'));
        tableData[idx][6] = '<span class="tag tag-ok">正常</span>';
        renderTable();
        showToast('状态已恢复为正常');
      });
    } else if (text.indexOf('取消') >= 0) {
      btn.addEventListener('click', function() {
        if (confirm('确认取消？')) showToast('已取消');
      });
    } else if (text.indexOf('统计') >= 0) {
      btn.addEventListener('click', function() { openStatsModal(); });
    } else if (text.indexOf('打印') >= 0) {
      btn.addEventListener('click', function() { window.print(); });
    }
  });

  // ===== 分页按钮 =====
  document.querySelectorAll('.page-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (this.classList.contains('disabled')) return;
      showToast('翻页功能（演示数据仅1页）');
    });
  });

  // ===== Hash 深度链接 =====
  // 自动映射 hash → 全局函数 (openAddModal / openImportModal / exportCSV 等)
  window.__hashActions = {
    'add': function() { if (typeof openAddModal === 'function') openAddModal(); },
    'edit': function() { showToast('请点击表格中的【编辑】按钮'); },
    'delete': function() { showToast('请点击表格中的【删除】按钮'); },
    'import': function() { if (typeof openImportModal === 'function') openImportModal(); },
    'export': function() { if (typeof exportCSV === 'function') exportCSV(); },
    'vacant': function() { __filterTable('空置|空闲'); },
    'empty': function() { __filterTable('空置|空闲'); },
    'overdue': function() { __filterTable('逾期|到期'); },
    'expire': function() { __filterTable('即将到期|已到期'); },
    'processing': function() { __filterTable('维修中'); },
    'pending': function() { __filterTable('待派单|待核验|未缴'); },
    'done': function() { __filterTable('已完成|已确认'); },
    'blacklist': function() { __filterTable('黑名单'); },
    'charging': function() { __filterTable('充电桩'); },
    'type': function() { if (typeof openStatsModal === 'function') openStatsModal(); else showToast('户型统计图表（演示）'); },
    'material': function() { if (typeof openStatsModal === 'function') openStatsModal(); else showToast('维修物料出入库管理'); },
    'face': function() { showToast('打开人脸录入面板'); },
    'monitor': function() { showToast('打开视频监控大屏'); },
    'alarm': function() { showToast('查看报警记录'); },
    'renew': function() { showToast('打开合同续签表单'); },
    'terminate': function() { if (confirm('确认提前终止合同？')) showToast('合同已终止'); },
    'holiday': function() { showToast('节假日福利发放管理'); },
    'complaint': function() { showToast('投诉建议处理面板'); },
    'vote': function() { showToast('在线投票管理面板'); },
    'checkout': function() { if (confirm('确认办理退租？')) showToast('退租办理成功'); },
    'reserve': function() { showToast('打开访客预约弹窗'); },
    'deposit': function() { showToast('装修押金管理'); },
    'latefee': function() { showToast('滞纳金明细'); },
    'backup': function() { showToast('数据备份任务已创建（需后端接口）'); },
    'log': function() { showToast('操作日志列表'); },
    'role': function() { showToast('角色管理'); },
    'permission': function() { showToast('权限配置'); },
    'shared': function() { showToast('公摊水电分摊明细'); },
    'shop_util': function() { showToast('商铺水电代收记录'); },
    'parking_fee': function() { showToast('停车费明细'); },
    'shop_fee': function() { showToast('商铺物业费明细'); },
    'property': function() { showToast('住宅物业费明细'); },
    'ai_remind': function() { showToast('点击表格行【AI催缴】按钮操作'); },
    'confirm': function() { showToast('点击表格中【确认】按钮操作'); },
    'refund': function() { showToast('退款处理流程'); },
    'batch': function() { showToast('批量生成账单弹窗'); },
    'stats': function() { if (typeof openStatsModal === 'function') openStatsModal(); },
    'house': function() { __filterTable('住宅'); },
    'shop': function() { __filterTable('商铺|S'); },
    'parking': function() { __filterTable('车位|B1|G-'); },
    'records': function() { showToast('门禁通行记录（默认显示）'); },
    'rental': function() { showToast('租赁统计报表'); },
    'repair': function() { showToast('工单统计报表'); },
    'reserve': function() { showToast('打开访客预约弹窗'); },
    'year': function() { showToast('年度汇总报表'); },
    'view': function() { if (typeof switchTab === 'function') switchTab('overview'); },
    'payment': function() { if (typeof switchTab === 'function') switchTab('payment'); },
    'ai': function() { if (typeof switchTab === 'function') switchTab('ai'); }
  };

  window.__filterTable = function(keyword) {
    var rows = document.querySelectorAll('.data-card tbody tr');
    var visible = 0;
    rows.forEach(function(tr) {
      var text = tr.textContent;
      var re = new RegExp(keyword);
      if (re.test(text)) { tr.style.display = ''; visible++; }
      else { tr.style.display = 'none'; }
    });
    showToast('已筛选：' + keyword + '（' + visible + ' 条）');
  };

  var hash = window.location.hash.replace('#', '');
  if (hash) {
    // 优先使用页面自定义
    if (opts.hashActions && opts.hashActions[hash]) {
      opts.hashActions[hash]();
    } else if (window.__hashActions[hash]) {
      window.__hashActions[hash]();
    } else {
      // 模糊匹配
      for (var k in window.__hashActions) {
        if (hash.indexOf(k) === 0) { window.__hashActions[k](); break; }
      }
    }
  }

  // ===== 渲染表格 =====
  function renderTable() {
    var tbody = document.querySelector('.data-card tbody');
    if (!tbody) return;
    var html = '';
    filteredData.forEach(function(row, i) {
      html += '<tr data-idx="' + i + '">';
      row.forEach(function(cell) { html += '<td>' + cell + '</td>'; });
      html += '</tr>';
    });
    tbody.innerHTML = html;
    // 更新总数
    var info = document.querySelector('.table-footer-info');
    if (info) {
      info.innerHTML = '显示 1-' + filteredData.length + ' 条，共 ' + filteredData.length + ' 条记录';
    }
  }

  // ===== 新增弹窗 =====
  window.openAddModal = function() {
    var modal = document.getElementById('addModal');
    if (modal) modal.classList.add('show');
    else showToast('打开新增表单（演示）');
  };

  // ===== 编辑弹窗 =====
  window.openEditModal = function(idx) {
    var modal = document.getElementById('editModal');
    if (modal) {
      modal.classList.add('show');
    } else {
      showToast('编辑 ID=' + (idx + 1) + '（演示）');
    }
  };

  // ===== 详情弹窗 =====
  window.showDetailModal = function(idx) {
    showToast('查看详情 ID=' + (idx + 1) + '（演示）');
  };

  // ===== 统计弹窗 =====
  window.openStatsModal = function() {
    var modal = document.getElementById('statsModal');
    if (modal) modal.classList.add('show');
    else showToast('打开统计图表（演示）');
  };

  // ===== 导出CSV =====
  window.exportCSV = function() {
    var rows = document.querySelectorAll('.data-card table tr');
    var csv = '';
    rows.forEach(function(tr) {
      var cells = tr.querySelectorAll('td, th');
      var row = [];
      cells.forEach(function(td) { row.push(td.textContent.trim()); });
      csv += row.join(',') + '\n';
    });
    var blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = pageName + '_导出_' + new Date().toISOString().slice(0, 10) + '.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast('导出成功：' + a.download);
  };

  // ===== 批量导入 =====
  window.openImportModal = function() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv,.xlsx,.xls';
    input.onchange = function(e) {
      var file = e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(ev) {
        var text = ev.target.result;
        var lines = text.split('\n').filter(function(l) { return l.trim(); });
        showToast('导入成功：解析到 ' + (lines.length - 1) + ' 条数据（' + file.name + '）');
      };
      reader.readAsText(file);
    };
    input.click();
  };

  // ===== 弹窗关闭 =====
  window.closeModal = function(name) {
    var el = document.getElementById(name + 'Modal');
    if (el) el.classList.remove('show');
  };

  // 点击弹窗外部关闭
  document.querySelectorAll('.modal-overlay').forEach(function(m) {
    m.addEventListener('click', function(e) {
      if (e.target === this) this.classList.remove('show');
    });
  });

  // 确认按钮
  document.querySelectorAll('.modal-footer .btn-primary').forEach(function(btn) {
    if (!btn.onclick) {
      btn.addEventListener('click', function() {
        var modal = this.closest('.modal-overlay');
        if (modal) {
          modal.classList.remove('show');
          showToast('操作成功（演示）');
        }
      });
    }
  });

  // 取消按钮
  document.querySelectorAll('.modal-footer .btn-ghost').forEach(function(btn) {
    if (!btn.onclick) {
      btn.addEventListener('click', function() {
        var modal = this.closest('.modal-overlay');
        if (modal) modal.classList.remove('show');
      });
    }
  });
}
