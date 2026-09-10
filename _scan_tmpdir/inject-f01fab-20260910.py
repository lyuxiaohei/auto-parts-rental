# -*- coding: utf-8 -*-
"""f01-fab 注入：每页右下角加「流程图」按钮，跳 F01 业务流程导航图（2026-09-10）
规则：
- 跳过 P3-R01-F01-业务流程导航图.html 自身；已有 f01-fab 跳过（幂等）
- 有 pn-fab（标注开关）的页：把最后一个 pn-fab 包进 .fab-row 并排容器
- 无 pn-fab 的页（含 弹窗/ 预览页）：</body> 前插独立 fixed 按钮（z-index 1001 避免被预览遮罩压住）
- 相对路径按深度：根=''，一层='../'，两层='../../'
"""
import pathlib, sys

ROOT = pathlib.Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
TARGET = 'P3-R01-F01-业务流程导航图.html'
SELF = ROOT / TARGET

STYLE_ROW = ('<style id="f01-fab-style">'
  '.fab-row{position:fixed;right:12px;bottom:12px;z-index:880;display:flex;align-items:center;gap:6px}'
  '.fab-row .pn-fab{position:static}'
  '.f01-fab{display:flex;align-items:center;height:24px;padding:0 10px;border-radius:4px;background:#fff;'
  'border:1px solid #d9d9d9;color:#8c8c8c;font-size:11px;'
  "font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;cursor:pointer;"
  'box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}'
  '.f01-fab:hover{opacity:1;border-color:#722ed1;color:#722ed1}'
  '</style>')

STYLE_SOLO = ('<style id="f01-fab-style">'
  '.f01-fab{position:fixed;right:12px;bottom:12px;z-index:1001;display:flex;align-items:center;'
  'height:24px;padding:0 10px;border-radius:4px;background:#fff;'
  'border:1px solid #d9d9d9;color:#8c8c8c;font-size:11px;'
  "font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;cursor:pointer;"
  'box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}'
  '.f01-fab:hover{opacity:1;border-color:#722ed1;color:#722ed1}'
  '</style>')

PNFAB = '<div class="pn-fab" id="protoNotesFab">标注</div>'

def fab(rel):
    return '<div class="f01-fab" onclick="location.href=\'%s\'">流程图</div>' % rel

changed, skipped_self, skipped_done = [], [], []
for f in sorted(ROOT.rglob('*.html')):
    if f == SELF:
        skipped_self.append(f)
        continue
    text = f.read_text(encoding='utf-8')
    if 'f01-fab' in text:
        skipped_done.append(f)
        continue
    depth = len(f.relative_to(ROOT).parts) - 1
    rel = '../' * depth + TARGET
    if PNFAB in text:
        # 只包最后一个 pn-fab（个别页面有游离重复片段，不动它）
        idx = text.rfind(PNFAB)
        new = (text[:idx] + STYLE_ROW
               + '<div class="fab-row">' + fab(rel) + PNFAB + '</div>'
               + text[idx + len(PNFAB):])
        mode = 'wrap'
    elif '</body>' in text:
        new = text.replace('</body>', STYLE_SOLO + '\n' + fab(rel) + '\n</body>', 1)
        mode = 'solo'
    else:
        print('NO-BODY-TAG 跳过:', f)
        continue
    f.write_text(new, encoding='utf-8', newline='')
    changed.append((mode, str(f.relative_to(ROOT))))

wrap = sum(1 for m, _ in changed if m == 'wrap')
solo = sum(1 for m, _ in changed if m == 'solo')
print('注入完成: 共 %d 页（并排 wrap=%d / 独立 solo=%d），跳过自身 %d，幂等跳过 %d'
      % (len(changed), wrap, solo, len(skipped_self), len(skipped_done)))
for m, p in changed:
    print(' ', m, p)
