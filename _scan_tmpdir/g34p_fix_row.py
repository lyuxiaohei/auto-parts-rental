# -*- coding: utf-8 -*-
"""G34 试点补丁：修复 poSoPick 带出明细的行模板列数（6 列 → 11 列，与表格结构一致）

既有 bug：原弹窗的 poSoPick 生成行只有 6 个 td，而明细表是 9 列（新页 11 列），
浏览器渲染错位、且缺 data-tax 属性导致税率换算失效。试点中一并修正。
"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
N_P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html')

N = io.open(N_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')

old_line = """      return '<tr><td>' + (idx + 1) + '</td><td><input value=""></td><td><input value="' + mth[1] + '"></td><td class="td-num"><input value="' + String(mth[2]).replace(/,/g, '') + '"></td><td class="td-num"><input value="13%"></td><td class="td-num"><span class="td-num">自动计算</span></td></tr>';"""

new_line = """      return '<tr><td>' + (idx + 1) + '</td>'
        + '<td><select data-tax="prod" style="width:100%;min-width:130px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"><option selected>' + mth[1] + '</option></select></td>'
        + '<td><input value="' + mth[1] + '"></td>'
        + '<td><input value=""></td>'
        + '<td><input value="件"></td>'
        + '<td class="td-num"><input data-tax="qty" value="' + String(mth[2]).replace(/,/g, '') + '"></td>'
        + '<td class="td-num"><input data-tax="excl" value=""></td>'
        + '<td><input data-tax="rate" value="13%" style="width:56px;"></td>'
        + '<td class="td-num"><input data-tax="incl" value=""></td>'
        + '<td class="td-num"><input data-tax="amt" class="auto" readonly></td>'
        + '<td class="ops sticky-op"><a>删除</a></td></tr>';"""

assert N.count(old_line) == 1, f'poSoPick 行模板锚点异常 {N.count(old_line)}'
N = N.replace(old_line, new_line)

# 校验：新模板列数应为 11（序号列以 '</td>' 结尾形式拼接，故数 </td> 总数）
tds = new_line.count('</td>')
assert tds == 11, f'模板列数异常 {tds}'
print(f'[PATCH] poSoPick 行模板：6 列 → {tds} 列（与表格结构一致）')

io.open(N_P, 'w', encoding='utf-8', newline='').write(N.replace('\r\n', '\n').replace('\n', '\r\n'))
print('[写出]', N_P, len(N), '字符')
