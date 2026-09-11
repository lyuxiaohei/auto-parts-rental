#!/usr/bin/env python3
# G21 T2b 产品档案.html：两段表单行→三段式 + 单位下拉注入 id/onchange + g21RentHint script
# T2c 新建产品.html：同款替换（复用同函数）
import sys

NEW_ROWS = '''  <div class="form-row">
    <span class="form-label">参考未税租入价</span>
    <div style="display:flex;gap:6px;align-items:center;">
      <div class="input-box select-box" style="width:116px;flex:none;"><select id="rentInModeSel" onchange="g21RentHint('rentIn')" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>按时间周期</option><option>按次</option></select></div>
      <div class="input-box select-box" style="width:72px;flex:none;"><select id="rentInUnitSel" onchange="g21RentHint('rentIn')" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>月</option><option>年</option><option>日</option></select></div>
      <div class="input-box" style="flex:1;min-width:0;"><input placeholder="数值，如 45.00（无租入来源留空）"></div>
      <span id="rentInHint" style="font-size:12px;color:#8c8c8c;white-space:nowrap;">元/只·月</span>
    </div>
  </div>
  <div class="form-row">
    <span class="form-label">参考未税租赁价</span>
    <div style="display:flex;gap:6px;align-items:center;">
      <div class="input-box select-box" style="width:116px;flex:none;"><select id="rentalModeSel" onchange="g21RentHint('rental')" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>按时间周期</option><option>按次</option></select></div>
      <div class="input-box select-box" style="width:72px;flex:none;"><select id="rentalUnitSel" onchange="g21RentHint('rental')" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>月</option><option>年</option><option>日</option></select></div>
      <div class="input-box" style="flex:1;min-width:0;"><input placeholder="数值，如 60.00"></div>
      <span id="rentalHint" style="font-size:12px;color:#8c8c8c;white-space:nowrap;">元/只·月</span>
    </div>
  </div>'''

OLD_ROWS = '''  <div class="form-row">
    <span class="form-label">参考未税租入价</span>
    <div class="input-box"><input placeholder="如 45.00 元/只·月（无租入来源留空）"></div>
  </div>
  <div class="form-row">
    <span class="form-label">参考未税租赁价</span>
    <div class="input-box"><input placeholder="按周期或按次，如 60.00 元/只·月 / 15.00 元/块·次"></div>
  </div>'''

SCRIPT = '<script>/* G21 租价三段式联动：计费方式(按时间周期/按次)×周期单位(月/年/日·默认月)+数值，后缀=元/计量单位·周期（单位取同表单「单位」下拉） */ function g21RentHint(p){var m=document.getElementById(p+\'ModeSel\').value;var u=document.getElementById(p+\'UnitSel\');u.disabled=(m===\'按次\');var us=document.getElementById(\'unitSel\');var unit=us?us.value:\'只\';document.getElementById(p+\'Hint\').textContent=\'元/\'+unit+\'·\'+(m===\'按次\'?\'次\':u.value);}</script>'

UNIT_INJECT = ' id="unitSel" onchange="g21RentHint(\'rentIn\');g21RentHint(\'rental\');"'


def apply(path, need_unit=True):
    s = open(path, encoding='utf-8').read()
    # 1. 两段表单行 → 三段式（恰 1 处）
    assert s.count(OLD_ROWS) == 1, '旧两段块锚 %d（%s）' % (s.count(OLD_ROWS), path)
    s = s.replace(OLD_ROWS, NEW_ROWS, 1)
    # 2. 单位下拉注入（锚 <span class="form-label">单位</span> 所在 form-row 的 select 起标签）
    if need_unit:
        lines = s.splitlines(keepends=True)
        iu = [i for i, l in enumerate(lines) if '<span class="form-label">单位</span>' in l]
        assert len(iu) == 1, '单位 label %d 处（%s）' % (len(iu), path)
        # 其后第一个 <select 起标签
        for j in range(iu[0], min(iu[0] + 4, len(lines))):
            if '<select ' in lines[j]:
                k = lines[j].index('<select ')
                pos = k + len('<select')
                assert 'id="unitSel"' not in lines[j], 'unitSel 已注入'
                lines[j] = lines[j][:pos] + UNIT_INJECT + lines[j][pos:]
                break
        else:
            raise AssertionError('单位 form-row 内未找到 select（%s）' % path)
        s = ''.join(lines)
    # 3. createModal 结束后追加 script（恰 1 处）
    assert s.count('function g21RentHint') == 0, 'g21RentHint 已存在（%s）' % path
    cm = s.index('id="createModal"')
    depth, end = 0, None
    for off in range(cm, len(s)):
        pass
    # 逐行配平找 createModal 块尾
    seg = s[cm:]
    depth = 0
    for ln, line in enumerate(seg.splitlines(keepends=True)):
        depth += line.count('<div') - line.count('</div')
        if depth <= 0 and ln > 0:
            end = sum(len(x) for x in seg.splitlines(keepends=True)[:ln + 1]) + cm
            break
    assert end, 'createModal 配平失败（%s）' % path
    s = s[:end] + '\n' + SCRIPT + s[end:]
    # 4. 断言与配平
    for probe in ['id="rentInModeSel"', 'id="rentInUnitSel"', 'id="rentalModeSel"', 'id="rentalUnitSel"', 'id="rentInHint"', 'id="rentalHint"']:
        assert s.count(probe) == 1, '%s 计数 %d（%s）' % (probe, s.count(probe), path)
    assert s.count('function g21RentHint') == 1
    if need_unit:
        assert s.count('id="unitSel"') == 1, 'unitSel 计数 %d（%s）' % (s.count('id="unitSel"'), path)
    assert s.count('<div') == s.count('</div'), 'div 配平 %d/%d（%s）' % (s.count('<div'), s.count('</div'), path)
    assert s.count('<select') == s.count('</select>'), 'select 配平 %d/%d（%s）' % (s.count('<select'), s.count('</select>'), path)
    assert s.count('<option') == s.count('</option>'), 'option 配平 %d/%d（%s）' % (s.count('<option'), s.count('</option>'), path)
    assert '如 45.00 元/只·月（无租入来源留空）' not in s and '按周期或按次，如 60.00' not in s
    open(path, 'w', encoding='utf-8').write(s)
    print('PASS', path.split('/')[-1], '三段式+联动落位，div/select/option 配平过')


ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/'
apply(ROOT + '基础数据/产品档案.html', need_unit=True)
# T2c 同款（模板已引 demo-data.js，不新增引用）
apply(ROOT + '基础数据/弹窗/新建产品.html', need_unit=True)
# 模板引 demo-data.js 断言（e7ff975 补引，不新增）
tpl = open(ROOT + '基础数据/弹窗/新建产品.html', encoding='utf-8').read()
assert 'demo-data.js' in tpl, '模板缺 demo-data.js 引用'
print('PASS 新建产品.html demo-data.js 引用在')
