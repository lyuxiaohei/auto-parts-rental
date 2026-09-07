# -*- coding: utf-8 -*-
"""
任务三e：加行类修复（每页 1 行、日期 09-01~09-05、单号顺延、现有 tag 类、不加 A04 pin）
1) 租出台账：ZL-20260903-034 近月在租行（L1 退租回库 60 套再出租·与 TZRK-20260902-008 贯通）
2) 组合出库：CK-20260903-016 近月已出库行（同上循环链）
3) 组装列表：ZZ-20260904-007 L2 再组装行（承接 CX-20260902-006 拆散 50 套·循环闭环）
4) 退租申请：TZSQ-20260904-009 部分退租行（退 200 / 留 294·关联 ZL-20260312-0088）
5) 开票登记：INV-20260902-013 已红冲行（负数金额·AR-2026-08-PRJ2603）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")

ROWS = {
    "包装管理/租出台账.html": ("ZL-20260903-034", """<tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZL-20260903-034</span></td>
          <td>PRJ-2601</td>
          <td>一汽解放汽车有限公司</td>
          <td>ZH-2601-A × 60 套（退租回库件再出租）</td>
          <td>自有</td>
          <td><span class="td-num">2026-09-03</span></td>
          <td>2026-12-03</td>
          <td><span class="td-num">0 套</span></td>
          <td><span class="tag tag-blue">在租</span></td>
          <td>—</td>
          <td class="sticky-op"><span class="ops"><a onclick="openModal('trackModal')">详情</a><a onclick="go('../包装管理/退租申请列表.html')">退租</a></span></td>
        </tr>
"""),
    "仓储作业/组合出库列表.html": ("CK-20260903-016", """<tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">CK-20260903-016</span></td>
          <td>PRJ-2601</td>
          <td>一汽解放汽车有限公司</td>
          <td><span class="lk">ZL-20260903-034</span></td>
          <td>ZH-2601-A × 60 套（退租回库件循环出库）</td>
          <td>—（租赁出库）</td>
          <td>长春基地一号门</td>
          <td><span class="tag tag-green">已出库</span></td>
          <td>2026-09-03 09:15</td>
          <td class="sticky-op"><span class="ops"><a onclick="openModal('detailModal')">详情</a><a>打印</a><a onclick="openModal('exitConfirmModal')">出库确认</a></span></td>
        </tr>
"""),
    "仓储作业/组装列表.html": ("ZZ-20260904-007", """<tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">ZZ-20260904-007</span></td>
          <td>PRJ-2601</td>
          <td>ZH-2601-A 驾驶室围板箱整箱套件（承接 CX-20260902-006 拆散件再组装）</td>
          <td><span class="tag tag-gray">纯自有</span></td>
          <td><div style="display:flex;align-items:center;gap:8px;">
            <div style="flex:1;height:8px;background:#f0f0f0;border-radius:2px;min-width:70px;"><div style="width:64%;height:100%;background:var(--primary);border-radius:2px;"></div></div>
            <span style="font-size:12px;color:var(--text-2);">32/50</span>
          </div></td>
          <td>自营运营</td>
          <td>刘志强</td>
          <td>2026-09-04 08:30</td>
          <td><span class="tag tag-blue">组装中</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="openModal('auditModal')">组装确认</a><a onclick="openModal('detailModal')">详情</a><a onclick="go('../仓储作业/组装录单.html')">录单</a></span></td>
        </tr>
"""),
    "包装管理/退租申请列表.html": ("TZSQ-20260904-009", """<tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">TZSQ-20260904-009</span></td>
          <td><span class="lk">ZL-20260312-0088</span></td>
          <td>一汽解放汽车有限公司</td>
          <td>PRJ-2601</td>
          <td>ZH-2601-A 驾驶室围板箱套件（部分退租 · 退 200 / 留 294）</td>
          <td><span class="td-num">200 套</span></td>
          <td>2026-09-04</td>
          <td>2026-09-06</td>
          <td>—</td>
          <td><span class="tag tag-orange">待审核</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="openModal('auditModal')">审核</a><a onclick="openModal('auditModal')">驳回</a></span></td>
        </tr>
"""),
    "财务协同/开票登记.html": ("INV-20260902-013", """<tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">INV-20260902-013</span></td>
          <td>26119800421390</td>
          <td><span class="tag tag-blue">专票</span></td>
          <td>上汽大众汽车有限公司宁波分公司</td>
          <td>AR-2026-08-PRJ2603</td>
          <td><span class="td-num"><b>-46,800.00</b></span></td>
          <td>13%</td>
          <td>2026-09-02</td>
          <td><span class="tag tag-red">已红冲</span></td>
          <td class="sticky-op"><span class="ops"><a onclick="openModal('detailModal')">详情</a><a onclick="go('../财务协同/应收账单.html')">查看账单</a></span></td>
        </tr>
"""),
}

def main():
    BK.mkdir(parents=True, exist_ok=True)
    for f, (num, row) in ROWS.items():
        p = ROOT / f
        b = p.read_bytes()
        dst = BK / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        nb_ = num.encode("utf-8")
        if nb_ in b:
            print(f"{f}: {num} 已存在，跳过")
            continue
        anchor = b"<tbody>"
        i = b.find(anchor)
        assert i != -1, f"{f} 无 tbody"
        # 只插主列表 tbody（第一个 tbody 即主表）
        insert_at = i + len(anchor)
        nl = "\r\n" if b[insert_at:insert_at+2] == b"\r\n" else "\n"
        row_b = row.replace("\n", nl).encode("utf-8") + b"        "
        nb2 = b[:insert_at] + row_b + b[insert_at:]
        # assert：新单号恰 1 次；tbody 后紧跟新行
        assert nb2.count(nb_) == 1, f"{f} 新单号计数异常"
        p.write_bytes(nb2)
        print(f"{f}: +1 行 {num}")

if __name__ == "__main__":
    main()
