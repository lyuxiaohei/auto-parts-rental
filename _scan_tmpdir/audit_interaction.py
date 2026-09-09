# -*- coding: utf-8 -*-
"""
P3-R01 原型全站交互体检（只读审计）
- 对 91 个 HTML 逐页 Playwright 实测：JS错误/按钮/链接/弹窗/radio/checkbox/select/input/页签
- 不修改任何原型文件；结果只写入 _scan_tmpdir/
用法: python audit_interaction.py [页面相对路径过滤串]
"""
import json, re, sys, traceback
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
OUT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
FILTER = sys.argv[1] if len(sys.argv) > 1 else ""

HARNESS = r"""
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const problems = [];
  let idxSeq = 0;
  const tested = new Set();

  // ---- 拦截导航 ----
  window.__navs = [];
  window.go = function (u) { window.__navs.push(String(u)); };

  // ---- 变化计数器 ----
  window.__mut = 0;
  new MutationObserver(muts => { window.__mut += muts.length; })
    .observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true });

  const shownModals = () => [...document.querySelectorAll('.modal-overlay.show')];
  const closeOne = m => {
    if (typeof window.closeModal === 'function' && m.id) window.closeModal(m.id);
    else m.classList.remove('show');
  };
  const closeAllModals = () => shownModals().forEach(closeOne);
  // 加载时默认打开的弹窗（演示页）——清扫过程中保持打开
  const initialShown = new Set(shownModals());
  // 关闭 exclude 之外新出现的弹窗，恢复基准态
  const closeNewModals = exclude => shownModals().forEach(m => { if (!exclude.has(m)) closeOne(m); });

  const visible = el => {
    if (!el.isConnected) return false;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };

  const describe = el => {
    const txt = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 20);
    const row = el.closest('tr');
    let rowKey = '';
    if (row && row.cells.length) {
      for (const c of row.cells) {
        if (c.contains(el)) continue; // 跳过操作列自身
        const t = (c.textContent || '').replace(/\s+/g, ' ').trim();
        if (t) { rowKey = t.slice(0, 16); break; }
      }
    }
    const modal = el.closest('.modal-overlay');
    return {
      tag: el.tagName.toLowerCase(),
      id: el.id || '',
      cls: (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className || '').toString().slice(0, 60),
      text: txt || el.getAttribute('title') || el.getAttribute('aria-label') || '',
      row: rowKey,
      inModal: modal ? (modal.id || (modal.querySelector('.modal-title') || {}).textContent || '').toString().trim().slice(0, 16) : ''
    };
  };

  const snapSelf = el => el.className + '|' + (el.getAttribute('aria-expanded') || '') + '|' + (el.getAttribute('checked') || '');

  // SVG 元素没有 .click()，统一走事件派发
  const fireClick = el => {
    if (typeof el.click === 'function') el.click();
    else el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
  };

  // 点击并判定是否有反馈
  async function clickFeedback(el) {
    await sleep(80);            // 静置：排空上一次操作的异步残留 mutation
    const navBefore = window.__navs.length;
    window.__mut = 0;
    const shownBefore = shownModals().length;
    const selfBefore = snapSelf(el);
    try { fireClick(el); } catch (e) { return { error: String(e) }; }
    await sleep(60);
    return {
      navs: window.__navs.length - navBefore,
      mut: window.__mut,
      modalDelta: shownModals().length - shownBefore,
      selfChanged: snapSelf(el) !== selfBefore,
      navTarget: window.__navs[window.__navs.length - 1] || null
    };
  }
  const hasFeedback = fb => fb && !fb.error && (fb.navs > 0 || fb.mut > 0 || fb.modalDelta !== 0 || fb.selfChanged);

  // ---- 可点击元素清扫：button / a / .sm-link / [onclick] ----
  // reopen：弹窗内清扫时，若所在弹窗被点关（如点了取消），重开以继续测后续元素
  async function sweepClickables(scope, phase, reopen) {
    const scopeOv = scope.classList && scope.classList.contains('modal-overlay') ? scope : null;
    const els = [...scope.querySelectorAll('button, a, .sm-link, [onclick]')];
    for (const el of els) {
      if (tested.has(el)) continue;
      const d = describe(el);
      // 真链接（HTML 或 SVG 命名空间）不点击，由 Python 静态校验目标存在
      const href = d.tag === 'a' ? (el.getAttribute('href') || el.getAttribute('xlink:href')) : null;
      if (href && href !== '#' && !/^javascript:/i.test(href)) { tested.add(el); continue; }
      if (el.disabled) { tested.add(el); continue; }
      if (!visible(el)) continue;
      tested.add(el);
      const fb = await clickFeedback(el);
      if (!hasFeedback(fb)) {
        problems.push({ cat: '按钮', type: 'dead-button', phase, where: d, detail: '点击后无任何反馈（无弹窗/跳转/视觉态变化）' });
      }
      // 恢复基准态：关掉新开的弹窗（保留演示页默认弹窗/当前清扫弹窗）
      const keep = new Set([...initialShown]); if (scopeOv) keep.add(scopeOv);
      closeNewModals(keep);
      if (reopen && scopeOv && !scopeOv.classList.contains('show')) await reopen();
    }
  }

  // ---- radio / checkbox 视觉态 ----
  async function sweepRadioCheckbox(scope, phase) {
    for (const el of [...scope.querySelectorAll('.radio, .checkbox')]) {
      if (tested.has(el)) continue;
      if (!visible(el)) continue;
      tested.add(el);
      const d = describe(el);
      const isRadio = el.classList.contains('radio');
      if (isRadio) {
        if (el.classList.contains('checked')) continue; // 默认选中项：再点自身无变化属正常
        const hadChecked = el.parentElement.querySelector('.radio.checked');
        fireClick(el);
        await sleep(20);
        const selfOn = el.classList.contains('checked');
        const otherOff = !hadChecked || !hadChecked.classList.contains('checked');
        if (!selfOn || !otherOff) {
          problems.push({ cat: '弹窗', type: 'radio-no-visual', phase, where: d, detail: '点击后未选中自身或未取消同组原选中' });
        }
      } else {
        const before = el.classList.contains('checked');
        fireClick(el);
        await sleep(20);
        const after = el.classList.contains('checked');
        if (after === before) {
          problems.push({ cat: '弹窗', type: 'checkbox-no-visual', phase, where: d, detail: '点击后 checked 视觉态未翻转' });
        }
        fireClick(el); // 还原
        await sleep(10);
      }
    }
  }

  // ---- 输入框 ----
  function sweepInputs(scope, phase) {
    const sel = 'input:not([type=checkbox]):not([type=radio]):not([type=button]):not([type=submit]):not([type=reset]):not([type=hidden]):not([type=file]), textarea';
    for (const el of [...scope.querySelectorAll(sel)]) {
      if (tested.has(el)) continue;
      if (!visible(el)) continue;
      tested.add(el);
      const d = describe(el);
      if (el.disabled || el.readOnly) {
        problems.push({ cat: '输入框', type: 'input-not-editable', phase, where: d, detail: el.disabled ? 'disabled 不可输入' : 'readonly 不可输入' + (el.value ? '（预填:' + String(el.value).slice(0, 12) + '）' : '') });
        continue;
      }
      try { el.focus(); } catch (e) {}
      const okFocus = document.activeElement === el;
      const old = el.value;
      el.value = old + 'T';
      const okType = el.value !== old;
      el.value = old;
      if (!okFocus || !okType) {
        problems.push({ cat: '输入框', type: 'input-dead', phase, where: d, detail: !okFocus ? '无法聚焦' : '无法输入' });
      }
      if (!el.placeholder && !el.value) {
        problems.push({ cat: '输入框', type: 'input-no-placeholder', phase, where: d, detail: '无 placeholder 且无预填值' });
      }
    }
  }

  // ---- 页签 ----
  async function sweepTabs(phase) {
    for (const t of [...document.querySelectorAll('.stab')]) {
      if (!visible(t)) continue;
      const d = describe(t);
      fireClick(t);
      await sleep(20);
      if (!t.classList.contains('active')) {
        problems.push({ cat: '页签', type: 'stab-no-active', phase, where: d, detail: '点击后未获得 active 选中态' });
      }
    }
    for (const t of [...document.querySelectorAll('.tab')]) {
      if (!visible(t)) continue;
      const d = describe(t);
      const navBefore = window.__navs.length;
      fireClick(t);
      await sleep(20);
      if (!t.classList.contains('active') && window.__navs.length === navBefore) {
        problems.push({ cat: '页签', type: 'tab-no-active', phase, where: d, detail: '点击后无 active 选中态且无跳转' });
      }
    }
  }

  // ---- 弹窗 ----
  async function sweepModals() {
    const overlays = [...document.querySelectorAll('.modal-overlay')];
    const results = [];
    for (const ov of overlays) {
      const mid = ov.id || '(无id)';
      const title = ((ov.querySelector('.modal-title') || {}).textContent || '').trim().slice(0, 20) || mid;
      // 找页内触发器
      let trigger = null, scriptOpen = false;
      if (ov.id) {
        trigger = [...document.querySelectorAll('[onclick]')].find(el => {
          const oc = el.getAttribute('onclick') || '';
          return oc.includes("openModal('" + ov.id + "')") || oc.includes('openModal("' + ov.id + '")');
        });
        // 数据驱动包装器触达（openRolePerm/openGenericDetail 等包装函数内调用 openModal）：
        // 页内脚本含 openModal('id') 字面调用即视为可达，清扫走 window.openModal 兜底（2026-09-09 G01）
        if (!trigger) {
          const html = document.documentElement.innerHTML;
          scriptOpen = html.includes("openModal('" + ov.id + "')") || html.includes('openModal("' + ov.id + '")');
        }
      }
      const openVia = async () => {
        if (trigger) { fireClick(trigger); await sleep(30); }
        else if (typeof window.openModal === 'function' && ov.id) { window.openModal(ov.id); await sleep(30); }
        return ov.classList.contains('show');
      };
      const closeVia = async () => { if (typeof window.closeModal === 'function' && ov.id) window.closeModal(ov.id); else ov.classList.remove('show'); await sleep(20); };

      if (trigger) {
        const fb = await clickFeedback(trigger);
        if (!ov.classList.contains('show')) {
          problems.push({ cat: '弹窗', type: 'modal-open-fail', phase: 'modal', where: { text: title, id: mid }, detail: '点击触发器后弹窗未出现' });
          continue;
        }
        await sweepRadioCheckbox(ov, 'modal');
        sweepInputs(ov, 'modal');
        await sweepClickables(ov, 'modal', openVia);
        // ---- 关闭路径1：× ----
        await openVia();
        const x = ov.querySelector('.modal-close');
        if (!x) problems.push({ cat: '弹窗', type: 'modal-no-close-x', phase: 'modal', where: { text: title }, detail: '缺少右上角 × 关闭按钮' });
        else { fireClick(x); await sleep(30); if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-x-not-close', phase: 'modal', where: { text: title }, detail: '点 × 后弹窗未关闭' }); }
        // ---- 关闭路径2：footer 取消/关闭 ----
        const reopened = await openVia();
        const cancelBtn = [...ov.querySelectorAll('.modal-footer button, .modal-footer a, .modal-footer .btn')].find(b => /取\s*消|关\s*闭|返\s*回/.test(b.textContent || ''));
        if (!cancelBtn) problems.push({ cat: '弹窗', type: 'modal-no-cancel-btn', phase: 'modal', where: { text: title }, detail: 'footer 无 取消/关闭 按钮' });
        else { fireClick(cancelBtn); await sleep(30); if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-cancel-not-close', phase: 'modal', where: { text: title, text2: (cancelBtn.textContent || '').trim() }, detail: '点取消按钮后弹窗未关闭' }); }
        // ---- 关闭路径3：遮罩 ----
        if (await openVia()) {
          fireClick(ov); await sleep(30); // JS click 的 target 即 overlay 自身
          if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-overlay-not-close', phase: 'modal', where: { text: title }, detail: '点遮罩后弹窗未关闭' });
        } else if (!reopened) {
          problems.push({ cat: '弹窗', type: 'modal-reopen-untested', phase: 'modal', where: { text: title }, detail: '关闭后无法重开，遮罩关闭路径未测全' });
        }
        await closeVia();
        results.push(title);
      } else {
        // 无页内触发器：独立演示页（默认已开）/ 包装器触达（scriptOpen）或死弹窗
        if (!initialShown.has(ov) && !scriptOpen) {
          problems.push({ cat: '弹窗', type: 'modal-unreachable', phase: 'modal', where: { text: title }, detail: '页内无 openModal 触发器且默认未打开（不可达弹窗）' });
          continue;
        }
        await sweepRadioCheckbox(ov, 'modal');
        sweepInputs(ov, 'modal');
        await sweepClickables(ov, 'modal', openVia);
        if (!ov.classList.contains('show')) await openVia();
        const x = ov.querySelector('.modal-close');
        if (!x) problems.push({ cat: '弹窗', type: 'modal-no-close-x', phase: 'modal', where: { text: title }, detail: '缺少右上角 × 关闭按钮' });
        else { fireClick(x); await sleep(30); if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-x-not-close', phase: 'modal', where: { text: title }, detail: '点 × 后弹窗未关闭' }); }
        // 能重开则补测 取消/遮罩 两条关闭路径
        if (await openVia()) {
          const cancelBtn = [...ov.querySelectorAll('.modal-footer button, .modal-footer a, .modal-footer .btn')].find(b => /取\s*消|关\s*闭|返\s*回/.test(b.textContent || ''));
          if (cancelBtn) { fireClick(cancelBtn); await sleep(30); if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-cancel-not-close', phase: 'modal', where: { text: title }, detail: '点取消按钮后弹窗未关闭' }); }
          if (await openVia()) { fireClick(ov); await sleep(30); if (ov.classList.contains('show')) problems.push({ cat: '弹窗', type: 'modal-overlay-not-close', phase: 'modal', where: { text: title }, detail: '点遮罩后弹窗未关闭' }); }
        }
        await closeVia();
        results.push(title + '(演示页)');
      }
    }
    return results;
  }

  // ---- 静态收集：select / 假下拉 / 链接目标 ----
  function staticCollect() {
    const selects = [...document.querySelectorAll('select')].map(s => {
      const d = describe(s);
      return { where: d, options: s.options.length, disabled: !!s.disabled, firstOpts: [...s.options].slice(0, 3).map(o => (o.textContent || '').trim()) };
    });
    for (const s of [...document.querySelectorAll('select')]) {
      const d = describe(s);
      if (s.options.length < 2) problems.push({ cat: '下拉框', type: 'select-few-options', phase: 'static', where: d, detail: '选项数 ' + s.options.length + '（<2）' });
      if (s.disabled) problems.push({ cat: '下拉框', type: 'select-disabled', phase: 'static', where: d, detail: 'select 处于 disabled' });
    }
    // 假下拉：div.select-box 不含真 select
    const fakeBoxes = [...document.querySelectorAll('.select-box')].filter(b => !b.querySelector('select'));
    for (const b of fakeBoxes) {
      const d = describe(b);
      problems.push({ cat: '下拉框', type: 'select-box-fake', phase: 'static', where: d, detail: '假下拉（div.select-box+input，无 <select> 无选项列表，点击无下拉）' });
    }
    // 链接目标收集（Python 校验存在性）
    const targets = [];
    for (const el of document.querySelectorAll('[onclick]')) {
      const oc = el.getAttribute('onclick') || '';
      const m = oc.match(/go\(\s*['"]([^'"]+)['"]\s*\)/) || oc.match(/location\.href\s*=\s*['"]([^'"]+)['"]/);
      if (m) targets.push(m[1]);
    }
    for (const a of document.querySelectorAll('a[href]')) {
      const h = a.getAttribute('href');
      if (h && h !== '#' && !/^javascript:/i.test(h)) targets.push(h);
    }
    return { selects, fakeBoxes: fakeBoxes.length, targets: [...new Set(targets)] };
  }

  // ================= 主流程 =================
  const st = staticCollect();
  // 背景mutation探针：静置150ms统计页面自发的DOM变化（>0 说明有定时器在改DOM，mut信号不可靠）
  window.__mut = 0; await sleep(150); const bgMut = window.__mut;
  await sweepClickables(document, 'base');
  await sweepRadioCheckbox(document, 'base');
  sweepInputs(document, 'base');
  await sweepTabs('base');
  const modalTitles = await sweepModals();
  closeAllModals();

  return {
    problems,
    stats: {
      buttons: document.querySelectorAll('button').length,
      links: document.querySelectorAll('a').length,
      onclickEls: document.querySelectorAll('[onclick]').length,
      modals: document.querySelectorAll('.modal-overlay').length,
      modalTitles,
      selects: st.selects.length,
      fakeSelects: st.fakeBoxes,
      radios: document.querySelectorAll('.radio').length,
      checkboxes: document.querySelectorAll('.checkbox').length,
      inputs: document.querySelectorAll('input, textarea').length,
      stabs: document.querySelectorAll('.stab').length,
      tabs: document.querySelectorAll('.tab').length,
      bgMut
    },
    linkTargets: st.targets
  };
})
"""

