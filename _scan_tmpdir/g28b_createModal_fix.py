# -*- coding: utf-8 -*-
"""新建物料弹窗去滚动条：专属 900px + modal-body 两列网格（g2 行跨全列）
双层：产品档案.html + 弹窗/新建产品.html（结构同构，相同替换串）
"""
import io, re, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\基础数据\产品档案.html", ROOT + r"\基础数据\弹窗\新建产品.html"]

CSS_BLOCK = """<div class="modal-overlay" id="createModal">
  <style>
  /* 2026-09-14 道远拍板：新建物料弹窗加宽 900px+两列布局，消除横竖滚动条（四参考价+三段式+税率区内容增量后 640px 单列溢出） */
  #createModal .modal{width:900px;max-width:94vw;}
  #createModal .modal-body{display:grid;grid-template-columns:1fr 1fr;column-gap:18px;align-content:start;}
  #createModal .form-row{margin-bottom:14px;}
  #createModal .form-row.g2{grid-column:1/-1;}
  #createModal .tax-sec{grid-column:1/-1;}
  </style>"""

G2_LABELS = ["参考未税租入价", "参考未税租赁价", "备注"]

for fp in FILES:
    t = io.open(fp, encoding="utf-8", newline="").read()
    # 1. CSS 块：插在 createModal overlay 开标签后
    anchor = '<div class="modal-overlay" id="createModal">'
    assert t.count(anchor) == 1, fp + " overlay 锚点 %d" % t.count(anchor)
    t = t.replace(anchor, CSS_BLOCK, 1)
    # 2. g2 行
    for lab in G2_LABELS:
        pat = re.compile(r'<div class="form-row">(\s*<span class="form-label">(?:<span class="req">[^<]*</span>)?' + re.escape(lab) + r')</span>')
        n = len(pat.findall(t))
        assert n == 1, "%s %s 命中 %d" % (fp, lab, n)
        t = pat.sub(r'<div class="form-row g2">\1</span>', t, count=1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw = open(fp, "rb").read()
    print("PASS", fp.split("\\")[-1], "·CSS 块+g2×3·CRLF=%d 裸LF=%d" % (
        raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
