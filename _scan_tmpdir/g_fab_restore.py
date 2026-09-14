# -*- coding: utf-8 -*-
"""恢复 35 业务页「流程图」fab：有标注块的用 fab-row 合并形态；无标注的独立 fab 插 </body> 前"""
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
LACK = """我的待办.html
仓储作业/库存查询.html
仓储作业/盘点列表.html
仓储作业/盘点录入.html
基础数据/BOM.html
基础数据/BOM维护.html
基础数据/产品档案.html
基础数据/客商管理.html
基础数据/库位档案.html
租赁管理/租入入库列表.html
租赁管理/租入单列表.html
租赁管理/租入归还列表.html
租赁管理/租赁出库列表.html
租赁管理/租赁出库录单.html
租赁管理/租赁单列表.html
租赁管理/退租入库列表.html
系统管理/操作日志.html
系统管理/数据字典.html
系统管理/用户权限.html
系统管理/角色管理.html
财务协同/付款登记.html
财务协同/回款登记.html
财务协同/应付账单.html
财务协同/应收账单.html
财务协同/开票登记.html
财务协同/盈亏报表.html
财务协同/银行水单核销.html
采购管理/采购入库列表.html
采购管理/采购入库录单.html
采购管理/采购订单列表.html
销售管理/销售出库列表.html
销售管理/销售订单列表.html
项目管理/项目档案.html
项目管理/项目详情.html
首页/项目看板.html""".splitlines()

STYLE_ROW = ('<style id="f01-fab-style">.fab-row{position:fixed;right:12px;bottom:12px;z-index:880;display:flex;align-items:center;gap:6px}'
             '.fab-row .pn-fab{position:static}'
             '.f01-fab{display:flex;text-decoration:none;align-items:center;height:24px;padding:0 10px;border-radius:4px;background:#fff;border:1px solid #d9d9d9;color:#8c8c8c;font-size:11px;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}'
             '.f01-fab:hover{opacity:1;border-color:#722ed1;color:#722ed1}</style>')
STYLE_STANDALONE = ('<style id="f01-fab-style">.f01-fab{position:fixed;right:12px;bottom:12px;z-index:1001;display:flex;align-items:center;height:24px;padding:0 10px;border-radius:4px;background:#fff;border:1px solid #d9d9d9;color:#8c8c8c;font-size:11px;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}'
                    '.f01-fab:hover{opacity:1;border-color:#722ed1;color:#722ed1}</style>')

done = skipped = 0
for key in LACK:
    key = key.strip()
    if not key:
        continue
    fp = ROOT + "\\" + key.replace("/", "\\")
    raw = open(fp, "rb").read()
    c0, l0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
    nl = "\r\n" if c0 > l0 else "\n"
    t = io.open(fp, encoding="utf-8", newline="").read()
    depth = "" if "/" not in key else "../"
    href = depth + "P3-R01-F01-业务流程导航图.html"
    if "f01-fab" in t:
        print("SKIP 已有", key)
        skipped += 1
        continue
    pnfab_tail = '<div class="pn-fab" id="protoNotesFab">标注</div></div>'
    if t.count(pnfab_tail) == 1:
        rep = (STYLE_ROW + nl +
               '<div class="fab-row"><a class="f01-fab" href="' + href + '">流程图</a>' +
               '<div class="pn-fab" id="protoNotesFab">标注</div></div></div>')
        t = t.replace(pnfab_tail, rep, 1)
    else:
        anchor_old = "</body>"
        assert t.count(anchor_old) == 1, key + " </body> 异常"
        rep = (STYLE_STANDALONE + nl +
               '<a class="f01-fab" href="' + href + '">流程图</a>' + nl + anchor_old)
        t = t.replace(anchor_old, rep, 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    c1, l1 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
    assert (l1 == 0) == (l0 == 0) and (c1 == 0) == (c0 == 0), key + " 行尾风格改变 %s→%s" % ((c0, l0), (c1, l1))
    done += 1
print("PASS 恢复 %d 页·跳过 %d 页" % (done, skipped))
