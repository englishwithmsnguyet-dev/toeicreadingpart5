import json
import re

data_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_reading_web/js/data.js"

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

# Try to find "const toeicReadingData = ["
match = re.search(r'(const\s+toeicReadingData\s*=\s*)(\[[\s\S]+\]);?\s*$', content)
if match:
    prefix = match.group(1)
    json_str = match.group(2)
    try:
        data = json.loads(json_str)
        chapter = next(ch for ch in data if ch.get("id") == 5)
        
        slide_101_new_html = '<strong><span class="hl-green">LƯU Ý CHUNG:</span></strong><br>▪ <strong>Động từ chính</strong> trong câu bị động <strong>KHÔNG CHIA THEO THÌ</strong>, mà luôn ở dạng <strong>V3ed</strong>.<br>▪ <strong>Động từ tobe</strong> trong câu bị động <strong>PHẢI CHIA THEO THÌ</strong> và phải phù hợp với <strong>CHỦ TỪ</strong>.<br>▪ <strong>“by + O”</strong> được lược bỏ khi <strong>tác nhân không quan trọng, không xác định hoặc mang tính chung chung</strong> (people, someone, they, we, you, the police, the government, experts...); <strong><em>giữ lại khi cần nhấn mạnh người thực hiện</em></strong>.'
        slide_102_new_html = '<strong>🔵 Hiện tại đơn:</strong> S + am / is / are + V3ed + [by O].<br><strong>🔵 Hiện tại tiếp diễn:</strong> S + am / is / are + being + V3ed + [by O].<br><strong>🔵 Hiện tại hoàn thành:</strong> S + have / has + been + V3ed + [by O].<br><strong>🔵 Hiện tại hoàn thành tiếp diễn:</strong> S + have / has + been + being + V3ed + [by O].<br><strong>🔵 Quá khứ đơn:</strong> S + was / were + V3ed + [by O].<br><strong>🔵 Quá khứ tiếp diễn:</strong> S + was / were + being + V3ed + [by O].<br><strong>🔵 Quá khứ hoàn thành:</strong> S + had + been + V3ed + [by O].<br><strong>🔵 Quá khứ hoàn thành tiếp diễn:</strong> S + had + been + being + V3ed + [by O].'
        slide_103_new_html = '<strong>🔵 Tương lai đơn:</strong> S + will + be + V3ed + [by O].<br><strong>🔵 Tương lai gần:</strong> S + am / is / are + going to + be + V3ed + [by O].<br><strong>🔵 Tương lai tiếp diễn:</strong> S + will be + being + V3ed + [by O].<br><strong>🔵 Tương lai hoàn thành:</strong> S + will + have + been + V3ed + [by O].<br><strong>🔵 Tương lai hoàn thành tiếp diễn:</strong> S + will + have + been + being + V3ed + [by O].'

        for slide in chapter["slides"]:
            if slide.get("slide_index") == 101:
                slide["title"] = "LƯU Ý CHUNG"
                slide["html_content"] = slide_101_new_html
            elif slide.get("slide_index") == 102:
                slide["title"] = "CẤU TRÚC THEO CÁC THÌ (HT & QK)"
                slide["html_content"] = slide_102_new_html
            elif slide.get("slide_index") == 103:
                slide["title"] = "CẤU TRÚC THEO CÁC THÌ (TƯƠNG LAI)"
                slide["html_content"] = slide_103_new_html
                
        new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        # Replace the original json string with the new one
        new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]
        
        with open(data_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Successfully updated via JSON parsing.")
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
else:
    print("Could not find const toeicReadingData = ...")
