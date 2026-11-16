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

# Target pattern with 0 consecutive duplicates and exactly 5 A, 5 B, 5 C, 5 D
TARGET_PATTERN = ['A', 'B', 'C', 'D', 'B', 'A', 'D', 'C', 'A', 'C', 'B', 'D', 'C', 'A', 'D', 'B', 'D', 'A', 'B', 'C']

def shuffle_question_to_target(q, target_key):
    current_key = q["answer"]
    if current_key == target_key:
        return
    
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
    q["explanation"] = q["explanation"].replace(old_prefix, new_prefix)

# Chapters that need balancing & streak removal:
# Chapter 4 (ADVERBS - currently almost all B)
# Chapter 5 (PASSIVE VOICE - streaks of B)
# Chapter 6 (RELATIVE CLAUSES - almost all A)
# Chapter 11 (DETERMINERS - streaks of B)
# Chapter 12 (COMPARISONS - almost all B)
# Chapter 13 (WORD CHOICE - streaks of A and B)
# Chapter 1 (NOUNS - minor streaks)
# Chapter 2 (VERBS - minor streaks)
# Chapter 3 (ADJECTIVES - minor streaks)

target_chapters = [1, 2, 3, 4, 5, 6, 11, 12, 13]

for ch_id in target_chapters:
    ch = next((c for c in data if c.get("id") == ch_id), None)
    if not ch or not ch.get("questions"):
        continue
    
    qs = ch["questions"]
    if len(qs) != 20:
        continue
    
    # We want a diverse permutation of A, B, C, D so each chapter doesn't have the identical answer key
    # Shift TARGET_PATTERN by (ch_id * 3) % 20
    shift = (ch_id * 3) % 20
    pat = TARGET_PATTERN[shift:] + TARGET_PATTERN[:shift]
    
    # Verify no adjacent duplicates
    has_dup = False
    for i in range(1, len(pat)):
        if pat[i] == pat[i-1]:
            has_dup = True
            break
    if has_dup:
        # Fallback to TARGET_PATTERN directly
        pat = list(TARGET_PATTERN)
        
    for idx, q in enumerate(qs):
        shuffle_question_to_target(q, pat[idx])
        
    answers = [q["answer"] for q in qs]
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
        
    print(f"Chapter {ch_id} [{ch.get('title')}]:")
    print(f"   Distribution: { {opt: answers.count(opt) for opt in ['A', 'B', 'C', 'D']} }")
    print(f"   Streaks: {streaks}")
    print(f"   Answers: {' '.join(answers)}")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nSuccessfully updated and balanced questions across all chapters!")
