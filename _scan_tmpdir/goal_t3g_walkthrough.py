# -*- coding: utf-8 -*-
"""
任务三g：租赁单编辑表单 Playwright 逐字段走查（P3-R04 P2 验证类）
- 打开 包装管理/租赁单列表.html → 首行「编辑」→ createModal
- 逐字段：聚焦 / 输入测试 / 恢复原值；select 逐项切换；行内明细 input 同测
- 结果写入 _scan_tmpdir/goal-t3g-walkthrough.md
"""
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\goal-t3g-walkthrough.md")
page_file = ROOT / "包装管理" / "租赁单列表.html"

JS = r"""
(() => {
  const modal = document.getElementById('createModal');
  const fields = [];
  // 表单行：label + 控件
  modal.querySelectorAll('.form-row').forEach((row, ri) => {
    const lab = (row.querySelector('.form-label')||{}).textContent || '';
    const label = lab.replace(/[*\s]/g, '');
    row.querySelectorAll('input, select').forEach(el => {
      fields.push({group:'form-row', label, tag: el.tagName.toLowerCase(), type: el.type||'', 
        value: el.value||'', options: el.tagName==='SELECT' ? [...el.options].map(o=>o.text) : null,
        disabled: el.disabled, readonly: el.readOnly, idx: fields.length});
    });
  });
  // 明细表内 input
  modal.querySelectorAll('table input').forEach(el => {
    const cell = el.closest('td');
    const hdr = [...modal.querySelectorAll('table thead th')][cell ? cell.cellIndex : -1];
    fields.push({group:'detail-tbl', label: hdr ? hdr.textContent.trim() : '?', tag:'input', type: el.type||'',
      value: el.value||'', options:null, disabled: el.disabled, readonly: el.readOnly, idx: fields.length});
  });
  return fields;
})()
"""

WALK = r"""
(fields => {
  const out = [];
  for (const f of fields) {
    const el = [...document.querySelectorAll('#createModal .form-row input, #createModal .form-row select, #createModal table input')][f.idx];
    if (!el) { out.push({...f, result:'元素丢失'}); continue; }
    if (f.disabled) { out.push({...f, result:'disabled（不可编辑）'}); continue; }
    if (f.readonly) { out.push({...f, result:'readonly（预填只读）'}); continue; }
    if (f.tag === 'select') {
      const orig = el.selectedIndex;
      let ok = true, seq = [];
      [...el.options].forEach((o, k) => { el.selectedIndex = k; seq.push(o.text.slice(0,12)); });
      el.selectedIndex = orig;
      out.push({...f, result:`切换 OK（${el.options.length} 项：${seq.join(' / ')}）`, restored: el.selectedIndex===orig});
      continue;
    }
    el.focus();
    const focused = document.activeElement === el;
    const old = el.value;
    el.value = old + '测';
    const typed = el.value !== old;
    el.value = old;
    const restored = el.value === old;
    out.push({...f, result: focused && typed && restored ? '聚焦+输入+还原 OK' : `异常 focus=${focused} type=${typed} restore=${restored}`});
  }
  return out;
})
"""

def main():
    results, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(page_file.as_uri())
        pg.wait_for_timeout(300)
        # 打开编辑弹窗（首行 编辑 按钮）
        pg.evaluate("() => { const a=[...document.querySelectorAll('.ops a')].find(x=>x.textContent.trim()==='编辑'); a.click(); }")
        pg.wait_for_timeout(200)
        shown = pg.evaluate("() => document.getElementById('createModal').classList.contains('show')")
        assert shown, "编辑弹窗未打开"
        fields = pg.evaluate(JS)
        results = pg.evaluate(WALK, fields)
        # 按钮排验：footer 按钮
        btns = pg.evaluate("""() => [...document.querySelectorAll('#createModal .modal-footer button')].map(b=>b.textContent.trim())""")
        b.close()
    lines = ["# 任务三g：租赁单编辑表单逐字段走查（2026-09-05）", "",
             f"- 页面：包装管理/租赁单列表.html → 首行「编辑」→ createModal 打开 {'✅' if shown else '❌'}",
             f"- JS 错误：{len(errors)} {errors if errors else ''}",
             f"- 字段总数：{len(results)}；footer 按钮：{' / '.join(btns)}", "",
             "| # | 区 | 字段 | 控件 | 预填值 | 走查结果 |", "|---|---|---|---|---|---|"]
    bad = 0
    for r in results:
        ok = 'OK' in r['result'] or 'readonly' in r['result'] or 'disabled' in r['result']
        if not ok: bad += 1
        v = (r['value'] or '')[:16]
        lines.append(f"| {r['idx']+1} | {r['group']} | {r['label'][:14]} | {r['tag']}{('/'+r['type']) if r['type'] and r['tag']=='input' else ''} | {v} | {r['result'][:80]} |")
    lines += ["", f"**结论：{'全部通过' if bad==0 else f'{bad} 个字段异常'}（聚焦/输入/还原三步 + select 逐项切换）**"]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-3:]))
    print(f"明细已写入 {OUT}")

if __name__ == "__main__":
    main()
