import json
import os
import re

# Base paths
pptx_slides_path = "../extracted_reading_slides.json"
highlights_path = "../extracted_highlights.json"

# In case paths are relative to current dir
if not os.path.exists(pptx_slides_path):
    pptx_slides_path = "extracted_reading_slides.json"
    highlights_path = "extracted_highlights.json"

with open(pptx_slides_path, "r", encoding="utf-8") as f:
    raw_slides = json.load(f)

with open(highlights_path, "r", encoding="utf-8") as f:
    raw_highlights = json.load(f)

print(f"Loaded {len(raw_slides)} slides and {len(raw_highlights)} highlight slides.")

# Define Chapter ranges (slide indexes, 1-based)
CHAPTER_RANGES = [
    {"id": 1, "title": "Danh từ (Nouns)", "start": 3, "end": 35},
    {"id": 2, "title": "Động từ (Verbs)", "start": 36, "end": 55},
    {"id": 3, "title": "Tính từ (Adjectives)", "start": 56, "end": 83},
    {"id": 4, "title": "Trạng từ (Adverbs)", "start": 84, "end": 98},
    {"id": 5, "title": "Câu bị động (Passive Voice)", "start": 99, "end": 115},
    {"id": 6, "title": "Mệnh đề quan hệ (Relative Clauses)", "start": 116, "end": 127},
    {"id": 7, "title": "Sự hòa hợp Chủ - Vị (Subject-Verb Agreement)", "start": 128, "end": 151},
    {"id": 8, "title": "Gerunds & Infinitives (Danh động từ & Động từ nguyên mẫu)", "start": 152, "end": 173}
]

def get_chapter_id(slide_num):
    for ch in CHAPTER_RANGES:
        if ch["start"] <= slide_num <= ch["end"]:
            return ch["id"]
    return None

# Parse options helper
def parse_options(text, slide_num):
    # Custom parsing for known PPTX anomalies
    if slide_num == 72:
        return {'A': 'analyze', 'B': 'analysis', 'C': 'analytical', 'D': 'analytically'}
    if slide_num == 87:
        return {'A': 'careful', 'B': 'carefully', 'C': 'care', 'D': 'caring'}
        
    matches = re.findall(r'\(([A-D])\)\s*([^\n\t\(\)]+)', text)
    if len(matches) < 4:
        matches = re.findall(r'\b([A-D])\.\s*([^\n\t\(\)\.]+)', text)
        
    parsed = {}
    for letter, opt_text in matches:
        opt_text = opt_text.strip()
        opt_text = re.sub(r'[\s_]+$', '', opt_text)
        opt_text = re.sub(r'\s{2,}', ' ', opt_text)
        parsed[letter] = opt_text
    return parsed

# Determine correct option based on coordinates
def determine_correct_option(hl, tb, slide_num):
    # Explicit mapping for known hard cases
    if slide_num == 35:
        # Example 1 is C, Example 2 is D
        return "C" if hl["name"] == "Rounded Rectangle 26" else "D"
    if slide_num == 115:
        # Example 1 is A, Example 2 is C
        return "A" if hl["name"] == "Oval 2" else "C"
    if slide_num == 72:
        return "C"
    if slide_num == 87:
        return "B"
        
    # Standard lists
    if slide_num in [105, 106, 107, 108, 109, 110, 111, 112]:
        special_answers = {105: "B", 106: "C", 107: "C", 108: "C", 109: "C", 110: "B", 111: "B", 112: "D"}
        return special_answers.get(slide_num)
        
    vertical_slides = [39, 41, 43, 45, 47, 49, 51, 53, 55, 70, 72, 74, 76, 78, 80, 87, 89, 91, 93]
    
    if slide_num in vertical_slides:
        # Vertical list
        y = hl["y"]
        if y < 5100000:
            return "A"
        elif y < 6100000:
            return "B"
        elif y < 7100000:
            return "C"
        else:
            return "D"
    else:
        # Grid 2x2
        is_left = hl["x"] < 6000000
        is_top = hl["y"] < 7800000
        if is_left and is_top:
            return "A"
        elif (not is_left) and is_top:
            return "B"
        elif is_left and (not is_top):
            return "C"
        else:
            return "D"

# Build structure
chapters_data = {ch["id"]: {"id": ch["id"], "title": ch["title"], "slides": [], "questions": []} for ch in CHAPTER_RANGES}

# Map slides to highlights for quick lookup
highlight_map = {hl["slide"]: hl for hl in raw_highlights}

