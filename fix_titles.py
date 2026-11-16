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

# Find Chapter 8
ch8 = next(ch for ch in data if ch.get("id") == 8)

slide156_items = [
    ("agree to Vo", "đồng ý làm gì"),
    ("decide to Vo", "quyết định làm gì"),
    ("plan to Vo", "lên kế hoạch làm gì"),
    ("hope to Vo", "hy vọng làm gì"),
    ("expect to Vo", "mong đợi làm gì"),
    ("want to Vo", "muốn làm gì"),
    ("need to Vo", "cần làm gì"),
    ("offer to Vo", "đề nghị làm gì"),
    ("refuse to Vo", "từ chối làm gì"),
    ("promise to Vo", "hứa làm gì"),
    ("attempt to Vo", "cố gắng làm gì"),
    ("intend to Vo", "có ý định làm gì"),
    ("arrange to Vo", "sắp xếp làm gì"),
    ("prepare to Vo", "chuẩn bị làm gì"),
    ("fail to Vo", "thất bại trong việc làm gì"),
    ("manage to Vo", "xoay xở làm gì"),
    ("choose to Vo", "chọn làm gì"),
    ("afford to Vo", "có đủ khả năng làm gì"),
    ("aim to Vo", "nhắm đến việc làm gì"),
    ("seek to Vo", "tìm cách làm gì")
]

slide158_items = [
    ("avoid Ving", "tránh làm gì"),
    ("consider Ving", "cân nhắc làm gì"),
    ("finish Ving", "hoàn thành việc gì"),
    ("enjoy Ving", "thích làm gì"),
    ("suggest Ving", "đề xuất làm gì"),
    ("recommend Ving", "đề xuất làm gì"),
    ("mind Ving", "phiền làm gì"),
    ("postpone Ving", "trì hoãn làm gì"),
    ("delay Ving", "trì hoãn làm gì"),
    ("deny Ving", "phủ nhận làm gì"),
    ("risk Ving", "mạo hiểm làm gì"),
    ("practice Ving", "luyện tập làm gì"),
    ("keep Ving", "tiếp tục làm gì"),
    ("stop Ving", "ngừng làm gì"),
    ("admit Ving", "thừa nhận làm gì"),
    ("appreciate Ving", "cảm kích việc gì"),
    ("mention Ving", "đề cập việc gì"),
    ("discuss Ving", "thảo luận việc gì"),
    ("involve Ving", "liên quan đến việc gì"),
    ("include Ving", "bao gồm việc gì")
]

slide160_items = [
    ("ask s.o to Vo", "yêu cầu ai làm gì"),
    ("tell s.o to Vo", "bảo ai làm gì"),
    ("advise s.o to Vo", "khuyên ai làm gì"),
    ("encourage s.o to Vo", "khuyến khích ai làm gì"),
    ("remind s.o to Vo", "nhắc ai làm gì"),
    ("require s.o to Vo", "yêu cầu ai làm gì"),
    ("allow s.o to Vo", "cho phép ai làm gì"),
    ("permit s.o to Vo", "cho phép ai làm gì"),
    ("invite s.o to Vo", "mời ai làm gì"),
    ("expect s.o to Vo", "mong đợi ai làm gì"),
    ("want s.o to Vo", "muốn ai làm gì"),
    ("need s.o to Vo", "cần ai làm gì"),
    ("urge s.o to Vo", "thúc giục ai làm gì"),
    ("force s.o to Vo", "buộc ai làm gì")
]

slide165_items = [
    ("tobe unlikely to Vo", "không có khả năng làm gì"),
    ("tobe eager to Vo", "háo hức làm gì"),
    ("tobe pleased to Vo", "vui khi làm gì"),
    ("tobe happy to Vo", "vui khi làm gì"),
    ("tobe disappointed to Vo", "thất vọng khi làm gì"),
    ("tobe difficult to Vo", "khó làm gì"),
    ("tobe easy to Vo", "dễ làm gì"),
    ("tobe important to Vo", "quan trọng để làm gì"),
    ("tobe necessary to Vo", "cần thiết để làm gì"),
    ("tobe convenient to Vo", "thuận tiện để làm gì")
]

