/* ============================================================================
 * 通用四段式详情弹窗 · 数据渲染（财务协同下游单据：付款/回款/开票/水单核销）
 * ----------------------------------------------------------------------------
 * 用法：
 *   <script src="../_data/demo-data.js"></script>
 *   <script src="../_data/detail-generic.js"></script>
 *   列表页接线（页面脚本一行）：wireDetailModal('payments')
 *     —— 自动找所有 onclick 指向 detailModal 的「详情」按钮，剥离 onclick，
 *        用行文本匹配 DEMO_DATA[entity] 的键，改绑 addEventListener。
 *   弹窗模板预览（弹窗/ 目录）：openGenericDetail('payments', 'PAY-xxx', '../../')
 *
 * 记录结构（demo-data.js 内）：
 *   title 弹窗标题前缀 / titleNo 标题单号（缺省用键）
 *   info: [{label, text, full?, url?, tag?}]   tag 值走 STATUS_CLS 统一状态色
 *   feeCols: [列名...] + fees: [{cells:[...], links:{列号:url}}]
 *   chain: [{role, name, url?, self?}] / timeline: [{t, text, who?, off?}]
 * 金额/数量存展示字符串，渲染器不做语义格式化。
 * ========================================================================== */
(function () {
  var STATUS_CLS = {
    '待确认': 'tag-orange', '已确认': 'tag-green',
    '已上传': 'tag-green', '补传回单': 'tag-orange',
    '待核销': 'tag-orange', '部分核销': 'tag-blue', '已核销': 'tag-green',
    '已登记': 'tag-green', '已红冲': 'tag-red', '停用': 'tag-gray',
    '待付款': 'tag-red', '未付款': 'tag-red', '已付款': 'tag-green',
    '未开票': 'tag-red', '部分收款': 'tag-orange', '已结清': 'tag-green', '已收': 'tag-green',
    '已退租': 'tag-gray', '在租': 'tag-green', '待审核': 'tag-orange', '已审核': 'tag-green',
    '已关闭': 'tag-gray', '已出库': 'tag-green', '拣货中': 'tag-orange', '待出库': 'tag-orange',
    '履行中': 'tag-blue', '部分归还': 'tag-orange', '已归还': 'tag-green', '已终止': 'tag-gray',
    '待入库': 'tag-orange', '已入库': 'tag-green', '赔偿中': 'tag-orange', '已转应收': 'tag-blue',
    '已赔偿': 'tag-green', '部分退租': 'tag-blue',
    '已完成': 'tag-green', '待发货': 'tag-orange', '待验收': 'tag-orange', '已验收': 'tag-green',
    '组装中': 'tag-blue', '待组装': 'tag-orange', '待结算': 'tag-orange', '进行中': 'tag-blue'
  };

  function lk(text, url, base) {
    return url ? '<span class="lk" onclick="go(\'' + base + url + '\')">' + text + '</span>' : text;
  }
  function drow(label, valHtml, full) {
    return '<div class="drow"' + (full ? ' style="grid-column:1/-1;"' : '') +
      '><div class="dlabel">' + label + '</div><div class="dval">' + valHtml + '</div></div>';
  }

  window.renderGenericDetailHTML = function (rec, base) {
    base = base || '../';
    var h = '';

    h += '<div class="dt-sec">单据信息</div><div class="dgrid c3">';
    rec.info.forEach(function (f) {
      var v;
      if (f.tag) v = '<span class="tag ' + (STATUS_CLS[f.tag] || 'tag-gray') + '">' + f.tag + '</span>';
      else v = lk(f.text, f.url, base);
      h += drow(f.label, v, f.full);
    });
    h += '</div>';

    if (rec.feeCols && rec.fees) {
      h += '<div class="dt-sec">' + (rec.feeSecTitle || '费用明细') + '</div><div class="table-wrap"><table><thead><tr>';
      rec.feeCols.forEach(function (c, i) {
        h += i === 0 ? '<th>' + c + '</th>' : '<th>' + c + '</th>';
      });
      h += '</tr></thead><tbody>';
      rec.fees.forEach(function (f) {
        h += '<tr>';
        f.cells.forEach(function (cell, ci) {
          var url = f.links && f.links[ci];
          var isNum = /^[\-—☑]?[\d,]*\.?\d{0,2}/.test(cell) && /[\d,]+\.\d{2}/.test(cell) && !url;
          h += '<td' + (isNum ? ' class="td-num"' : '') + '>' + (url ? lk(cell, url, base) : cell) + '</td>';
        });
        h += '</tr>';
      });
      h += '</tbody></table></div>';
    }

    if (rec.chain) {
      h += '<div class="dt-sec">关联单据</div><div class="chain">';
      rec.chain.forEach(function (n, i) {
        if (i > 0) h += '<span class="link-arrow">→</span>';
        h += '<div class="node"' + (n.self ? ' style="border-color:#1677ff;background:#e6f4ff;"' : '') +
          '><div class="n-role">' + n.role + '</div><div class="n-name">' +
          (n.url ? lk(n.name, n.url, base) : n.name) + '</div></div>';
      });
      h += '</div>';
    }

    if (rec.timeline) {
      h += '<div class="dt-sec">流转时间线</div><div class="tl">';
      rec.timeline.forEach(function (t) {
        h += '<div class="tl-i' + (t.off ? ' off' : '') + '"><span class="tl-t">' + t.t + '</span>' +
          t.text + (t.who ? '<span class="tl-who">' + t.who + '</span>' : '') + '</div>';
      });
      h += '</div>';
    }
    return h;
  };

  window.openGenericDetail = function (entity, key, base) {
    var rec = window.DEMO_DATA && window.DEMO_DATA[entity] ? window.DEMO_DATA[entity][key] : null;
    if (!rec) { console.warn('[demo-data] ' + entity + ' 无数据: ' + key); return; }
    document.getElementById('detailTitle').textContent = rec.title + ' · ' + (rec.titleNo || key);
    document.getElementById('detailBody').innerHTML = window.renderGenericDetailHTML(rec, base);
    openModal('detailModal');
  };

  /* 列表页接线：把指向 detailModal 的「详情」按钮改绑为按行数据渲染 */
  window.wireDetailModal = function (entity) {
    var keys = Object.keys(window.DEMO_DATA && window.DEMO_DATA[entity] ? window.DEMO_DATA[entity] : {});
    if (!keys.length) { console.warn('[demo-data] 无实体: ' + entity); return; }
    document.querySelectorAll('tbody .ops a').forEach(function (a) {
      if (a.textContent.trim() !== '详情') return;
      if ((a.getAttribute('onclick') || '').indexOf('detailModal') < 0) return;
      var text = a.closest('tr').textContent;
      var key = null;
      for (var i = 0; i < keys.length; i++) {
        if (text.indexOf(keys[i]) > -1) { key = keys[i]; break; }
      }
      if (!key) return;
      a.removeAttribute('onclick');
      a.addEventListener('click', function () { openGenericDetail(entity, key); });
    });
  };
})();
