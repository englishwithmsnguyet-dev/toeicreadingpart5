import json
import re

# Balanced distribution pattern with NO adjacent duplicates:
# 5 A, 5 B, 5 C, 5 D
TARGET_PATTERNS = {
    "ch10_practice": ['B', 'C', 'D', 'A', 'B', 'D', 'A', 'C', 'D', 'B', 'A', 'C', 'D', 'A', 'C', 'B', 'C', 'A', 'D', 'B'],
    "ch10_homework": ['C', 'A', 'D', 'B', 'A', 'D', 'B', 'C', 'A', 'C', 'B', 'D', 'C', 'A', 'D', 'B', 'D', 'C', 'A', 'B'],
    "ch11_homework": ['D', 'C', 'B', 'A', 'C', 'D', 'A', 'B', 'D', 'B', 'A', 'C', 'B', 'D', 'A', 'B', 'C', 'A', 'D', 'C'],
    "ch12_homework": ['B', 'A', 'D', 'C', 'A', 'B', 'C', 'D', 'C', 'B', 'A', 'D', 'B', 'C', 'A', 'D', 'B', 'A', 'D', 'C']
}

def rebalance_questions(questions, pattern):
    for idx, q in enumerate(questions):
        target_key = pattern[idx]
        current_key = q["answer"]
        if current_key == target_key:
            continue
        
        opts = q["options"]
        correct_val = opts[current_key]
        target_val = opts[target_key]
        
        # Swap values between current_key and target_key
        opts[current_key] = target_val
        opts[target_key] = correct_val
        q["answer"] = target_key
        
        # Update explanation
        old_prefix = f">{current_key}."
        new_prefix = f">{target_key}."
        if old_prefix in q["explanation"]:
            q["explanation"] = q["explanation"].replace(old_prefix, new_prefix)
        else:
            # Handle possible format variations like "B. entering"
            q["explanation"] = re.sub(r'([A-D])\.\s*', f'{target_key}. ', q["explanation"], count=1)

data_path = "js/data.js"
with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
data = json.loads(match.group(2))

# 1. Chapter 10 Practice & Homework
ch10 = next(c for c in data if c.get("id") == 10)
rebalance_questions(ch10["questions"], TARGET_PATTERNS["ch10_practice"])
rebalance_questions(ch10["homework"], TARGET_PATTERNS["ch10_homework"])

# 2. Chapter 11 Homework
ch11 = next(c for c in data if c.get("id") == 11)
rebalance_questions(ch11["homework"], TARGET_PATTERNS["ch11_homework"])

# 3. Chapter 12 Homework
ch12 = next(c for c in data if c.get("id") == 12)
rebalance_questions(ch12["homework"], TARGET_PATTERNS["ch12_homework"])

# Audit
for ch_id in [10, 11, 12]:
    ch = next(c for c in data if c.get("id") == ch_id)
    for q_type in ["questions", "homework"]:
        qs = ch.get(q_type, [])
        ans = [q["answer"] for q in qs]
        dist = {opt: ans.count(opt) for opt in ['A', 'B', 'C', 'D']}
        streaks = []
        curr = 1
        for i in range(1, len(ans)):
            if ans[i] == ans[i-1]:
                curr += 1
            else:
                if curr >= 2:
                    streaks.append((ans[i-1], curr))
                curr = 1
        if curr >= 2:
            streaks.append((ans[-1], curr))
        print(f"Ch{ch_id} {q_type.upper()}: dist={dist} | streaks={streaks} | ans={' '.join(ans)}")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nSuccessfully updated data.js!")
