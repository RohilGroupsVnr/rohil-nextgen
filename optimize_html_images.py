
from pathlib import Path
import re
import shutil

ROOT = Path(r"D:\projects\rohil-next-gen\rohil_nextgen_academy")
BACKUP = ROOT / "_backup_before_image_loading"

# Only process actual website HTML files.
# Ignore backup folders.
SKIP_DIRS = {
    "_backup_before_image_loading",
    "_backup_before_webp_update"
}

updated_files = 0
updated_images = 0
skipped_images = 0

def optimize_img(match):
    global updated_images, skipped_images

    tag = match.group(0)

    # Skip tracking pixels and empty/dynamic image tags.
    if 'display:none' in tag.replace(" ", "").lower():
        skipped_images += 1
        return tag

    if not re.search(r'\bsrc\s*=\s*["\'][^"\']+["\']', tag, re.I):
        skipped_images += 1
        return tag

    # Keep existing loading priority if already specified.
    has_loading = re.search(r'\bloading\s*=', tag, re.I)

    # Identify likely above-the-fold / priority images.
    priority = (
        'fetchpriority="high"' in tag.lower()
        or 'class="hero' in tag.lower()
        or 'class="banner' in tag.lower()
        or 'class="logo' in tag.lower()
    )

    if not has_loading:
        loading = 'eager' if priority else 'lazy'
        tag = tag[:-1] + f' loading="{loading}">'

    # Add async decoding if not already specified.
    if not re.search(r'\bdecoding\s*=', tag, re.I):
        tag = tag[:-1] + ' decoding="async">'

    if tag != match.group(0):
        updated_images += 1

    return tag


for html in ROOT.rglob("*.html"):

    if any(part in SKIP_DIRS for part in html.parts):
        continue

    try:
        original = html.read_text(encoding="utf-8")
    except Exception as e:
        print("READ ERROR:", html, e)
        continue

    updated = re.sub(
        r'<img\b[^>]*>',
        optimize_img,
        original,
        flags=re.I | re.S
    )

    if updated != original:
        relative = html.relative_to(ROOT)
        backup_file = BACKUP / relative

        backup_file.parent.mkdir(parents=True, exist_ok=True)

        if not backup_file.exists():
            shutil.copy2(html, backup_file)

        html.write_text(updated, encoding="utf-8")

        updated_files += 1
        print("UPDATED:", relative)

print("\nOptimization completed!")
print("HTML files updated:", updated_files)
print("Image tags updated:", updated_images)
print("Skipped image tags:", skipped_images)
print("Backup location:", BACKUP)
