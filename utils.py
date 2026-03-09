import json
from pathlib import Path

root = Path(r"D:\OneDrive\Desktop\Personal project\Email_Automation\paperlists")  # root folder
output_file = root / "merged.json"

all_objects = []

# rglob('*.json') finds .json in *all* subdirectories
for path in root.rglob("*.json"):   # <- key change
    if path.resolve() == output_file.resolve():
        continue  # skip the merged file itself

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

        if isinstance(data, list):
            all_objects.extend(data)
        elif isinstance(data, dict):
            all_objects.append(data)
        else:
            print(f"Skipping {path} (unexpected JSON type: {type(data)})")

with output_file.open("w", encoding="utf-8") as f:
    json.dump(all_objects, f, ensure_ascii=False, indent=2)

print(f"Merged {len(all_objects)} objects into {output_file}")
