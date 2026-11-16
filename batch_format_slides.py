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

def format_suffix_slide(html):
    # Pattern: <strong><span class="...">HEADER</span></strong><br> followed by lines like:
    # <strong class="hl-vocab">word</strong> /ipa/ – meaning
    lines = [l.strip() for l in html.split("<br>") if l.strip()]
    if not lines:
        return html
    
    header_line = lines[0]
    items = []
    
    # Try parsing items
    for line in lines[1:]:
        # Match: word, optional ipa, meaning
        # Example: <strong class="hl-vocab">economist</strong> /ɪˈkɑːnəmɪst/ – nhà kinh tế
        # Or: <strong class="hl-vocab">approval</strong> /əˈpruːvəl/ – sự chấp thuận
        m = re.match(r'<strong[^>]*>([^<]+)</strong>\s*(/[^/]+/)?\s*[–\-—:]\s*(.+)', line)
        if m:
            word = m.group(1).strip()
            ipa = m.group(2).strip() if m.group(2) else ""
            meaning = m.group(3).strip()
            items.append((word, ipa, meaning))
        else:
            # Check if line without html tags
            clean = re.sub(r'<[^>]+>', '', line).strip()
            m2 = re.match(r'([a-zA-Z\-\s]+)\s*(/[^/]+/)?\s*[–\-—:]\s*(.+)', clean)
            if m2:
                word = m2.group(1).strip()
                ipa = m2.group(2).strip() if m2.group(2) else ""
                meaning = m2.group(3).strip()
                items.append((word, ipa, meaning))

    if len(items) >= 3:
        # Extract title from header
        clean_header = re.sub(r'<[^>]+>', '', header_line).strip()
        new_html = f'<div class="suffix-header-badge"><i class="fa-solid fa-bookmark" style="margin-right: 6px;"></i> {clean_header}</div>'
        new_html += '<div class="suffix-grid">'
        for w, ipa, m in items:
            ipa_html = f'<span class="suffix-ipa">{ipa}</span>' if ipa else ''
            new_html += f'''<div class="suffix-card">
    <div class="suffix-word-row">
        <span class="suffix-word">{w}</span>
        {ipa_html}
    </div>
    <div class="suffix-meaning">{m}</div>
</div>'''
        new_html += '</div>'
        return new_html
    return html

