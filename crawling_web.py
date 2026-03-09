import os
import requests
from urllib.parse import urlparse, parse_qs
import re

INPUT_FILE = "sites.txt"  
OUTPUT_FOLDER = "openreview_pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download(pdf_url, filename_hint=None):
    print(f"Downloading {pdf_url} ...")
    r = requests.get(pdf_url)
    r.raise_for_status()
    filename = filename_hint or os.path.basename(urlparse(pdf_url).path) or "paper.pdf"
    out_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {out_path}")

with open(INPUT_FILE, "r") as f:
    links = [line.strip() for line in f if line.strip()]

for link in links:
    try:
        parsed = urlparse(link)

        # OpenReview
        if "openreview.net" in parsed.netloc:
            qs = parse_qs(parsed.query)
            paper_id = qs.get("id", [None])[0]
            if not paper_id:
                print(f"Skipping (no id): {link}")
                continue
            pdf_url = f"https://openreview.net/pdf?id={paper_id}"
            filename = f"{paper_id}.pdf"

        #  CVF WACV / CVPR 
        elif "openaccess.thecvf.com" in parsed.netloc:
            pdf_url = link.replace("/html/", "/papers/").replace("_paper.html", "_paper.pdf")
            filename = os.path.basename(pdf_url)

        # ACL Anthology
        elif "aclanthology.org" in parsed.netloc:
            # https://aclanthology.org/2024.emnlp-main.877/
            base = link
            if base.endswith("/"):
                base = base[:-1]
            pdf_url = f"{base}.pdf"
            filename = os.path.basename(base) + ".pdf"

        # ECCV virtual 
        elif "eccv2024.ecva.net" in parsed.netloc:

            print(f"No direct rule from ECCV virtual URL to PDF: {link}")
            continue

        # IJCAI
        elif "ijcai.org/proceedings" in parsed.path:
            # https://www.ijcai.org/proceedings/2024/652 -> https://www.ijcai.org/proceedings/2024/0652.pdf
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
