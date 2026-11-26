
from pathlib import Path
from urllib.parse import urlparse, unquote, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor
import re
import xml.etree.ElementTree as ET
import shutil

# ---------------- CONFIGURATION ----------------

BASE_URL = "https://www.rohilnextgen.com"

BACKUP_NAMES = {
    "_backup_before_image_loading",
    "_backup_before_webp_update"
}

# Supports running from project parent or project folder
ROOT = (
    Path("rohil_nextgen_academy")
    if Path("rohil_nextgen_academy").exists()
    else Path(__file__).resolve().parent
)

SITEMAP_PATH = ROOT / "sitemap.xml"

# Backup of existing sitemap
BACKUP_PATH = ROOT / "sitemap_backup.xml"

# ------------------------------------------------


def is_backup_file(path):
    return any(part in BACKUP_NAMES for part in path.parts)


def local_html_files():
    files = []

    for html in ROOT.rglob("*.html"):
        if not is_backup_file(html):
            files.append(html)

    return sorted(files)


def file_to_url(html):
    relative = html.relative_to(ROOT).as_posix()

    # Root index.html should use homepage URL
    if relative.lower() == "index.html":
        return BASE_URL + "/"

    # Folder index.html should use folder URL
    if relative.lower().endswith("/index.html"):
        relative = relative[:-len("index.html")]

    return BASE_URL + "/" + quote(relative, safe="/-._~")


def normalize_url(url):
    parsed = urlparse(url.strip())

    if parsed.scheme not in ("http", "https"):
        return None

    if parsed.netloc.lower() not in (
        "www.rohilnextgen.com",
        "rohilnextgen.com"
    ):
        return None

    path = unquote(parsed.path or "/")

    # Treat /index.html and / as same homepage
    if path.lower() == "/index.html":
        path = "/"

    return BASE_URL + quote(path, safe="/-._~")


def url_to_local_file(url):
    parsed = urlparse(url)
    relative = unquote(parsed.path).lstrip("/")

    if not relative:
        relative = "index.html"
    elif relative.endswith("/"):
        relative += "index.html"

    file_path = ROOT / relative

    if file_path.is_file() and not is_backup_file(file_path):
        return file_path

    return None


def read_sitemap():
    if not SITEMAP_PATH.exists():
        print("ERROR: sitemap.xml not found:", SITEMAP_PATH)
        return []

    try:
        tree = ET.parse(SITEMAP_PATH)
        root = tree.getroot()

        urls = []

        for element in root.iter():
            if element.tag.endswith("loc") and element.text:
                urls.append(element.text.strip())

        return urls

    except ET.ParseError as error:
        print("ERROR: Invalid sitemap XML:", error)
        return []


def check_http(url):
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "RohilNextGen-Sitemap-Audit/1.0"
            }
        )

        with urlopen(request, timeout=20) as response:
            return {
                "url": url,
                "status": response.status,
                "final_url": response.geturl()
            }

    except HTTPError as error:
        return {
            "url": url,
            "status": error.code,
            "final_url": error.geturl()
        }

    except (URLError, TimeoutError, OSError) as error:
        return {
            "url": url,
            "status": "ERROR",
            "final_url": url,
            "error": str(error)
        }


# ---------------- IMAGE AUDIT ----------------

print("\n========== IMAGE LOADING AUDIT ==========\n")

html_files = local_html_files()

for html in html_files:
    content = html.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    images = re.findall(
        r"<img\b[^>]*>",
        content,
        flags=re.I | re.S
    )

    lazy = sum(
        bool(re.search(
            r'\bloading\s*=\s*["\']lazy["\']',
            x,
            re.I
        ))
        for x in images
    )

    eager = sum(
        bool(re.search(
            r'\bloading\s*=\s*["\']eager["\']',
            x,
            re.I
        ))
        for x in images
    )

    no_loading = len(images) - lazy - eager

    print(
        f"{html.name}: Total={len(images)}, "
        f"Lazy={lazy}, Eager={eager}, "
        f"No loading={no_loading}"
    )


# ---------------- SITEMAP AUDIT ----------------

print("\n========== SITEMAP AUDIT ==========\n")

existing_urls = read_sitemap()

if not existing_urls:
    print(
        "ERROR: No sitemap URLs found. "
        "Check sitemap.xml before continuing."
    )
    raise SystemExit(1)


# Normalize existing URLs and remove duplicates
normalized_existing = []

for url in existing_urls:
    normalized = normalize_url(url)

    if normalized:
        normalized_existing.append(normalized)
    else:
        print("INVALID DOMAIN / URL:", url)