def render_verb_grid(items, theme_class=""):
    html = '<div class="verb-pattern-grid">'
    for phrase, meaning in items:
        # Highlight pattern
        parts = phrase.split(" to ")
        if len(parts) == 2:
            verb_display = f'<span class="hl-vocab">{parts[0]}</span> to {parts[1]}'
        elif " V-ing" in phrase or " Ving" in phrase:
            v_part = phrase.replace(" V-ing", "").replace(" Ving", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> V-ing'
        elif " s.o to Vo" in phrase:
            v_part = phrase.replace(" s.o to Vo", "")
            verb_display = f'<span class="hl-vocab">{v_part}</span> s.o to Vo'
        else:
            verb_display = f'<span class="hl-vocab">{phrase}</span>'

        html += f'''<div class="verb-pattern-item {theme_class}">
    <div class="verb-phrase"><i class="fa-solid fa-circle-check" style="font-size: 0.8rem; opacity: 0.7;"></i> {verb_display}</div>
    <div class="verb-meaning">{meaning}</div>
</div>'''
    html += '</div>'
    return html

# 1. Update Chapter 1 (Noun Suffixes: slides 7 to 19)
ch1 = next(ch for ch in data if ch.get("id") == 1)
for slide in ch1["slides"]:
    s_idx = slide.get("slide_index")
    if 7 <= s_idx <= 19:
        slide["html_content"] = format_suffix_slide(slide["html_content"])
        print(f"Updated Ch1 Slide {s_idx}")

# 2. Update Chapter 3 (Adjective Suffixes: slides 59 to 69)
ch3 = next(ch for ch in data if ch.get("id") == 3)
for slide in ch3["slides"]:
    s_idx = slide.get("slide_index")
    if 59 <= s_idx <= 69:
        slide["html_content"] = format_suffix_slide(slide["html_content"])
        print(f"Updated Ch3 Slide {s_idx}")

# 3. Update Chapter 8 (Gerunds & Infinitives: slide 162, 163, 168, 171, 172)
ch8 = next(ch for ch in data if ch.get("id") == 8)
for slide in ch8["slides"]:
    s_idx = slide.get("slide_index")
    if s_idx == 162:
        items = [
            ("look forward to V-ing", "mong chờ làm gì"),
            ("be committed to V-ing", "cam kết làm gì"),
            ("be dedicated to V-ing", "tận tâm với việc gì"),
            ("be used to V-ing", "quen với việc gì")
        ]
        slide["html_content"] = 'Không phải sau <strong>to</strong> lúc nào cũng dùng <strong>V</strong><strong>o</strong>. Trong một số cụm cố định, <strong>to</strong> là giới từ, nên sau nó dùng <strong>V</strong><strong>ing</strong>.<br>Cấu trúc: <strong><span class="hl-cyan">to + V-ing</span></strong><br><strong>Các cụm thường gặp:</strong>' + render_verb_grid(items, "theme-pink")
        print("Updated Ch8 Slide 162")
    elif s_idx == 163:
        items = [
            ("get used to V-ing", "dần quen với việc gì"),
            ("object to V-ing", "phản đối việc gì"),
            ("contribute to V-ing", "góp phần vào việc gì"),
            ("lead to V-ing", "dẫn đến việc gì")
        ]
        slide["html_content"] = render_verb_grid(items, "theme-pink") + '<br><strong>EXAMPLE:</strong><br>We <strong><span class="hl-red">look forward to </span></strong><strong>working</strong> with you.<br>The company <strong><span class="hl-red">is committed to </span></strong><strong>providing</strong> excellent service.<br>The new policy <strong><span class="hl-red">contributed to </span></strong><strong>reducing</strong> costs.'
        print("Updated Ch8 Slide 163")
    elif s_idx == 168:
        items = [
            ("effort to Vo", "nỗ lực làm gì"),
            ("right to Vo", "quyền làm gì"),
            ("permission to Vo", "sự cho phép làm gì"),
            ("chance to Vo", "cơ hội làm gì"),
            ("time to Vo", "thời gian để làm gì")
        ]
        slide["html_content"] = render_verb_grid(items, "theme-purple") + '<br><strong>EXAMPLE:</strong><br>She has the <strong><span class="hl-red">ability </span></strong><strong>to lead</strong> a team.<br>Employees have the <strong><span class="hl-red">opportunity </span></strong><strong>to attend</strong> training courses.<br>Visitors need <strong><span class="hl-red">permission </span></strong><strong>to enter</strong> the building.<br>Everyone has the <strong><span class="hl-red">right</span></strong> <strong>to express </strong>an opinion.'
        print("Updated Ch8 Slide 168")
    elif s_idx == 171:
        items = [
            ("be required to Vo", "được yêu cầu làm gì"),
            ("be expected to Vo", "được mong đợi làm gì"),
            ("be asked to Vo", "được yêu cầu làm gì"),
            ("be allowed to Vo", "được cho phép làm gì"),
            ("be scheduled to Vo", "được lên lịch làm gì"),
            ("be supposed to Vo", "được cho là / phải làm gì")
        ]
        slide["html_content"] = 'Cấu trúc: <strong><span class="hl-cyan">be + V3ed + to Vo</span></strong><br><strong>Các cụm thường gặp:</strong>' + render_verb_grid(items, "theme-orange")
        print("Updated Ch8 Slide 171")
    elif s_idx == 172:
        items = [
            ("be encouraged to Vo", "được khuyến khích làm gì"),
            ("be advised to Vo", "được khuyên làm gì"),
            ("be permitted to Vo", "được cho phép làm gì"),
            ("be invited to Vo", "được mời làm gì")
        ]
        slide["html_content"] = render_verb_grid(items, "theme-orange") + '<br><strong>EXAMPLE:</strong><br>All employees <strong><span class="hl-red">are required to attend</span></strong> the training.<br>The report <strong><span class="hl-red">is expected to be completed</span></strong> by Friday.<br>The meeting <strong><span class="hl-red">is scheduled to begin</span></strong> at 9 a.m.<br>Visitors are <strong><span class="hl-red">not allowed to enter</span></strong> this area.'
        print("Updated Ch8 Slide 172")

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("ALL FORMATTING UPGRADES COMPLETED SUCCESSFULLY!")
