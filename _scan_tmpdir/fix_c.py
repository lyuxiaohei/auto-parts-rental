# -*- coding: utf-8 -*-
"""C组：组合出库录单 / 采购入库录单「添加明细」= 克隆明细表末行示例数据 + 重排序号。"""
import sys
sys.path.insert(0, r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
from detail_modal_lib import *

ADD_JS = '''<script>
/* ===== 添加明细：克隆明细表末行示例数据并重排序号（详情落地页补齐 2026-09-04） ===== */
function addDetailRow(btn) {
  var card = btn.closest('.card');
  var tbody = card ? card.querySelector('tbody') : null;
  if (!tbody) return;
  var last = tbody.querySelector('tr:last-child');
  if (!last) return;
  var row = last.cloneNode(true);
  row.querySelectorAll('input').forEach(function (i) { i.value = i.defaultValue || i.value; });
  tbody.appendChild(row);
  var rows = tbody.querySelectorAll('tr');
  rows.forEach(function (r, i) { r.cells[0].textContent = i + 1; });
}
</script>'''

for page in ['仓储作业/组合出库录单.html', '仓储作业/采购入库录单.html']:
    t = read_page(page)
    t, t2 = inject_block(page, ADD_JS, with_js=False, extra_css=False)  # 锚点=绑定脚本前，仅注入函数
    old = '<button class="btn btn-dashed btn-sm">添加明细</button>'
    new = '<button class="btn btn-dashed btn-sm" onclick="addDetailRow(this)">添加明细</button>'
    t2 = bind_buttons(t2, old, new, 1)
    write_page(page, t2)
    print('OK 添加明细克隆行', page)
print('C 组完成')
