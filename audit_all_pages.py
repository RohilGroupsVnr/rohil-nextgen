from pathlib import Path
import re

root = Path("rohil_nextgen_academy")

for html in sorted(root.rglob("*.html")):
    if any("_backup" in part for part in html.parts):
        continue

    content = html.read_text(encoding="utf-8", errors="ignore")
    images = re.findall(r"<img\b[^>]*>", content, re.I | re.S)

    lazy = sum(bool(re.search(r'\bloading\s*=\s*["\']lazy["\']', x, re.I)) for x in images)
    eager = sum(bool(re.search(r'\bloading\s*=\s*["\']eager["\']', x, re.I)) for x in images)
    no_loading = len(images) - lazy - eager

    print(f"{html.name}: Total={len(images)}, Lazy={lazy}, Eager={eager}, No loading={no_loading}")

print("\nAudit completed!")
