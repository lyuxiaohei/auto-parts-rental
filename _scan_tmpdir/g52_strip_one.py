# -*- coding: utf-8 -*-
"""G52 单页变换器：剥旧标注三件块，保留 f01 流程图钮，替换为共享件两行引用。
一次只处理一页（argv[1]）；任何断言失败立即退出、不写盘；幂等可重入。
块结构断言全部通过后才组装新文本；写盘走临时文件+os.replace（3 次重试）。
"""
import sys, os, re, time

def die(page, msg):
    print('FAIL %s :: %s' % (page, msg))
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print('usage: g52_strip_one.py <page.html>'); sys.exit(2)
    page = sys.argv[1].replace('\\', '/')
    try:
        raw = open(page, 'rb').read()
    except Exception as e:
        die(page, 'read %s' % e)
    t = raw.decode('utf-8')

    A_STYLE = '<style id="proto-notes-style">'
    A_PINS = '<div id="proto-pins">'
    A_F01 = '<style id="f01-fab-style">'
    A_JS = '<script id="proto-notes-js">'

    # 幂等重入：已完成页跳过
    if t.count(A_JS) == 0 and t.count(A_STYLE) == 0 and t.count(A_PINS) == 0:
        if ('notes-data.js' in t) and ('notes-drawer.js' in t):
            print('SKIP %s :: 已改造（幂等）' % page); return
        die(page, '无旧块亦无引用（非预期形态）')

    # 计数断言（三件各恰 1，f01 样式恰 1）
    for a, nm in [(A_STYLE, 'style块'), (A_PINS, 'pins容器'), (A_JS, 'js块'), (A_F01, 'f01-fab-style')]:
        c = t.count(a)
        if c != 1: die(page, '%s计数=%d' % (nm, c))

    si = t.index(A_STYLE)
    se = t.index('</style>', si) + len('</style>')
    pi = t.index(A_PINS)
    fi = t.index(A_F01)
    jk = t.index(A_JS)
    je = t.index('</script>', jk) + len('</script>')
    if not (si < pi < fi < jk): die(page, '块顺序异常')

    # 行尾风格
    crlf = raw.count(b'\r\n'); lf = raw.count(b'\n') - crlf
    NL = '\r\n' if crlf > lf else '\n'

    # gap1：style 块与 pins 之间只允许空白
    if t[se:pi].strip(): die(page, 'style→pins 间隙有内容 %r' % t[se:pi][:60])

    # pins 内部：到 f01 样式之前只允许 pin 行（每行一个完整 proto-pin div）
    pin_ids = []
    for ln in t[pi + len(A_PINS):fi].split('\n'):
        s = ln.strip()
        if not s: continue
        m = re.match(r'^<div class="proto-pin" id="proto-pin-(\d+)">.+</div>$', s)
        if not m: die(page, 'pins 内非 pin 行 %r' % s[:100])
        pin_ids.append(int(m.group(1)))
    if not pin_ids: die(page, 'pins 区无 pin')

    # fab 行：f01 样式起至行尾；剥其中 pn-fab，保留 f01 链接
    le = t.find('\n', fi)
    if le < 0: die(page, 'fab 行无行尾')
    fab_line = t[fi:le].rstrip('\r')
    m2 = re.match(r'^(<style id="f01-fab-style">.+</style>)(<div class="fab-row">.+</div>)</div>$', fab_line)
    if not m2: die(page, 'fab 行形态异常 %r' % fab_line[:120])
    style_part, fabrow = m2.group(1), m2.group(2)
    am = re.search(r'<a class="f01-fab"[^>]*>[^<]*</a>', fabrow)
    if not am: die(page, 'fab-row 内无 f01-fab 链接')
    tail = fabrow[am.end():-len('</div>')]
    if tail.strip():
        if not re.match(r'^<div class="pn-fab"[^>]*>.+</div>$', tail.strip()):
            die(page, 'f01 链接后非 pn-fab %r' % tail[:80])
    new_fab_line = style_part + '<div class="fab-row">' + am.group(0) + '</div>'
    href_m = re.search(r'href="([^"]*)"', am.group(0))

    # gap2：fab 行与 js 块之间只允许空白
    if t[le:jk].strip(): die(page, 'fab→js 间隙有内容 %r' % t[le:jk][:60])

    # 基线计数
    dn_before = t.count('data-note="')
    f01_before = t.count('<a class="f01-fab"')
    opens_before = t.count('<div') - t.count('</div>')

    # 引用前缀：根级页 _data/，子目录页 ../_data/
    prefix = '_data/' if '/' not in page else '../_data/'
    ref = ('<script src="%snotes-data.js"></script>%s<script src="%snotes-drawer.js"></script>'
           % (prefix, NL, prefix))

    # 组装：删 [si,pi)（style 块+换行+pins 开+pin 行），fab 行替换，删 proto-pins 闭合（并入 fab 行重写），js 块→两行引用
    new_t = t[:si] + new_fab_line + NL + ref + t[je:]
    removed = t[si:fi] + t[fi:le].rstrip('\r') + t[jk:je]
    added = new_fab_line + ref
    bal = lambda x: x.count('<div') - x.count('</div>')
    expect_bal = (opens_before - bal(removed) + bal(added))

    # 写前自检
    for a, nm in [(A_STYLE, 'style残留'), (A_PINS, 'pins残留'), (A_JS, 'js残留')]:
        if new_t.count(a): die(page, '写前%s>0' % nm)
    if new_t.count('proto-pin-'): die(page, '写前 proto-pin 残留')
    if new_t.count('protoNotesFab'): die(page, '写前 protoNotesFab 残留')
    if new_t.count('data-note="') != dn_before: die(page, 'data-note 数变化')
    if new_t.count('<a class="f01-fab"') != f01_before: die(page, 'f01 链接数变化')
    if new_t.count(A_F01) != 1: die(page, 'f01-fab-style 数变化')
    if new_t.count('notes-data.js') != 1 or new_t.count('notes-drawer.js') != 1: die(page, '引用行数异常')
    if (new_t.count('<div') - new_t.count('</div>')) != expect_bal: die(page, 'div 配平差与移除/新增实算不符')

    # 写盘：临时文件 + os.replace，3 次重试（中文路径惯例）
    data = new_t.encode('utf-8')
    tmp = page + '.g52tmp'
    for attempt in range(3):
        try:
            with open(tmp, 'wb') as f: f.write(data)
            os.replace(tmp, page)
            break
        except Exception as e:
            if attempt == 2: die(page, 'write %s' % e)
            time.sleep(0.3)

    # 写后复读自检
    chk = open(page, 'rb').read().decode('utf-8')
    for a in (A_STYLE, A_PINS, A_JS, 'proto-pin-', 'protoNotesFab'):
        if a in chk: die(page, '写后残留 %s' % a)
    if chk.count('data-note="') != dn_before: die(page, '写后 data-note 变化')
    if chk.count('<a class="f01-fab"') != f01_before: die(page, '写后 f01 变化')

    print('PASS %s :: pins=%d(%s) data-note=%d fab_href=%s refs=2' %
          (page, len(pin_ids), ','.join(map(str, pin_ids)), dn_before, href_m.group(1) if href_m else '?'))

if __name__ == '__main__':
    main()
