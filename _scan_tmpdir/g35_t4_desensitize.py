# -*- coding: utf-8 -*-
"""G35 T4 真名脱敏
Phase 1：36 词 + 疑似残留词的上下文扫描（只读·防误伤判定）
Phase 2：长词优先精确替换（assert 计数·EOL 保持）
Phase 3：清零扫描（36 词残留必须 0）+ 一致性抽样
"""
import io, os, sys

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# 映射表（任务书第四节·36 词）——执行时按长度降序（长词优先）
PAIRS = [
    ('一汽解放汽车有限公司', '华骏重卡汽车有限公司'),
    ('上汽大众汽车有限公司宁波分公司', '东海商用汽车有限公司宁波分公司'),
    ('小鹏汽车科技有限公司', '星途新能源汽车科技有限公司'),
    ('东风本田汽车有限公司', '长风汽车制造有限公司'),
    ('路凯包装运营（上海）有限公司', '环通循环包装运营（上海）有限公司'),
    ('宁波华塑包装制品有限公司', '甬城塑业包装制品有限公司'),
    ('苏州联恒五金制品有限公司', '吴越联合五金制品有限公司'),
    ('常州正大塑料托盘厂', '延陵塑料托盘厂'),
    ('上汽大众汽车有限公司', '东海商用汽车有限公司'),
    ('东风锂电科技', '长丰锂电科技'),
    ('上汽通用五菱', '南方汽造'),
    ('吉利汽车', '星河汽车'),
    ('一汽解放', '华骏重卡'),
    ('上汽大众', '东海商用'),
    ('小鹏汽车', '星途新能源'),
    ('东风本田', '长风汽制'),
    ('苏州联恒', '吴越联合'),
    ('常州正大', '延陵托盘'),
    ('王琳总', '沈总'),
    ('袁丽晶', '严丽'),
    ('李国栋', '林国栋'),
    ('王志远', '周志远'),
    ('吕道远', '陆鸣'),
    ('路凯', '环通'),
    ('华塑', '甬城塑业'),
    ('联恒', '吴越'),
    ('正大', '延陵'),
    ('袁工', '严工'),
    ('徐蔚', '徐文'),
    ('王琳', '沈婷'),
    ('王强', '江强'),
    ('陈金', '陈锋'),
    ('赵磊', '邵磊'),
    ('何静', '何雅'),
    ('李静', '李婧'),
    ('袁明', '严明'),
    ('张伟', '张帆'),
]
# 疑似真名碎片（表外扫描·发现须处置）
SUSPECTS = ['吉客云', '瑞迅凯', '一汽', '上汽', '东风', '本田', '小鹏', '吉利', '五菱', '大众']

# 表外派生替换（勘察发现·按任务书规则派生·记失败清单）
DERIVED = [
    ('宁波华塑', '甬城塑业'),          # 长词特例：与全称族一致（先于 华塑）
    ('林芳', '林岚'),
    ('孙建军', '孙建平'),
    ('吴海涛', '吴海川'),
    ('郑卫东', '郑卫平'),
    ('FAW-BX-0970', 'HJ-BX-0970'),     # 一汽英文缩写痕迹（products.innerCode）
    ('吉客云', '捷科云'),               # 第三方系统真名（登录页 brand-tag+A05）
    ('wangqiang', 'jiangqiang'),        # 真名拼音账号（users.search·随人名映射派生）
    ('chenjin', 'chenfeng'),
    ('liguodong', 'linguodong'),
    ('zhaolei', 'shaolei'),
    ('道远', '陆鸣'),                   # 名字单独引用（吕道远→陆鸣 的同族引用·任重道远=0 已验证）
]

def iter_files():
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f.endswith(('.html', '.js', '.md', '.json', '.css')):
                yield os.path.join(dp, f)

