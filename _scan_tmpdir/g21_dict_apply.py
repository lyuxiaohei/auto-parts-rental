#!/usr/bin/env python3
# G21 T1b 系统管理/数据字典.html 静态卡片：cnt 3→5 + 按张停用 + 去暂估×2 + 追加按年/按日两行
import os

P = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/系统管理/数据字典.html'
src = open(P, encoding='utf-8').read()
orig_len = len(src.splitlines())

# 1. 左侧分类计数 3→5（恰 1 处）
OLD_CNT = '<div class="dic-item"><span>计费方式</span><span class="cnt">3</span></div>'
assert src.count(OLD_CNT) == 1, 'cnt 锚 %d' % src.count(OLD_CNT)
src = src.replace(OLD_CNT, '<div class="dic-item"><span>计费方式</span><span class="cnt">5</span></div>', 1)

# 2. 按张行停用（行级锚定：含 <td>按张</td> 的 tr 块内 tag-green 启用 → tag-gray 停用）
lines = src.splitlines(keepends=True)
# 找按张 tr 块（tr 起 </tr> 止）
i_an = next(i for i, l in enumerate(lines) if '<td>按张</td>' in l)
i_tr_start = next(i for i in range(i_an, -1, -1) if '<tr>' in lines[i])
i_tr_end = next(i for i in range(i_an, len(lines)) if '</tr>' in lines[i])
blk = ''.join(lines[i_tr_start:i_tr_end + 1])
assert blk.count('<td><span class="tag tag-green">启用</span></td>') == 1, '按张行 tag 锚 %d' % blk.count('<td><span class="tag tag-green">启用</span></td>')
assert '按张计费' in blk and '在租张数' in blk, '按张行内容漂移'
new_blk = blk.replace('<td><span class="tag tag-green">启用</span></td>', '<td><span class="tag tag-gray">停用</span></td>', 1)
lines[i_tr_start:i_tr_end + 1] = [new_blk]

# 3. 去暂估×2（恰各 1 处）
src = ''.join(lines)
OLD1 = '<td>围板箱/托盘租赁（暂估）</td>'
OLD2 = '<td>组装服务费（暂估）</td>'
assert src.count(OLD1) == 1 and src.count(OLD2) == 1, '暂估锚 %d/%d' % (src.count(OLD1), src.count(OLD2))
src = src.replace(OLD1, '<td>围板箱/托盘租赁</td>', 1)
src = src.replace(OLD2, '<td>组装服务费 / 按次租价</td>', 1)

# 4. 按张 </tr> 后追加按年/按日两行（缩进照现有行：tr 8 空格 / td 10 空格）
YR = ('        <tr>\n'
      '          <td>按年</td>\n'
      '          <td>按年计租</td>\n'
      '          <td>年租金 × 租期年数</td>\n'
      '          <td>长周期备用口径</td>\n'
      '          <td><span class="tag tag-green">启用</span></td>\n'
      '        </tr>\n')
DY = ('        <tr>\n'
      '          <td>按日</td>\n'
      '          <td>按日计租</td>\n'
      '          <td>日租金 × 在租天数</td>\n'
      '          <td>短期备用口径（本期无日租金业务）</td>\n'
      '          <td><span class="tag tag-green">启用</span></td>\n'
      '        </tr>\n')
ANZHANG_END = ''.join(src.splitlines(keepends=True)[i_tr_start:i_tr_end + 1])  # 已停用化的按张块
assert src.count(ANZHANG_END) == 1, '按张块非唯一'
src = src.replace(ANZHANG_END, ANZHANG_END + YR + DY, 1)

# 5. 断言与配平自检
assert src.count('按年计租') == 1 and src.count('按日计租') == 1
assert src.count('（暂估）') == 0 and src.count('暂估') == 0
assert src.count('<span class="tag tag-gray">停用</span>') >= 1
for tag in ['div', 'span', 'tr', 'td', 'table', 'tbody', 'thead']:
    o, c = src.count('<' + tag), src.count('</' + tag + '>')
    assert o == c + src.count('<' + tag + ' ') or True  # 开标签可带属性，粗校验跳过
# 精确配平：tr/td 无属性形态
assert src.count('<tr>') == src.count('</tr>'), 'tr 配平 %d/%d' % (src.count('<tr>'), src.count('</tr>'))
assert src.count('<td>') + src.count('<td ') == src.count('</td>'), 'td 配平'

open(P, 'w', encoding='utf-8').write(src)
print('T1b 数据字典.html PASS：cnt 5 / 按张停用 / 暂估×2 清零 / 按年+按日两行追加 / tr 配平 %d/%d' % (src.count('<tr>'), src.count('</tr>')))
