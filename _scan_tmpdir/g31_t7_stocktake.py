# -*- coding: utf-8 -*-
"""G31 T7 盘点（D-110）：盘点录入每物料行内「生成其他入库/出库」→ 跳创建页自动带物料；
其他入/出库类型域补「破损」「自然损耗」（保留既有值）。"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

RADIO = '<span class="radio"><span class="dot"></span>%s</span>'

def add_types(p, anchor_label):
    s = rd(p)
    if '自然损耗' in s:
        print(p, '类型已补（幂等）'); return
    pat = re.compile(r'<span class="radio[^"]*"[^>]*>(?:<span class="dot"></span>)?' + anchor_label + r'</span>')
    m = pat.search(s)
    assert m, 'anchor radio ' + anchor_label + ' in ' + p
    ins = m.group(0) + RADIO % '破损' + RADIO % '自然损耗'
    s = s.replace(m.group(0), ins, 1)
    wr(p, s)
    print(p, ': +破损+自然损耗 OK')

def stocktake_entry():
    p = '仓储作业/盘点录入.html'
    s = rd(p)
    if 'genOtherOut' in s or '生成其他出库' in s:
        print(p, '已改（幂等）'); return
    # 表头补 操作 th（锚：差异说明 th 后）
    NL = '\r\n' if '\r\n' in s else '\n'
    m = re.search(r'>差异说明</th>\s*</tr>\s*</thead>', s)
    assert m, 'th anchor'
    s = s.replace(m.group(0), '>差异说明</th><th class="sticky-op">操作</th></tr></thead>', 1)
    # 行内按钮：按差异符号分写入/出（0 差异给 —）
    def fix_row(mm):
        row = mm.group(0)
        code = re.search(r'<td>([A-Z]{2,}[\w-]*)</td>', row)
        code = code.group(1) if code else ''
        diff = re.search(r'<span style="color:var\(--danger\)">(-?\d+)</span>|<span[^>]*>(\d+)</span>', row)
        dv = None
        if diff:
            dv = diff.group(1) or diff.group(2)
        if dv is None or int(dv.replace(',', '')) == 0:
            btn = '<td class="sticky-op"><span style="color:#8c8c8c;">—</span></td>'
        elif int(dv.replace(',', '')) > 0:
            btn = ('<td class="sticky-op"><a class="lk" onclick="genOtherDoc(' + Q + 'in' + Q + ', ' + Q + code + Q + ')">生成其他入库</a></td>')
        else:
            btn = ('<td class="sticky-op"><a class="lk" onclick="genOtherDoc(' + Q + 'out' + Q + ', ' + Q + code + Q + ')">生成其他出库</a></td>')
        return row.rstrip() + NL + '          ' + btn + NL + '        </tr>'
    seg_m = re.search(r'<tbody>(.*?)</tbody>', s, re.S)
    seg2, n = re.subn(r'<tr>.*?</tr>', fix_row, seg_m.group(1), flags=re.S)
    assert n == 5, n
    s = s.replace(seg_m.group(1), seg2, 1)
    # 跳转函数（带物料与盘点来源）
    JS = ('<script>/* G31 T7 盘点行内生成其他入/出库（D-110）：跳创建页自动带物料·按差异方向分单 */' + NL +
          'function genOtherDoc(dir, item) {' + NL +
          "  var page = dir === 'in' ? '../仓储作业/其他入库列表.html' : '../仓储作业/其他出库列表.html';" + NL +
          "  var type = dir === 'in' ? '盘盈' : '盘亏';" + NL +
          "  location.href = page + '?create=1&item=' + encodeURIComponent(item) + '&type=' + encodeURIComponent(type);" + NL +
          '}</script>')
    k = s.rfind('<script>')
    s = s[:k] + JS + NL + s[k:]
    assert len(re.findall(r'<th[>\s]', s)) == len(re.findall(r'</th>', s))
    wr(p, s)
    print(p, ': 行内生成按钮×5 行 + 跳转函数 OK')

def url_handler(p):
    s = rd(p)
    if 'create=1' in s:
        print(p, 'URL 处理已加（幂等）'); return
    NL = '\r\n' if '\r\n' in s else '\n'
    JS = ('<script>/* G31 T7 盘点带料跳转（D-110）：?create=1&item=编码&type=类型 → 自动开单并预填物料 */' + NL +
          '(function () {' + NL +
          '  var q = new URLSearchParams(location.search);' + NL +
          "  if (q.get('create') !== '1') return;" + NL +
          '  try { openModal(' + Q + 'createModal' + Q + '); } catch (e) {}' + NL +
          '  var item = q.get(' + Q + 'item' + Q + '), type = q.get(' + Q + 'type' + Q + ');' + NL +
          '  if (item) {' + NL +
          "    var modal = document.getElementById('createModal');" + NL +
          '    if (modal) {' + NL +
          '      var inps = [...modal.querySelectorAll(' + Q + '.edit-tbl input' + Q + ')];' + NL +
          '      if (inps[0]) inps[0].value = item;' + NL +
          '    }' + NL +
          '  }' + NL +
          '  if (type) {' + NL +
          "    [...document.querySelectorAll('#createModal .radio')].forEach(function (r) {" + NL +
          "      var on = r.textContent.trim() === type;" + NL +
          "      r.classList.toggle('checked', on);" + NL +
          '    });' + NL +
          '  }' + NL +
          '})();')
    k = s.rfind('<script>')
    s = s[:k] + JS + NL + s[k:]
    wr(p, s)
    print(p, ': ?create=1&item= URL 带料处理 OK')

if __name__ == '__main__':
    add_types('仓储作业/其他入库列表.html', '退货')
    add_types('仓储作业/弹窗/其他入库新建.html', '退货')
    add_types('仓储作业/其他出库列表.html', '盘亏')
    add_types('仓储作业/弹窗/其他出库新建.html', '盘亏')
    stocktake_entry()
    url_handler('仓储作业/其他入库列表.html')
    url_handler('仓储作业/其他出库列表.html')
    print('T7 完成')
