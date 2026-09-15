
import sys, io
sys.argv = [sys.argv[0], "出货单打印"]
exec(io.open(r"_scan_tmpdir/audit_interaction.py", encoding="utf-8").read())
