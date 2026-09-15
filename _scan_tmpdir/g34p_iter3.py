# -*- coding: utf-8 -*-
"""G34 试点迭代 3：备注并入表单区末尾 + 改文本域

依据：项目既有惯例（G31「弹窗备注行上移普查」——备注统一在表单区末尾·明细段之前）；
      textarea 写法沿用 租赁管理/退租入库列表.html 的「.input-box 内嵌 textarea」形态（复用表单体系样式）。
"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
N_P = os.path.join(ROOT, r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html')

N = io.open(N_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# ---- 1. 在「订单信息」卡末尾（预计到货日期之后）插入备注（textarea） ----
old1 = """  <div class="form-row">
    <div class="form-label">预计到货日期：</div>
    <div>
      <div class="input-box" style="width:180px;"><input type="text" value="2026-09-15" placeholder="请输入"></div>
    </div>
  </div>
</div>"""
assert N.count(old1) == 1, f'订单信息卡末尾锚点异常 {N.count(old1)}'
new1 = old1[:-len('</div>')] + """  <div class="form-row" style="align-items:flex-start;">
    <div class="form-label" style="padding-top:6px;">备注：</div>
    <div>
      <div class="input-box" style="width:520px;height:auto;padding:6px 11px;"><textarea placeholder="选填" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea></div>
    </div>
  </div>
</div>"""
N = N.replace(old1, new1)
print('[1] 备注已并入「订单信息」卡末尾（预计到货日期之后）')

# ---- 2. 删除独立的「随附信息」卡 ----
old2 = """<div class="card">
  <h3 class="card-title">随附信息</h3>
  <div class="form-row">
    <div class="form-label">备注：</div>
    <div>
      <div class="input-box" style="width:520px;"><input type="text" value="" placeholder="选填"></div>
    </div>
  </div>
</div>
"""
assert N.count(old2) == 1, f'随附信息卡锚点异常 {N.count(old2)}'
N = N.replace(old2, '')
print('[2] 已删除独立「随附信息」卡')

# ---- 3. 校验 ----
assert N.count('<textarea') == 1, f'textarea 数异常 {N.count(chr(60)+"textarea")}'
assert '随附信息' not in N, '随附信息卡残留'
assert N.count('备注：') == 1, '备注 label 数异常'
cards = N.count('<div class="card">')
print(f'[3] 卡片数: {cards}（应为 2：订单信息 / 采购明细）')

io.open(N_P, 'w', encoding='utf-8', newline='').write(N.replace('\r\n', '\n').replace('\n', '\r\n'))
print(f'[写出] {N_P} —— {len(N)} 字符')
