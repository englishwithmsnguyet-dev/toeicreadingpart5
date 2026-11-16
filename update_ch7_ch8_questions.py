# -*- coding: utf-8 -*-
import json
import re

# 20 TOEIC questions for Chapter 7: Subject-Verb Agreement (Sự hòa hợp Chủ - Vị)
# Carefully calibrated: Authentic TOEIC contexts, deceptive traps (intervening prepositional phrases, relative clauses,
# inverted structures, correlative conjunctions, quantity expressions, collective nouns, fractions/percentages, gerund subjects),
# and evenly distributed answers (5 A, 5 B, 5 C, 5 D).

ch7_questions = [
    {
        "question": "The manager of the regional branch offices ______ to review all expenditure reports before the quarterly audit.",
        "options": {
            "A": "plan",
            "B": "plans",
            "C": "are planning",
            "D": "have planned"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. plans</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy cụm giới từ chêm vào: 'of the regional branch offices' bổ nghĩa cho danh từ đứng trước. Chủ ngữ cốt lõi là danh từ số ít <strong>The manager</strong>, do đó động từ chính phải chia số ít ở thì hiện tại đơn -> chọn <strong>plans</strong>.<br>- Các phương án A, C, D đều là dạng số nhiều (plan, are, have) bị bẫy bởi danh từ gần nhất là 'offices'.<br><br><strong>Dịch câu:</strong><br><em>Người quản lý của các văn phòng chi nhánh khu vực lên kế hoạch xem xét tất cả các báo cáo chi tiêu trước kỳ kiểm toán quý.</em>"
    },
    {
        "question": "Neither the head chef nor the kitchen assistants ______ aware that the refrigeration unit had malfunctioned overnight.",
        "options": {
            "A": "was",
            "B": "is",
            "C": "were",
            "D": "has been"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. were</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Quy tắc liên từ tương quan: Trong cấu trúc <strong>Neither S1 nor S2</strong>, động từ luôn hòa hợp theo chủ ngữ thứ hai (S2 - danh từ đứng gần động từ nhất).<br>- Ở đây, S2 là danh từ số nhiều <strong>the kitchen assistants</strong>. Sự việc diễn ra trong quá khứ kết hợp với mệnh đề 'had malfunctioned' nên động từ chia số nhiều ở quá khứ đơn -> chọn <strong>were</strong>.<br><br><strong>Dịch câu:</strong><br><em>Cả bếp trưởng lẫn các phụ bếp đều không nhận biết được việc tủ lạnh đã gặp sự cố trong đêm.</em>"
    },
    {
        "question": "The CEO, accompanied by members of the senior advisory council, ______ scheduled to deliver the keynote speech.",
        "options": {
            "A": "are",
            "B": "were",
            "C": "have been",
            "D": "is"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. is</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Quy tắc chủ ngữ đi kèm liên từ phụ trợ: Khi chủ ngữ liên kết bởi <strong>accompanied by</strong> (hoặc <em>along with, as well as, together with</em>), động từ chỉ chia hòa hợp với chủ ngữ đứng trước là <strong>The CEO</strong> (ngôi thứ ba số ít).<br>- Cụm 'members of the senior advisory council' là thông tin bổ sung, không làm chủ ngữ trở thành số nhiều -> chọn <strong>is</strong>.<br><br><strong>Dịch câu:</strong><br><em>Tổng giám đốc, cùng với các thành viên của hội đồng cố vấn cấp cao, được lên lịch sẽ phát biểu bài diễn văn chính.</em>"
    },
    {
        "question": "A complete inventory of all office supplies and computer peripherals ______ conducted at the end of every fiscal year.",
        "options": {
            "A": "is",
            "B": "are",
            "C": "were",
            "D": "have been"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. is</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy danh từ ghép và giới từ: Dù phía sau có 'supplies and computer peripherals' (số nhiều), chủ ngữ thực sự đứng đầu là <strong>A complete inventory</strong> (bản kiểm kê toàn bộ - số ít đếm được).<br>- Dấu hiệu thói quen định kỳ 'at the end of every fiscal year' kết hợp thể bị động yêu cầu thì hiện tại đơn số ít -> chọn <strong>is</strong>.<br><br><strong>Dịch câu:</strong><br><em>Một đợt kiểm kê toàn bộ tất cả vật tư văn phòng và thiết bị ngoại vi máy tính được tiến hành vào cuối mỗi năm tài chính.</em>"
    },
    {
        "question": "The committee ______ divided in their opinions regarding how the excess budget should be distributed.",
        "options": {
            "A": "is",
            "B": "are",
            "C": "was",
            "D": "has been"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. are</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy danh từ tập hợp (Collective Noun): Danh từ tập hợp <strong>The committee</strong> đi kèm với tính từ <em>divided</em> (chia rẽ/bất đồng) và tính từ sở hữu <strong>their opinions</strong> (ý kiến của từng người) -> hành động nhắm đến từng cá nhân thành viên riêng lẻ chứ không phải một khối thống nhất.<br>- Khi danh từ tập hợp diễn tả sự bất đồng hoặc các thành viên hành động riêng rẽ, động từ phải chia ở dạng số nhiều -> chọn <strong>are</strong>.<br><br><strong>Dịch câu:</strong><br><em>Các thành viên trong ủy ban bất đồng ý kiến về việc ngân sách dư thừa nên được phân bổ như thế nào.</em>"
    },
    {
        "question": "A total of twenty applicants ______ invited for a second round of interviews next Tuesday.",
        "options": {
            "A": "was",
            "B": "is",
            "C": "have been",
            "D": "has been"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. have been</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cụm <strong>A total of + danh từ đếm được số nhiều</strong> (twenty applicants) diễn tả số lượng nhiều cá nhân -> động từ chia ở dạng số nhiều.<br>- Phía sau là dạng bị động đã hoàn tất việc gửi lời mời -> chọn <strong>have been</strong> (loại was, is, has been vì là số ít).<br><br><strong>Dịch câu:</strong><br><em>Tổng cộng hai mươi ứng viên đã được mời tham gia vòng phỏng vấn thứ hai vào thứ Ba tuần tới.</em>"
    },
    {
        "question": "The number of defective items identified during the quality assurance inspection ______ remarkably low this month.",
        "options": {
            "A": "are",
            "B": "were",
            "C": "have been",
            "D": "was"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. was</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt kinh điển trong TOEIC: <strong>The number of + N số nhiều</strong> mang nghĩa là 'con số / số lượng của...' -> luôn chia động từ ở dạng <strong>số ít</strong>.<br>- Bẫy 'defective items' (số nhiều) và mệnh đề quan hệ rút gọn 'identified during...' xen giữa. Ta loại are, were, have been -> chọn <strong>was</strong>.<br><br><strong>Dịch câu:</strong><br><em>Số lượng sản phẩm lỗi được phát hiện trong đợt kiểm tra đảm bảo chất lượng đã ở mức thấp đáng kể trong tháng này.</em>"
    },
    {
        "question": "Every supervisor, manager, and department head ______ to submit the quarterly performance appraisal by Friday.",
        "options": {
            "A": "needs",
            "B": "need",
            "C": "are needing",
            "D": "have needed"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. needs</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy liệt kê với Every: Khi chủ ngữ bắt đầu bằng <strong>Every</strong> hoặc <strong>Each</strong>, dù có nối nhiều danh từ bằng liên từ <em>and</em> (supervisor, manager, and department head) thì chủ ngữ vẫn luôn được tính là <strong>số ít</strong>.<br>- Động từ chính chia số ít ở hiện tại đơn -> chọn <strong>needs</strong>.<br><br><strong>Dịch câu:</strong><br><em>Mọi giám sát viên, trưởng phòng và người đứng đầu bộ phận cần phải nộp bản đánh giá hiệu suất làm việc hàng quý trước thứ Sáu.</em>"
    },
    {
        "question": "Statistics ______ that customer satisfaction levels have increased by 15 percent following the website redesign.",
        "options": {
            "A": "indicates",
            "B": "indicate",
            "C": "is indicating",
            "D": "was indicated"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. indicate</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Điểm gài bẫy từ vựng quan trọng: <em>Statistics</em> nếu là 'môn thống kê' thì chia số ít. Nhưng khi đứng một mình mang nghĩa <strong>các số liệu thống kê / dữ liệu đo đạc</strong> và đi với mệnh đề <em>that...</em> (các số liệu chỉ ra rằng...), từ này đóng vai trò là <strong>danh từ số nhiều</strong>.<br>- Động từ chính chia số nhiều ở hiện tại đơn -> chọn <strong>indicate</strong> (loại indicates, is, was).<br><br><strong>Dịch câu:</strong><br><em>Các số liệu thống kê chỉ ra rằng mức độ hài lòng của khách hàng đã tăng 15% sau khi trang web được thiết kế lại.</em>"
    },
    {
        "question": "Two-thirds of the newly acquired manufacturing machinery ______ regular maintenance to prevent system downtime.",
        "options": {
            "A": "are requiring",
            "B": "require",
            "C": "requires",
            "D": "have required"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. requires</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Quy tắc phân số / phần trăm: Trong cấu trúc <strong>Phân số / Phần trăm + of + Danh từ</strong>, động từ chia theo danh từ đứng sau giới từ <em>of</em>.<br>- Danh từ sau <em>of</em> là <strong>machinery</strong> (máy móc thiết bị) - đây là danh từ <strong>không đếm được</strong> trong tiếng Anh (luôn là số ít). Do đó động từ phải chia số ít -> chọn <strong>requires</strong>.<br><br><strong>Dịch câu:</strong><br><em>Hai phần ba số máy móc sản xuất mới được mua yêu cầu bảo dưỡng định kỳ để ngăn ngừa thời gian ngừng hoạt động của hệ thống.</em>"
    },
    {
        "question": "Across the street from the municipal convention center ______ two highly acclaimed boutique hotels.",
        "options": {
            "A": "is located",
            "B": "was located",
            "C": "has been",
            "D": "are located"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. are located</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc đảo ngữ địa điểm (Inversion of Location): Khi cụm giới từ chỉ nơi chốn đứng đầu câu (<em>Across the street from...</em>), cấu trúc đảo là <strong>Giới từ chỉ nơi chốn + Động từ + Chủ ngữ</strong>.<br>- Chủ ngữ thực sự nằm sau động từ: <strong>two highly acclaimed boutique hotels</strong> (danh từ số nhiều). Vì vậy động từ phải chia ở số nhiều -> chọn <strong>are located</strong>.<br><br><strong>Dịch câu:</strong><br><em>Ở bên kia đường đối diện trung tâm hội nghị thành phố là hai khách sạn boutique được đánh giá rất cao.</em>"
    },
    {
        "question": "Ten thousand dollars ______ deemed an excessive amount to spend on corporate entertainment last quarter.",
        "options": {
            "A": "was",
            "B": "were",
            "C": "are",
            "D": "have been"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. was</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Các cụm từ chỉ khoản tiền (Ten thousand dollars), khoảng cách, thời gian hoặc khối lượng khi làm chủ ngữ biểu thị một tổng lượng đơn nhất nên động từ luôn chia ở <strong>số ít</strong>.<br>- Dấu hiệu thời gian 'last quarter' (quý trước) yêu cầu chia ở quá khứ đơn -> chọn <strong>was</strong> (loại were, are, have been).<br><br><strong>Dịch câu:</strong><br><em>Mười nghìn đô la đã bị coi là một khoản tiền quá mức để chi tiêu cho việc tiếp khách của công ty trong quý trước.</em>"
    },
    {
        "question": "The guidelines specifying how to handle confidential customer records ______ available on the company intranet.",
        "options": {
            "A": "is",
            "B": "are",
            "C": "was",
            "D": "has been"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. are</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy mệnh đề phân từ hiện tại (Present Participle Phrase): Cụm 'specifying how to handle confidential customer records' là cụm V-ing bổ nghĩa cho danh từ đứng trước.<br>- Chủ ngữ chính của câu là <strong>The guidelines</strong> (danh từ số nhiều) -> động từ to be phải chia số nhiều ở hiện tại -> chọn <strong>are</strong>.<br><br><strong>Dịch câu:</strong><br><em>Các hướng dẫn chỉ rõ cách xử lý hồ sơ mật của khách hàng hiện có sẵn trên mạng nội bộ của công ty.</em>"
    },
    {
        "question": "Developing innovative marketing strategies for competitive overseas markets ______ extensive research and consumer analysis.",
        "options": {
            "A": "require",
            "B": "are requiring",
            "C": "requires",
            "D": "have required"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. requires</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy danh động từ (Gerund as Subject): Khi V-ing đứng đầu làm chủ ngữ (<strong>Developing...</strong>), động từ chính luôn luôn chia ở <strong>ngôi thứ ba số ít</strong>.<br>- Bẫy xuất hiện do các danh từ số nhiều nằm trong tân ngữ của danh động từ: 'strategies', 'markets'. Động từ chính ở hiện tại đơn số ít -> chọn <strong>requires</strong>.<br><br><strong>Dịch câu:</strong><br><em>Việc phát triển các chiến lược tiếp thị đổi mới cho các thị trường nước ngoài đầy tính cạnh tranh đòi hỏi nghiên cứu sâu rộng và phân tích người tiêu dùng.</em>"
    },
    {
        "question": "Not only the regional sales representatives but also the vice president ______ optimistic about meeting this year's targets.",
        "options": {
            "A": "seem",
            "B": "are",
            "C": "were",
            "D": "is"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. is</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc liên từ tương quan: <strong>Not only S1 but also S2</strong> -> động từ chia theo chủ ngữ gần nhất là S2.<br>- S2 ở đây là <strong>the vice president</strong> (Phó chủ tịch - ngôi thứ ba số ít). Do đó, động từ to be phải chia số ít -> chọn <strong>is</strong> (loại seem, are, were vì là số nhiều).<br><br><strong>Dịch câu:</strong><br><em>Không chỉ các đại diện bán hàng khu vực mà cả Phó chủ tịch cũng cảm thấy lạc quan về việc đạt được các mục tiêu của năm nay.</em>"
    },
    {
        "question": "More than sixty percent of the employee feedback survey responses ______ submitted electronically.",
        "options": {
            "A": "were",
            "B": "was",
            "C": "is",
            "D": "has been"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. were</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Quy tắc phần trăm: <strong>Percent of + Noun</strong> -> động từ chia hòa hợp theo danh từ đứng sau giới từ <em>of</em>.<br>- Danh từ đứng sau là <strong>responses</strong> (các phản hồi - danh từ đếm được số nhiều) -> động từ chia ở dạng số nhiều -> chọn <strong>were</strong>.<br><br><strong>Dịch câu:</strong><br><em>Hơn sáu mươi phần trăm phản hồi trong cuộc khảo sát ý kiến nhân viên đã được gửi trực tuyến.</em>"
    },
    {
        "question": "Neither of the proposed solutions ______ practical under the current economic circumstances.",
        "options": {
            "A": "appear",
            "B": "appears",
            "C": "are appearing",
            "D": "have appeared"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. appears</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Quy tắc đại từ phân bổ: Cấu trúc <strong>Neither of + the + N số nhiều</strong> (Không phương án nào trong hai...) luôn làm chủ ngữ số ít, động từ chia ở <strong>số ít</strong>.<br>- Bẫy 'solutions' (số nhiều) đứng ngay trước chỗ trống. Động từ liên kết chia số ít ở hiện tại đơn -> chọn <strong>appears</strong>.<br><br><strong>Dịch câu:</strong><br><em>Không giải pháp nào trong số hai giải pháp được đề xuất tỏ ra khả thi trong hoàn cảnh kinh tế hiện tại.</em>"
    },
    {
        "question": "The criteria used to select candidates for the executive leadership program ______ extremely stringent.",
        "options": {
            "A": "is",
            "B": "was",
            "C": "are",
            "D": "has been"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. are</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy danh từ bất quy tắc gốc Hy Lạp/Latinh: <strong>Criteria</strong> là dạng số nhiều của <em>Criterion</em> (tiêu chí).<br>- Phía sau là cụm phân từ quá khứ rút gọn 'used to select...'. Vì chủ ngữ là danh từ số nhiều <em>criteria</em> nên động từ phải chia ở số nhiều -> chọn <strong>are</strong> (loại is, was, has been).<br><br><strong>Dịch câu:</strong><br><em>Các tiêu chí được sử dụng để lựa chọn ứng viên cho chương trình lãnh đạo điều hành là cực kỳ khắt khe.</em>"
    },
    {
        "question": "A series of lectures on financial asset management ______ scheduled to take place at the auditorium next week.",
        "options": {
            "A": "are",
            "B": "were",
            "C": "have been",
            "D": "is"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. is</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cụm định lượng đặc biệt: <strong>A series of + N số nhiều</strong> mang nghĩa là 'một chuỗi các...' được coi là một thể thống nhất số ít (mạo từ 'A') -> động từ chia ở <strong>số ít</strong>.<br>- Dù có danh từ số nhiều 'lectures' đứng gần, động từ to be vẫn chia số ít -> chọn <strong>is</strong>.<br><br><strong>Dịch câu:</strong><br><em>Một chuỗi các bài giảng về quản lý tài sản tài chính được lên lịch diễn ra tại hội trường vào tuần tới.</em>"
    },
    {
        "question": "One of the technicians who ______ responsible for maintaining the ventilation network noticed the pressure drop.",
        "options": {
            "A": "are",
            "B": "is",
            "C": "was",
            "D": "has been"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. are</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy cực hiểm trong đề thi TOEIC: Cấu trúc <strong>One of the + N số nhiều + WHO/THAT + V</strong>. Đại từ quan hệ <em>who</em> thay thế trực tiếp cho danh từ số nhiều đứng ngay trước nó là <strong>the technicians</strong> (những kỹ thuật viên phụ trách việc...), do đó động từ trong mệnh đề quan hệ phải chia ở <strong>số nhiều</strong>.<br>- (Lưu ý: Động từ chính của cả câu là 'noticed' chia theo 'One of...'). Chỗ trống nằm trong mệnh đề quan hệ nên chia số nhiều -> chọn <strong>are</strong>.<br><br><strong>Dịch câu:</strong><br><em>Một trong những kỹ thuật viên chịu trách nhiệm bảo trì mạng lưới thông gió đã nhận thấy sự sụt giảm áp suất.</em>"
    }
]

# 20 TOEIC questions for Chapter 8: Gerunds & Infinitives (Danh động từ & Động từ nguyên mẫu)
# Carefully calibrated: Traps with prepositions ('to' as preposition vs to-infinitive), verbs taking both V-ing/To-V with different meanings,
# causative verbs (make/let/have), passive infinitives, adjectives/nouns + to-V, fixed idiomatic expressions,
# and evenly distributed answers (5 A, 5 B, 5 C, 5 D).

ch8_questions = [
    {
        "question": "The senior management team is firmly committed to ______ full transparency across all financial operations.",
        "options": {
            "A": "maintain",
            "B": "maintaining",
            "C": "maintenance",
            "D": "to maintain"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. maintaining</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy 'to' là giới từ kinh điển trong TOEIC: Cấu trúc <strong>be committed to + V-ing / Noun</strong> (cam kết làm điều gì đó). Ở đây 'to' là giới từ chứ không phải to-infinitive.<br>- Theo sau giới từ cần một danh động từ có tân ngữ (full transparency) -> chọn <strong>maintaining</strong> (loại maintain, maintenance, to maintain).<br><br><strong>Dịch câu:</strong><br><em>Đội ngũ quản lý cấp cao cam kết mạnh mẽ trong việc duy trì sự minh bạch hoàn toàn trong tất cả các hoạt động tài chính.</em>"
    },
    {
        "question": "Please remember ______ all air conditioning units and lock the conference room before leaving the building.",
        "options": {
            "A": "shutting off",
            "B": "shut off",
            "C": "to shut off",
            "D": "having shut off"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. to shut off</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt <strong>Remember to V</strong> vs <strong>Remember V-ing</strong>:<br>  + <em>Remember + to-V</em>: Nhớ phải làm gì (nhiệm vụ, bổn phận trong tương lai hoặc chưa làm).<br>  + <em>Remember + V-ing</em>: Nhớ đã làm gì trong quá khứ.<br>- Câu mang tính chất lời nhắc nhở thực hiện hành động trước khi rời đi ('before leaving') -> chọn <strong>to shut off</strong>.<br><br><strong>Dịch câu:</strong><br><em>Xin vui lòng nhớ tắt tất cả các thiết bị điều hòa không khí và khóa phòng hội nghị trước khi rời khỏi tòa nhà.</em>"
    },
    {
        "question": "The software update will eliminate the need ______ paper invoices manually, saving hundreds of labor hours.",
        "options": {
            "A": "processing",
            "B": "processed",
            "C": "for process",
            "D": "to process"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. to process</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc danh từ đi với động từ nguyên mẫu: <strong>the need / ability / opportunity / effort + to-infinitive</strong> (nhu cầu/khả năng/cơ hội để làm gì).<br>- Đi sau danh từ 'the need' cần động từ nguyên mẫu có 'to' -> chọn <strong>to process</strong>.<br><br><strong>Dịch câu:</strong><br><em>Bản cập nhật phần mềm sẽ loại bỏ sự cần thiết phải xử lý hóa đơn giấy theo cách thủ công, giúp tiết kiệm hàng trăm giờ lao động.</em>"
    },
    {
        "question": "Due to unexpected supply chain disruptions, the manufacturer had no choice but ______ production at the plant.",
        "options": {
            "A": "to suspend",
            "B": "suspending",
            "C": "suspend",
            "D": "suspended"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. to suspend</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cụm thành ngữ TOEIC nâng cao: <strong>have no choice but + to-infinitive</strong> (không còn sự lựa chọn nào khác ngoài việc làm gì).<br>- Ở đây 'but' mang nghĩa giới từ 'ngoại trừ', và cấu trúc bắt buộc đi với to-infinitive -> chọn <strong>to suspend</strong>.<br><br><strong>Dịch câu:</strong><br><em>Do sự gián đoạn chuỗi cung ứng ngoài dự kiến, nhà sản xuất không còn lựa chọn nào khác ngoài việc tạm dừng sản xuất tại nhà máy.</em>"
    },
    {
        "question": "Although the budget was severely constrained, the marketing department managed ______ all promotional targets.",
        "options": {
            "A": "achieving",
            "B": "to achieve",
            "C": "achieve",
            "D": "achievement"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. to achieve</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Động từ <strong>manage</strong> luôn đi kèm với to-infinitive: <strong>manage to do something</strong> (xoay xở / thành công làm được việc gì dù có khó khăn).<br>- Do đó, ta chọn phương án <strong>to achieve</strong>.<br><br><strong>Dịch câu:</strong><br><em>Mặc dù ngân sách bị hạn chế nghiêm ngặt, phòng tiếp thị vẫn xoay xở đạt được tất cả các mục tiêu quảng bá.</em>"
    },
    {
        "question": "The building supervisor let the external contractors ______ the renovation work during the weekend.",
        "options": {
            "A": "to begin",
            "B": "beginning",
            "C": "begin",
            "D": "began"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. begin</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc động từ chỉ sự cho phép / sai khiến (Causative Verb): <strong>let + tân ngữ + V nguyên mẫu không to (bare infinitive)</strong> (để cho / cho phép ai làm gì).<br>- Sau 'let the external contractors' bắt buộc phải là động từ nguyên mẫu không 'to' -> chọn <strong>begin</strong>.<br><br><strong>Dịch câu:</strong><br><em>Người giám sát tòa nhà đã cho phép các nhà thầu bên ngoài bắt đầu công việc cải tạo vào dịp cuối tuần.</em>"
    },
    {
        "question": "Mr. Evans distinctly regrets ______ confidential proprietary data to a competitor before signing the NDA.",
        "options": {
            "A": "to disclose",
            "B": "disclose",
            "C": "disclosure",
            "D": "disclosing"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. disclosing</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt <strong>Regret to V</strong> vs <strong>Regret V-ing</strong>:<br>  + <em>Regret + to-V</em>: Tiếc/lấy làm tiếc khi phải làm gì (thường dùng trong văn thư trang trọng: We regret to inform you...).<br>  + <em>Regret + V-ing</em>: Hối hận / tiếc vì đã lỡ làm điều gì trong quá khứ.<br>- Ngữ cảnh câu diễn tả sự ân hận vì đã làm lộ thông tin trước đó ('before signing the NDA') -> chọn <strong>disclosing</strong>.<br><br><strong>Dịch câu:</strong><br><em>Ông Evans thực sự hối hận vì đã tiết lộ dữ liệu độc quyền bảo mật cho một đối thủ cạnh tranh trước khi ký thỏa thuận bảo mật.</em>"
    },
    {
        "question": "The human resources division strongly recommends ______ the mandatory cybersecurity seminar by Friday afternoon.",
        "options": {
            "A": "completing",
            "B": "to complete",
            "C": "complete",
            "D": "completed"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. completing</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy cấu trúc với Recommend/Suggest: Khi động từ <strong>recommend</strong> không có tân ngữ chỉ người ngay phía sau (không phải dạng recommend s.o to-V), động từ trực tiếp theo sau bắt buộc phải ở dạng danh động từ: <strong>recommend + V-ing</strong>.<br>- Do đó ta chọn <strong>completing</strong>.<br><br><strong>Dịch câu:</strong><br><em>Bộ phận nhân sự khuyến nghị mạnh mẽ việc hoàn thành hội thảo an ninh mạng bắt buộc trước chiều thứ Sáu.</em>"
    },
    {
        "question": "Our corporate legal advisors strongly objected to ______ the partnership agreement without introducing liability caps.",
        "options": {
            "A": "sign",
            "B": "signing",
            "C": "signed",
            "D": "be signed"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. signing</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cụm động từ cố định với giới từ: <strong>object to + V-ing</strong> (phản đối việc làm gì). Trong cụm này, 'to' đóng vai trò là giới từ.<br>- Theo sau giới từ phải là danh động từ V-ing -> chọn <strong>signing</strong>.<br><br><strong>Dịch câu:</strong><br><em>Các cố vấn pháp lý của công ty chúng tôi đã kịch liệt phản đối việc ký thỏa thuận hợp tác mà không đưa ra các điều khoản giới hạn trách nhiệm.</em>"
    },
    {
        "question": "The complex financial model developed by the consulting firm is difficult ______ without specialized training.",
        "options": {
            "A": "interpreting",
            "B": "for interpreting",
            "C": "to interpret",
            "D": "interpreted"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. to interpret</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc tính từ đi với động từ nguyên mẫu: <strong>Subject + be + Adjective (difficult/easy/impossible/ready...) + to-infinitive</strong> (Cái gì như thế nào để làm việc gì).<br>- Theo sau tính từ 'difficult' là động từ nguyên thể có 'to' -> chọn <strong>to interpret</strong>.<br><br><strong>Dịch câu:</strong><br><em>Mô hình tài chính phức tạp do công ty tư vấn phát triển rất khó để diễn giải nếu không có sự đào tạo chuyên môn.</em>"
    },
    {
        "question": "All international conference attendees are kindly requested ______ in the lobby at least thirty minutes prior to departure.",
        "options": {
            "A": "gathering",
            "B": "gather",
            "C": "for gathering",
            "D": "to gather"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. to gather</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Dạng bị động của động từ yêu cầu/đề nghị: Chủ động là <em>request someone to do something</em> -> Chuyển sang bị động là <strong>be requested + to-infinitive</strong> (được yêu cầu làm gì).<br>- Do đó, chỗ trống cần điền động từ nguyên mẫu có 'to' -> chọn <strong>to gather</strong>.<br><br><strong>Dịch câu:</strong><br><em>Tất cả những người tham dự hội nghị quốc tế vui lòng tập trung tại sảnh ít nhất ba mươi phút trước giờ khởi hành.</em>"
    },
    {
        "question": "Instead of ______ resources into outdated legacy infrastructure, the executive board decided to migrate to cloud servers.",
        "options": {
            "A": "pouring",
            "B": "to pour",
            "C": "pour",
            "D": "poured"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. pouring</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc sau cụm giới từ: <strong>Instead of + V-ing / Noun</strong> (Thay vì làm việc gì đó).<br>- Đứng sau giới từ 'of' cần một danh động từ có tân ngữ 'resources' -> chọn <strong>pouring</strong>.<br><br><strong>Dịch câu:</strong><br><em>Thay vì đổ nguồn lực vào cơ sở hạ tầng cũ kỹ lỗi thời, ban giám đốc đã quyết định chuyển dịch sang các máy chủ điện toán đám mây.</em>"
    },
    {
        "question": "The senior research analyst will never forget ______ the lifetime achievement award from the industry association.",
        "options": {
            "A": "to receive",
            "B": "receiving",
            "C": "receive",
            "D": "receipt"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. receiving</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt <strong>Forget to V</strong> vs <strong>Forget V-ing</strong>:<br>  + <em>Forget + to-V</em>: Quên phải làm gì (bổn phận/nhiệm vụ).<br>  + <em>Forget + V-ing</em>: Quên một kỷ niệm/hành động đã từng xảy ra trong quá khứ.<br>- Cụm 'will never forget receiving...' là cấu trúc phổ biến mang nghĩa 'sẽ không bao giờ quên cảm giác khi được nhận giải thưởng trong quá khứ' -> chọn <strong>receiving</strong>.<br><br><strong>Dịch câu:</strong><br><em>Chuyên viên nghiên cứu cấp cao sẽ không bao giờ quên khoảnh khắc nhận được giải thưởng thành tựu trọn đời từ hiệp hội ngành nghề.</em>"
    },
    {
        "question": "The CEO made the marketing team ______ the entire promotional campaign following negative customer feedback.",
        "options": {
            "A": "to restructure",
            "B": "restructuring",
            "C": "restructure",
            "D": "restructured"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. restructure</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc động từ sai khiến thể chủ động: <strong>make someone + V nguyên mẫu không to (bare infinitive)</strong> (bắt buộc/khiến ai đó làm gì).<br>- Bẫy hay gặp là chọn to-infinitive (to restructure). Đáp án chính xác bắt buộc là động từ nguyên mẫu không 'to' -> chọn <strong>restructure</strong>.<br><br><strong>Dịch câu:</strong><br><em>Tổng giám đốc đã yêu cầu đội ngũ tiếp thị phải tái cơ cấu lại toàn bộ chiến dịch quảng bá sau những phản hồi tiêu cực từ khách hàng.</em>"
    },
    {
        "question": "The executive committee is currently considering ______ a new branch office in Singapore next quarter.",
        "options": {
            "A": "to open",
            "B": "open",
            "C": "opened",
            "D": "opening"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. opening</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Động từ <strong>consider</strong> (cân nhắc / xem xét việc gì) luôn đòi hỏi một danh động từ theo sau: <strong>consider + V-ing</strong>.<br>- Bẫy thường gặp là người học nhầm với to-V. Ta chọn phương án <strong>opening</strong>.<br><br><strong>Dịch câu:</strong><br><em>Ủy ban điều hành hiện đang cân nhắc việc mở một văn phòng chi nhánh mới tại Singapore vào quý tới.</em>"
    },
    {
        "question": "The logistics firm succeeded in ______ delivery expenses by renegotiating fuel supplier contracts.",
        "options": {
            "A": "reducing",
            "B": "to reduce",
            "C": "reduction",
            "D": "reduce"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. reducing</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cụm động từ: <strong>succeed in doing something</strong> (thành công trong việc làm gì). Đứng sau giới từ 'in' và có tân ngữ danh từ 'delivery expenses' phía sau nên bắt buộc dùng danh động từ V-ing.<br>- Không chọn danh từ 'reduction' vì danh từ không nhận trực tiếp tân ngữ mà cần giới từ 'of' -> chọn <strong>reducing</strong>.<br><br><strong>Dịch câu:</strong><br><em>Công ty hậu cần đã thành công trong việc cắt giảm chi phí giao hàng bằng cách tái đàm phán hợp đồng với các nhà cung cấp nhiên liệu.</em>"
    },
    {
        "question": "The operations supervisor stopped ______ personal calls on company time after receiving a formal warning from HR.",
        "options": {
            "A": "to make",
            "B": "making",
            "C": "make",
            "D": "made"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. making</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt <strong>Stop to V</strong> vs <strong>Stop V-ing</strong>:<br>  + <em>Stop + to-V</em>: Dừng một hành động lại để làm một việc khác.<br>  + <em>Stop + V-ing</em>: Dứt điểm / từ bỏ / ngừng hẳn một thói quen hoặc hành động đang làm.<br>- Ngữ cảnh câu là sau khi nhận cảnh cáo từ phòng Nhân sự thì người này dừng hẳn việc gọi điện thoại cá nhân trong giờ làm việc -> chọn <strong>making</strong>.<br><br><strong>Dịch câu:</strong><br><em>Người giám sát vận hành đã ngừng hẳn việc gọi các cuộc điện thoại cá nhân trong giờ làm việc của công ty sau khi nhận được cảnh cáo chính thức từ phòng nhân sự.</em>"
    },
    {
        "question": "The proposed merger is expected ______ significant cost savings across supply chain operations within two years.",
        "options": {
            "A": "generating",
            "B": "generation",
            "C": "to generate",
            "D": "generate"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. to generate</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Dạng bị động của expect: <strong>be expected + to-infinitive</strong> (được kỳ vọng sẽ làm gì/đạt được điều gì).<br>- Theo sau dạng bị động 'is expected' cần một động từ nguyên mẫu có 'to' -> chọn <strong>to generate</strong>.<br><br><strong>Dịch câu:</strong><br><em>Vụ sáp nhập được đề xuất kỳ vọng sẽ tạo ra khoản tiết kiệm chi phí đáng kể trong các hoạt động chuỗi cung ứng trong vòng hai năm.</em>"
    },
    {
        "question": "Before ______ the confidential agreement, please review all terms and conditions with your legal counsel.",
        "options": {
            "A": "sign",
            "B": "signature",
            "C": "to sign",
            "D": "signing"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. signing</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Đứng sau liên từ/giới từ chỉ thời gian <strong>Before / After</strong> khi rút gọn cùng chủ ngữ (hoặc đóng vai trò giới từ) có tân ngữ phía sau ('the confidential agreement'), ta dùng <strong>V-ing</strong>.<br>- Ta chọn phương án <strong>signing</strong>.<br><br><strong>Dịch câu:</strong><br><em>Trước khi ký kết thỏa thuận bảo mật, vui lòng xem xét kỹ lưỡng tất cả các điều khoản và điều kiện với cố vấn pháp lý của bạn.</em>"
    },
    {
        "question": "Given the delicate nature of the negotiations, the spokesperson chose ______ on the unconfirmed rumors.",
        "options": {
            "A": "not to comment",
            "B": "not commenting",
            "C": "to not comment",
            "D": "no comment"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. not to comment</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc động từ: <strong>choose + to-infinitive</strong> (chọn/quyết định làm gì).<br>- Thể phủ định của to-infinitive có cấu trúc chuẩn là <strong>not + to-infinitive</strong> (đặt 'not' ngay trước 'to') -> chọn <strong>not to comment</strong>.<br><br><strong>Dịch câu:</strong><br><em>Xét tính chất nhạy cảm của các cuộc đàm phán, người phát ngôn đã chọn không đưa ra bình luận về những tin đồn chưa được xác thực.</em>"
    }
]

# Update data.js
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

# Update Chapter 7
ch7 = next(c for c in data if c.get("id") == 7)
ch7["questions"] = ch7_questions
print(f"Updated Chapter 7 questions ({len(ch7_questions)} questions).")
ch7_ans = [q["answer"] for q in ch7_questions]
print("Chapter 7 Answer Distribution:", {opt: ch7_ans.count(opt) for opt in ['A', 'B', 'C', 'D']})

# Update Chapter 8
ch8 = next(c for c in data if c.get("id") == 8)
ch8["questions"] = ch8_questions
print(f"Updated Chapter 8 questions ({len(ch8_questions)} questions).")
ch8_ans = [q["answer"] for q in ch8_questions]
print("Chapter 8 Answer Distribution:", {opt: ch8_ans.count(opt) for opt in ['A', 'B', 'C', 'D']})

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Data update successfully written to data.js!")