def check_dead_links(page_path: Path, targets):
    """相对目标解析到文件，校验存在性"""
    dead = []
    for t in targets:
        if re.match(r"^(https?:|mailto:|tel:)", t) or t.startswith("#"):
            continue
        t = unquote(t.split("#")[0].split("?")[0])
        if not t:
            continue
        cand = (page_path.parent / t).resolve()
        try:
            cand.relative_to(ROOT.resolve())
        except ValueError:
            dead.append((t, "越界路径"))
            continue
        if not cand.exists():
            dead.append((t, "目标文件不存在"))
    return dead

def audit_page(browser, path: Path):
    r = {"page": str(path.relative_to(ROOT)), "js_errors": [], "problems": [], "stats": {}, "dead_links": [], "nav_anomaly": None}
    page = browser.new_page()
    page.on("console", lambda m: r["js_errors"].append({"type": m.type, "text": m.text[:200]}) if m.type == "error" else None)
    page.on("pageerror", lambda e: r["js_errors"].append({"type": "pageerror", "text": str(e)[:200]}))
    url_before = [None]
    page.on("framenavigated", lambda f: url_before.__setitem__(0, f.url) if f == page.main_frame else None)
    try:
        page.goto(path.as_uri(), wait_until="load", timeout=15000)
        # 列表数据驱动适配（2026-09-08 试点）：动态渲染行需等待 tbody 出现；无 tbody 页静默跳过
        try:
            page.wait_for_selector('tbody tr', timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(300)
        res = page.evaluate(HARNESS)
        r["problems"] = res["problems"]
        r["stats"] = res["stats"]
        r["dead_links"] = check_dead_links(path, res["linkTargets"])
        if url_before[0] and unquote(url_before[0]) != unquote(path.as_uri()):
            r["nav_anomaly"] = url_before[0]
    except Exception as e:
        r["audit_error"] = f"{type(e).__name__}: {str(e)[:300]}"
    finally:
        page.close()
    return r

def main():
    pages = sorted(p for p in ROOT.rglob("*.html"))
    if FILTER:
        pages = [p for p in pages if FILTER in str(p)]
    print(f"共 {len(pages)} 页待审计")
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for i, p in enumerate(pages, 1):
            r = audit_page(browser, p)
            results.append(r)
            n_err = len([e for e in r["js_errors"]])
            print(f"[{i}/{len(pages)}] {r['page']}  问题:{len(r['problems'])} 死链:{len(r['dead_links'])} JS错:{n_err}" + (f" 审计异常:{r.get('audit_error','')[:80]}" if r.get("audit_error") else ""))
        browser.close()
    outf = OUT / ("audit_results_sample.json" if FILTER else "audit_results.json")
    outf.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n结果已写入 {outf}")

if __name__ == "__main__":
    main()
