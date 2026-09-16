# -*- coding: utf-8 -*-
"""G40 T6-a 静态死链检查（只读·不依赖浏览器）
抽取全站 HTML 中 href / go('...') / onload 跳转 / demo-data 的 url: '...' 目标，解析相对路径，报告不存在项。
"""
import io, os, re, sys, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, 'P3-R01-包装租赁管理后台原型')

PAT = [
    re.compile(r"""href\s*=\s*["']([^"'#]+)["']"""),
    re.compile(r"""go\(\s*['"]([^'"]+)['"]"""),
    re.compile(r"""url\s*:\s*['"]([^'"]+)['"]"""),
    re.compile(r"""location\.href\s*=\s*['"]([^'"]+)['"]"""),
    re.compile(r"""open\(\s*['"]([^'"]+)['"]"""),
]
SKIP_PREFIX = ('http://', 'https://', 'mailto:', 'javascript:', 'data:', '#', 'tel:')


def targets():
    for dp, dn, fn in os.walk(ROOT):
        if '.prompts' in dp:
            continue
        for f in fn:
            if not f.lower().endswith(('.html', '.js')):
                continue
            p = os.path.join(dp, f)
            s = io.open(p, encoding='utf-8', errors='replace').read()
            for rx in PAT:
                for m in rx.finditer(s):
                    yield p, m.group(1)


def main():
    missing = {}
    total = 0
    seen = set()
    for src, t in targets():
        t = t.strip()
        if not t or t.startswith(SKIP_PREFIX):
            continue
        if not t.lower().endswith('.html'):
            continue
        total += 1
        path = t.split('?')[0].split('#')[0]
        key = (src, path)
        if key in seen:
            continue
        seen.add(key)
        dest = os.path.normpath(os.path.join(os.path.dirname(src), path))
        if not os.path.isfile(dest):
            missing.setdefault(os.path.relpath(src, ROOT), []).append(path)
    print('HTML 目标引用（去重后）%d 条' % len(seen))
    if not missing:
        print('死链 0 —— 全部目标文件存在')
    else:
        n = sum(len(v) for v in missing.values())
        print('死链 %d 条：' % n)
        for k in sorted(missing):
            for v in sorted(set(missing[k])):
                print('   %s -> %s' % (k, v))
    # 旧名残留
    OLD = ['回款登记', '回款详情', '盈亏报表', '银行水单核销', '水单核销详情']
    bad = 0
    for dp, dn, fn in os.walk(ROOT):
        if '.prompts' in dp:
            continue
        for f in fn:
            if not f.lower().endswith(('.html', '.js', '.json', '.md', '.css')):
                continue
            p = os.path.join(dp, f)
            s = io.open(p, encoding='utf-8', errors='replace').read()
            for o in OLD:
                if o in s:
                    print('   [旧名残留] %s in %s' % (o, os.path.relpath(p, ROOT)))
                    bad += 1
    print('旧名残留 = %d' % bad)
    return 0 if (not missing and bad == 0) else 1


if __name__ == '__main__':
    sys.exit(main())
