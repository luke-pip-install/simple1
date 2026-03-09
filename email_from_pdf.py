import os
import re
import json
import fitz  # PyMuPDF: pip install PyMuPDF
from pathlib import Path

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

def extract_emails_from_pdf(pdf_path):
    """Extract all unique emails from a single PDF file."""
    emails = set()
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        # Extract text from all pages
        for page in doc:
            full_text += page.get_text()
        
        doc.close()
        
        # Find all email matches
        matches = EMAIL_REGEX.findall(full_text)
        emails.update(matches)
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    
    return emails

def process_pdf_folder(folder_path):
    """Process all PDF files in a folder and save emails to JSON."""
    folder = Path(folder_path)
    all_results = {}
    
    # Find all PDF files
    pdf_files = list(folder.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        emails = extract_emails_from_pdf(pdf_file)
        if emails:
            all_results[pdf_file.name] = sorted(list(emails))
            print(f"  Found {len(emails)} emails")
        else:
            all_results[pdf_file.name] = []
            print("  No emails found")
    
    # Save to JSON file - just emails organized by filename
    output_file = "openview_emails.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to {output_file}")
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Total emails: {sum(len(e) for e in all_results.values())}")
    
    return all_results

if __name__ == "__main__":
    folder_path = r'D:\OneDrive\Desktop\Personal project\Email_Automation\openreview_pdfs'
    
    if not os.path.exists(folder_path):
        print("Folder not found!")
    else:
        process_pdf_folder(folder_path)
