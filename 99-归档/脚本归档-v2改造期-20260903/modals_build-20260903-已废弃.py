#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃·禁止运行（双版本之一，同上）
# 说明：双版本之一（P3-R01内份，20260903 12:44，含标注层注入顺序修复）。
#       另一份（根目录份，12:16）归档时同名互覆丢失，两份均已废弃无实质影响。
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""
弹窗构建脚本：将 弹窗/ 文件夹中的模板注入到引用它的页面中。
用法: python _build/modals_build.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent  # 原型根目录

# 弹窗 CSS（如果页面缺少）
MODAL_CSS = '''
<style id="modal-css">
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:1000;align-items:center;justify-content:center}
.modal-overlay.show{display:flex}
.modal{background:#fff;border-radius:8px;width:480px;max-width:90vw;max-height:85vh;overflow-y:auto;box-shadow:0 4px 20px rgba(0,0,0,.15)}
.modal-lg{width:680px}
.modal-header{padding:16px 24px;border-bottom:1px solid #f0f0f0;display:flex;justify-content:space-between;align-items:center}
.modal-title{font-size:16px;font-weight:600;color:#262626}
.modal-close{cursor:pointer;font-size:20px;color:#8c8c8c;line-height:1}
.modal-close:hover{color:#262626}
.modal-body{padding:20px 24px}
.modal-footer{padding:12px 24px;border-top:1px solid #f0f0f0;display:flex;justify-content:flex-end;gap:8px}
</style>
'''

# 弹窗 JS（如果页面缺少）
MODAL_JS = '''
<script id="modal-js">
function openModal(id){document.getElementById(id).classList.add('show')}
function closeModal(id){document.getElementById(id).classList.remove('show')}
document.addEventListener('click',function(e){
  var t=e.target;
  if(t.classList&&t.classList.contains('modal-close')){var m=t.closest('.modal-overlay');if(m)m.classList.remove('show')}
  if(t.classList&&t.classList.contains('modal-overlay')){t.classList.remove('show')}
});
</script>
'''

def strip_template_comments(content):
    """去除模板文件头部的注释行"""
    lines = content.split('\n')
    while lines and lines[0].strip().startswith('<!--'):
        lines.pop(0)
    return '\n'.join(lines)

def main():
    # 1. 收集所有弹窗模板
    templates = {}  # {注入目标页面路径: [弹窗HTML内容]}
    for tmpl in sorted(ROOT.rglob('弹窗/*.html')):
        content = tmpl.read_text(encoding='utf-8')
        content = strip_template_comments(content)
        # 提取注入标记
        m = re.search(r'注入标记[：:]\s*(.+?)(?:\s*$|\n)', content) or re.search(r'<!--\s*注入标记[：:]\s*(.+?)\s*-->', tmpl.read_text(encoding='utf-8'))
        if not m:
            # 尝试从原始文件（未剥离注释）中提取
            raw = tmpl.read_text(encoding='utf-8')
            m = re.search(r'注入标记[：:]\s*(.+)', raw)
        if m:
            target = m.group(1).strip()
            # 去除可能的HTML注释尾部
            target = re.sub(r'\s*-->\s*$', '', target)
            templates.setdefault(target, []).append(content)
        else:
            print(f"  ⚠️ 模板无注入标记: {tmpl.as_posix()}")

    print(f"收集到 {sum(len(v) for v in templates.values())} 个弹窗模板，涉及 {len(templates)} 个目标页面")

    # 2. 注入到页面
    injected = 0
    replaced = 0
    skipped = 0
    for target_path, modal_list in sorted(templates.items()):
        page = ROOT / target_path
        if not page.exists():
            print(f"  ❌ 目标页面不存在: {target_path}")
            continue

        html = page.read_text(encoding='utf-8')

        for modal_html in modal_list:
            # 提取弹窗 id
            mid = re.search(r'id="([^"]+)"', modal_html)
            if not mid:
                print(f"  ⚠️ 弹窗无 id，跳过: {target_path}")
                skipped += 1
                continue
            modal_id = mid.group(1)

            # 检查页面是否已有该弹窗
            existing = re.search(
                rf'<div[^>]*class="modal-overlay[^"]*"[^>]*id="{modal_id}"[^>]*>.*?</div>\s*</div>\s*</div>',
                html, re.S
            )
            if existing:
                # 替换已有弹窗（模板优先）
                html = html[:existing.start()] + modal_html + html[existing.end():]
                replaced += 1
            else:
                # 注入新弹窗（在 </body> 前的已有 script 之前）
                inject_pos = html.find('</body>')
                if inject_pos == -1:
                    inject_pos = len(html)
                html = html[:inject_pos] + '\n' + modal_html + '\n' + html[inject_pos:]
                injected += 1

        # 检查是否需要补 CSS
        if 'modal-overlay' in html and 'modal-css' not in html:
            inject_pos = html.find('</head>')
            if inject_pos == -1: inject_pos = html.find('</body>')
            html = html[:inject_pos] + MODAL_CSS + html[inject_pos:]

        # 检查是否需要补 JS
        if "openModal(" in html and 'function openModal' not in html:
            inject_pos = html.find('</body>')
            html = html[:inject_pos] + MODAL_JS + '\n' + html[inject_pos:]
        elif 'modal-overlay' in html and 'closeModal' not in html:
            inject_pos = html.find('</body>')
            html = html[:inject_pos] + MODAL_JS + '\n' + html[inject_pos:]

        page.write_text(html, encoding='utf-8')

    print(f"\n注入完成: 新增={injected} 替换={replaced} 跳过={skipped}")

    # 3. 验证
    print("\n=== 验证 ===")
    ghost = 0
    orphan = 0
    biz_pages = [p for p in ROOT.rglob('*.html')
                 if 'F01' not in p.name and 'A02' not in p.name and 'A03' not in p.name
                 and '弹窗' not in str(p) and '_build' not in str(p)]
    for p in biz_pages:
        h = p.read_text(encoding='utf-8')
        cut = h.find('<div id="proto-pins"')
        zone = h[:cut] if cut > 0 else h
        opens = set(re.findall(r"openModal\('([^']+)'\)", zone))
        modals = set(re.findall(r'<div[^>]*class="modal-overlay[^"]*"[^>]*id="([^"]+)"', zone))
        dangling = opens - modals
        unused_m = modals - opens
        if dangling:
            print(f"  ❌ 幽灵: {p.name} → {dangling}")
            ghost += len(dangling)
        if unused_m:
            print(f"  ⚠️ 未引用: {p.name} → {unused_m}")
            orphan += len(unused_m)

    print(f"幽灵引用: {ghost} | 未引用弹窗: {orphan}")

if __name__ == '__main__':
    main()
