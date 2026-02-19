import json
import pandas as pd

# -------- Load JSON Data --------
input_file = "all_urdu_moral_stories.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------- Convert to DataFrame --------
df = pd.DataFrame(data)

# -------- Save as CSV --------
csv_file = "all_urdu_moral_stories.csv"
df.to_csv(csv_file, index=False, encoding="utf-8-sig")  # utf-8-sig ensures Excel reads Urdu correctly

# -------- Save as XLSX --------
xlsx_file = "all_urdu_moral_stories.xlsx"
df.to_excel(xlsx_file, index=False, engine="openpyxl")

print(f"✅ JSON converted to CSV ({csv_file}) and XLSX ({xlsx_file}) successfully!")