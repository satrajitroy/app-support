#!/usr/bin/env python3

import sys
import ssl
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

START = sys.argv[1] if len(sys.argv) > 1 else \
    "https://www.simulationmcmc.com/app-support/"

TIMEOUT = 20


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs = dict(attrs)
            if "href" in attrs:
                self.links.append(attrs["href"])
        elif tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def fetch(url):
    req = Request(
        url,
        headers={"User-Agent": "AppSupportLinkChecker/1.0"}
    )

    with urlopen(
        req,
        timeout=TIMEOUT,
        context=ssl._create_unverified_context()
    ) as r:
        return (
            getattr(r, "status", 200),
            r.headers.get("Content-Type", ""),
            r.read(),
            r.geturl(),
        )


start = START if START.endswith("/") else START + "/"

parsed = urlparse(start)
allowed_host = parsed.netloc.lower()
allowed_prefix = parsed.path.rstrip("/") + "/"

queue = deque([start])
seen = set()

results = []
broken = []
directory_listings = []
missing_titles = []
external = set()

while queue:
    url = queue.popleft()
    url, _ = urldefrag(url)

    if url in seen:
        continue

    seen.add(url)

    try:
        status, ctype, body, final = fetch(url)
        final, _ = urldefrag(final)

        text = body.decode("utf-8", errors="replace")
        results.append((url, status, final))

        if status != 200:
            broken.append((url, f"HTTP {status}"))
            continue

        low = text.lower()

        if "<title>index of " in low or "<h1>index of " in low:
            directory_listings.append(url)

        if "text/html" not in ctype.lower() and not final.endswith("/"):
            continue

        parser = LinkParser()
        parser.feed(text)

        if not parser.title.strip():
            missing_titles.append(url)

        for href in parser.links:
            href = href.strip()

            if not href:
                continue

            if href.startswith((
                "#",
                "mailto:",
                "tel:",
                "javascript:",
                "data:"
            )):
                continue

            absolute = urljoin(final, href)
            absolute, _ = urldefrag(absolute)

            ap = urlparse(absolute)

            if ap.scheme not in ("http", "https"):
                continue

            if ap.netloc.lower() != allowed_host:
                external.add(absolute)
                continue

            if not ap.path.startswith(allowed_prefix):
                external.add(absolute)
                continue

            if absolute not in seen:
                queue.append(absolute)

    except HTTPError as e:
        broken.append((url, f"HTTP {e.code}"))

    except URLError as e:
        broken.append((url, f"URL error: {e.reason}"))

    except Exception as e:
        broken.append((url, f"{type(e).__name__}: {e}"))


print()
print("=== APP SUPPORT SITE CHECK ===")
print("Start:", start)
print("Pages checked:", len(seen))

print()
print("--- Internal pages ---")
for url, status, final in sorted(results):
    redirect = "" if url == final else f" -> {final}"
    print(f"[{status}] {url}{redirect}")

print()
print("--- Broken internal links/pages ---")
if broken:
    for url, why in broken:
        print("FAIL", url, f"({why})")
else:
    print("None")

print()
print("--- Directory listings ---")
if directory_listings:
    for url in directory_listings:
        print("FAIL", url)
else:
    print("None")

print()
print("--- Missing <title> ---")
if missing_titles:
    for url in missing_titles:
        print("WARN", url)
else:
    print("None")

print()
print("--- External links found (not crawled) ---")
if external:
    for url in sorted(external):
        print(url)
else:
    print("None")


expected = [
    urljoin(start, "privacy/"),
    urljoin(start, "puzzles/sudoku/"),
    urljoin(start, "puzzles/word-search/"),
    urljoin(start, "puzzles/polyomino/"),
    urljoin(start, "schedules/childcare/"),
]

known_ok = {
    url
    for url, status, final in results
    if status == 200
}

print()
print("--- Expected top-level destinations ---")
for url in expected:
    print(("OK   " if url in known_ok else "MISS ") + url)

failed = (
    bool(broken)
    or bool(directory_listings)
    or any(url not in known_ok for url in expected)
)

print()
print("RESULT:", "FAIL" if failed else "PASS")

sys.exit(1 if failed else 0)
