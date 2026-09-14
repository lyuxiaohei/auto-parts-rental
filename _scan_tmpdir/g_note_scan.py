# -*- coding: utf-8 -*-
"""G-备注普查：全站扫描「备注 form-row 位于明细区之后」的弹窗（双层：弹窗模板+业务页内嵌）
判据：文件内同时存在「XX明细</div>」段标题 与 备注 form-row，且备注位置在该明细标题对应的
      </table> 之后（即备注挂在明细区尾部）。
输出：候选清单+上下文证据（只读不改）。
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

SKIP_DIRS = {"backup-g25-20260912", "node_modules"}
cands = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith("backup")]
    parts = rel.split(os.sep)
    if "mobile" in parts or rel.startswith("backup"):
        continue
    for fn in sorted(filenames):
        if not fn.endswith(".html"):
            continue
        if fn.startswith(("P3-R01-F01", "P3-R01-A06")):
            continue
        fp = os.path.join(dirpath, fn)
        t = io.open(fp, encoding="utf-8", errors="replace", newline="").read()
        # 明细段标题（块级 div，非表头 th）
        det_titles = [m for m in re.finditer(r">([^<]{0,6}明细[^<]{0,10})</div>", t)]
        if not det_titles:
            continue
        note_rows = [m for m in re.finditer(r'<span class="form-label">备注</span>', t)]
        if not note_rows:
            continue
        # 表格闭合位置（供判断备注是否在某明细表格之后）
        for n in note_rows:
            # 该备注行前最近的明细标题
            prev_dets = [d for d in det_titles if d.start() < n.start()]
            if not prev_dets:
                continue
            d = prev_dets[-1]
            # 该明细标题之后、备注之前，是否存在 </table>（明细实体表）
            table_close = t.rfind("</table>", d.end(), n.start())
            if table_close < 0:
                continue
            # 确认备注行在表后（备注与表之间无新的明细标题）
            nxt_det = [x for x in det_titles if x.start() > table_close]
            if nxt_det:
                continue
            # 证据：备注前 90 字符（看是否粘接添加一行）+ 所在 modal id
            seg_before = t[max(0, n.start() - 110):n.start()].replace("\r", "").replace("\n", "⏎")
            modal_ids = re.findall(r'id="([A-Za-z]\w*[Mm]odal\w*)"', t[:n.start()])
            cands.append((os.path.relpath(fp, ROOT).replace(chr(92), "/"),
                          d.group(1).strip(), n.start(),
                          modal_ids[-1] if modal_ids else "?",
                          ("…粘接添加一行" if "添加一行</button><" in seg_before else "独立行"),
                          seg_before[-60:]))

print("候选（备注在明细表后）:", len(cands), "处")
for c in sorted(cands):
    print("  %s | 明细「%s」| modal=%s | %s" % (c[0], c[1], c[3], c[4]))
