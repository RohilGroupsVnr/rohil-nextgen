
from pathlib import Path
from PIL import Image, ImageOps
import io

# Source and output folders
BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "rohil_nextgen_academy" / "logos"
OUTPUT_DIR = BASE_DIR / "rohil_nextgen_academy" / "optimized-logos"

# Supported image formats
SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png", ".jfif",
    ".bmp", ".tif", ".tiff"
}

QUALITY = 85

def convert_logos():
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source folder not found: {SOURCE_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    converted = 0
    failed = 0
    skipped = 0

    for file_path in SOURCE_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            skipped += 1
            print(f"SKIPPED: {file_path.name}")
            continue

        try:
            # Preserve subfolder structure
            relative_path = file_path.relative_to(SOURCE_DIR)
            output_path = OUTPUT_DIR / relative_path.with_suffix(".webp")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with Image.open(file_path) as img:
                img = ImageOps.exif_transpose(img)

                # Preserve transparency when present
                has_alpha = (
                    "A" in img.getbands()
                    or "transparency" in img.info
                )

                if has_alpha:
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                save_options = {
                    "format": "WEBP",
                    "quality": QUALITY,
                    "method": 6
                }

                # Preserve embedded colour profile if available
                icc_profile = img.info.get("icc_profile")
                if icc_profile:
                    save_options["icc_profile"] = icc_profile

                img.save(output_path, **save_options)

            converted += 1
            print(f"CONVERTED: {file_path.name} -> {output_path.name}")

        except Exception as error:
            failed += 1
            print(f"FAILED: {file_path.name} | {error}")

    print("\n========== LOGO CONVERSION SUMMARY ==========")
    print(f"Successfully converted: {converted}")
    print(f"Skipped files: {skipped}")
    print(f"Failed files: {failed}")
    print(f"Output folder: {OUTPUT_DIR}")
    print("=============================================")


if __name__ == "__main__":
    convert_logos()
