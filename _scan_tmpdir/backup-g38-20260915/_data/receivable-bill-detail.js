/* ============================================================================
 * 应收账单详情弹窗 · 数据渲染（依赖 demo-data.js 的 receivableBills）
 * ----------------------------------------------------------------------------
 * 用法：
 *   <script src="../_data/demo-data.js"></script>
 *   <script src="../_data/receivable-bill-detail.js"></script>
 *   列表页：openReceivableBillDetail('AR-2026-09-PRJ2601-S1')   （base 默认 '../'）
 *   弹窗模板预览（弹窗/ 目录）：openReceivableBillDetail('AR-xxx', '../../')
 *
 * 要求页面弹窗骨架带两个挂载点：#detailTitle（标题）、#detailBody（正文容器），
 * 且已定义 go(url) / openModal(id)。
 * ========================================================================== */
(function () {
  var STATUS_CLS = { '未开票': 'tag-red', '部分收款': 'tag-orange', '已结清': 'tag-green', '已收': 'tag-green' };

  function fmt(n) {
    return Number(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function lk(text, url, base) {
    return url ? '<span class="lk" onclick="go(\'' + base + url + '\')">' + text + '</span>' : text;
  }
  function drow(label, valHtml, full) {
    return '<div class="drow"' + (full ? ' style="grid-column:1/-1;"' : '') +
      '><div class="dlabel">' + label + '</div><div class="dval">' + valHtml + '</div></div>';
  }

  /* 四段式详情 HTML：单据信息 / 费用明细 / 关联单据互溯链 / 流转时间线 */
  window.renderReceivableBillDetailHTML = function (b, base) {
    base = base || '../';
    var h = '';

    h += '<div class="dt-sec">单据信息</div><div class="dgrid c3">';
    h += drow('账单号', b.billNo, true);
    h += drow('状态', '<span class="tag ' + (STATUS_CLS[b.status] || 'tag-gray') + '">' + b.status + '</span>');
    h += drow('账期', b.period);
    h += drow('所属项目', b.project);
    h += drow('客户', b.customer, true);
    h += drow('费用类型', b.feeType, true);
    h += drow('账单金额', fmt(b.amount) + ' 元');
    h += drow('已核销', fmt(b.verified) + ' 元');
    h += drow('生成方式', b.genMode);
    h += drow('生成日期', b.genDate);
    h += '</div>';

    h += '<div class="dt-sec">费用明细</div>' +
      '<div class="table-wrap"><table><thead><tr><th>来源单据</th><th>费用说明</th><th class="td-num">数量</th><th class="td-num">单价(元)</th><th class="td-num">金额(元)</th></tr></thead><tbody>';
    b.fees.forEach(function (f) {
      h += '<tr><td>' + (f.url ? lk(f.src, f.url, base) : f.src) + '</td><td>' + f.desc +
        '</td><td class="td-num">' + f.qty + '</td><td class="td-num">' + f.price +
        '</td><td class="td-num">' + fmt(f.amount) + '</td></tr>';
    });
    h += '</tbody></table></div>';

    h += '<div class="dt-sec">关联单据</div><div class="chain">';
    b.chain.forEach(function (n, i) {
      if (i > 0) h += '<span class="link-arrow">→</span>';
      h += '<div class="node"' + (n.self ? ' style="border-color:#1677ff;background:#e6f4ff;"' : '') +
        '><div class="n-role">' + n.role + '</div><div class="n-name">' +
        (n.url ? lk(n.name, n.url, base) : n.name) + '</div></div>';
    });
    h += '</div>';

    h += '<div class="dt-sec">流转时间线</div><div class="tl">';
    b.timeline.forEach(function (t) {
      h += '<div class="tl-i' + (t.off ? ' off' : '') + '"><span class="tl-t">' + t.t + '</span>' +
        t.text + (t.who ? '<span class="tl-who">' + t.who + '</span>' : '') + '</div>';
    });
    h += '</div>';
    return h;
  };

  window.openReceivableBillDetail = function (billNo, base) {
    var b = window.DEMO_DATA && window.DEMO_DATA.receivableBills ? window.DEMO_DATA.receivableBills[billNo] : null;
    if (!b) { console.warn('[demo-data] 应收账单无数据: ' + billNo); return; }
    document.getElementById('detailTitle').textContent = '应收账单详情 · ' + billNo;
    document.getElementById('detailBody').innerHTML = window.renderReceivableBillDetailHTML(b, base);
    openModal('detailModal');
  };
})();
