#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# G21 收尾 A05 字段字典：四价登记块→三段式口径 + dictItems BF 登记与记录数同步 + 头部统计行同步
P = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型/P3-R01-A05-字段字典.md'
s = open(P, encoding='utf-8').read()

# 1. 头部统计行：字段行 321 → 325（products +4 结构化租价键）
OLD = '> **统计**：实体 38 ｜ 字段行 321'
assert s.count(OLD) == 1, '统计行锚 %d' % s.count(OLD)
s = s.replace(OLD, '> **统计**：实体 38 ｜ 字段行 325', 1)

# 2. 四价块：标题加 G21 注记
OLD_T = '## products 四参考价（2026-09-11 道远指令补齐·物料粒度·不落供应商）'
assert s.count(OLD_T) == 1
s = s.replace(OLD_T, '## products 四参考价（2026-09-11 道远指令补齐·物料粒度·不落供应商；G21 租价三段式结构化）', 1)

# 3. blockquote 尾部追加 G21 说明（原文行尾「fields 不加价键（价格非筛选维度）。」改为三段式口径）
OLD_Q = '四价落在 cells（列表 4 列）+info（详情 4 行）+弹窗表单（4 字段），fields 不加价键（价格非筛选维度）。'
assert s.count(OLD_Q) == 1, 'blockquote 锚 %d' % s.count(OLD_Q)
NEW_Q = ('四价落在 cells（列表 4 列）+info（详情 4 行）+弹窗表单（4 字段）。\n'
         '> **G21 三段式结构化（2026-09-11 拍板·形态 B）**：fields 追加 4 键 `rentInMode`/`rentInPrice`/`rentalMode`/`rentalPrice`（12/12 行）——租价=计费方式（按时间周期/按次）+周期单位（年/月/日·默认月）+数值；mode 值域 按月/按次/null（null=无租价）；弹窗表单改三段控件（方式 select+单位 select+数值 input+后缀 hint 联动「元/单位·周期」），cells/info 保持拼接文本零改动。计费方式值源=dictItems「计费方式」大类（BF-01 按月/BF-02 按次 启用）。')
s = s.replace(OLD_Q, NEW_Q, 1)

# 4. 表格两租价行演示值形态补结构化记法
OLD_R1 = '| 参考未税租入价 | 45.00 元/只·月 / —（无租入来源） | 有租入来源的物料 |'
assert s.count(OLD_R1) == 1
s = s.replace(OLD_R1, '| 参考未税租入价（rentInMode+rentInPrice） | 按月·45.00 / null（无租入来源） | 有租入来源的物料；cells 仍显 45.00 元/只·月 |', 1)
OLD_R2 = '| 参考未税租赁价 | 60.00 元/只·月 / 15.00 元/块·次 / —（采购件/停用不计租） | 器具类·月或次两形态 |'
assert s.count(OLD_R2) == 1
s = s.replace(OLD_R2, '| 参考未税租赁价（rentalMode+rentalPrice） | 按月·60.00 / 按次·15.00 / null（采购件/停用不计租） | 器具类·月或次两形态；cells 仍显拼接文本 |', 1)

# 5. dictItems 段：记录数 45→49 + BF 值域登记
OLD_D = '记录数 45 ｜ 消费页面：数据字典（系统管理/数据字典.html）'
assert s.count(OLD_D) == 1, 'dictItems 记录数锚 %d' % s.count(OLD_D)
s = s.replace(OLD_D, '记录数 49（G16 +WL-01/02 物料类型·G21 +BF-04 按年/BF-05 按日） ｜ 消费页面：数据字典（系统管理/数据字典.html）', 1)
OLD_ST = '| `status` | 状态〔待核〕 | 枚举 | 启用 / 停用 | 45/45 |'
assert s.count(OLD_ST) == 1, 'status 行锚 %d' % s.count(OLD_ST)
s = s.replace(OLD_ST, '| `status` | 状态〔待核〕 | 枚举 | 启用 / 停用 | 49/49 |\n\n> **G21 计费方式值域**：BF-01 按月 / BF-02 按次（启用）· BF-03 按张（**停用**·G21）· BF-04 按年 / BF-05 按日（G21 新增·启用）——物料档案两租价与租入单明细「计费方式」列值源；按日为短期备用口径（本期无日租金业务）。', 1)
for n in range(5):
    s = s.replace('| 45/45 |', '| 49/49 |', 1)  # 其余 4 行 _key/category/abbr/name

open(P, 'w', encoding='utf-8').write(s)
assert s.count('49/49') == 5, '49/49 计数 %d' % s.count('49/49')
assert '45/45' not in s
print('A05 PASS：统计 321→325 ｜ 四价块三段式注记+两行更新 ｜ dictItems 45→49+BF 值域登记')
