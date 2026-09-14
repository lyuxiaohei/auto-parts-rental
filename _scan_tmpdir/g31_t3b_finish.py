# -*- coding: utf-8 -*-
"""G31 T3b：locations 手术（修 ops 重复 bug）+ 三页面落地（t3_stock_page/t3_location_page/t3_location_modal 原样取自 g31_t3_stock.py）
stockFlows 已是终态（前次执行完成），本脚本不再触碰。
"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('g31t3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g31_t3_stock.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)  # 只取函数，不触发 __main__

Q = chr(39)

def t3b_locations():
    p = '_data/demo-data.js'
    s = m.rd(p)
    WHMAP = {'XNC-AJZX': '客户虚拟仓（安吉智行）', 'RC-01': '次品仓', 'RC-02': '次品仓'}
    def wh_of(key):
        return WHMAP.get(key, '正品仓')
    i = s.find('  locations: {')
    j = s.find('  bomVersions', i)
    seg = s[i:j]
    keys = [k for k in re.findall(r"^[ ]{2,6}'([^']+)': \{", seg, re.M) if k != 'row']
    assert len(keys) == 11, keys
    for key in keys:
        ki = seg.find("'" + key + "': {")
        nk = re.search(r"^[\s]{2,6}'[^']+': \{", seg[ki + 10:], re.M)
        kend = ki + 10 + nk.start() if nk else len(seg)
        block = seg[ki:kend]
        rm = re.search(r"'row': (\{.*\}),\r\n", block)
        assert rm, 'row line ' + key
        row_src = rm.group(1)
        om = re.search(r'"ops": \[.*\]', row_src)
        ops = om.group(0) if om else '[]'
        fm = re.search(r'"fields": \{(.*?)\}, "cells"', row_src)
        assert fm, 'fields ' + key
        f = dict(re.findall(r'"(\w+)": "([^"]*)"', fm.group(1)))
        assert f.get('ltype'), (key, f)
        wh = wh_of(key)
        tag = 'tag-green' if f['status'] == '启用' else 'tag-gray'
        cells = '["%s", "%s", "%s", "%s", "<span class=\\"%s\\">%s</span>"]' % (wh, f['ltype'], f['spec'], f['usage'], tag, f['status'])
        new_row = ('{"fields": {"wh": "%s", "ltype": "%s", "spec": "%s", "usage": "%s", "status": "%s"}, '
                   '"cells": %s, %s}' % (wh, f['ltype'], f['spec'], f['usage'], f['status'], cells, ops))
        assert new_row.count('"ops"') == 1
        block = block.replace(rm.group(1), new_row, 1)
        bm = re.search(r"('label': '仓库',\r\n          'text': ')[^']*'", block)
        assert bm, 'info 仓库 ' + key
        block = block[:bm.start()] + bm.group(1) + wh + "'" + block[bm.end():]
        am = re.search(r"\{\r\n          'label': '库区',\r\n          'text': '[^']*'\r\n        \},\r\n", block)
        assert am, 'info 库区 ' + key
        block = block[:am.start()] + block[am.end():]
        seg = seg[:ki] + block + seg[kend:]
    # 终态断言：无库区标签、无 area 字段
    assert seg.count("'库区'") == 0 and seg.count('"area"') == 0
    s = s[:i] + seg + s[j:]
    m.wr(p, s)
    print('T3b locations 11 行手术 OK（title/info/chain 保留·库区标签清除）')

if __name__ == '__main__':
    t3b_locations()
    m.t3_location_page()
    m.t3_location_modal()
    m.t3_stock_page()
    print('T3b 全部完成')
