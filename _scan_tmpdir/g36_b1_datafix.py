# -*- coding: utf-8 -*-
"""G36 B1 demo-data ops 重定向（修正版：键跟踪排除 'row' 内层键）"""
import io, os, re, shutil

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
BAK = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b1-20260915\_data\demo-data.js'

# 从备份还原（上一轮 ?id=row 事故）
shutil.copy2(BAK, os.path.join(ROOT, '_data', 'demo-data.js'))
print('demo-data restored from backup')

p = '_data/demo-data.js'
s = io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
log = []

def entity_span(s, ent):
    a = s.index(ent + ': {')
    a = s.rfind('\n', 0, a) + 1
    b = s.index('\n  },', a)
    return a, b

def rew_ops(s, ent, mapping, detail_page, det_label='详情'):
    a, b = entity_span(s, ent)
    blk = s[a:b]
    lines = blk.split('\n')
    key = None; cnt = 0
    for i, ln in enumerate(lines):
        mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
        if mk and mk.group(1) != 'row':  # 'row' 是内层键，不作记录键
            key = mk.group(1)
        if 'openModal' not in ln and '"detail": true' not in ln:
            continue
        for mid, url in mapping.items():
            ln = ln.replace("openModal('%s')" % mid, "go('%s')" % url)
        det = '{"t": "%s", "detail": true}' % det_label
        if det in ln:
            assert key and key != 'row', 'no key for detail line in ' + ent
            ln = ln.replace(det, '{"t": "%s", "act": "go(\'%s?id=%s\')"}' % (det_label, detail_page, key))
            cnt += 1
        lines[i] = ln
    s = s[:a] + '\n'.join(lines) + s[b:]
    return s, cnt

s, n = rew_ops(s, 'products', {'createModal': '../基础数据/物料新建.html'}, '../基础数据/物料详情.html')
log.append('products: 详情×%d→物料详情?id=KEY；编辑→物料新建；停用留 stopModal' % n)
s, n = rew_ops(s, 'partners', {'createModal': '../基础数据/客商新建.html', 'invoiceInfoModal': '../基础数据/客商开票资料.html', 'recvInfoModal': '../基础数据/客商收货信息.html'}, '../基础数据/客商详情.html')
log.append('partners: 详情×%d→客商详情?id=KEY；编辑/开票资料/收货信息→三新页' % n)
s, n = rew_ops(s, 'locations', {'createModal': '../基础数据/库位新建.html'}, '../基础数据/库位详情.html')
log.append('locations: 详情×%d→库位详情?id=KEY；编辑→库位新建；停用留 stopModal' % n)
a, b = entity_span(s, 'bomVersions')
blk = s[a:b]
mkey = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", blk, re.M)
blk2 = blk.replace('{"t": "查看", "detail": true}', '{"t": "查看", "act": "go(\'../基础数据/BOM版本查看.html?id=%s\')"}' % mkey.group(1))
assert blk2 != blk
s = s[:a] + blk2 + s[b:]
log.append('bomVersions: 查看→go BOM版本查看?id=%s' % mkey.group(1))
a, b = entity_span(s, 'projects')
blk = s[a:b]
cnt = blk.count("openModal('bindModal')")
blk = blk.replace("openModal('bindModal')", "go('../项目管理/上下游绑定.html')")
s = s[:a] + blk + s[b:]
log.append('projects: bindModal→go 上下游绑定 ×%d' % cnt)

# 校验：不得残留 ?id=row；本批删除的弹窗 id 在这四个实体内不得回流
assert 'id=row' not in s, 'id=row residue!'
io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)
print('\n'.join(log))
print('DONE datafix')
