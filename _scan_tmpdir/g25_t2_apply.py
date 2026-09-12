# -*- coding: utf-8 -*-
"""G25 T2：stockFlows 末位插入租入态行（CRLF 保持）+ 库存查询筛选 option
键=RZRK-20260910-024（租入入库流水号格式）；fields.status=租入；500 只；上海一号库
"""
import io, re, sys, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
DD = ROOT + r"\_data\demo-data.js"
PG = ROOT + r"\仓储作业\库存查询.html"

# ---------- 1. demo-data.js 插入 ----------
txt = io.open(DD, encoding="utf-8", newline="").read()
NL = "\r\n" if txt.count("\r\n") > (txt.count("\n") - txt.count("\r\n")) else "\n"

anchor = ("      'timeline': [" + NL +
          "        {" + NL +
          "          't': '09-06'," + NL +
          "          'text': '客户安吉智行转租终端用户 · 360 只（客户转租出＝在租子状态）'," + NL +
          "          'who': '王琳'" + NL +
          "        }" + NL +
          "      ]" + NL +
          "    }," + NL + NL +
          "  },")
n = txt.count(anchor)
assert n == 1, "锚点命中 %d 次（预期 1）" % n

ENTRY_LINES = [
    "    'RZRK-20260910-024': {",
    "      'row': {\"fields\": {\"status\": \"租入\", \"name\": \"围板箱 1200×1000×970（路凯租入 · 在库未转租）\", \"cls\": \"租赁器具\", \"project\": \"PRJ-2603\", \"area\": \"上海一号库\"}, \"cells\": [\"围板箱 1200×1000×970（路凯租入）\", \"<span class=\\\"tag tag-blue\\\">租赁器具</span>\", \"PRJ-2603\", \"<span class=\\\"td-num\\\">500</span>\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\"><b>500</b></span>\", \"<span class=\\\"td-num\\\">340.00</span>\", \"只\", \"上海一号库\"], \"ops\": [{\"t\": \"库存流水\", \"detail\": true}]},",
    "      'title': '库存流水',",
    "      'titleNo': 'RZRK-20260910-024 围板箱（路凯租入 · 在库未转租）',",
    "      'info': [",
    "        {",
    "          'label': '物料编码',",
    "          'text': 'WBX-1210L'",
    "        },",
    "        {",
    "          'label': '名称规格',",
    "          'text': '围板箱 1200×1000×970（路凯租入）',",
    "          'full': true",
    "        },",
    "        {",
    "          'label': '物料类别',",
    "          'text': '租赁器具'",
    "        },",
    "        {",
    "          'label': '资产来源',",
    "          'tag': '租入'",
    "        },",
    "        {",
    "          'label': '供应商',",
    "          'text': '路凯包装运营（上海）有限公司',",
    "          'full': true",
    "        },",
    "        {",
    "          'label': '适用项目',",
    "          'text': 'PRJ-2603',",
    "          'full': true",
    "        },",
    "        {",
    "          'label': '在库（租入）',",
    "          'text': '500 只'",
    "        },",
    "        {",
    "          'label': '口径',",
    "          'text': '租入＝租入在库未转租，转租后计入客户态（来源标记区分）',",
    "          'full': true",
    "        },",
    "        {",
    "          'label': '库区',",
    "          'text': '上海一号库'",
    "        }",
    "      ],",
    "      'feeSecTitle': '进出流水（时间倒序）',",
    "      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],",
    "      'fees': [",
    "        {",
    "          'cells': ['09-10', '租入入库', 'RZRK-20260910-024', '+500', '500'],",
    "          'links': {",
    "            2: '租赁管理/租入入库列表.html'",
    "          }",
    "        }",
    "      ],",
    "      'chain': [",
    "        {",
    "          'role': '租入单',",
    "          'name': 'RZD-20260815-003 · 路凯',",
    "          'url': '租赁管理/租入单列表.html'",
    "        },",
    "        {",
    "          'role': '租入库批次（本批）',",
    "          'name': 'RZRK-20260910-024 · 上海一号库',",
    "          'self': true",
    "        },",
    "        {",
    "          'role': '转租客户（未发生）',",
    "          'name': '转租后计入客户态 · 来源标记区分'",
    "        }",
    "      ],",
    "      'timeline': [",
    "        {",
    "          't': '09-10',",
    "          'text': '租入入库 +500 · 路凯（在库未转租 · 计入租入态）',",
    "          'who': '张伟'",
    "        }",
    "      ]",
    "    }",
]
new_entry = NL.join(ENTRY_LINES)
replacement = anchor.replace("    }," + NL + NL + "  },",
                             "    }," + NL + NL + new_entry + "," + NL + NL + "  },")
txt = txt.replace(anchor, replacement)
io.open(DD, "w", encoding="utf-8", newline="").write(txt)

# 断言：键 1 次；stockFlows 段 status 租入 1 次；CRLF 不变
t2 = io.open(DD, encoding="utf-8", newline="").read()
i = t2.find("stockFlows: {")
seg = t2[i:t2.find("/* ----", i + 20)]
assert t2.count("'RZRK-20260910-024'") == 1, "键出现 %d 次" % t2.count("'RZRK-20260910-024'")
assert seg.count('"status": "租入"') == 1, "租入态 %d 次" % seg.count('"status": "租入"')
raw = open(DD, "rb").read()
print("PASS demo-data 插入：键 1 次·status 租入 1 次·CRLF=%d 裸LF=%d" % (
    raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))

# node --check
r = subprocess.run(["node", "--check", DD], capture_output=True, text=True)
print("PASS node --check" if r.returncode == 0 else "FAIL node --check: " + r.stderr[:300])
assert r.returncode == 0

# ---------- 2. 库存查询.html 筛选 option ----------
pg = io.open(PG, encoding="utf-8", newline="").read()
old = "<option>退租待入库</option></select>"
new = "<option>退租待入库</option><option>租入</option></select>"
assert pg.count(old) == 1, "option 锚点 %d 次" % pg.count(old)
pg = pg.replace(old, new)
io.open(PG, "w", encoding="utf-8", newline="").write(pg)
pg2 = io.open(PG, encoding="utf-8", newline="").read()
assert pg2.count("<option>租入</option>") == 1
raw = open(PG, "rb").read()
print("PASS 库存查询 option：<option>租入</option> 1 次·CRLF=%d 裸LF=%d" % (
    raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
print("T2 全部完成")
