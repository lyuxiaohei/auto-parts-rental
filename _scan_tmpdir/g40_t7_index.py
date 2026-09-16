# -*- coding: utf-8 -*-
"""G40 T7 第二步：_索引.md G40 行状态 ⏳→✅ ＋ 挂 commit 哈希
用法: python g40_t7_index.py <short-hash>
"""
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(BASE, 'agent-handoff', '_索引.md')

OLD = ('｜任务书=20260915-G40-原型侧变更包.md | ⏳ | （待执行） | 20260915-G40-原型侧变更包.md |')

SUMMARY = ('｜**执行摘要（09-16）**：T0 **D-149 落账**（D-142 状态列更正为「补做·原标并入 G36 系状态虚报」）｜'
           'T1 术语三条替换（`银行水单核销.html`→`银行回单核销.html` 181／`水单核销详情.html`→`银行回单核销详情.html` 9／'
           '`回款登记.html`→`收款登记.html` 149／`回款详情.html`→`收款详情.html` 11／`盈亏报表.html`→`损益报表.html` 132／'
           '自由文本 `回款`→`收款` 1·147 文件·白名单先掩码后还原·顺序敏感：长串路径优先）｜'
           'T2 `git mv` 5 处＋引用同步四处（侧边栏／demo-data／A02·A05·A06 路径行／A03·A04 标注层）·旧名残留 0·净新增死链 0｜'
           'T3 「货品」实测＝`供货品类` 子串假阳性（页面域真术语本就 0）＋A02 备注列改「多物料明细」；库龄／在库时长／流转次数＝0；'
           '零件号·入库库区 页面域 0（仅 A05 白名单沿革注记）｜'
           'T4 F01 v3.6→v3.7：**L1/L3 各补「转移出库」节点**（170×56）＋L1 跨线决策备注框「L1–L4 通用」注记四点＋箭头标签「分批·非必经」·'
           '计费文案 7 条串改「按持有量计租＋期段账单」·状态驱动方 2 处改「转移单审核驱动」·虚拟仓注记改「不维护」·Mermaid 源同步｜'
           'T5 开发规则 v3.7（补 §4 节点规格＋新 §12 计费与状态口径·viewBox 更正 880·章节 1–13 连续）｜'
           '验证：audit **132 页 0/0/0**＋PW **16/16**＋溢出 **0** 处（双 viewBox 未调整·支图零变动）＋node --check **0**｜'
           '失败清单**无失败项**（登记 9 条）')


def main():
    assert len(sys.argv) > 1, '需要短哈希参数'
    h = sys.argv[1]
    s = io.open(IDX, encoding='utf-8', newline='').read()
    assert s.count(OLD) == 1, '索引 G40 行尾锚点计数 %d' % s.count(OLD)
    s = s.replace(OLD, '｜任务书=20260915-G40-原型侧变更包.md | ✅ | %s+回填 | 20260915-G40-原型侧变更包.md |%s' % (h, SUMMARY))
    io.open(IDX, 'w', encoding='utf-8', newline='').write(s)
    print('OK 索引 G40 行 → ✅ ｜ %s+回填' % h)
    s2 = io.open(IDX, encoding='utf-8', newline='').read()
    for l in s2.split('\n'):
        if l.startswith('| G40 |'):
            print('   %s' % l[-360:])
    return 0


if __name__ == '__main__':
    sys.exit(main())
