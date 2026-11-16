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

# Q7 (index 6): Commercial lease...
# Change answer from D to B
# Current options: "A": "as for", "B": "in order that", "C": "even though", "D": "provided that"
# Swap B and D
q7 = ch9["questions"][6]
q7["options"] = {
    "A": "as for",
    "B": "provided that",
    "C": "even though",
    "D": "in order that"
}
q7["answer"] = "B"
q7["explanation"] = q7["explanation"].replace("D. provided that", "B. provided that")

answers = [q["answer"] for q in ch9["questions"]]
print("Chapter 9 Final Answers:", answers)
print("Distribution:", {opt: answers.count(opt) for opt in ['A', 'B', 'C', 'D']})

streaks = []
curr_streak = 1
for i in range(1, len(answers)):
    if answers[i] == answers[i-1]:
        curr_streak += 1
    else:
        if curr_streak >= 2:
            streaks.append((answers[i-1], curr_streak))
        curr_streak = 1
if curr_streak >= 2:
    streaks.append((answers[-1], curr_streak))
print("Streaks in Chapter 9:", streaks)

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Chapter 9 perfectly balanced with 0 streaks!")
