# -*- coding: utf-8 -*-
"""G51 T5: P1-R08 第三节 _data 登记 mat-search.js（九件实算口径）"""
import io

p = 'P1-R08-项目文件索引.md'
t = io.open(p, encoding='utf-8', newline='').read()

def sub1(old, new):
    global t
    n = t.count(old)
    assert n == 1, 'ANCHOR FAIL count=%d: %s' % (n, old[:60])
    t = t.replace(old, new)

sub1('| 演示数据 | `_data/`（demo-data.js 主数据+list/detail 通用渲染器+pc-auth 登录态+pc-msg 站内信·**打包 zip 必含**） |',
     '| 演示数据 | `_data/`（demo-data.js 主数据＋list/detail 通用渲染器＋receivable/payable-bill-detail 账单渲染器＋pc-auth 登录态＋pc-msg 站内信＋select-source.js 下拉数据源化〔G43〕＋**mat-search.js 搜索下拉共享件〔0917·D-155·表单搜索下拉全站约 43 处接线·两种形态/选中派发 change/幂等重绑〕**＝九件·**打包 zip 必含**） |')

for trial in range(3):
    try:
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        break
    except OSError:
        if trial == 2: raise
chk = io.open(p, encoding='utf-8', newline='').read()
assert 'mat-search.js 搜索下拉共享件' in chk and '＝九件' in chk, 'VERIFY FAIL'
print('T5 OK: P1-R08 _data row updated with mat-search.js (九件)')
