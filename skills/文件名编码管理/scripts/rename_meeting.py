#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""会议材料批量规范化改名。

用法:
  python rename_meeting.py <原始文件夹> [--theme 主题] [--date YYYY-MM-DD] [--csv 对照表.csv] [--dry-run]

流程: 扫描文件 -> 推断会议日期与主题 -> 按载体判类型 -> 生成改名计划 -> 执行(文件夹占用自动重试) -> 追加对照表(CRLF)。
规则源: D:\\工作台-吕道远\\1-会议材料\\00-命名规则.md
"""
import argparse
import csv
import datetime as dt
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".avi", ".wmv", ".flv", ".ts"}
AUDIO_EXT = {".mp3", ".m4a", ".wav", ".aac", ".flac", ".amr"}
ARCHIVE_EXT = {".rar", ".zip", ".7z"}
NOISE_RE = [
    r"周[一二三四五六日天]\s*\d{1,2}点\d{1,2}分",            # 周三 10点56分
    r"周[一二三四五六日天]",
    r"Video_\d{4}-\d{2}-\d{2}_\d{6}",                          # Video_2026-09-01_100048
    r"\d{8}_\d{6}",                                            # 20260831_143424
    r"\d{4}[-./年]\d{1,2}[-./月]\d{1,2}[日]?(\s*\d{1,2}点\d{1,2}分)?",  # 2026年08月31日 14点31分 / 2026.8.31
    r"_?AI总结",
    r"\s+ai\s+",
    r"[-_][0-9a-f]{8,}$",                                       # 企微下载哈希后缀 -60661269f720
]
WEEKDAY = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}


def sniff_docx(path: Path) -> str:
    """返回 docx 内容特征: transcribe(发言总结/说话人) / summary(纪要) / unknown"""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
        text = re.sub(r"<[^>]*>", "", xml)
        if "发言总结" in text or "说话人" in text:
            return "transcribe"
        for kw in ("本视频讲述", "会议纪要", "要点", "总结"):
            if kw in text[:800]:
                return "summary"
    except Exception:
        pass
    return "unknown"


def probe_archive(path: Path) -> str:
    """bsdtar 探测压缩包内容: video / other / unknown"""
    tar = Path(r"C:\Windows\System32\tar.exe")
    if not tar.exists():
        return "unknown"
    try:
        out = subprocess.run([str(tar), "-tf", str(path)], capture_output=True, text=True, timeout=30)
        names = out.stdout.lower()
        if out.returncode == 0:
            return "video" if any(e in names for e in VIDEO_EXT) else "other"
    except Exception:
        pass
    return "unknown"


def infer_date(names, mtimes) -> tuple[str, str]:
    """返回 (日期前缀, 依据)。优先文件名显式日期 > 周X > mtime(未知日期)。"""
    joined = " ".join(names)
    m = re.search(r"(20\d{2})[-./年](\d{1,2})[-./月](\d{1,2})", joined)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        return f"{y:04d}-{mo:02d}-{d:02d}", "文件名显式日期"
    m = re.search(r"周([一二三四五六日天])", joined)
    if m:
        wd = WEEKDAY[m.group(1)]
        today = dt.date.today()
        delta = (today.weekday() - wd) % 7  # 最近一个匹配的周X（含今天）
        day = today - dt.timedelta(days=delta)
        return day.isoformat(), f"文件名周{m.group(1)}→最近匹配"
    mt = min(mtimes)
    return f"未知日期-{mt:%Y%m%d}", "无日期线索，按 mtime"


def infer_theme(names, theme_arg):
    if theme_arg:
        return theme_arg
    # 取信息量最大的原名（去扩展名后最长者）提炼主题
    best = max(names, key=lambda n: len(re.sub(r"\.[^.]+$", "", n)))
    stem = re.sub(r"\.(m4a|mp3|mp4|wav)$", "", best)  # 修 .m4a.m4a 双扩展
    stem = re.sub(r"\.[^.]+$", "", stem)
    for pat in NOISE_RE:
        stem = re.sub(pat, " ", stem)
    stem = re.sub(r"[\s_]+", "", stem)
    stem = stem.strip("-_－— ")
    if "ai" in stem.lower() and "AI" not in stem:
        stem = re.sub(r"(?i)ai", "AI", stem)
    return stem[:20] or "未命名会议"


def classify(files: list[Path]) -> dict:
    """files -> {tag: [(file, 载体)]}，载体 in {video,audio,other}"""
    groups: dict[str, list] = {}
    for f in files:
        ext = f.suffix.lower()
        carrier = None
        if ext in VIDEO_EXT:
            tag, carrier = "视频", "video"
        elif ext in AUDIO_EXT:
            tag, carrier = "录音", "audio"
        elif ext in ARCHIVE_EXT:
            kind = probe_archive(f)
            if kind == "video":
                tag, carrier = "视频", "video"
            else:
                print(f"  ! 跳过 {f.name}: 压缩包内非视频({kind})，请人工定名")
                continue
        elif ext == ".txt":
            tag, carrier = "转写", "text"
        elif ext in (".docx", ".doc"):
            kind = sniff_docx(f)
            if kind == "summary":
                tag, carrier = "纪要", "text"
            elif kind == "transcribe":
                tag, carrier = "转写", "text"
            else:
                print(f"  ! 跳过 {f.name}: docx 内容无法识别(非发言总结/纪要)")
                continue
        else:
            print(f"  ! 跳过 {f.name}: 未知扩展名 {ext}")
            continue
        groups.setdefault(tag, []).append((f, carrier))
    return groups


def source_prefix(tag: str, carrier: str, groups: dict, name: str) -> str:
    """转写/纪要按来源载体加前缀: 显式扩展名标记 > 同名视频 > 同名音频 > 文件夹内唯一载体 > 不带。"""
    if tag not in ("转写", "纪要"):
        return tag
    if re.search(r"\.(m4a|mp3|wav|aac)\.(txt|docx|doc)$", name, re.I):
        return "音频" + tag  # xxx.m4a.txt = 转写自音频
    base = re.sub(r"(\.(m4a|mp3|mp4|wav|txt|docx|doc))+$", "", name, flags=re.I)
    for other_tag in ("视频", "录音"):
        for f, c in groups.get(other_tag, []):
            if f.stem.startswith(base[:6]):
                return ("视频" if c == "video" else "音频") + tag
    has_video = bool(groups.get("视频"))
    has_audio = bool(groups.get("录音"))
    if has_video and not has_audio:
        return "视频" + tag
    if has_audio and not has_video:
        return "音频" + tag
    return tag  # 来源不明/单一无歧义，不带前缀


def plan(src: Path, args):
    files = sorted(p for p in src.iterdir() if p.is_file())
    usable, skipped = [], []
    for f in files:
        if f.name.endswith((".qkdownloading",)) or f.name.lower() in ("desktop.ini", "thumbs.db"):
            print(f"  ! 跳过 {f.name}: 下载中/系统文件")
            skipped.append(f)
        else:
            usable.append(f)
    if not usable:
        sys.exit("无可处理文件")
    names = [f.name for f in usable]
    date_prefix, date_basis = infer_date(names, [f.stat().st_mtime for f in usable])
    if args.date:
        date_prefix, date_basis = args.date, "命令行指定"
    theme = infer_theme(names, args.theme)
    groups = classify(usable)

    new_folder = f"{date_prefix} {theme}"
    actions = []  # (原Path, 新名)
    for tag, items in groups.items():
        items.sort(key=lambda x: x[0].stat().st_mtime)
        for i, (f, carrier) in enumerate(items):
            suffix = "" if i == 0 else f"~{i + 1}"
            full_tag = source_prefix(tag, carrier, groups, f.name) if tag in ("转写", "纪要") else tag
            actions.append((f, f"{date_prefix} {theme} [{full_tag}]{suffix}{f.suffix.lower()}"))
    return date_prefix, date_basis, theme, new_folder, actions


def execute(src: Path, new_folder: str, actions, csv_path: Path, dry: bool):
    rows = []
    for f, new_name in actions:
        rows.append((f, new_name))
    if dry:
        for f, new_name in actions:
            print(f"  {f.name}  ->  {new_name}")
        print(f"  文件夹: {src.name}  ->  {new_folder}")
        return
    # 1) 文件就地改名（避开文件夹占用问题）
    for f, new_name in actions:
        f.rename(f.with_name(new_name))
    # 2) 文件夹改名，占用则重试
    target = src.with_name(new_folder)
    for i in range(5):
        try:
            src.rename(target)
            break
        except OSError:
            if i == 4:  # 兜底: 建目标夹搬文件
                target.mkdir(exist_ok=True)
                for p in src.iterdir():
                    shutil.move(str(p), str(target / p.name))
                try:
                    src.rmdir()
                except OSError:
                    print(f"  ! 空壳文件夹被占用未删: {src}")
            else:
                time.sleep(1)
    # 3) 对照表追加（CRLF, 原 UTF-8 带头不动）
    exists = csv_path.exists()
    with open(csv_path, "a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        if not exists:
            w.writerow(["原路径", "新路径"])
        for f, new_name in actions:
            w.writerow([str(f), str(target / new_name)])
        w.writerow([str(src), str(target)])
    print(f"完成: {target}")


def main():
    ap = argparse.ArgumentParser(description="会议材料规范化改名")
    ap.add_argument("src", help="含原始会议文件的文件夹")
    ap.add_argument("--theme", help="覆盖自动推断的主题")
    ap.add_argument("--date", help="覆盖日期, 格式 YYYY-MM-DD")
    ap.add_argument("--csv", default=r"D:\工作台-吕道远\1-会议材料\改名对照表.csv")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    src = Path(args.src)
    if not src.is_dir():
        sys.exit(f"不是文件夹: {src}")
    date_prefix, date_basis, theme, new_folder, actions = plan(src, args)
    print(f"日期: {date_prefix}（{date_basis}）  主题: {theme}")
    execute(src, new_folder, actions, Path(args.csv), args.dry_run)


if __name__ == "__main__":
    main()
