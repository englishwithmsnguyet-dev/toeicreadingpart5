import json
import re

data_path = "js/data.js"
with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
data = json.loads(match.group(2))
ch10 = next(c for c in data if c.get("id") == 10)

# Q13 (index 12):
# question: "Please ensure that you read the safety handbook before ______ the laboratory."
# options: {'A': 'enter', 'B': 'entering', 'C': 'to enter', 'D': 'entered'}
# answer: 'B'
# Swap B and C so answer becomes C
q13 = ch10["questions"][12]
q13["options"] = {
    "A": "enter",
    "B": "to enter",
    "C": "entering",
    "D": "entered"
}
q13["answer"] = "C"
q13["explanation"] = q13["explanation"].replace("B. entering", "C. entering")

answers = [q["answer"] for q in ch10["questions"]]
print("Chapter 10 New Answers:", answers)

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
print("Streaks in Chapter 10:", streaks)

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Chapter 10 updated!")