def phase1():
    print('== Phase 1: 危险短词上下文扫描 ==')
    terms = ['路凯', '华塑', '联恒', '正大', '王琳', '王强', '陈金', '赵磊', '何静', '李静', '徐蔚', '袁明', '张伟', '袁工', '袁丽晶', '吕道远', '李国栋', '王志远']
    hits = {}
    for p in iter_files():
        t = io.open(p, encoding='utf-8', newline='').read()
        for term in terms:
            i = t.find(term)
            while i > -1:
                ctx = t[max(0, i-18):i+len(term)+18].replace('\r', '').replace('\n', '⏎')
                hits.setdefault(term, []).append((os.path.relpath(p, ROOT), ctx))
                i = t.find(term, i + len(term))
    for term in terms:
        lst = hits.get(term, [])
        ctxs = sorted(set(c for _, c in lst))
        print('[%s] %d 处 / %d 个上下文' % (term, len(lst), len(ctxs)))
        for c in ctxs[:6]:
            print('    …%s…' % c)
    return hits

def phase2():
    """长词优先精确替换（长度降序·assert 总计数·EOL 不动）"""
    allpairs = PAIRS + DERIVED
    allpairs.sort(key=lambda x: len(x[0]), reverse=True)
    print('== Phase 2: 替换执行（%d 对·长度降序） ==' % len(allpairs))
    totals = {}
    files_touched = set()
    for p in iter_files():
        t = io.open(p, encoding='utf-8', newline='').read()
        orig = t
        for old, new in allpairs:
            if old in t:
                n = t.count(old)
                t = t.replace(old, new)
                totals[old] = totals.get(old, 0) + n
        if t != orig:
            io.open(p, 'w', encoding='utf-8', newline='').write(t)
            files_touched.add(os.path.relpath(p, ROOT))
    print('touched files:', len(files_touched))
    for old, new in allpairs:
        print('  %s -> %s : %d' % (old, new, totals.get(old, 0)))
    assert all(v > 0 for k, v in totals.items() if k in ('一汽解放汽车有限公司', '路凯', '王琳', '张伟', '李国栋')), '核心词计数异常'
    return totals

def phase3():
    """清零扫描：36 映射词 + 派生词原词 + 残留碎片，全部须 0"""
    print('== Phase 3: 残留扫描 ==')
    bad = 0
    words = [o for o, _ in PAIRS] + [o for o, _ in DERIVED] + ['一汽', '上汽', '东风', '本田', '小鹏', '吉利', '五菱', '蔚山基地一汽']
    for w in words:
        n = 0
        where = []
        for p in iter_files():
            t = io.open(p, encoding='utf-8', newline='').read()
            c = t.count(w)
            if c:
                n += c
                where.append((os.path.relpath(p, ROOT), c))
        flag = 'OK(0)' if n == 0 else 'RESIDUE=%d' % n
        if n:
            bad += 1
            for rel, c in where[:3]:
                print('  [%-14s] %s in %s x%d' % (w, flag, rel, c))
        else:
            print('  [%-14s] OK(0)' % w)
    print('RESIDUE WORDS:', bad)
    return bad

def phase4():
    """一致性抽样：同一实体跨文件表述一致"""
    print('== Phase 4: 一致性抽样 ==')
    checks = [
        ('华骏重卡汽车有限公司', ['_data/demo-data.js', '基础数据/客商管理.html']),
        ('环通循环包装运营（上海）有限公司', ['_data/demo-data.js']),
        ('星途新能源汽车科技有限公司', ['_data/demo-data.js', '基础数据/客商管理.html']),
        ('延陵塑料托盘厂', ['_data/demo-data.js', '基础数据/客商管理.html']),
        ('沈婷', ['_data/demo-data.js', '我的待办.html']),
        ('林国栋', ['_data/demo-data.js', '租入管理/租入入库列表.html']),
    ]
    allok = True
    for word, files in checks:
        row = []
        for f in files:
            t = io.open(os.path.join(ROOT, f), encoding='utf-8', newline='').read()
            row.append('%s:%d' % (f.split('/')[-1].split(chr(92))[-1], t.count(word)))
        print('  %-22s %s' % (word, ' '.join(row)))
    return allok

if __name__ == '__main__':
    if '--run' in sys.argv:
        phase2()
        bad = phase3()
        phase4()
        print('PHASE3 RESIDUE WORDS =', bad)
    else:
        phase1()
