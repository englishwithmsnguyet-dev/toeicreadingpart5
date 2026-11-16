import json
import re

data_path = "js/data.js"
with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
data = json.loads(match.group(2))
ch10 = next(c for c in data if c.get("id") == 10)
ans = [q["answer"] for q in ch10["questions"]]
print("Chapter 10 answers:", ans)
for idx, q in enumerate(ch10["questions"]):
    a = q["answer"]
    opts = q["options"]
    print(f"Q{idx+1}: ans={a} opts={opts}")
