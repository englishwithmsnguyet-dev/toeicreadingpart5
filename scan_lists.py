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

print("=== SCANNING ALL CHAPTERS FOR PLAIN LISTS / VOCAB PAIRS ===")
for ch in data:
    ch_id = ch.get("id")
    ch_title = ch.get("title")
    for slide in ch.get("slides", []):
        s_idx = slide.get("slide_index")
        s_title = slide.get("title", "")
        html = slide.get("html_content", "")
        
        # Check if contains multiple ":" or " – " or " - " lines (indicative of vocab/collocation lists)
        lines = [l.strip() for l in re.split(r'<br\s*/?>|\n', html) if l.strip()]
        colon_lines = [l for l in lines if (':' in l or ' – ' in l or ' - ' in l) and not l.startswith('<strong>EX') and not l.startswith('EX:') and not l.startswith('Cấu trúc:') and not l.startswith('Dấu hiệu:') and not l.startswith('📌') and not l.startswith('👉') and not l.startswith('🔵') and not l.startswith('▪') and not 'class="verb-pattern-grid"' in html and not 'class="pill-container"' in html]
        
        if len(colon_lines) >= 3 and not slide.get("is_example"):
            print(f"Chapter {ch_id} [{ch_title}] - Slide {s_idx} ({s_title}) -> {len(colon_lines)} list items:")
            for cl in colon_lines[:3]:
                print(f"   • {re.sub('<[^<]+?>', '', cl)[:60]}...")
