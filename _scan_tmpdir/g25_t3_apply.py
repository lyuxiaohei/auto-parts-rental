# -*- coding: utf-8 -*-
"""G25 T3：receivableBills 末位插入 供应商应收演示行（CRLF 保持）
键=AR-2026-09-PRJ2601-SUP；btype=供应商应收；路凯赔付 18600；未收款；手动建单形态
"""
import io, re, sys, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
DD = ROOT + r"\_data\demo-data.js"

txt = io.open(DD, encoding="utf-8", newline="").read()
NL = "\r\n"

anchor = ("      timeline: [" + NL +
          "        { t: '09-08', text: '按客户对账量录入生成 · 数量×单价（46,600 × 4.00）', who: '王芳' }," + NL +
          "        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }" + NL +
          "      ]" + NL +
          "    }," + NL + NL +
          "  },")
n = txt.count(anchor)
assert n == 1, "锚点命中 %d 次（预期 1）" % n

ENTRY_LINES = [
    "    /* ===== 供应商应收（路凯赔付我方 · 租入器具损坏 · 手动建单，2026-09-12 G25 R-01） ===== */",
    "    'AR-2026-09-PRJ2601-SUP': {",
    "      'row': {\"fields\": {\"period\": \"2026-09\", \"project\": \"PRJ-2601\", \"customer\": \"路凯包装运营（上海）有限公司\", \"btype\": \"供应商应收\", \"docs\": \"—（无关联单据 · 手动建单）\", \"gen\": \"手动建单\", \"date\": \"2026-09-10\", \"status\": \"未收款\"}, \"cells\": [\"2026-09\", \"PRJ-2601\", \"路凯包装运营（上海）有限公司\", \"供应商应收\", \"—（无关联单据 · 手动建单）\", \"<span class=\\\"td-num\\\"><b>18,600.00</b></span>\", \"<span class=\\\"td-num\\\">0.00</span>\", \"<span class=\\\"tag tag-red\\\">未收款</span>\", \"<span class=\\\"tag tag-blue\\\">手动建单</span>\", \"2026-09-10 15:40\"], \"ops\": [{\"t\": \"账单确认\", \"act\": \"openModal('auditModal')\"}, {\"t\": \"详情\", \"detail\": true}, {\"t\": \"开票\", \"act\": \"go('../财务协同/开票登记.html')\"}, {\"t\": \"核销\", \"act\": \"go('../财务协同/银行水单核销.html')\"}]},",
    "      billNo: 'AR-2026-09-PRJ2601-SUP',",
    "      billType: '供应商应收',",
    "      status: '未收款',",
    "      customer: '路凯包装运营（上海）有限公司',",
    "      project: 'PRJ-2601',",
    "      period: '2026-09',",
    "      amount: 18600,",
    "      verified: 0,",
    "      genMode: '手动建单（无关联单据 · 手填金额）',",
    "      genDate: '2026-09-10',",
    "      feeType: '丢损缺损赔偿（供应商赔付我方）',",
    "      scenario: 'S5 · 供应商赔付转应收',",
    "      fees: [",
    "        { src: '—（手动建单）', desc: '租入器具丢损缺损赔偿 · 供应商赔付我方（路凯）', qty: '—', price: '—', amount: 18600 }",
    "      ],",
    "      chain: [",
    "        { role: '供应商赔付确认', name: '路凯 · 租入器具损坏' },",
    "        { role: '应收账单（本单）', name: 'AR-2026-09-PRJ2601-SUP · 供应商应收', self: true },",
    "        { role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' },",
    "        { role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }",
    "      ],",
    "      timeline: [",
    "        { t: '09-10', text: '供应商赔付确认 · 租入器具丢损缺损 18,600 元（路凯）', who: '王芳' },",
    "        { t: '09-10', text: '手动建单生成供应商应收（无关联单据 · 手填金额）', who: '王芳' },",
    "        { t: '—', text: '待开票 → 回款 → 水单核销', off: true }",
    "      ]",
    "    }",
]
new_entry = NL.join(ENTRY_LINES)
replacement = anchor.replace("    }," + NL + NL + "  },",
                             "    }," + NL + NL + new_entry + "," + NL + NL + "  },")
txt = txt.replace(anchor, replacement)
io.open(DD, "w", encoding="utf-8", newline="").write(txt)

# 断言
t2 = io.open(DD, encoding="utf-8", newline="").read()
m = re.search(r"^  receivableBills: \{", t2, re.M)
seg = t2[m.start():t2.find("\n  /* ----", m.start())]
assert seg.count("'AR-2026-09-PRJ2601-SUP': {") == 1, "键声明非 1"
assert seg.count("billNo: 'AR-2026-09-PRJ2601-SUP'") == 1
assert seg.count('"btype": "供应商应收"') == 1, "btype 供应商应收非 1"
assert seg.count("供应商赔付确认") == 2, "供应商赔付确认应 2 处（chain+timeline），实际 %d" % seg.count("供应商赔付确认")
r = subprocess.run(["node", "--check", DD], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:300]
raw = open(DD, "rb").read()
print("PASS demo-data T3 插入：键 1·btype 1·赔付确认 2·node --check 0·CRLF=%d 裸LF=%d" % (
    raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
print("receivableBills 行数：14 → 15（含 row 字段键）")
