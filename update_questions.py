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

# Find chapter 7 (SỰ HÒA HỢP CHỦ VỊ)
chapter = next(ch for ch in data if ch.get("id") == 7)

# The questions are in slides that have is_example=True or maybe in tests?
# Wait, let's look at how the questions are structured.
# The user's screenshot shows "Câu hỏi 15 / 20", which means it's a test or a long quiz.
# Ah, it's inside chapter 7, but probably in a specific slide that has a list of questions, or it's a test?
# Let's find where the question is in the json.

for slide in chapter["slides"]:
    if "questions" in slide:
        for q in slide["questions"]:
            if "The design team" in q.get("question", "") and "to present their ideas" in q.get("question", ""):
                q["question"] = "The marketing department ______ to launch a new promotional campaign next month."
                q["options"] = {
                    "A": "plans",
                    "B": "plan",
                    "C": "planning",
                    "D": "are planning"
                }
                q["answer"] = "A"
                q["explanation"] = "<strong>Đáp án đúng: <span class=\"hl-green\">A. plans</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Danh từ tập hợp 'The marketing department' (Phòng tiếp thị) được coi là một tổ chức duy nhất, thực hiện hành động như một thể thống nhất nên động từ chia ở dạng số ít -> chọn 'plans'.<br>- Do đó, ta chọn phương án <strong class=\"hl-vocab\">plans</strong>.<br><br><strong>Dịch câu:</strong><br><em>Phòng tiếp thị lên kế hoạch ra mắt chiến dịch khuyến mãi mới vào tháng tới.</em>"
                print("Updated design team question.")
                
            if "The statistics published by" in q.get("question", ""):
                q["question"] = "Statistics ______ considered a challenging subject by many university students."
                q["options"] = {
                    "A": "is",
                    "B": "are",
                    "C": "were",
                    "D": "have been"
                }
                q["answer"] = "A"
                q["explanation"] = "<strong>Đáp án đúng: <span class=\"hl-green\">A. is</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Danh từ 'Statistics' (môn thống kê) kết thúc bằng -s nhưng thuộc nhóm danh từ chỉ môn học (số ít) nên động từ chính chia ở dạng số ít -> chọn 'is'.<br>- Do đó, ta chọn phương án <strong class=\"hl-vocab\">is</strong>.<br><br><strong>Dịch câu:</strong><br><em>Môn thống kê được coi là một môn học đầy thử thách bởi nhiều sinh viên đại học.</em>"
                print("Updated statistics question.")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done.")