for slide in raw_slides:
    slide_num = slide["slide_index"]
    ch_id = get_chapter_id(slide_num)
    if not ch_id:
        continue
        
    # Check if this slide is a multiple-choice example slide
    is_example_slide = slide_num in highlight_map
    
    if is_example_slide:
        hl_info = highlight_map[slide_num]
        main_text = hl_info["text"]
        tb = hl_info["tb"]
        highlights = hl_info["highlights"]
        
        # Parse clues and explanations from other text shapes on the slide
        explanation_blocks = []
        for block in slide["blocks"]:
            if block["shape_name"] != "TextBox 20":
                explanation_blocks.append(block["text"].strip())
                
        # Clean explanations
        explanation_text = " ".join(explanation_blocks)
        
        # Handle multi-question slides (Slide 35 and Slide 115)
        if slide_num == 35:
            slide_content = (
                "EXAMPLE 01:\n"
                "That ____ was mentioned in the previous report.\n"
                "  (A) explain          (B) explained\n"
                "  (C) explanation      (D) explaining\n\n"
                "👉 ĐÁP ÁN: C. explanation\n"
                "Giải thích: Cần danh từ số ít làm chủ ngữ sau tính từ chỉ định 'That'.\n\n"
                "EXAMPLE 02:\n"
                "Several ____ were postponed due to budget constraints.\n"
                "  (A) arrange          (B) arranging\n"
                "  (C) arrangement      (D) arrangements\n\n"
                "👉 ĐÁP ÁN: D. arrangements\n"
                "Giải thích: Cần danh từ số nhiều đứng sau từ chỉ số lượng 'Several'."
            )
        elif slide_num == 115:
            slide_content = (
                "1. The marketing team ____ a new strategy to increase sales this quarter.\n"
                "  (A) develops        (B) is developed\n"
                "  (C) developed by    (D) developing\n\n"
                "👉 ĐÁP ÁN: A. develops\n"
                "Giải thích: Chủ ngữ 'The marketing team' chủ động thực hiện hành động chia theo số ít.\n\n"
                "2. The final proposal was ____ to the board for approval.\n"
                "  (A) submit          (B) submitting\n"
                "  (C) submitted       (D) submits\n\n"
                "👉 ĐÁP ÁN: C. submitted\n"
                "Giải thích: Cấu trúc bị động của quá khứ đơn: was + V3/ed."
            )
        else:
            opts = parse_options(main_text, slide_num)
            correct_ans = "A"
            if highlights:
                correct_ans = determine_correct_option(highlights[0], tb, slide_num)
            
            ans_word = opts.get(correct_ans, "")
            
            # Format answers and explanations nicely
            explanation_box = f"\n\n👉 ĐÁP ÁN ĐÚNG: {correct_ans}. {ans_word}"
            if explanation_text:
                explanation_box += f"\nGiải thích: {explanation_text}"
            else:
                explanation_box += "\nPhân tích: Chọn loại từ phù hợp theo cấu trúc ngữ pháp."
                
            slide_content = main_text + explanation_box
            
        chapters_data[ch_id]["slides"].append({
            "slide_index": slide_num,
            "title": "VÍ DỤ LUYỆN TẬP",
            "blocks": [{"type": "paragraph", "text": slide_content}]
        })
    else:
        # Process regular theory slide
        content_blocks = []
        slide_title = ""
        
        sorted_blocks = sorted(slide["blocks"], key=lambda x: (x.get("top", 0), x.get("left", 0)))
        
        for idx_b, block in enumerate(sorted_blocks):
            b_text = block["text"].strip()
            if not b_text:
                continue
            
            lines = b_text.split('\n')
            first_line = lines[0].strip()
            
            if idx_b == 0:
                slide_title = first_line
                remaining_text = "\n".join(lines[1:])
                if remaining_text.strip():
                    content_blocks.append({"type": "paragraph", "text": remaining_text})
            else:
                content_blocks.append({"type": "paragraph", "text": b_text})
                
        if not slide_title:
            slide_title = f"Slide {slide_num}"
            
        chapters_data[ch_id]["slides"].append({
            "slide_index": slide_num,
            "title": slide_title,
            "blocks": content_blocks
        })

# We empty the questions array for now, as you will provide the exercises later
for ch_id in chapters_data:
    chapters_data[ch_id]["questions"] = []

# Format chapters as a list
chapters_list = [chapters_data[i] for i in sorted(chapters_data.keys())]

# Write js/data.js
output_dir = "toeic_reading_web/js"
os.makedirs(output_dir, exist_ok=True)
js_file_path = os.path.join(output_dir, "data.js")

with open(js_file_path, "w", encoding="utf-8") as f:
    f.write("// TOEIC Reading Part 5 Course Data - Auto Generated\n")
    f.write("const toeicReadingData = ")
    json.dump(chapters_list, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"Successfully generated JS database at {js_file_path} with {len(chapters_list)} chapters.")
