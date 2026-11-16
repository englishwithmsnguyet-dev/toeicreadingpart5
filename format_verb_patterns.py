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

chapter8 = next(ch for ch in data if ch.get("id") == 8)

def render_grid(items, theme_class=""):
    html = '<div class="verb-pattern-grid">'
    for phrase, meaning in items:
        parts = phrase.split(" to ")
        if len(parts) == 2:
            verb_display = f'<span class="hl-vocab">{parts[0]}</span> to Vo'
        elif " Ving" in phrase:
            v_part = phrase.replace(" Ving", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> Ving'
        elif " s.o to Vo" in phrase:
            v_part = phrase.replace(" s.o to Vo", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> s.o to Vo'
        elif phrase.startswith("tobe "):
            adj_part = phrase.replace("tobe ", "").replace(" to Vo", "")
            verb_display = f'tobe <span class="hl-vocab">{adj_part}</span> to Vo'
        elif " to Vo" in phrase:
            n_part = phrase.replace(" to Vo", "")
            verb_display = f'<span class="hl-vocab">{n_part}</span> to Vo'
        else:
            verb_display = phrase

        html += f'''<div class="verb-pattern-item {theme_class}">
    <div class="verb-phrase"><i class="fa-solid fa-circle-check" style="font-size: 0.8rem; opacity: 0.7;"></i> {verb_display}</div>
    <div class="verb-meaning">{meaning}</div>
</div>'''
    html += '</div>'
    return html

slide164_items = [
    ("tobe able to Vo", "có thể làm gì"),
    ("tobe ready to Vo", "sẵn sàng làm gì"),
    ("tobe willing to Vo", "sẵn lòng làm gì"),
    ("tobe likely to Vo", "có khả năng làm gì"),
    ("tobe unlikely to Vo", "không có khả năng làm gì")
]

slide165_items = [
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

slide167_items = [
    ("way to Vo", "cách để làm gì"),
    ("opportunity to Vo", "cơ hội làm gì"),
    ("ability to Vo", "khả năng làm gì"),
    ("decision to Vo", "quyết định làm gì")
]

for slide in chapter8["slides"]:
    s_idx = slide.get("slide_index")
    if s_idx == 164:
        slide["html_content"] = f'Nhiều tính từ trong TOEIC đi với <strong>to V</strong><strong>o</strong>.<br>Cấu trúc: <strong><span class="hl-cyan">tobe + adjective + to V</span></strong><br><strong>Các tính từ thường gặp:</strong>' + render_grid(slide164_items, "theme-orange")
        print("Updated slide 164")
    elif s_idx == 165:
        slide["html_content"] = render_grid(slide165_items, "theme-orange")
        print("Updated slide 165")
    elif s_idx == 167:
        slide["html_content"] = f'Một số danh từ thường đi với <strong>to V</strong><strong>o</strong> để chỉ mục đích, nhiệm vụ, quyền, cơ hội hoặc kế hoạch.<br>Cấu trúc: <strong><span class="hl-cyan">noun + to V</span></strong><strong><span class="hl-cyan">o</span></strong><br><strong>Các danh từ thường gặp:</strong>' + render_grid(slide167_items, "theme-purple")
        print("Updated slide 167")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Formatting update complete.")
