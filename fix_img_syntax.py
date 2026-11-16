
from pathlib import Path
import re

root = Path("rohil_nextgen_academy")
fixed = 0

for file in root.rglob("*.html"):
    if "_backup" in str(file):
        continue

    content = file.read_text(encoding="utf-8", errors="ignore")

    updated = re.sub(
        r'\s+/\s+(?=(?:loading|decoding)\s*=)',
        ' ',
        content,
        flags=re.I
    )

    if updated != content:
        file.write_text(updated, encoding="utf-8")
        fixed += 1
        print("FIXED:", file)

print("\nFiles corrected:", fixed)
