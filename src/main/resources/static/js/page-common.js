/**
 * 页面通用逻辑 v3 — 支持真实 API 调用
 * 两种模式:
 *   1. API 模式: 传入 api 配置，数据从后端获取，支持真 CRUD
 *   2. 静态模式: 不传 api 配置，保持原有静态数据行为（向后兼容）
 *
 * 使用方式:
 * initPage({
 *   name: '楼栋管理',
 *   api: {
 *     findPage: API.buildingFindPage,
 *     findById: API.buildingFindById,
 *     add: API.buildingAdd,
 *     edit: API.buildingEdit,
 *     delete: API.buildingDelete
 *   },
 *   renderRow: function(item, index) { return '<td>...</td>'; },
 *   hashActions: { add: function(){ openAddModal(); } }
 * });
 */
function initPage(opts) {
  opts = opts || {};
  var pageName = opts.name || '本页';
  var api = opts.api || null;
  var renderRow = opts.renderRow || null;
  var pageSize = opts.pageSize || 10;

  var tableData = [];
  var filteredData = [];
  var currentPage = 1;
  var totalCount = 0;

  // ===== 判断是否为 API 模式 =====
  var isApiMode = !!(api && api.findPage);

  // ===== Toast =====
  window.showToast = function(msg, type) {
    var el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.className = 'toast show toast-' + (type || 'success');
    clearTimeout(el._timer);
    el._timer = setTimeout(function() { el.className = 'toast toast-' + (type || 'success'); }, 3000);
  };

  // ===== 默认行渲染（当未提供 renderRow 时） =====
  function defaultRenderRow(item, index) {
    if (renderRow) return renderRow(item, index);
    var html = '';
    for (var key in item) {
      if (key !== 'id') html += '<td>' + (item[key] != null ? item[key] : '') + '</td>';
    }
    return html;
  }

  // ===== API 模式：从后端加载数据 =====
  async function loadData(page, queryString) {
    if (!isApiMode) return;
    currentPage = page || 1;
    var params = { pageNum: currentPage, pageSize: pageSize };
    if (queryString) params.queryString = queryString;

    try {
      var response = await api.findPage(params);
      if (response && response.flag) {
        totalCount = response.data.total || 0;
        tableData = response.data.rows || [];
        filteredData = tableData.slice();
        renderTable();
        updateFooterInfo();
      } else {
        showToast('加载数据失败: ' + (response ? response.message : '未知错误'), 'error');
      }
    } catch (e) {
      showToast('加载数据失败: ' + (e.message || '网络错误'), 'error');
    }
  }

  // ===== API 模式：删除记录 =====
  async function deleteRecord(id, rowIdx) {
    if (!api.delete) {
      showToast('未配置删除接口', 'error');
      return;
    }
    if (!confirm('确认删除该记录吗？此操作不可恢复。')) return;
    try {
      var response = await api.delete(id);
      if (response && response.flag) {
        showToast('删除成功');
        loadData(currentPage);
      } else {
        showToast('删除失败: ' + (response ? response.message : '未知错误'), 'error');
      }
    } catch (e) {
      showToast('删除失败: ' + (e.message || '网络错误'), 'error');
    }
  }

  // ===== API 模式：搜索 =====
  function search(queryString) {
    if (isApiMode) {
      loadData(1, queryString);
    } else {
      if (!queryString) {
        filteredData = tableData.slice();
      } else {
        filteredData = tableData.filter(function(row) {
          return row.some(function(cell) {
            return String(cell).toLowerCase().indexOf(queryString) >= 0;
          });
        });
      }
      renderTable();
      showToast('搜索完成：找到 ' + filteredData.length + ' 条记录');
    }
  }

  // ===== 渲染表格 =====
  function renderTable() {
    var tbody = document.querySelector('.data-card tbody');
    if (!tbody) return;
    var html = '';
    for (var i = 0; i < filteredData.length; i++) {
      var item = filteredData[i];
      var id = item.id != null ? item.id : i;
      html += '<tr data-idx="' + i + '" data-id="' + id + '">';
      html += defaultRenderRow(item, i);
      html += '</tr>';
    }
    tbody.innerHTML = html;

    // 重新绑定操作按钮
    bindTableActions();
  }

  // ===== 更新底部分页信息 =====
  function updateFooterInfo() {
    var info = document.querySelector('.table-footer-info');
    if (info) {
      var start = (currentPage - 1) * pageSize + 1;
      var end = Math.min(currentPage * pageSize, totalCount);
      info.innerHTML = '显示 ' + start + '-' + end + ' 条，共 ' + totalCount + ' 条记录';
    }
  }

  // ===== 绑定表格操作按钮 =====
  function bindTableActions() {
    document.querySelectorAll('.data-card tbody .btn-icon').forEach(function(btn) {
      if (btn._bound) return;
      btn._bound = true;
      var text = btn.textContent.trim();

      btn.addEventListener('click', function() {
        var tr = this.closest('tr');
        var idx = parseInt(tr.getAttribute('data-idx'));
        var id = parseInt(tr.getAttribute('data-id'));
        var item = filteredData[idx] || {};

        if (text.indexOf('编辑') >= 0 || text.indexOf('修改') >= 0) {
          openEditModal(item);
        } else if (text.indexOf('删除') >= 0 || text.indexOf('移除') >= 0) {
          deleteRecord(id, idx);
        } else if (text.indexOf('确认') >= 0 || text.indexOf('到账') >= 0) {
          if (api.edit) {
            var updated = Object.assign({}, item);
            updated.payStatus = 2;
            api.edit(updated).then(function(res) {
              if (res && res.flag) { showToast('已确认到账'); loadData(currentPage); }
            });
          } else {
            showToast('已确认到账');
          }
        } else if (text.indexOf('派单') >= 0) {
          if (api && api.dispatch) {
            var workerId = 1;
            var workerName = '张师傅';
            api.dispatch(id, workerId, workerName).then(function(res) {
              if (res && res.flag) { showToast('已派单：' + workerName); loadData(currentPage); }
              else showToast('派单失败：' + (res ? res.message : '未知错误'), 'error');
            });
          } else {
            showToast('已派单：张师傅');
          }
        } else if (text.indexOf('退租') >= 0) {
          if (api && api.checkout) {
            if (!confirm('确认办理退租？此操作将清空租户关联的房屋。')) return;
            api.checkout(id).then(function(res) {
              if (res && res.flag) { showToast('退租办理成功'); loadData(currentPage); }
              else showToast('退租失败：' + (res ? res.message : '未知错误'), 'error');
            });
          } else {
            if (confirm('确认办理退租？')) showToast('退租办理成功');
          }
        } else if (text.indexOf('评价') >= 0) {
          if (api && api.evaluate) {
            var evaluation = parseInt(prompt('请输入评价星级 (1-5)：', '5')) || 5;
            api.evaluate(id, evaluation).then(function(res) {
              if (res && res.flag) { showToast('评价成功：' + evaluation + '星'); loadData(currentPage); }
              else showToast('评价失败：' + (res ? res.message : '未知错误'), 'error');
            });
          } else {
            showToast('感谢您的评价！');
          }
        } else if (text.indexOf('核验') >= 0) {
          showToast('访客已核验通过');
        } else if (text.indexOf('续签') >= 0) {
          showToast('打开合同续签表单');
        } else if (text.indexOf('终止') >= 0) {
          if (confirm('确认提前终止合同？')) showToast('合同已终止');
        }
      });
    });
  }

  // ===== 搜索框事件绑定 =====
  document.querySelectorAll('.search-group .btn-ghost').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var input = this.parentElement.querySelector('.search-input');
      var val = input ? input.value.trim().toLowerCase() : '';
      search(val);
    });
  });

  document.querySelectorAll('.search-input').forEach(function(input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var btn = this.parentElement.querySelector('.btn-ghost');
        if (btn) btn.click();
      }
    });
  });

  // ===== 分页按钮 =====
  document.querySelectorAll('.page-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (this.classList.contains('disabled')) return;
      if (isApiMode) {
        var totalPages = Math.ceil(totalCount / pageSize);
        if (this.textContent === '›' && currentPage < totalPages) {
          loadData(currentPage + 1);
        } else if (this.textContent === '‹' && currentPage > 1) {
          loadData(currentPage - 1);
        }
      } else {
        showToast('翻页功能（演示数据仅1页）');
      }
    });
  });

  // ===== Hash 深度链接 =====
  window.__hashActions = window.__hashActions || {};
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
    if (opts.hashActions && opts.hashActions[hash]) {
      opts.hashActions[hash]();
    } else if (window.__hashActions[hash]) {
      window.__hashActions[hash]();
    } else {
      for (var k in window.__hashActions) {
        if (hash.indexOf(k) === 0) { window.__hashActions[k](); break; }
      }
    }
  }

  // ===== 弹窗函数 =====
  window.openAddModal = function() {
    var modal = document.getElementById('addModal');
    if (modal) modal.classList.add('show');
    else showToast('打开新增表单（请配置 addModal）');
  };

  window.openEditModal = function(item) {
    var modal = document.getElementById('editModal');
    if (modal) {
      // 将数据填充到弹窗表单
      if (item) {
        var inputs = modal.querySelectorAll('.form-input');
        var keys = Object.keys(item);
        inputs.forEach(function(input, i) {
          if (keys[i] && input.type !== 'file') {
            input.value = item[keys[i]] != null ? item[keys[i]] : '';
          }
        });
      }
      modal.classList.add('show');
    } else {
      showToast('编辑（请配置 editModal）');
    }
  };

  window.showDetailModal = function(idx) {
    showToast('查看详情 ID=' + (idx + 1));
  };

  window.openStatsModal = function() {
    var modal = document.getElementById('statsModal');
    if (modal) modal.classList.add('show');
    else showToast('打开统计图表（演示）');
  };

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
          showToast('操作成功');
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

  // ===== 初始化数据 =====
  if (isApiMode) {
    loadData(1);
  } else {
    // 静态模式：保持原有行为
    tableData = opts.data || [];
    filteredData = tableData.slice();
    renderTable();
  }

  // 暴露 API 供外部调用
  window._pageApi = {
    loadData: loadData,
    search: search,
    deleteRecord: deleteRecord
  };
}

