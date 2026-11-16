
from pathlib import Path
import shutil

root = Path(r"D:\projects\rohil-next-gen\rohil_nextgen_academy")
backup = root / "_backup_before_webp_update"

extensions = {".html", ".css", ".js"}

updated_count = 0

for webp in root.rglob("*.webp"):

    original_name = webp.stem

    for ext in [".png", ".jpg", ".jpeg"]:

        original = webp.with_name(original_name + ext)

        if not original.exists():
            continue

        old_name = original.name
        new_name = webp.name

        for source in root.rglob("*"):

            if not source.is_file():
                continue

            if backup in source.parents:
                continue

            if source.suffix.lower() not in extensions:
                continue

            try:
                content = source.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if old_name not in content:
                    continue

                updated_content = content.replace(
                    old_name,
                    new_name
                )

                if updated_content == content:
                    continue

                relative = source.relative_to(root)
                backup_file = backup / relative

                backup_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                if not backup_file.exists():
                    shutil.copy2(source, backup_file)

                source.write_text(
                    updated_content,
                    encoding="utf-8"
                )

                print(
                    f"UPDATED: {relative} | "
                    f"{old_name} -> {new_name}"
                )

                updated_count += 1

            except Exception as e:
                print("ERROR:", source, e)

print("\nTotal files updated:", updated_count)
print("Backup folder:", backup)
