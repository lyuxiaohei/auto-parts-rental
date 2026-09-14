# -*- coding: utf-8 -*-
"""annotate.py 防复发补丁：strip 时 stash f01-fab 片段，重建 pins 时以 fab-row 形态保留（两副本）"""
import io, subprocess

PATCH_STRIP_OLD = 'def strip_injected(html):\n    for tag, marker'
PATCH_STRIP_NEW = ('F01_STASH = \'\'\n\n\n'
    'def strip_injected(html):\n'
    '    global F01_STASH\n'
    "    st = ''\n"
    "    m = re.search(r'<style id=\"f01-fab-style\">.*?</style>', html, re.S)\n"
    '    if m:\n'
    '        st += m.group(1)\n'
    '    m = re.search(r\'<div class="fab-row"><a class="f01-fab"[^>]*>[^<]*</a>\', html)\n'
    '    if m:\n'
    '        st += m.group(1)\n'
    '    else:\n'
    "        m = re.search(r'<a class=\"f01-fab\"[^>]*>[^<]*</a>', html)\n"
    '        if m:\n'
    '            st += m.group(1)\n'
    '    F01_STASH = st\n'
    '    for tag, marker')

PATCH_BUILD_OLD = 'def build_pins(items, codes=None):'
PATCH_BUILD_NEW = 'def build_pins(items, codes=None, f01=\'\'):'

PATCH_FAB_OLD = ("    fab = ('<div class=\"pn-fab\" id=\"protoNotesFab\">标注</div>')\n"
                 "    return '<div id=\"proto-pins\">' + '\\n'.join(pins) + '\\n' + fab + '</div>'")
PATCH_FAB_NEW = ("    fab = ('<div class=\"pn-fab\" id=\"protoNotesFab\">标注</div>')\n"
                 "    if f01:\n"
                 "        ms = re.search(r'(<style id=\"f01-fab-style\">.*?</style>)', f01, re.S)\n"
                 "        ma = re.search(r'(<a class=\"f01-fab\"[^>]*>[^<]*</a>)', f01)\n"
                 "        if ma:\n"
                 "            fab = (ms.group(1) if ms else '') + '<div class=\"fab-row\">' + ma.group(1) + fab + '</div>'\n"
                 "    return '<div id=\"proto-pins\">' + '\\n'.join(pins) + '\\n' + fab + '</div>'")

PATCH_INJ_OLD = '    pins = build_pins(items, codes)'
PATCH_INJ_NEW = '    pins = build_pins(items, codes, f01=F01_STASH)'

for copy in [r"C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py",
             r"C:\Users\Administrator\.claude\skills\原型标注\scripts\annotate.py"]:
    t = io.open(copy, encoding="utf-8", newline="").read()
    if "F01_STASH" in t:
        print("SKIP 已打补丁", copy)
        continue
    nl = chr(13) + chr(10) if t.count(chr(13) + chr(10)) > (t.count(chr(10)) - t.count(chr(13) + chr(10))) else chr(10)
    for old, new in [(PATCH_STRIP_OLD, PATCH_STRIP_NEW), (PATCH_BUILD_OLD, PATCH_BUILD_NEW),
                     (PATCH_FAB_OLD, PATCH_FAB_NEW), (PATCH_INJ_OLD, PATCH_INJ_NEW)]:
        old = old.replace(chr(10), nl)
        new = new.replace(chr(10), nl)
        assert t.count(old) == 1, copy + " 锚点异常: " + repr(old[:50]) + " = " + str(t.count(old))
        t = t.replace(old, new, 1)
    io.open(copy, "w", encoding="utf-8", newline="").write(t)
    print("PASS 补丁", copy)

r = subprocess.run(["python", "-m", "py_compile",
                    r"C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py",
                    r"C:\Users\Administrator\.claude\skills\原型标注\scripts\annotate.py"],
                   capture_output=True, text=True)
print("py_compile:", "PASS" if r.returncode == 0 else r.stderr[:300])
