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

for ch_id in range(1, len(data) + 1):
    ch = next((c for c in data if c.get("id") == ch_id), None)
    if ch and ch.get("questions"):
        ans = [q.get("answer") for q in ch["questions"]]
        # find streaks
        streaks = []
        curr_streak = 1
        for i in range(1, len(ans)):
            if ans[i] == ans[i-1]:
                curr_streak += 1
            else:
                if curr_streak >= 2:
                    streaks.append((ans[i-1], curr_streak, i - curr_streak + 1, i))
                curr_streak = 1
        if curr_streak >= 2:
            streaks.append((ans[-1], curr_streak, len(ans) - curr_streak + 1, len(ans)))
        print(f"Chapter {ch_id} [{ch.get('title')}]: {len(ans)} questions, streaks: {streaks}")
        print(f"   Answers: {' '.join(ans)}")
