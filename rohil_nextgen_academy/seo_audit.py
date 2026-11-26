"""
SEO audit for a static HTML website.
Run inside the project folder:   python seo_audit.py
Creates seo_report.csv  (open in Excel / Google Sheets).
Only reads files - changes nothing.
"""
import csv
import os
import re
import sys
from collections import Counter
from html import unescape

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SITE = "https://www.rohilnextgen.com/"
SKIP_DIRS = {"node_modules", ".git", ".vscode"}


def read(path):
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return ""


def first(pattern, text):
    m = re.search(pattern, text, re.I | re.S)
    return unescape(m.group(1).strip()) if m else ""


def visible_words(html):
    body = re.search(r"<body.*?>(.*)</body>", html, re.I | re.S)
    text = body.group(1) if body else html
    text = re.sub(r"<(script|style|noscript|svg)\b.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"[A-Za-z0-9]{2,}", unescape(text)))


pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for name in filenames:
        if name.lower().endswith(".html"):
            pages.append(os.path.relpath(os.path.join(dirpath, name), ROOT).replace("\\", "/"))

existing = {p.lower() for p in pages}
rows = []
for page in sorted(pages):
    html = read(os.path.join(ROOT, page))
    title = first(r"<title[^>]*>(.*?)</title>", html)
    desc = first(r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']', html)
    canon = first(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', html)
    h1 = len(re.findall(r"<h1\b", html, re.I))
    words = visible_words(html)

    broken = set()
    for href in re.findall(r'href=["\']([^"\'#?]+\.html)', html, re.I):
        if href.startswith(("http://", "https://")):
            if not href.startswith(SITE):
                continue
            href = href[len(SITE):]
        target = os.path.normpath(os.path.join(os.path.dirname(page), href.lstrip("/"))).replace("\\", "/")
        if target.lower() not in existing:
            broken.add(href)

    rows.append(dict(page=page, title=title, desc=desc, canon=canon, h1=h1, words=words, broken=sorted(broken)))

title_count = Counter(r["title"].lower() for r in rows if r["title"])
desc_count = Counter(r["desc"].lower() for r in rows if r["desc"])

out = []
for r in rows:
    problems = []
    if " " in r["page"]:
        problems.append("SPACE IN FILE NAME")
    if not r["title"]:
        problems.append("no title")
    elif title_count[r["title"].lower()] > 1:
        problems.append("duplicate title")
    if not r["desc"]:
        problems.append("no description")
    elif desc_count[r["desc"].lower()] > 1:
        problems.append("duplicate description")
    expected = SITE + r["page"]
    if not r["canon"]:
        problems.append("no canonical")
    elif r["canon"] != expected and not (r["page"] == "index.html" and r["canon"] in (SITE, SITE.rstrip("/"))):
        problems.append("canonical points elsewhere")
    if r["h1"] == 0:
        problems.append("no h1")
    elif r["h1"] > 1:
        problems.append(f"{r['h1']} h1 tags")
    if r["words"] < 300:
        problems.append("THIN CONTENT (<300 words)")
    if r["broken"]:
        problems.append(f"{len(r['broken'])} broken link(s)")

    out.append([r["page"], r["words"], len(problems), "; ".join(problems),
                " | ".join(r["broken"]), r["title"], r["canon"]])

out.sort(key=lambda x: (-x[2], x[1]))
with open(os.path.join(ROOT, "seo_report.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Page", "Word count", "Problem count", "Problems", "Broken links", "Title", "Canonical"])
    w.writerows(out)

thin = sum(1 for r in rows if r["words"] < 300)
broken_pages = sum(1 for r in rows if r["broken"])
print(f"Checked {len(rows)} pages")
print(f"  Thin content (<300 words): {thin}")
print(f"  Pages with broken links:   {broken_pages}")
print(f"  Duplicate titles:          {sum(1 for c in title_count.values() if c > 1)}")
print("Report saved: seo_report.csv")
