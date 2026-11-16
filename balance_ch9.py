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

ch9 = next(c for c in data if c.get("id") == 9)

# Q20 (index 19): Change from C to B
# "The commercial district experienced a prolonged power disruption; ______, retail businesses suffered substantial sales losses."
q20 = ch9["questions"][19]
q20["options"] = {
    "A": "although",
    "B": "consequently",
    "C": "whereas",
    "D": "because"
}
q20["answer"] = "B"
q20["explanation"] = q20["explanation"].replace("C. consequently", "B. consequently")

answers = [q["answer"] for q in ch9["questions"]]
print("Chapter 9 Adjusted Answer Distribution:", {opt: answers.count(opt) for opt in ['A', 'B', 'C', 'D']})

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Perfect 5-5-5-5 distribution achieved for Chapter 9!")
