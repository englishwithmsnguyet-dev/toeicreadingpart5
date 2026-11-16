import re
import os

data_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_reading_web/js/data.js"

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define new contents
slide_101_new_html = '<strong><span class=\\"hl-green\\">LƯU Ý CHUNG:</span></strong><br>▪ <strong>Động từ chính</strong> trong câu bị động <strong>KHÔNG CHIA THEO THÌ</strong>, mà luôn ở dạng <strong>V3ed</strong>.<br>▪ <strong>Động từ tobe</strong> trong câu bị động <strong>PHẢI CHIA THEO THÌ</strong> và phải phù hợp với <strong>CHỦ TỪ</strong>.<br>▪ <strong>“by + O”</strong> được lược bỏ khi <strong>tác nhân không quan trọng, không xác định hoặc mang tính chung chung</strong> (people, someone, they, we, you, the police, the government, experts...); <strong><em>giữ lại khi cần nhấn mạnh người thực hiện</em></strong>.'
slide_102_new_html = '<strong>🔵 Hiện tại đơn:</strong> S + am / is / are + V3ed + [by O].<br><strong>🔵 Hiện tại tiếp diễn:</strong> S + am / is / are + being + V3ed + [by O].<br><strong>🔵 Hiện tại hoàn thành:</strong> S + have / has + been + V3ed + [by O].<br><strong>🔵 Hiện tại hoàn thành tiếp diễn:</strong> S + have / has + been + being + V3ed + [by O].<br><strong>🔵 Quá khứ đơn:</strong> S + was / were + V3ed + [by O].<br><strong>🔵 Quá khứ tiếp diễn:</strong> S + was / were + being + V3ed + [by O].<br><strong>🔵 Quá khứ hoàn thành:</strong> S + had + been + V3ed + [by O].<br><strong>🔵 Quá khứ hoàn thành tiếp diễn:</strong> S + had + been + being + V3ed + [by O].'
slide_103_new_html = '<strong>🔵 Tương lai đơn:</strong> S + will + be + V3ed + [by O].<br><strong>🔵 Tương lai gần:</strong> S + am / is / are + going to + be + V3ed + [by O].<br><strong>🔵 Tương lai tiếp diễn:</strong> S + will be + being + V3ed + [by O].<br><strong>🔵 Tương lai hoàn thành:</strong> S + will + have + been + V3ed + [by O].<br><strong>🔵 Tương lai hoàn thành tiếp diễn:</strong> S + will + have + been + being + V3ed + [by O].'

# We'll use regex to find slide 101, 102, 103 and replace their title and html_content
def replace_slide(content, slide_index, new_title, new_html):
    pattern = r'(\{\s*"slide_index":\s*' + str(slide_index) + r',\s*"title":\s*")[^"]+("\s*,\s*"is_html":\s*true\s*,\s*"html_content":\s*")[^"]+("\s*\})'
    
    # We might need to handle the case where html_content could contain quotes, but in this JSON it's usually escaped
    # Let's use a simpler pattern
    pattern = r'("slide_index":\s*' + str(slide_index) + r',\s*"title":\s*")[^"]+("\s*,\s*"is_html":\s*true\s*,\s*"html_content":\s*")[^"]+("\s*)'
    
    replacement = r'\g<1>' + new_title + r'\g<2>' + new_html + r'\g<3>'
    
    new_content, count = re.subn(pattern, replacement, content)
    if count == 0:
        print(f"Failed to replace slide {slide_index}")
    else:
        print(f"Successfully replaced slide {slide_index}")
    return new_content

content = replace_slide(content, 101, "LƯU Ý CHUNG", slide_101_new_html)
content = replace_slide(content, 102, "CẤU TRÚC THEO CÁC THÌ (HT & QK)", slide_102_new_html)
content = replace_slide(content, 103, "CẤU TRÚC THEO CÁC THÌ (TƯƠNG LAI)", slide_103_new_html)

with open(data_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
