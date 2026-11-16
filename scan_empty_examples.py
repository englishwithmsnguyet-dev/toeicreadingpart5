import json
import re

data_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_reading_web/js/data.js"

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
if not match:
    print("Could not find json data.")
    exit(1)

data = json.loads(match.group(2))

print("=== CHECKING FOR EMPTY OPTIONS / MISCLASSIFIED EXAMPLES ===")
for ch in data:
    ch_id = ch.get("id")
    for slide in ch.get("slides", []):
        s_idx = slide.get("slide_index")
        s_title = slide.get("title", "")
        if slide.get("is_example"):
            opts = slide.get("options", {})
            if not opts or len(opts) == 0:
                print(f"Chapter {ch_id} - Slide {s_idx} ({s_title}) has is_example=True but empty options!")
