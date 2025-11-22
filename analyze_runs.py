import re
from collections import defaultdict
from pathlib import Path

pattern = re.compile(
    r"Polymarket fetch https://clob\.polymarket\.com/price in ([0-9.]+)s params=\{'token_id': '([^']+)', 'side': '(BUY|SELL)'\}"
)
fail_pattern = re.compile(
    r"Polymarket fetch failed in ([0-9.]+)s url=https://clob\.polymarket\.com/price params=\{'token_id': '([^']+)', 'side': '(BUY|SELL)'\}"
)
slow = defaultdict(list)
run_stats = {}

for path in sorted(Path(".").glob("run*.log")):
    raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # Merge multi-line log entries where params or error were wrapped
    lines = []
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        merged = line
        if (
            "Polymarket fetch https://clob.polymarket.com/price" in line
            and "params=" not in line
            and i + 1 < len(raw_lines)
            and raw_lines[i + 1].strip().startswith("params=")
        ):
            merged = f"{line} {raw_lines[i + 1].strip()}"
            i += 1
            if i + 1 < len(raw_lines) and raw_lines[i + 1].strip().startswith("error="):
                merged = f"{merged} {raw_lines[i + 1].strip()}"
                i += 1
        lines.append(merged)
        i += 1
    run = path.stem
    run_slow = []
    for line in lines:
        m = pattern.search(line)
        status = "ok"
        if not m:
            m = fail_pattern.search(line)
            status = "fail" if m else "skip"
        if not m:
            continue
        dur = float(m.group(1))
        token = m.group(2)
        side = m.group(3)
        if dur >= 5 or status == "fail":
            run_slow.append((dur, token, side, status))
            slow[token].append((run, dur, status, side))
    run_stats[run] = run_slow

print("Slow-call counts per run (>=5s or failed):")
for run in sorted(run_stats):
    print(f"  {run}: {len(run_stats[run])} slow calls")

print("\nTop repeated slow tokens:")
for token, entries in sorted(slow.items(), key=lambda kv: -len(kv[1]))[:25]:
    durs = [dur for _, dur, _, _ in entries]
    fails = sum(1 for _, _, status, _ in entries if status == "fail")
    sides = sorted({side for *_, side in entries})
    print(
        f"  token {token[:12]}.. count={len(entries)}, avg={sum(durs)/len(durs):.1f}s, max={max(durs):.1f}s, fails={fails}, sides={','.join(sides)}"
    )

print("\nSample slow events per token:")
for token, entries in sorted(slow.items(), key=lambda kv: -len(kv[1]))[:5]:
    print(
        f"  token {token[:12]}.. ->",
        ", ".join(f"{run} {dur:.1f}s {status}" for run, dur, status, _ in entries[:5]),
    )
