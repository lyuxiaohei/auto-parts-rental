# -*- coding: utf-8 -*-
"""G40 T4 截图留档：全页高倍截图 + PIL 裁切（主图 L1/L3/F1F2 行 + 支线 S1 五态行）"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = Path(__file__).resolve().parent.parent
F01 = BASE / 'P3-R01-包装租赁管理后台原型' / 'P3-R01-F01-业务流程导航图.html'
OUT = BASE / '_scan_tmpdir'
S = 2

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 1200}, device_scale_factor=S)
    pg.goto(F01.as_uri(), wait_until='load')
    pg.wait_for_timeout(800)
    box_main = pg.locator('svg').nth(0).bounding_box()
    pg.evaluate('window.scrollTo(0,0)')
    pg.wait_for_timeout(200)
    full = OUT / 'g40_f01_fullpage.png'
    pg.screenshot(path=str(full), full_page=True)
    b.close()

im = Image.open(full)
print('fullpage', im.size)
bx, by = box_main['x'], box_main['y']
# 主图 880x2184 显示为 800 宽 → 缩放因子
k = box_main['width'] / 880.0
print('scale k = %.4f' % k)


def crop(name, x, y, w, h):
    """坐标按 SVG 用户单位（880 宽）给出"""
    px = int((bx + x * k) * S)
    py = int((by + y * k) * S)
    pw = int(w * k * S)
    ph = int(h * k * S)
    im.crop((px, py, px + pw, py + ph)).save(str(OUT / name))
    print('  %s  %s' % (name, (px, py, pw, ph)))


crop('g40_f01_L1_row.png', 20, 330, 840, 180)
crop('g40_f01_L3_row.png', 20, 745, 840, 180)
crop('g40_f01_L1_box.png', 450, 330, 400, 180)
crop('g40_f01_L3_box.png', 450, 880, 400, 90)
crop('g40_f01_F1F2.png', 20, 1860, 840, 200)
crop('g40_f01_T2_note.png', 20, 1770, 840, 110)
print('done')
