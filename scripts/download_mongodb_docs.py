import re
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

manifest_files = [
    Path("/tmp/mongodb-manual-1.txt"),
    Path("/tmp/mongodb-manual-2.txt"),
    Path("/tmp/mongodb-manual-4.txt"),
]

topics = (
    "/crud/",
    "/indexes/",
    "/aggregation",
    "/connect",
    "/core/",
    "/databases-and-collections",
    "/transactions",
)

output_dir = Path("data/raw/mongodb")

urls = set()

for manifest_file in manifest_files:
    text = manifest_file.read_text(encoding="utf-8")
    for url in re.findall(r"https://www\.mongodb\.com/docs/[^\s)]+\.md", text):
        if any(topic in url for topic in topics):
            urls.add(url)

import certifi
import ssl

ssl_context = ssl.create_default_context(cafile=certifi.where())

for url in sorted(urls):
    relative_path = url.split("/docs/", 1)[1]
    output_path = output_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"Already exists, skipping: {output_path}")
        continue

    print(f"Downloading {url}")

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "DevDocs-Assistant/1.0"},
        )

        with urllib.request.urlopen(
            request,
            context=ssl_context,
            timeout=30,
        ) as response:
            output_path.write_bytes(response.read())

    except HTTPError as error:
        print(f"Skipping unavailable page ({error.code}): {url}")

    except URLError as error:
        print(f"Skipping network error: {url} — {error.reason}")

    except Exception as error:
        print(f"Skipping unexpected error: {url} — {error}")

print(f"Downloaded {len(urls)} documentation pages")