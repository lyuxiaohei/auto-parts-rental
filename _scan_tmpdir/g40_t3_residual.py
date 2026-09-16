# -*- coding: utf-8 -*-
"""G40 T3 残留清理与复核
- 「货品」：demo-data 命中系「供货品类」子串假阳性（不改·记注）；A05 禁用写法列/沿革注记属白名单；
  A02:59 备注列「多货品明细」按 G38 口径（货品退场→物料）改「多物料明细」
- 「零件号」：A05 禁用写法列/沿革注记白名单；A03 标注层 desc 残留按 G38 概念表（material.code 禁用写法＝零件号）改「物料编码」
- 「入库库区」：仅 A05 G35 变更记录行（沿革注记）→ 白名单保留
- 库龄／在库时长／流转次数：全库应 0
"""
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, 'P3-R01-包装租赁管理后台原型')

EDITS = [
    ('P3-R01-A02-页面类型与入口对照表.md', ['（多货品明细：月租/按套）'], ['（多物料明细：月租/按套）']),
    ('P3-R01-A03-标注数据.json', ['"desc": "零件号、名称、供应商来源、多项目共用标记"'],
     ['"desc": "物料编码、名称、供应商来源、多项目共用标记"']),
]


def main():
    for rel, olds, news in EDITS:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding='utf-8', newline='').read()
        for o, n in zip(olds, news):
            c = s.count(o)
            assert c == 1, '%s 锚点计数 %d != 1 : %r' % (rel, c, o)
            s = s.replace(o, n)
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print('OK  %s  替换 %d 处' % (rel, len(olds)))

    print('--- 终检（原型目录·含 A 类文档·排除 .prompts）---')
    EXTS = ('.html', '.js', '.json', '.md', '.css')
    terms = ['货品', '零件号', '入库库区', '库龄', '在库时长', '流转次数']
    hits = {t: [] for t in terms}
    for dp, dn, fn in os.walk(ROOT):
        if '.prompts' in dp:
            continue
        for f in fn:
            if not f.lower().endswith(EXTS):
                continue
            p = os.path.join(dp, f)
            s = io.open(p, encoding='utf-8', newline='').read()
            for t in terms:
                for i, l in enumerate(s.split('\n')):
                    if t in l:
                        hits[t].append((os.path.relpath(p, ROOT), i + 1, l.strip()[:150]))
    for t in terms:
        print('  %s : %d 处' % (t, len(hits[t])))
        for h in hits[t]:
            print('      %s:%d  %s' % h)
    return 0


if __name__ == '__main__':
    sys.exit(main())
