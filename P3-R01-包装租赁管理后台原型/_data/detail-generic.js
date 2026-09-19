/* ============================================================================
 * 通用四段式详情弹窗 · 数据渲染（财务协同下游单据：付款/收款/开票/银行回单核销）
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
    '已转移': 'tag-green',
    '待入库': 'tag-orange', '已入库': 'tag-green', '赔偿中': 'tag-orange', '已转应收': 'tag-blue',
    '已赔偿': 'tag-green', '部分退租': 'tag-blue',
    '已完成': 'tag-green', '待发货': 'tag-orange', '待验收': 'tag-orange', '已验收': 'tag-green',
    '组装中': 'tag-blue', '待组装': 'tag-orange', '待结算': 'tag-orange', '进行中': 'tag-blue',
    '盘点中': 'tag-blue', '生效': 'tag-green', '超期未还': 'tag-red', '已退回': 'tag-gray',
    '缺损待赔': 'tag-orange', '已报废': 'tag-gray', '正常': 'tag-green', '空闲': 'tag-gray', '启用': 'tag-green', '已停用': 'tag-gray'
  };

  /* 导出给 list-generic.js 列表行 tag 复用（2026-09-08 列表试点） */
  window.DEMO_STATUS_CLS = STATUS_CLS;

  function lk(text, url, base) {
    return url ? '<span class="lk" onclick="go(\'' + base + url + '\')">' + text + '</span>' : text;
  }
  function drow(label, valHtml, full) {
    return '<div class="drow"' + (full ? ' style="grid-column:1/-1;"' : '') +
      '><div class="dlabel">' + label + '</div><div class="dval">' + valHtml + '</div></div>';
  }

  /* 新建版式模式（2026-09-18 道远指示：详情/审核向新建页版式靠拢）：
     记录含 formRows 时启用——信息段=form-row 只读行（字段名/顺序=新建页基准），
     明细段=itemCols/items 只读表（=新建明细列去操作列），流转段=关联单据链+时间线（详情专属）。
     无 formRows 的记录走原四段式，存量页面零影响。 */
  function renderFormModeHTML(rec, base) {
    base = base || '../';
    var h = '';
    /* 三张独立卡片：信息卡 / 明细卡 / 流转卡（2026-09-18 道远指示：拆成几个卡片，不要一整块）。
       外层壳卡由下方 CSS 透明化（页面零改动），壳卡标题条保留单号+返回按钮。 */
    h += '<div class="card fm-card"><div class="card-head"><h3 class="card-title">' + (rec.formTitle || '单据信息') + '</h3></div>';
    rec.formRows.forEach(function (f) {
      var v;
      if (f.tag) v = '<span class="tag ' + (STATUS_CLS[f.tag] || 'tag-gray') + '">' + f.tag + '</span>';
      else v = lk(f.text, f.url, base);
      h += '<div class="fm-row"><div class="form-label">' + f.label + '：</div>' +
           '<div class="fm-val"' + (f.full ? ' style="flex:1;min-width:0;"' : '') + '>' + v + '</div></div>';
    });
    h += '</div>';
    if (rec.itemCols && rec.items) {
      h += '<div class="card fm-card"><div class="card-head"><h3 class="card-title">' + (rec.itemTitle || '单据明细') + '</h3></div>' +
        '<div class="table-wrap"><table><thead><tr>';
      rec.itemCols.forEach(function (c) { h += '<th>' + c + '</th>'; });
      h += '</tr></thead><tbody>';
      rec.items.forEach(function (r) {
        h += '<tr>';
        r.forEach(function (cell) {
          var isNum = /^[\d,]+(\.\d{1,2})?$/.test(String(cell));
          h += '<td' + (isNum ? ' class="td-num"' : '') + '>' + cell + '</td>';
        });
        h += '</tr>';
      });
      h += '</tbody></table></div></div>';
    }
    if (rec.chain || rec.timeline) {
      h += '<div class="card fm-card"><div class="card-head"><h3 class="card-title">流转信息</h3></div>';
      if (rec.chain) {
        h += '<div class="chain">';
        rec.chain.forEach(function (n, i) {
          if (i > 0) h += '<span class="link-arrow">→</span>';
          h += '<div class="node"' + (n.self ? ' style="border-color:#1677ff;background:#e6f4ff;"' : '') +
            '><div class="n-role">' + n.role + '</div><div class="n-name">' +
            (n.url ? lk(n.name, n.url, base) : n.name) + '</div></div>';
        });
        h += '</div>';
      }
      if (rec.timeline) {
        h += '<div class="tl">';
        rec.timeline.forEach(function (t) {
          h += '<div class="tl-i' + (t.off ? ' off' : '') + '"><span class="tl-t">' + t.t + '</span>' +
            t.text + (t.who ? '<span class="tl-who">' + t.who + '</span>' : '') + '</div>';
        });
        h += '</div>';
      }
      h += '</div>';
    }
    h += '<style>' +
      /* 壳卡透明化：detailBody 的宿主卡退化为容器，标题条（单号+返回按钮）保留 */
      '.card:has(> #detailBody){background:transparent;box-shadow:none;padding:0;border-radius:0;}' +
      '.card:has(> #detailBody) > .card-head{padding:0 4px;}' +
      '.fm-row{display:flex;align-items:flex-start;margin-bottom:14px;}' +
      '.fm-row .form-label{flex:0 0 120px;text-align:right;margin-right:8px;font-size:13px;white-space:nowrap;}' +
      '.fm-val{width:380px;min-height:30px;border:1px solid #e5e6eb;border-radius:6px;padding:4px 11px;background:#fafafa;color:#595959;font-size:13px;display:flex;align-items:center;flex-wrap:wrap;word-break:break-all;box-sizing:border-box;}' +
      '.fm-val .tag{margin:0;}' +
      '.fm-card > .card-head .card-title{margin-bottom:14px;}' +
      /* 流转卡内两段间距：关联单据链与时间线（道远 09-19 反馈 0px 太近·+10px） */
      '.fm-card .chain{margin-bottom:10px;}' +
      '</style>';
    return h;
  }

  window.renderGenericDetailHTML = function (rec, base) {
    base = base || '../';
    if (rec.formRows) return renderFormModeHTML(rec, base); /* 新建版式模式（见上） */
    /* 2026-09-14 双列布局（陆鸣拍板：弹窗不出滚动条）——列1=单据信息+费用明细，列2=关联单据+时间线 */
    var h = '';
    var h1 = '', h2 = '';

    h1 += '<div class="dt-sec">单据信息</div><div class="dgrid c3">';
    rec.info.forEach(function (f) {
      var v;
      if (f.tag) v = '<span class="tag ' + (STATUS_CLS[f.tag] || 'tag-gray') + '">' + f.tag + '</span>';
      else v = lk(f.text, f.url, base);
      h1 += drow(f.label, v, f.full);
    });
    h1 += '</div>';

    /* G42 T7a：可选第二信息段（如客商详情·开票资料）——无 info2 键的页面零影响 */
    if (rec.info2) {
      h1 += '<div class="dt-sec">' + (rec.info2Title || '更多信息') + '</div><div class="dgrid c3">';
      rec.info2.forEach(function (f) {
        var v;
        if (f.tag) v = '<span class="tag ' + (STATUS_CLS[f.tag] || 'tag-gray') + '">' + f.tag + '</span>';
        else v = lk(f.text, f.url, base);
        h1 += drow(f.label, v, f.full);
      });
      h1 += '</div>';
    }

    if (rec.feeCols && rec.fees) {
      h1 += '<div class="dt-sec">' + (rec.feeSecTitle || '费用明细') + '</div><div class="table-wrap"><table><thead><tr>';
      rec.feeCols.forEach(function (c, i) {
        h1 += i === 0 ? '<th>' + c + '</th>' : '<th>' + c + '</th>';
      });
      h1 += '</tr></thead><tbody>';
      rec.fees.forEach(function (f) {
        h1 += '<tr>';
        f.cells.forEach(function (cell, ci) {
          var url = f.links && f.links[ci];
          var isNum = /^[\-—☑]?[\d,]*\.?\d{0,2}/.test(cell) && /[\d,]+\.\d{2}/.test(cell) && !url;
          h1 += '<td' + (isNum ? ' class="td-num"' : '') + '>' + (url ? lk(cell, url, base) : cell) + '</td>';
        });
        h1 += '</tr>';
      });
      h1 += '</tbody></table></div>';
    }

    if (rec.chain) {
      h2 += '<div class="dt-sec">关联单据</div><div class="chain">';
      rec.chain.forEach(function (n, i) {
        if (i > 0) h2 += '<span class="link-arrow">→</span>';
        h2 += '<div class="node"' + (n.self ? ' style="border-color:#1677ff;background:#e6f4ff;"' : '') +
          '><div class="n-role">' + n.role + '</div><div class="n-name">' +
          (n.url ? lk(n.name, n.url, base) : n.name) + '</div></div>';
      });
      h2 += '</div>';
    }

    if (rec.timeline) {
      h2 += '<div class="dt-sec">流转时间线</div><div class="tl">';
      rec.timeline.forEach(function (t) {
        h2 += '<div class="tl-i' + (t.off ? ' off' : '') + '"><span class="tl-t">' + t.t + '</span>' +
          t.text + (t.who ? '<span class="tl-who">' + t.who + '</span>' : '') + '</div>';
      });
      h2 += '</div>';
    }

    h += '<style>.dt2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 22px;align-content:start;}' +
      '.dt2 .dt-sec{margin-top:0;}.dt2 .dgrid.c3{grid-template-columns:repeat(2,1fr);}.dt2 .table-wrap td,.dt2 .table-wrap th{white-space:nowrap;}</style>';
    h += '<div class="dt2"><div class="dt2-c">' + h1 + '</div><div class="dt2-c">' + h2 + '</div></div>';
    return h;
  };

  window.openGenericDetail = function (entity, key, base, modalId) {
    var rec = window.DEMO_DATA && window.DEMO_DATA[entity] ? window.DEMO_DATA[entity][key] : null;
    if (!rec) { console.warn('[demo-data] ' + entity + ' 无数据: ' + key); return; }
    var mdl = document.getElementById(modalId || 'detailModal');
    mdl = mdl ? mdl.querySelector('.modal') : null;
    if (mdl) { mdl.style.width = '1080px'; mdl.style.maxWidth = '94vw'; } /* 2026-09-14 双列详情配套加宽 */
    document.getElementById('detailTitle').textContent = rec.title + ' · ' + (rec.titleNo || key);
    document.getElementById('detailBody').innerHTML = window.renderGenericDetailHTML(rec, base);
    openModal(modalId || 'detailModal');
  };

  /* 列表页接线：把指向指定弹窗的触发锚改绑为按行数据渲染。
     opts 可选：{ anchorText: '详情'|其他, modalId: 'detailModal'|其他 }（2026-09-08 批3扩展） */
  window.wireDetailModal = function (entity, opts) {
    opts = opts || {};
    var anchorText = opts.anchorText || '详情';
    var modalId = opts.modalId || 'detailModal';
    var keys = Object.keys(window.DEMO_DATA && window.DEMO_DATA[entity] ? window.DEMO_DATA[entity] : {});
    if (!keys.length) { console.warn('[demo-data] 无实体: ' + entity); return; }
    document.querySelectorAll('tbody .ops a').forEach(function (a) {
      if (a.textContent.trim() !== anchorText) return;
      if ((a.getAttribute('onclick') || '').indexOf(modalId) < 0) return;
      var text = a.closest('tr').textContent;
      var key = null;
      for (var i = 0; i < keys.length; i++) {
        if (text.indexOf(keys[i]) > -1) { key = keys[i]; break; }
      }
      if (!key) return;
      a.removeAttribute('onclick');
      a.addEventListener('click', function () { openGenericDetail(entity, key, undefined, modalId); });
    });
  };
})();
