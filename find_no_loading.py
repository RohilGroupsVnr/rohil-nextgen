from pathlib import Path
import re

root = Path("rohil_nextgen_academy")

for html in sorted(root.rglob("*.html")):
    if any("_backup" in part for part in html.parts):
        continue

    content = html.read_text(encoding="utf-8", errors="ignore")
    images = re.findall(r"<img\b[^>]*>", content, re.I | re.S)

    for img in images:
        if not re.search(r"\bloading\s*=", img, re.I):
            print(f"\n--- {html.name} ---")
            print(img[:600])
