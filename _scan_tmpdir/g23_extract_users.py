# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
txt = open(r"P3-R01-包装租赁管理后台原型\_data\demo-data.js", encoding="utf-8").read()

def block(name):
    m = re.search(r"^\s{2}(?:/\*.*?\*/\s*)?" + name + r"\s*:\s*[\[{](.*?)^\s{2}\}", txt, re.M | re.S)
    return m.group(1) if m else ""

b = block("users")
print("== users 全行 ==")
pat = re.compile(r"'(\w+)': \{ 'row': \{\"fields\": \{\"search\": \"([^\"]+)\", \"role\": \"([^\"]+)\", \"side\": \"([^\"]+)\", \"scope\": \"([^\"]+)\"")
for mm in pat.finditer(b):
    print(" -", mm.group(1), "|", mm.group(2).replace(" ", " / "), "|", mm.group(3), "|", mm.group(4), "|", mm.group(5))

print()
b2 = block("projects")
print("== projects 首行完整 fields ==")
m = re.search(r'\"fields\": \{(.*?)\}', b2, re.S)
print(m.group(1)[:400] if m else "none")

print()
print("== projects 各行 suppliers 值 ==")
for mm in re.finditer(r'\"name\": \"([^\"]+)\", \"customer\": \"([^\"]+)\", \"suppliers\": \"([^\"]*)\"', b2):
    print(" -", mm.group(1), "| customer:", mm.group(2), "| suppliers:", mm.group(3))
