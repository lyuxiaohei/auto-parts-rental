# -*- coding: utf-8 -*-
"""G12 T3：9 个 A 类页面接线。
7 页 renderListPage（操作日志/用户权限/项目档案/项目详情/BOM/盈亏报表/项目看板）
2 页自写渲染器（我的待办·实体重建行 / 数据字典·分类切换）
纪律：锚点唯一断言/标签精确断言/写后校验/CRLF→LF 归一"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
ANCHOR = '/* ===== 菜单折叠 / 页签与表单视觉态（统一脚本） ===== */'

def labels_of(txt):
    out = []
    for m in re.finditer(r'<span class="ff-label">([\s\S]*?)</span>', txt):
        s = re.sub(r'<[^>]+>', '', m.group(1))
        out.append(s.strip().rstrip('::：').strip())
    return out

def insert_before_menu(path, block):
    txt = open(path, encoding='utf-8').read()
    assert txt.count(ANCHOR) == 1, 'anchor !=1 in ' + path
    assert 'demo-data.js' not in txt, 'already wired: ' + path
    crlf = '\r\n' in txt
    eol = '\r\n' if crlf else '\n'
    blk = block.replace('\n', eol)
    ci = txt.find(ANCHOR)
    si = txt.rfind('<script>', 0, ci)
    assert si > 0, 'script tag before anchor not found: ' + path
    new = txt[:si] + blk + txt[si:]
    new = new.replace('\r\n', '\n')  # G11 惯例 LF 归一
    open(path, 'w', encoding='utf-8', newline='\n').write(new)
    chk = open(path, encoding='utf-8').read()
    assert 'demo-data.js' in chk and ANCHOR in chk and chk.count('<html') == 1
    print('WIRED:', path, '| 标签集:', labels_of(txt) or '(无 filter)')

def lp(src_prefix, cfg_js):
    return ('<script src="%s_data/demo-data.js"></script>\n'
            '<script src="%s_data/list-generic.js"></script>\n'
            '<script>\n/* G12 数据驱动接线（2026-09-10）：tbody 实体渲染 + 真筛选 + stab 计数 */\n'
            'renderListPage(%s);\n</script>\n\n' % (src_prefix, src_prefix, cfg_js))

# ---------- 1. 操作日志 ----------
cfg = """{
  entity: 'opLogs',
  noCheckbox: true,
  filters: [
    { label: '操作人', field: 'user' },
    { label: '所属模块', field: 'module' },
    { label: '操作类型', field: 'opType' },
    { label: '操作时间', field: 'time', range: true },
    { label: '内容关键字', field: 'summary' }
  ]
}"""
insert_before_menu(ROOT + r'\系统管理\操作日志.html', lp('../', cfg))

# ---------- 2. 用户权限 ----------
cfg = """{
  entity: 'users',
  stabs: true,
  stabField: 'side',
  filters: [
    { label: '用户账号 / 姓名', field: 'search' },
    { label: '角色', field: 'role' },
    { label: '所属方', field: 'side' },
    { label: '数据权限范围', field: 'scope' }
  ]
}"""
insert_before_menu(ROOT + r'\系统管理\用户权限.html', lp('../', cfg))

# ---------- 3. 项目档案 ----------
cfg = """{
  entity: 'projects',
  filters: [
    { label: '项目编码 （自动生成：前缀+日期+序号）', field: '_key' },
    { label: '项目名称', field: 'name' },
    { label: '客户名称', field: 'customer' },
    { label: '项目状态', field: 'status' },
    { label: '立项时间', field: 'start', range: true },
    { label: '项目负责人', field: 'owner' }
  ]
}"""
insert_before_menu(ROOT + r'\项目管理\项目档案.html', lp('../', cfg))

# ---------- 4. 项目详情（标签先探后配） ----------
p4 = ROOT + r'\项目管理\项目详情.html'
t4 = open(p4, encoding='utf-8').read()
lbs = labels_of(t4)
print('项目详情 实测标签:', lbs)
MAP = {'单据编号': ("{ label: '单据编号', field: '_key' }"),
       '单据类型': ("{ label: '单据类型', field: 'type' }"),
       '状态': ("{ label: '状态', field: 'status' }"),
       '单据日期': ("{ label: '单据日期', field: 'date', range: true }"),
       '开始日期': ("{ label: '开始日期', field: 'date', range: true }"),
       '关键字': ("{ label: '关键字', field: 'summary' }"),
       '内容关键字': ("{ label: '内容关键字', field: 'summary' }")}
fl = [MAP[l] for l in lbs if l in MAP]
cfg = "{\n  entity: 'projectDocs',\n  noCheckbox: true,\n  stabs: true,\n  stabField: 'type'" + \
      (",\n  filters: [\n    " + ",\n    ".join(fl) + "\n  ]" if fl else "") + "\n}"
insert_before_menu(p4, lp('../', cfg))

# ---------- 5. BOM ----------
cfg = """{
  entity: 'bomList',
  filters: [
    { label: '父项编码', field: '_key' },
    { label: '父项名称', field: 'name' },
    { label: '版本', field: 'ver' },
    { label: '状态', field: 'status' },
    { label: '更新时间', field: 'update', range: true }
  ]
}"""
insert_before_menu(ROOT + r'\基础数据\BOM.html', lp('../', cfg))

# ---------- 6. 盈亏报表 ----------
cfg = """{
  entity: 'profitRows',
  noCheckbox: true,
  filters: [
    { label: '账期', field: 'period' },
    { label: '所属项目', field: 'code' }
  ]
}"""
insert_before_menu(ROOT + r'\财务协同\盈亏报表.html', lp('../', cfg))

# ---------- 7. 项目看板 ----------
cfg = """{
  entity: 'boardRows',
  noCheckbox: true,
  filters: []
}"""
insert_before_menu(ROOT + r'\首页\项目看板.html', lp('../', cfg))

print('renderListPage 7 页接线完成')