slide168_items = [
    ("effort to Vo", "nỗ lực làm gì"),
    ("right to Vo", "quyền làm gì"),
    ("permission to Vo", "sự cho phép làm gì"),
    ("chance to Vo", "cơ hội làm gì"),
    ("time to Vo", "thời gian để làm gì")
]

slide172_items = [
    ("be encouraged to Vo", "được khuyến khích làm gì"),
    ("be advised to Vo", "được khuyên làm gì"),
    ("be permitted to Vo", "được cho phép làm gì"),
    ("be invited to Vo", "được mời làm gì")
]

def render_verb_grid(items, theme_class=""):
    html = '<div class="verb-pattern-grid">'
    for phrase, meaning in items:
        parts = phrase.split(" to ")
        if len(parts) == 2:
            verb_display = f'<span class="hl-vocab">{parts[0]}</span> to {parts[1]}'
        elif " V-ing" in phrase or " Ving" in phrase:
            v_part = phrase.replace(" V-ing", "").replace(" Ving", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> Ving'
        elif " s.o to Vo" in phrase:
            v_part = phrase.replace(" s.o to Vo", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> s.o to Vo'
        elif phrase.startswith("tobe "):
            adj_part = phrase.replace("tobe ", "").replace(" to Vo", "")
            verb_display = f'tobe <span class="hl-vocab">{adj_part}</span> to Vo'
        else:
            verb_display = f'<span class="hl-vocab">{phrase}</span>'

        html += f'''<div class="verb-pattern-item {theme_class}">
    <div class="verb-phrase"><i class="fa-solid fa-circle-check" style="font-size: 0.8rem; opacity: 0.7;"></i> {verb_display}</div>
    <div class="verb-meaning">{meaning}</div>
</div>'''
    html += '</div>'
    return html

for slide in ch8["slides"]:
    s_idx = slide.get("slide_index")
    if s_idx == 156:
        slide["title"] = "CÁC ĐỘNG TỪ ĐI VỚI TO VO"
        slide["html_content"] = render_verb_grid(slide156_items, "")
        print("Updated Slide 156")
    elif s_idx == 158:
        slide["title"] = "CÁC ĐỘNG TỪ ĐI VỚI V-ING"
        slide["html_content"] = render_verb_grid(slide158_items, "theme-purple")
        print("Updated Slide 158")
    elif s_idx == 160:
        slide["title"] = "CẤU TRÚC V + O + TO VO"
        slide["html_content"] = render_verb_grid(slide160_items, "theme-pink")
        print("Updated Slide 160")
    elif s_idx == 165:
        slide["title"] = "CẤU TRÚC TOBE + ADJ + TO VO"
        slide["html_content"] = render_verb_grid(slide165_items, "theme-orange")
        print("Updated Slide 165")
    elif s_idx == 168:
        slide["title"] = "CẤU TRÚC NOUN + TO VO"
        slide["html_content"] = render_verb_grid(slide168_items, "theme-purple") + '<br><strong>EXAMPLE:</strong><br>She has the <strong><span class="hl-red">ability </span></strong><strong>to lead</strong> a team.<br>Employees have the <strong><span class="hl-red">opportunity </span></strong><strong>to attend</strong> training courses.<br>Visitors need <strong><span class="hl-red">permission </span></strong><strong>to enter</strong> the building.<br>Everyone has the <strong><span class="hl-red">right</span></strong> <strong>to express </strong>an opinion.'
        print("Updated Slide 168")
    elif s_idx == 172:
        slide["title"] = "CẤU TRÚC BỊ ĐỘNG + TO VO"
        slide["html_content"] = render_verb_grid(slide172_items, "theme-orange") + '<br><strong>EXAMPLE:</strong><br>All employees <strong><span class="hl-red">are required to attend</span></strong> the training.<br>The report <strong><span class="hl-red">is expected to be completed</span></strong> by Friday.<br>The meeting <strong><span class="hl-red">is scheduled to begin</span></strong> at 9 a.m.<br>Visitors are <strong><span class="hl-red">not allowed to enter</span></strong> this area.'
        print("Updated Slide 172")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Slide titles and first items fixed successfully!")
