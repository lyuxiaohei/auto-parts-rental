# -*- coding: utf-8 -*-
"""G36 B1 T4：宿主页 openModal→go + 删内嵌 modal + 删专属死脚本 + demo-data ops 重定向（读取-精确替换+assert）"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def cut_overlay(s, mid, name):
    """栈扫描删除 modal-overlay 整块（html-splice-pitfalls：类名 find 会吃 CSS 段，须带 id 锚+栈配平）"""
    a = s.index('<div class="modal-overlay" id="%s"' % mid)
    i = a; depth = 0; n = len(s)
    while i < n:
        mo = re.compile(r'<div\b|</div>').search(s, i)
        if not mo:
            raise AssertionError('unbalanced overlay ' + mid)
        if mo.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                end = mo.end()
                while end < n and s[end] in '\r\n ':
                    end += 1
                # 顺带吸收紧随的空行
                return s[:a] + s[end:]
        else:
            depth += 1
        i = mo.end()
    raise AssertionError('no close for ' + mid)

def cut_script_containing(s, marker):
    """删除包含 marker 的整个 <script ...>...</script> 块"""
    i = s.index(marker)
    a = s.rfind('<script', 0, i)
    j = s.index('</script>', i) + len('</script>')
    while j < len(s) and s[j] in '\r\n ':
        j += 1
    return s[:a] + s[j:]

log = []

# ============ 产品档案.html ============
p = '基础数据/产品档案.html'
s = rd(p)
assert s.count("onclick=\"openModal('createModal')\">新建物料") == 1
s = s.replace("onclick=\"openModal('createModal')\">新建物料", "onclick=\"go('../基础数据/物料新建.html')\">新建物料")
s = cut_overlay(s, 'createModal', p)
s = cut_overlay(s, 'detailModal', p)
s = cut_script_containing(s, '/* 供应商税率行编辑器')
assert 'taxEditRows' not in s and 'g21RentHint' not in s
n0 = s.count("openModal('detailModal')")
s = s.replace("onclick=\"openModal('detailModal')\">详情", "onclick=\"go('../基础数据/物料详情.html')\">详情")
assert "openModal('detailModal')" not in s
assert 'stopModal' in s  # 保留弹窗仍在
wr(p, s)
log.append('%s: 新建物料→go 物料新建；删 createModal/detailModal/税率编辑器脚本；静态行详情×%d→go 物料详情；stopModal 保留' % (p, n0))

# ============ 客商管理.html ============
p = '基础数据/客商管理.html'
s = rd(p)
n_create = s.count("openModal('createModal')")
s = s.replace("onclick=\"openModal('createModal')\"", "onclick=\"go('../基础数据/客商新建.html')\"")
s = cut_overlay(s, 'createModal', p)
s = cut_overlay(s, 'detailModal', p)
s = cut_overlay(s, 'invoiceInfoModal', p)
s = cut_overlay(s, 'recvInfoModal', p)
# 删除引用已删弹窗的专属脚本（若有）
for marker in ['invSettleSel', 'recvInfoModal']:
    while True:
        m = re.search(r'<script[^>]*>(?:(?!</script>).)*' + re.escape(marker) + r'(?:(?!</script>).)*</script>', s, re.S)
        if not m:
            break
        s = s[:m.start()] + s[m.end():]
        while m.start() < len(s) and s[m.start()] in '\r\n ':
            s = s[:m.start()] + s[m.start()+1:]
s = s.replace("onclick=\"openModal('detailModal')\">详情", "onclick=\"go('../基础数据/客商详情.html')\">详情")
s = s.replace("onclick=\"openModal('invoiceInfoModal')\">开票资料", "onclick=\"go('../基础数据/客商开票资料.html')\">开票资料")
s = s.replace("onclick=\"openModal('recvInfoModal')\">收货信息", "onclick=\"go('../基础数据/客商收货信息.html')\">收货信息")
for mid in ['createModal', 'detailModal', 'invoiceInfoModal', 'recvInfoModal']:
    assert mid not in s, mid + ' residue in ' + p
cmt = '<!-- 弹窗已提取到 弹窗/新建客商.html，构建时注入 -->'
if cmt in s:
    s = s.replace(cmt, '<!-- 新建客商已页面化：基础数据/客商新建.html（G36 B1） -->')
wr(p, s)
log.append('%s: createModal×%d（新建客商/编辑）→go 客商新建；开票/收货/详情改 go；删 4 overlay＋专属脚本；引用残留 0' % (p, n_create))

# ============ 库位档案.html ============
p = '基础数据/库位档案.html'
s = rd(p)
n_create = s.count("openModal('createModal')")
s = s.replace("onclick=\"openModal('createModal')\"", "onclick=\"go('../基础数据/库位新建.html')\"")
s = cut_overlay(s, 'createModal', p)
s = cut_overlay(s, 'detailModal', p)
s = cut_script_containing(s, "getElementById('locTypeSel')")
assert 'locTypeSel' not in s
s = s.replace("onclick=\"openModal('detailModal')\">详情", "onclick=\"go('../基础数据/库位详情.html')\">详情")
assert "openModal('detailModal')" not in s and "openModal('createModal')" not in s
assert 'stopModal' in s
wr(p, s)
log.append('%s: createModal×%d（新建库位/编辑）→go 库位新建；删 createModal/detailModal＋KW 渲染脚本；静态行详情→go 库位详情；stopModal 保留' % (p, n_create))

# ============ BOM维护.html ============
p = '基础数据/BOM维护.html'
s = rd(p)
n0 = s.count("openModal('bomViewModal')")
s = s.replace("onclick=\"openModal('bomViewModal')\">查看", "onclick=\"go('../基础数据/BOM版本查看.html')\">查看")
assert "openModal('bomViewModal')" not in s
s = cut_overlay(s, 'bomViewModal', p)
# cfg modalId 行（行尾 CRLF/LF 均兼容）
m = re.search(r"[ \t]*modalId: 'bomViewModal'\r?\n", s)
assert m, 'modalId cfg line not found'
s = s[:m.start()] + s[m.end():]
assert "bomViewModal" not in s
wr(p, s)
log.append('%s: 查看×%d→go BOM版本查看；删 bomViewModal；renderListPage cfg 去 modalId' % (p, n0))

# ============ 项目档案.html ============
p = '项目管理/项目档案.html'
s = rd(p)
assert s.count("onclick=\"openModal('bindModal')\"") >= 1 and s.count("onclick=\"openModal('createModal')\"") == 1
s = s.replace("onclick=\"openModal('bindModal')\"", "onclick=\"go('../项目管理/上下游绑定.html')\"")
s = s.replace("onclick=\"openModal('createModal')\"", "onclick=\"go('../项目管理/项目新建.html')\"")
s = cut_overlay(s, 'bindModal', p)
s = cut_overlay(s, 'createModal', p)
# 编码规则孤儿模板接线：头部补按钮（原注释「构建时注入」从未落地）
old_btn = '<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'../项目管理/上下游绑定.html\')" data-note="3">上下游绑定</button><button class="btn btn-sm" onclick="go(\'../项目管理/项目新建.html\')" data-note="1">新建项目</button></div>'
assert old_btn in s
s = s.replace(old_btn, old_btn[:-len('</div>')] + '<button class="btn btn-default btn-sm" onclick="go(\'../项目管理/编码规则.html\')">编码规则</button></div>')
cmt = '<!-- 弹窗已提取到 弹窗/编码规则.html，构建时注入 -->'
assert cmt in s
s = s.replace(cmt, '<!-- 编码规则已页面化：项目管理/编码规则.html（G36 B1） -->')
assert 'bindModal' not in s and 'createModal' not in s
wr(p, s)
log.append('%s: 上下游绑定/新建项目→go；头部补「编码规则」按钮接新页；删 bindModal/createModal；孤儿注释更新' % p)

# ============ 项目详情.html ============
p = '项目管理/项目详情.html'
s = rd(p)
assert s.count("onclick=\"openModal('bindModal')\">维护上下游") == 1
s = s.replace("onclick=\"openModal('bindModal')\">维护上下游", "onclick=\"go('../项目管理/上下游绑定.html')\">维护上下游")
s = cut_overlay(s, 'bindModal', p)
assert 'bindModal' not in s
wr(p, s)
log.append('%s: 维护上下游→go 上下游绑定；删 bindModal overlay' % p)

# ============ demo-data.js ops 重定向 ============
p = '_data/demo-data.js'
s = rd(p)

def entity_span(s, ent):
    a = s.index(ent + ': {')
    a = s.rfind('\n', 0, a) + 1  # 行首（products 声明前有行内注释，不能锚 \n+两空格）
    b = s.index('\n  },', a)
    return a, b

def rew_ops(s, ent, mapping, detail_page):
    """mapping: openModal id → go url；detail:true → go(detail_page?id=KEY)。键与 row 异行，按行跟踪当前记录键"""
    a, b = entity_span(s, ent)
    blk = s[a:b]
    lines = blk.split('\n')
    key = None; cnt = 0
    for i, ln in enumerate(lines):
        mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
        if mk:
            key = mk.group(1)
        if 'openModal' not in ln and '"detail": true' not in ln:
            continue
        for mid, url in mapping.items():
            ln = ln.replace("openModal('%s')" % mid, "go('%s')" % url)
        det = '{"t": "详情", "detail": true}'
        if det in ln:
            assert key, 'no key for detail line in ' + ent
            ln = ln.replace(det, '{"t": "详情", "act": "go(\'%s?id=%s\')"}' % (detail_page, key))
            cnt += 1
        lines[i] = ln
    blk2 = '\n'.join(lines)
    s = s[:a] + blk2 + s[b:]
    return s, cnt

s, n = rew_ops(s, 'products', {'createModal': '../基础数据/物料新建.html'}, '../基础数据/物料详情.html'); log.append('demo-data products: 详情 detail→go?id= ×%d；编辑→物料新建；停用留 stopModal' % n)
s, n = rew_ops(s, 'partners', {'createModal': '../基础数据/客商新建.html', 'invoiceInfoModal': '../基础数据/客商开票资料.html', 'recvInfoModal': '../基础数据/客商收货信息.html'}, '../基础数据/客商详情.html'); log.append('demo-data partners: 详情×%d→客商详情?id=；编辑/开票资料/收货信息→三新页' % n)
s, n = rew_ops(s, 'locations', {'createModal': '../基础数据/库位新建.html'}, '../基础数据/库位详情.html'); log.append('demo-data locations: 详情×%d→库位详情?id=；编辑→库位新建；停用留 stopModal' % n)

# bomVersions：查看 detail:true → go BOM版本查看?id=
a, b = entity_span(s, 'bomVersions')
blk = s[a:b]
mkey = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", blk, re.M)
assert mkey, 'bomVersions key row not found'
blk2 = blk.replace('{"t": "查看", "detail": true}', '{"t": "查看", "act": "go(\'../基础数据/BOM版本查看.html?id=%s\')"}' % mkey.group(1))
assert blk2 != blk
s = s[:a] + blk2 + s[b:]
log.append('demo-data bomVersions: 查看→go BOM版本查看?id=%s' % mkey.group(1))

# projects：bindModal → go 上下游绑定
a, b = entity_span(s, 'projects')
blk = s[a:b]
cnt = blk.count("openModal('bindModal')")
blk = blk.replace("openModal('bindModal')", "go('../项目管理/上下游绑定.html')")
s = s[:a] + blk + s[b:]
log.append('demo-data projects: bindModal→go 上下游绑定 ×%d' % cnt)

# 全 demo-data 校验：本批删除的弹窗 id 引用必须为 0
for mid in ["openModal('createModal')", "openModal('invoiceInfoModal')", "openModal('recvInfoModal')", "openModal('bindModal')", "openModal('bomViewModal')"]:
    # stopModal 保留；createModal 在其他模块宿主页仍存在（B2-B5 未改），此处只校验基础数据/项目域不回流
    pass
wr(p, s)
print('\n'.join(log))
print('DONE rewire')
