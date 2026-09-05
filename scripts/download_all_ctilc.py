from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

PAGE_URL = "https://ctilc.iec.cat/scripts/CTILCCorpus_Descarr.asp"
DOWNLOAD_BASE = "https://ctilc.iec.cat/scripts/CTILCCorpus_DescarrF.asp?fitxer="
RAW_DIR = Path("data/raw")

RAW_DIR.mkdir(parents=True, exist_ok=True)

response = requests.get(PAGE_URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

filenames = []

for tag in soup.find_all("a", onclick=True):
    onclick = tag.get("onclick", "")

    match = re.search( r"obredoc\('([^']+)'\)", onclick)

    if match:
        filenames.append(match.group(1))

filenames = list(dict.fromkeys(filenames))

print(f"Files found: {len(filenames)}")

downloaded = 0
skipped = 0
failed = 0

for i, filename in enumerate(filenames, start=1):

    output_path = RAW_DIR / filename

    if output_path.exists():
        skipped += 1
        print(f"[{i}/{len(filenames)}] SKIP {filename}")
        continue

    url = DOWNLOAD_BASE + quote(filename)

    try:
        r = requests.get(url, timeout=30)

        r.raise_for_status()
        text = r.text

        if "<OBRA" not in text or "<TEXT>" not in text:
            failed += 1
            print(f"[{i}/{len(filenames)}] INVALID {filename}")
            continue

        output_path.write_text(text, encoding="utf-8")

        downloaded += 1

        print(f"[{i}/{len(filenames)}] OK {filename}")

    except Exception as e:
        failed += 1
        print(f"[{i}/{len(filenames)}] FAILED {filename}: {e}")

print("\n=== DONE ===")
print(f"Downloaded: {downloaded}")
print(f"Skipped:    {skipped}")
print(f"Failed:     {failed}")