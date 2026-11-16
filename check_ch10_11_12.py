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
    practice = ch.get("questions", [])
    homework = ch.get("homework", [])
    print(f"\n================ Chapter {ch_id}: {title} ================")
    print(f"Practice questions count: {len(practice)}")
    if practice:
        p_ans = [q.get("answer") for q in practice]
        print(f"Practice answers: {' '.join(p_ans)}")
        print(f"Practice distribution: { {opt: p_ans.count(opt) for opt in ['A', 'B', 'C', 'D']} }")
        # Check streaks
        streaks = []
        curr = 1
        for i in range(1, len(p_ans)):
            if p_ans[i] == p_ans[i-1]:
                curr += 1
            else:
                if curr >= 2:
                    streaks.append((p_ans[i-1], curr))
                curr = 1
        if curr >= 2:
            streaks.append((p_ans[-1], curr))
        print(f"Practice streaks: {streaks}")
        # print first 2 questions as sample
        print("Sample Q1:", practice[0].get("question"), "Ans:", practice[0].get("answer"), practice[0].get("options"))
    
    print(f"Homework questions count: {len(homework)}")
    if homework:
        h_ans = [q.get("answer") for q in homework]
        print(f"Homework answers: {' '.join(h_ans)}")
        print(f"Homework distribution: { {opt: h_ans.count(opt) for opt in ['A', 'B', 'C', 'D']} }")
