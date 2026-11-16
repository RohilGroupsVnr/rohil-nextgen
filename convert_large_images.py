
from pathlib import Path
from PIL import Image

root = Path(r"D:\projects\rohil-next-gen\rohil_nextgen_academy")

files = []

for p in root.rglob("*"):
    if p.is_file() and p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        files.append(p)

files.sort(key=lambda p: p.stat().st_size, reverse=True)

print("Converting top 20 large images...\n")

for p in files[:20]:
    try:
        output = p.with_suffix(".webp")

        if output.exists():
            print("SKIPPED:", p.name, "- WebP already exists")
            continue

        with Image.open(p) as img:
            img.save(
                output,
                "WEBP",
                quality=78,
                method=6
            )

        old_size = p.stat().st_size / 1024
        new_size = output.stat().st_size / 1024

        print(
            f"CONVERTED: {p.relative_to(root)} | "
            f"{old_size:.1f} KB -> {new_size:.1f} KB"
        )

    except Exception as e:
        print("ERROR:", p.name, e)

print("\nConversion completed.")
