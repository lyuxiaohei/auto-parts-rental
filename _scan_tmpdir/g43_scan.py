# -*- coding: utf-8 -*-
"""
G43 T0 差集重扫（只读）：Playwright 遍历全 PC 页，采集每个 select 的
id / 上下文(筛选·弹窗表单·页面) / label / 运行时 option 文本 / 静态 HTML option，
产出 g43_scan_raw.json + g43_接线差集_v2.md 底表（分类由人工/后处理定）。
用法: python3 g43_scan.py
"""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"
OUT = Path(__file__).resolve().parent

pages = sorted(
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*.html")
    if "mobile/" not in p.relative_to(ROOT).as_posix()
)

JS = r"""
(() => {
  const out = [];
  document.querySelectorAll('select').forEach((s, i) => {
    const ctx = s.closest('.modal-overlay') ? '弹窗' : (s.closest('.filter-bar, .ff-wrap, .ff-row') || s.closest('.ff') ? '筛选' : '页面');
    // label 探测：ff-label / form-row 首子文本 / 前置兄弟
    let label = '';
    const ff = s.closest('.ff');
    if (ff) { const l = ff.querySelector('.ff-label'); if (l) label = l.textContent.trim(); }
    if (!label) {
      const fr = s.closest('.form-row, .form-grid .row, .fm-row');
      if (fr) {
        const kids = [...fr.children].filter(c => c !== s && !c.contains(s));
        for (const k of kids) { const t = k.textContent.replace(/\s+/g, ' ').trim(); if (t) { label = t.slice(0, 24); break; } }
      }
    }
    if (!label) {
      let p = s.previousElementSibling;
      while (p && !label) { const t = (p.textContent || '').replace(/\s+/g, ' ').trim(); if (t) label = t.slice(0, 24); else p = p.previousElementSibling; }
    }
    const opts = [...s.options].map(o => (o.textContent || '').replace(/\s+/g, ' ').trim());
    out.push({
      idx: i, id: s.id || '', ctx, label,
      cls: (s.className || '').trim(),
      opts
    });
  });
  return out;
})()
"""

def static_opts(html, sel_id, nth):
    """从原始 HTML 抓第 nth 个 select 块的静态 option 文本。"""
    # 抓所有 <select ...>...</select> 块（非贪婪）
    blocks = re.findall(r"<select\b[^>]*>.*?</select>", html, re.S)
    if nth >= len(blocks):
        return None
    b = blocks[nth]
    return [re.sub(r"<[^>]+>", "", o).strip() for o in re.findall(r"<option\b[^>]*>(.*?)</option>", b, re.S)]

rows = []
with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    pg = br.new_page()
    pg.on("pageerror", lambda e: None)  # 演示页容忍报错
    for rel in pages:
        f = ROOT / rel
        try:
            pg.goto(f.as_uri(), wait_until="load", timeout=15000)
            pg.wait_for_timeout(250)
            sels = pg.evaluate(JS)
        except Exception as e:
            rows.append({"page": rel, "error": str(e)[:120]})
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        static_sel_count = len(re.findall(r"<select\b[^>]*>", html))
        for s in sels:
            st = static_opts(html, s["id"], s["idx"]) if s["idx"] < static_sel_count else None
            rows.append({
                "page": rel, "id": s["id"], "ctx": s["ctx"], "label": s["label"],
                "runtime_opts": s["opts"], "static_opts": st,
            })
    br.close()

(OUT / "g43_scan_raw.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
n_sel = sum(1 for r in rows if "error" not in r)
print(f"pages={len(pages)} rows={len(rows)} selects={n_sel} err={sum(1 for r in rows if 'error' in r)}")
