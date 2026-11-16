
from pathlib import Path
import re

root = Path("rohil_nextgen_academy")

targets = [
    "img19.webp",
    "img25.webp",
    "img26.webp",
    "rohil_nextgen-removebg-preview.png"
]

all_files = [
    f for f in root.rglob("*")
    if f.is_file() and "_backup" not in str(f)
]

for target in targets:
    stem = Path(target).stem

    print(f"\nSearching for: {target}")

    matches = [
        f for f in all_files
        if f.stem.lower() == stem.lower()
    ]

    if matches:
        for match in matches:
            print("FOUND:", match)
    else:
        print("NOT FOUND anywhere")
