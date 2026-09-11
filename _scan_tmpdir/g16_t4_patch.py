# -*- coding: utf-8 -*-
"""G16 T4: dictItems 新增「物料类型」大类 + 数据字典页分类项 + 物料档案两弹窗「物料类型」下拉
铁律②：读取-精确替换+assert 计数；demo-data 插入后 node --check 由 T5 门跑
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'

# ---------- 1. demo-data.js dictItems 新增 WL-01/WL-02 ----------
f1 = PROT / '_data/demo-data.js'
s = f1.read_text(encoding='utf-8')
anchor = "    'ZF-02': { 'row': {\"fields\": {\"category\": \"支付方式\", \"abbr\": \"CD\", \"name\": \"银行承兑\""
assert s.count(anchor) == 1, f'ZF-02 anchor match={s.count(anchor)}'
NEW_REC = (
"""    'WL-01': { 'row': {"fields": {"category": "物料类型", "abbr": "QJ", "name": "器具", "status": "启用"}, "cells": ["QJ", "器具", "<span class=\\"td-num\\">1</span>", "循环包装器具（围板箱/托盘/料箱/料架）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
    'WL-02': { 'row': {"fields": {"category": "物料类型", "abbr": "LBJ", "name": "零部件", "status": "启用"}, "cells": ["LBJ", "零部件", "<span class=\\"td-num\\">2</span>", "汽车零部件散件（对客销售件）", "<span class=\\"tag tag-green\\">启用</span>"], "ops": [{"t": "编辑"}, {"t": "停用", "act": "openModal('stopModal')"}]} },
"""
)
# 找 ZF-02 所在行行尾（该行以 } }, 结尾），其后插入
i = s.index(anchor)
eol = s.index('\n', i)
assert s[eol-8:eol].endswith('}]} },'), f'ZF-02 行尾非预期: {s[eol-8:eol]!r}'
s2 = s[:eol+1] + NEW_REC + s[eol+1:]
assert s2.count('物料类型') == s.count('物料类型') + 2 and len(s2) == len(s) + len(NEW_REC)
f1.write_text(s2, encoding='utf-8')
print('[1] demo-data dictItems +WL-01/WL-02 ok')

# ---------- 2. 数据字典.html 分类列表加「物料类型」 ----------
f2 = PROT / '系统管理/数据字典.html'
s = f2.read_text(encoding='utf-8')
anchor2 = '<div class="dic-item"><span>支付方式</span><span class="cnt">2</span></div>'
assert s.count(anchor2) == 1, f'支付方式 dic-item match={s.count(anchor2)}'
NEW_ITEM = '<div class="dic-item"><span>物料类型</span><span class="cnt">2</span></div>'
s2 = s.replace(anchor2, anchor2 + '\n          ' + NEW_ITEM)
assert s2.count('dic-item') == s.count('dic-item') + 1
f2.write_text(s2, encoding='utf-8')
print('[2] 数据字典.html +物料类型 分类项 ok')

# ---------- 3. 两弹窗「分类」行前插「物料类型」行 ----------
CLS_ROW = '''<div class="form-row">
    <span class="form-label">分类</span>'''
NEW_ROW = '''<div class="form-row">
    <span class="form-label"><span class="req">*</span>物料类型</span>
    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>器具</option><option>零部件</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
  </div>
  <div class="form-row">
    <span class="form-label">分类</span>'''
for rel in ['基础数据/产品档案.html', '基础数据/弹窗/新建产品.html']:
    f3 = PROT / rel
    s = f3.read_text(encoding='utf-8')
    n = s.count(CLS_ROW)
    assert n == 1, f'{rel} 分类行 match={n}'
    s2 = s.replace(CLS_ROW, NEW_ROW)
    assert s2.count('物料类型') == s.count('物料类型') + 1 and s2.count('<div class="form-row">') == s.count('<div class="form-row">') + 1
    f3.write_text(s2, encoding='utf-8')
    print(f'[3] {rel} +物料类型 行（分类之前）ok')

print('T4 全部完成')
