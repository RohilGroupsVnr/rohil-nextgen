
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "rohil_nextgen_academy"
OPTIMIZED_DIR = SITE_DIR / "optimized-logos"

IMAGE_EXTENSIONS = r"(?:png|jpg|jpeg|jfif|bmp|tif|tiff)"

# Matches ./logos/file.png, ../logos/file.jpg, logos/file.png
PATTERN = re.compile(
    rf'(?P<prefix>(?:\.\.?/)?logos/)'
    rf'(?P<filename>[^"\'?#]+?)'
    rf'\.(?P<ext>{IMAGE_EXTENSIONS})'
    rf'(?P<suffix>[?#][^"\']*)?',
    re.IGNORECASE
)

def update_paths():
    if not OPTIMIZED_DIR.exists():
        print("ERROR: optimized-logos folder not found.")
        print("First run convert_logos.py")
        return

    updated_files = 0
    updated_images = 0
    missing_images = 0

    for html_file in SITE_DIR.rglob("*.html"):

        content = html_file.read_text(
            encoding="utf-8-sig"
        )

        def replace_path(match):
            nonlocal updated_images, missing_images

            prefix = match.group("prefix")
            filename = match.group("filename")
            suffix = match.group("suffix") or ""

            # Find corresponding converted image
            relative_path = Path(filename + ".webp")
            output_file = OPTIMIZED_DIR / relative_path

            # Only update if converted file exists
            if not output_file.exists():
                missing_images += 1
                print(f"MISSING: {output_file}")
                return match.group(0)

            updated_images += 1

            return (
                prefix.replace("logos/", "optimized-logos/")
                + filename
                + ".webp"
                + suffix
            )

        new_content = PATTERN.sub(replace_path, content)

        if new_content != content:
            html_file.write_text(
                new_content,
                encoding="utf-8"
            )

            updated_files += 1
            print(f"UPDATED: {html_file.name}")

    print("\n========== UPDATE SUMMARY ==========")
    print(f"HTML files updated: {updated_files}")
    print(f"Logo paths updated: {updated_images}")
    print(f"Missing converted logos: {missing_images}")
    print("====================================")

if __name__ == "__main__":
    update_paths()
