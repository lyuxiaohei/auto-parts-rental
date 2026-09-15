# -*- coding: utf-8 -*-
"""G33 T5/T6: 待办与审核矩阵 16→19 + 数据字典页同步
- 权限配置/用户权限/角色管理：auditPermMatrix +3 checked 项（插「租赁出库」后）
- 我的待办.html：速滤 option +3（插「租赁出库」后）
- 数据字典.html：待办单据类型 cnt 16→19 + dic-item +2 行（退货类型/退款类型）+ createModal select +2
- mobile/待办审批.html：消费行数注释 16→19
"""
import io, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型', *a)

def rd(fp):
    with io.open(P(*fp.split('/')), encoding='utf-8') as f:
        return f.read()

def wr(fp, s):
    with io.open(P(*fp.split('/')), 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(s)

def sub1(s, old, new, tag=''):
    n = s.count(old)
    assert n == 1, 'G33 锚点[%s] 命中 %d 次: %s' % (tag, n, old[:60])
    return s.replace(old, new)

MATRIX_NEW = ('<span class="checkbox checked" data-audit="采购退货单"><span class="box">✓</span>采购退货单</span>\n'
              '<span class="checkbox checked" data-audit="销售退货单"><span class="box">✓</span>销售退货单</span>\n'
              '<span class="checkbox checked" data-audit="退款登记"><span class="box">✓</span>退款登记</span>')

for fp in ['系统管理/弹窗/权限配置.html', '系统管理/用户权限.html', '系统管理/角色管理.html']:
    s = rd(fp)
    lines = s.split('\n')
    out, ins = [], 0
    for ln in lines:
        out.append(ln)
        if 'data-audit="租赁出库"' in ln:
            indent = ln[:len(ln) - len(ln.lstrip())]
            for piece in MATRIX_NEW.split('\n'):
                out.append(indent + piece)
            ins += 1
    assert ins == 1, 'G33 矩阵锚点 %s 命中 %d' % (fp, ins)
    s2 = '\n'.join(out)
    assert s2.count('data-audit=') == s.count('data-audit=') + 3
    wr(fp, s2)
    print('OK matrix +3:', fp, '(items %d→%d)' % (s.count('data-audit='), s2.count('data-audit=')))

# 我的待办 option
s = rd('我的待办.html')
s = sub1(s, '<option>租赁出库</option>', '<option>租赁出库</option><option>采购退货单</option><option>销售退货单</option><option>退款登记</option>', tag='todo-opt')
wr('我的待办.html', s)
print('OK 我的待办 option +3（%d→%d）' % (s.count('<option>') - 3, s.count('<option>')))

# 数据字典
s = rd('系统管理/数据字典.html')
s = sub1(s, '<div class="dic-item"><span>待办单据类型</span><span class="cnt">16</span></div>', '<div class="dic-item"><span>待办单据类型</span><span class="cnt">19</span></div>', tag='dic-dj')
s = sub1(s, '<div class="dic-item"><span>消息类型</span><span class="cnt">4</span></div>',
         '<div class="dic-item"><span>消息类型</span><span class="cnt">4</span></div>\n          <div class="dic-item"><span>退货类型</span><span class="cnt">2</span></div>\n          <div class="dic-item"><span>退款类型</span><span class="cnt">2</span></div>', tag='dic-msg')
s = sub1(s, '<option>消息类型</option>', '<option>消息类型</option><option>退货类型</option><option>退款类型</option>', tag='dic-sel')
wr('系统管理/数据字典.html', s)
print('OK 数据字典 dic-item %d 行 + select' % s.count('class="dic-item'))

# mobile 注释
s = rd('mobile/待办审批.html')
s = s.replace('消费 DEMO_DATA.todoItems（16 行）', '消费 DEMO_DATA.todoItems（19 行）')
wr('mobile/待办审批.html', s)
print('OK mobile 待办注释 16→19（动态渲染自动 19 行）')
print('=== G33 T5/T6 完成 ===')