existing_set = set(normalized_existing)


# Find all HTML pages in project
local_pages = {
    file_to_url(html): html
    for html in html_files
}

local_set = set(local_pages)

missing_urls = sorted(local_set - existing_set)
extra_urls = sorted(existing_set - local_set)

print("HTML pages found:", len(local_pages))
print("Existing sitemap URLs:", len(existing_set))
print("Missing URLs:", len(missing_urls))
print("URLs not found in local project:", len(extra_urls))


print("\n--- MISSING HTML URLS ---")

for url in missing_urls:
    print(url)


print("\n--- SITEMAP URLS NOT FOUND LOCALLY ---")

for url in extra_urls:
    print(url)


# ---------------- HTTP STATUS CHECK ----------------

urls_to_check = sorted(existing_set | local_set)

print(
    "\nChecking HTTP status for",
    len(urls_to_check),
    "URLs..."
)

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(
        executor.map(check_http, urls_to_check)
    )

status_map = {
    item["url"]: item
    for item in results
}


print("\n--- HTTP STATUS RESULTS ---")

for item in results:
    print(
        f'{item["status"]}: {item["url"]}'
    )


# ---------------- VALID URL FILTER ----------------

# Include only local HTML URLs returning HTTP 200
valid_urls = []

for url in sorted(local_set):
    result = status_map.get(url)

    if result and result["status"] == 200:
        valid_urls.append(url)


# Identify invalid URLs currently in sitemap
invalid_urls = []

for url in sorted(existing_set):
    result = status_map.get(url)

    if url not in local_set:
        invalid_urls.append(
            (url, "No matching local HTML file")
        )

    elif not result or result["status"] != 200:
        status = (
            result["status"]
            if result
            else "Not checked"
        )

        invalid_urls.append(
            (url, f"HTTP {status}")
        )


# ---------------- FINAL REPORT ----------------

print("\n========== FINAL REPORT ==========")

print("Valid HTTP 200 URLs:", len(valid_urls))
print("Invalid sitemap URLs:", len(invalid_urls))

print("\n--- INVALID URL DETAILS ---")

for url, reason in invalid_urls:
    print(f"{reason}: {url}")


# Stop if no valid URLs are found
if not valid_urls:
    print(
        "\nNo valid URLs found. "
        "Existing sitemap.xml was NOT modified."
    )

    raise SystemExit(1)


# ---------------- BACKUP EXISTING SITEMAP ----------------

if not SITEMAP_PATH.exists():
    print("\nERROR: sitemap.xml does not exist.")
    raise SystemExit(1)

try:
    shutil.copy2(
        SITEMAP_PATH,
        BACKUP_PATH
    )

    print("\nBackup created:")
    print(BACKUP_PATH)

except OSError as error:
    print("\nBackup failed:", error)
    print("Existing sitemap.xml was NOT modified.")
    raise SystemExit(1)


# ---------------- UPDATE EXISTING SITEMAP.XML ----------------

urlset = ET.Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)

for url in valid_urls:
    url_element = ET.SubElement(
        urlset,
        "url"
    )

    ET.SubElement(
        url_element,
        "loc"
    ).text = url


tree = ET.ElementTree(urlset)
ET.indent(tree, space="  ")


# Write to temporary file first, then replace sitemap.xml
TEMP_PATH = ROOT / "sitemap_temp.xml"

try:
    tree.write(
        TEMP_PATH,
        encoding="utf-8",
        xml_declaration=True
    )

    # Validate generated XML before replacing original
    ET.parse(TEMP_PATH)

    TEMP_PATH.replace(SITEMAP_PATH)

    print("\nExisting sitemap.xml updated successfully!")

except (OSError, ET.ParseError) as error:
    print("\nSitemap update failed:", error)

    if TEMP_PATH.exists():
        TEMP_PATH.unlink()

    print("Original sitemap.xml was preserved.")
    raise SystemExit(1)


# ---------------- VERIFY UPDATED SITEMAP ----------------

try:
    ET.parse(SITEMAP_PATH)

    print("\nUpdated sitemap XML validation: PASSED")

except ET.ParseError as error:
    print("\nUpdated sitemap XML validation failed:", error)
    raise SystemExit(1)


print("\n========== COMPLETED ==========")

print("Final sitemap:", SITEMAP_PATH)
print("Total URLs added:", len(valid_urls))
print("Backup file:", BACKUP_PATH)

print("\nOnly sitemap.xml was updated.")
print("No sitemap_corrected.xml was created.")
print("No sitemap-index.xml was created.")
