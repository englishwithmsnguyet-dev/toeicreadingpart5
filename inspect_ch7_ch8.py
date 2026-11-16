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

for ch_id in [7, 8]:
    ch = next(c for c in data if c.get("id") == ch_id)
    questions = ch.get("questions", [])
    print(f"\n--- Chapter {ch_id}: {ch.get('title')} ({len(questions)} questions) ---")
    answers = [q.get("answer") for q in questions]
    print("Answers:", answers)
    for idx, q in enumerate(questions):
        print(f"Q{idx+1}: {q.get('question')} | Ans: {q.get('answer')} | Opts: {q.get('options')}")
