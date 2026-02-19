from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import json
from multiprocessing import Pool, cpu_count

# Path to your scanned PDF
pdf_path = "Hamdard_Naunehal_July_2017_Paksociety_com.pdf"

# Convert PDF pages to images (high accuracy)
pages = convert_from_path(pdf_path, dpi=500)

# Function to OCR a single page
def ocr_page(args):
    page_number, page_image = args
    try:
        # OCR with Urdu language
        text = pytesseract.image_to_string(page_image, lang="urd")
    except:
        # Fallback if Urdu OCR fails
        text = pytesseract.image_to_string(page_image)
    return {"page": page_number, "text": text.strip()}

# Prepare arguments for multiprocessing
args = [(i+1, page) for i, page in enumerate(pages)]

# Use 2 cores for multiprocessing
with Pool(processes=2) as pool:
    results = pool.map(ocr_page, args)

# Save results to JSON
output_file = "ocr_result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"OCR complete! Results saved to {output_file}")