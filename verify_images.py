
from pathlib import Path
import re

root = Path("rohil_nextgen_academy")
missing = []

for html in root.rglob("*.html"):
    if "_backup" in str(html):
        continue

    content = html.read_text(encoding="utf-8", errors="ignore")

    for src in re.findall(r'<img\b[^>]*?\bsrc=["\']([^"\']+)', content, re.I | re.S):
        if src.startswith(("http://", "https://", "//", "data:", "#")):
            continue

        path = html.parent / src

        if not path.exists():
            missing.append((str(html), src))

print("Missing image paths:", len(missing))

for file, src in missing[:50]:
    print(file, "->", src)
