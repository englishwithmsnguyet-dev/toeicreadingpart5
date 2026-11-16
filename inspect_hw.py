import json
import re

data_path = "js/data.js"
with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
data = json.loads(match.group(2))

for ch_id in [10, 11, 12]:
    ch = next(c for c in data if c.get("id") == ch_id)
    title = ch.get("title")
    print(f"\n================ Chapter {ch_id}: {title} HOMEWORK ================")
    for idx, q in enumerate(ch.get("homework", [])):
        print(f"HW {idx+1}: {q.get('question')} | Ans: {q.get('answer')} | Opts: {q.get('options')}")
