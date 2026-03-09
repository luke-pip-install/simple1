import os
import requests
from urllib.parse import urlparse, parse_qs
import re

INPUT_FILE = "unique_sites.txt"  
OUTPUT_FOLDER = "openreview_pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download(pdf_url, filename_hint=None):
    filename = filename_hint or os.path.basename(urlparse(pdf_url).path) or "paper.pdf"
    out_path = os.path.join(OUTPUT_FOLDER, filename)
    
    if os.path.exists(out_path):
        print(f"Already exists, skipping: {out_path}")
        return
    
    print(f"Downloading {pdf_url} ...")
    r = requests.get(pdf_url)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {out_path}")

with open(INPUT_FILE, "r") as f:
    links = [line.strip() for line in f if line.strip()]

for link in links:
    try:
        parsed = urlparse(link)

        # 1) OpenReview
        if "openreview.net" in parsed.netloc:
            qs = parse_qs(parsed.query)
            paper_id = qs.get("id", [None])[0]
            if not paper_id:
                print(f"Skipping (no id): {link}")
                continue
            pdf_url = f"https://openreview.net/pdf?id={paper_id}"
            filename = f"{paper_id}.pdf"

        # 2) CVF WACV / CVPR (openaccess.thecvf.com)
        elif "openaccess.thecvf.com" in parsed.netloc:
            pdf_url = link.replace("/html/", "/papers/").replace("_paper.html", "_paper.pdf")
            filename = os.path.basename(pdf_url)

        # 3) ACL Anthology
        elif "aclanthology.org" in parsed.netloc:
            base = link
            if base.endswith("/"):
                base = base[:-1]
            pdf_url = f"{base}.pdf"
            filename = os.path.basename(base) + ".pdf"

        # 4) ECCV virtual (eccv2024.ecva.net)
        elif "eccv2024.ecva.net" in parsed.netloc:
            print(f"No direct rule from ECCV virtual URL to PDF: {link}")
            continue

        # 5) IJCAI
        elif "ijcai.org/proceedings" in parsed.path:
            match = re.search(r'/proceedings/(\d+)/(\d+)', parsed.path)
            if match:
                year = match.group(1)
                paper_id = match.group(2).zfill(4)
                pdf_url = f"https://www.ijcai.org/proceedings/{year}/{paper_id}.pdf"
                filename = f"{year}_{paper_id}.pdf"
            else:
                print(f"Skipping IJCAI (no year/id match): {link}")
                continue

        else:
            print(f"Unknown host, skipping: {link}")
            continue

        download(pdf_url, filename)

    except Exception as e:
        print(f"Error with {link}: {e}")
