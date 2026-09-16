# -*- coding: utf-8 -*-
"""提取菜单 v6 结构（活页面侧边栏为真值源）"""
import io, re
c = io.open(r"P3-R01-包装租赁管理后台原型/首页/项目看板.html", encoding="utf-8").read()
i = c.find('class="side-menu"')
seg = c[i:]
end = seg.find('class="side-foot"')
seg = seg[:end if end > 0 else 9000]
groups = re.findall(r'sm-item has-sub[^>]*>\s*<div class="sm-link">.*?</svg></span>([^<]+)<', seg, re.S)
singles = re.findall(r'<li class="sm-item"><div class="sm-link"[^>]*>.*?</svg></span>([^<]+)</div></li>', seg, re.S)
menu = []
pos = 0
for g in groups:
    gi = seg.find(">" + g + "<span", pos)
    if gi == -1:
        gi = seg.find(g, pos)
    ul_end = seg.find("</ul>", gi)
    block = seg[gi:ul_end]
    its = re.findall(r"go\('([^']+)'\)\">([^<]+)<", block)
    menu.append((g.strip(), its))
    pos = ul_end
out = []
out.append("== 组（%d） ==" % len(menu))
n = 0
for g, its in menu:
    out.append("◆ %s（%d 项）" % (g, len(its)))
    for h, t in its:
        n += 1
        out.append("   %2d. %-16s %s" % (n, t.strip(), h))
out.append("一级直达：%s" % [s.strip() for s in singles])
out.append("菜单项合计：%d" % n)
txt = "\n".join(out)
io.open(r"_scan_tmpdir/g41_menu_v6.txt", "w", encoding="utf-8").write(txt)
print(txt)
