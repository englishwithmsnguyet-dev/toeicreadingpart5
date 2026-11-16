import json
import re

data_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_reading_web/js/data.js"

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
if not match:
    print("Could not find json data.")
    exit(1)

prefix = match.group(1)
json_str = match.group(2)
data = json.loads(json_str)

# Find Chapter 7
ch7 = next(ch for ch in data if ch.get("id") == 7)

for slide in ch7["slides"]:
    if slide.get("slide_index") == 145:
        # Convert from broken is_example to normal theory slide
        q_html = slide.get("question_html", "")
        slide.clear()
        slide["slide_index"] = 145
        slide["title"] = "9. A number of / The number of"
        slide["is_html"] = True
        slide["html_content"] = q_html
        print("Successfully fixed Slide 145 in Chapter 7!")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done.")
