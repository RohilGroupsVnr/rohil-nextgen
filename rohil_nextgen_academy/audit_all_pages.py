
from pathlib import Path
import re

root = Path("rohil_nextgen_academy")
backup_names = {
    "_backup_before_image_loading",
    "_backup_before_webp_update"
}

for html in sorted(root.rglob("*.html")):
    if any(part in backup_names for part in html.parts):
        continue

    content = html.read_text(encoding="utf-8", errors="ignore")
    images = re.findall(r"<img\b[^>]*>", content, flags=re.I | re.S)

    lazy = sum(bool(re.search(r'\bloading\s*=\s*["\']lazy["\']', x, re.I)) for x in images)
    eager = sum(bool(re.search(r'\bloading\s*=\s*["\']eager["\']', x, re.I)) for x in images)
    no_loading = len(images) - lazy - eager

    print(
        f"{html.name}: Total={len(images)}, "
        f"Lazy={lazy}, Eager={eager}, No loading={no_loading}"
    )
