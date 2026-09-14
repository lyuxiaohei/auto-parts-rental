# -*- coding: utf-8 -*-
"""修正补丁 strip 段 group(1)→group(0)（无捕获组）"""
import io

OLD = """    m = re.search(r'<div class="fab-row"><a class="f01-fab"[^>]*>[^<]*</a>', html)
    if m:
        st += m.group(1)
    else:
        m = re.search(r'<a class="f01-fab"[^>]*>[^<]*</a>', html)
        if m:
            st += m.group(1)"""
NEW = OLD.replace("m.group(1)", "m.group(0)")

for copy in [r"C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py",
             r"C:\Users\Administrator\.claude\skills\原型标注\scripts\annotate.py"]:
    t = io.open(copy, encoding="utf-8", newline="").read()
    nl = chr(13) + chr(10) if t.count(chr(13) + chr(10)) > (t.count(chr(10)) - t.count(chr(13) + chr(10))) else chr(10)
    old_l = OLD.replace(chr(10), nl)
    new_l = NEW.replace(chr(10), nl)
    n = t.count(old_l)
    if n == 0 and NEW in t:
        print("SKIP 已修正", copy)
        continue
    assert n == 1, copy + " = " + str(n)
    io.open(copy, "w", encoding="utf-8", newline="").write(t.replace(old_l, new_l, 1))
    print("PASS 修正", copy)

r = __import__("subprocess").run(["python", "-m", "py_compile",
                                  r"C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py",
                                  r"C:\Users\Administrator\.claude\skills\原型标注\scripts\annotate.py"],
                                 capture_output=True, text=True)
print("py_compile:", "PASS" if r.returncode == 0 else r.stderr[:300])
