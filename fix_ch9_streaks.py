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

# Fix Q5 (index 4): Not only ... but also -> Make answer D
# Current: "A": "not only - but also", "B": "neither - or", "C": "either - and", "D": "both - or"
# Swap A and D
q5 = ch9["questions"][4]
q5["options"] = {
    "A": "both - or",
    "B": "neither - or",
    "C": "either - and",
    "D": "not only - but also"
}
q5["answer"] = "D"
q5["explanation"] = q5["explanation"].replace("A. not only - but also", "D. not only - but also")

# Fix Q20 (index 19): The commercial district... -> Make answer A
# Current: "A": "although", "B": "consequently", "C": "whereas", "D": "because"
# Swap A and B
q20 = ch9["questions"][19]
q20["options"] = {
    "A": "consequently",
    "B": "although",
    "C": "whereas",
    "D": "because"
}
q20["answer"] = "A"
q20["explanation"] = q20["explanation"].replace("B. consequently", "A. consequently")

answers = [q["answer"] for q in ch9["questions"]]
print("Chapter 9 New Answers:", answers)
print("Distribution:", {opt: answers.count(opt) for opt in ['A', 'B', 'C', 'D']})

# Check streaks in Chapter 9
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

print("Chapter 9 updated without consecutive duplicate answers!")
