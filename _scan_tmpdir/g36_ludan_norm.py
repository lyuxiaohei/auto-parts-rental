# -*- coding: utf-8 -*-
"""采购入库录单：按样板规范化（提交条居中 / 日期 / 控件宽 / 备注 / 卡头）"""
import io, os, re

FP = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\采购管理\采购入库录单.html'
s = io.open(FP, encoding='utf-8', newline='').read()
log = []

# 1) 提交条居中（规范：右对齐会与右下角 fab 打架）
old = '.submit-bar { position:fixed; left:208px; right:0; bottom:0; background:#fff; border-top:1px solid var(--border); padding:10px 24px; display:flex; justify-content:flex-end;'
new = old.replace('justify-content:flex-end', 'justify-content:center')
assert s.count(old) == 1
s = s.replace(old, new)
log.append('提交条 flex-end→center')

# 2) 自动生成字段改文本展示（样板惯例·避免 readonly 被审计判死）
old = '<div class="input-box" style="width:280px;"><input type="text" value="CGRK-20260831-007" placeholder="请输入"></div>'
new = '<div class="input-box" style="width:380px;background:#fafafa;"><span style="color:#8c8c8c;">CGRK-20260831-007（自动生成 · 不可编辑）</span></div>'
assert s.count(old) == 1
s = s.replace(old, new)
log.append('入库单号 → 文本展示 380px')

# 3) 到货日期 → type=date（保 value）
old = '<div class="input-box" style="width:180px;"><input type="text" value="2026-08-31" placeholder="请输入"></div>'
new = '<div class="input-box" style="width:380px;"><input type="date" value="2026-08-31"></div>'
assert s.count(old) == 1
s = s.replace(old, new)
log.append('到货日期 → type=date 380px')

# 4) 仓管员下拉 → 380px
old = '<div class="input-box select-box" style="width:180px;">'
assert s.count(old) == 1
s = s.replace(old, '<div class="input-box select-box" style="width:380px;">')
log.append('仓管员 → 380px')

# 5) 备注 → 样板 textarea（.input-box 外壳 + 72px + 顶部对齐）
old = '<div class="form-row">\r\n    <div class="form-label">备注：</div>\r\n    <div>\r\n      <div class="input-box" style="width:520px;"><input type="text" value="" placeholder="选填"></div>\r\n    </div>\r\n  </div>'
assert s.count(old) == 1, s.count(old)
new = ('<div class="form-row" style="align-items:flex-start;">\r\n'
       '    <div class="form-label" style="padding-top:6px;">备注：</div>\r\n'
       '    <div>\r\n'
       '      <div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea placeholder="选填" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea></div>\r\n'
       '    </div>\r\n  </div>')
s = s.replace(old, new)
log.append('备注 → textarea 样板形态 380px')

# 6) 随附信息卡头补 .card-head 包裹（样板写法）
old = '  <h3 class="card-title">随附信息</h3>'
assert s.count(old) == 1
s = s.replace(old, '  <div class="card-head">\r\n    <h3 class="card-title">随附信息</h3>\r\n  </div>')
log.append('随附信息 卡头 → .card-head 包裹')

# 7) 其余残留宽（若有）
rest = sorted(set(re.findall(r'class="input-box[^"]*"[^>]*style="width:(\d+)px', s)))
if rest != ['380']:
    log.append('!! 仍存宽度: %s' % rest)

io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('\n'.join('  ' + x for x in log))
