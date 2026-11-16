# -*- coding: utf-8 -*-
import json
import re

# Perfectly balanced 20 TOEIC questions for Chapter 9: Conjunctions (Liên từ)
# Distribution: Exactly 5 A, 5 B, 5 C, 5 D.

ch9_questions = [
    {
        "question": "______ torrential rain caused severe flooding across the metropolitan area, the annual technology summit commenced on schedule.",
        "options": {
            "A": "In spite of",
            "B": "Although",
            "C": "Despite",
            "D": "Regardless of"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. Although</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy kinh điển giữa <strong>Liên từ</strong> và <strong>Giới từ</strong>: Phía sau chỗ trống là một mệnh đề hoàn chỉnh (S + V + O: <em>torrential rain caused severe flooding...</em>).<br>- Do đó, vị trí đầu câu bắt buộc phải dùng một liên từ phụ thuộc (subordinating conjunction) để nối với mệnh đề chính phía sau.<br>- Ta chọn <strong>Although</strong> (mặc dù).<br>- Loại các phương án <strong>In spite of</strong>, <strong>Despite</strong>, và <strong>Regardless of</strong> vì tất cả đều là cụm giới từ, chỉ đi với cụm danh từ (Noun Phrase) hoặc V-ing chứ không đi với mệnh đề có động từ chia thì.<br><br><strong>Dịch câu:</strong><br><em>Mặc dù mưa xối xả gây ngập lụt nghiêm trọng khắp khu vực đô thị, hội nghị thượng đỉnh công nghệ thường niên vẫn khai mạc đúng lịch trình.</em>"
    },
    {
        "question": "The manufacturing line was temporarily suspended ______ urgent maintenance could be performed on the primary turbine.",
        "options": {
            "A": "in order to",
            "B": "so as to",
            "C": "so that",
            "D": "because of"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. so that</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy liên từ chỉ mục đích: Phía sau chỗ trống là một mệnh đề có chủ ngữ và động từ khiếm khuyết (<em>urgent maintenance could be performed...</em>).<br>- Cấu trúc chỉ mục đích đi với mệnh đề là: <strong>so that / in order that + S + modal verb (can/could/may...) + V</strong> (để mà...).<br>- Ta chọn phương án <strong>so that</strong>.<br>- Loại <strong>in order to</strong> và <strong>so as to</strong> vì theo sau phải là động từ nguyên mẫu (V-bare).<br>- Loại <strong>because of</strong> vì là giới từ chỉ nguyên nhân đi với danh từ.<br><br><strong>Dịch câu:</strong><br><em>Dây chuyền sản xuất đã tạm thời bị ngừng lại để việc bảo trì khẩn cấp có thể được thực hiện trên tuabin chính.</em>"
    },
    {
        "question": "The airline will issue a full refund or hotel accommodation voucher ______ a flight is delayed by more than six hours.",
        "options": {
            "A": "in the event of",
            "B": "in case of",
            "C": "as a result of",
            "D": "in the event that"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. in the event that</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt cụm từ kết thúc bằng giới từ vs liên từ có 'that': Phía sau chỗ trống là một mệnh đề đầy đủ (<em>a flight is delayed by more than six hours</em>).<br>- Cấu trúc: <strong>in the event that + clause = if + clause</strong> (trong trường hợp / nếu mà...).<br>- Ta chọn phương án <strong>in the event that</strong>.<br>- Loại <strong>in the event of</strong>, <strong>in case of</strong>, và <strong>as a result of</strong> vì tận cùng là giới từ 'of' nên chỉ đi sau bởi cụm danh từ hoặc V-ing.<br><br><strong>Dịch câu:</strong><br><em>Hãng hàng không sẽ hoàn tiền đầy đủ hoặc cấp phiếu lưu trú khách sạn trong trường hợp chuyến bay bị hoãn hơn sáu giờ.</em>"
    },
    {
        "question": "______ all confidential project files have been securely encrypted, they may be uploaded to the cloud repository.",
        "options": {
            "A": "Once",
            "B": "Until",
            "C": "Unless",
            "D": "While"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. Once</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Liên từ chỉ thời gian mang tính điều kiện: <strong>Once + S + have/has V3ed, S + V</strong> mang nghĩa 'Một khi... / Ngay sau khi... đã hoàn thành'.<br>- Ngữ cảnh: Một khi các tập tin dự án mật đã được mã hóa an toàn, chúng mới có thể được tải lên kho lưu trữ đám mây -> chọn <strong>Once</strong>.<br>- Các phương án còn lại trái ngược về mặt logic:<br>  + <em>Until</em>: Cho đến tận khi (thường đi với mệnh đề chính phủ định).<br>  + <em>Unless</em>: Trừ khi / Nếu không.<br>  + <em>While</em>: Trong khi (chỉ 2 hành động song song).<br><br><strong>Dịch câu:</strong><br><em>Một khi tất cả các tập tin dự án mật đã được mã hóa an toàn, chúng có thể được tải lên kho lưu trữ đám mây.</em>"
    },
    {
        "question": "The newly appointed executive director is respected ______ for her visionary leadership ______ for her integrity.",
        "options": {
            "A": "not only - but also",
            "B": "neither - or",
            "C": "either - and",
            "D": "both - or"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. not only - but also</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc liên từ tương quan (Correlative Conjunctions): Cặp từ cố định <strong>not only A but also B</strong> (không những A mà còn B).<br>- Cấu trúc này đảm bảo tính song hành hoàn hảo giữa hai cụm giới từ: <em>for her visionary leadership</em> và <em>for her integrity</em>.<br>- Các phương án ghép sai cặp từ:<br>  + B sai vì 'neither' phải đi với 'nor'.<br>  + C sai vì 'either' phải đi với 'or'.<br>  + D sai vì 'both' phải đi với 'and'.<br><br><strong>Dịch câu:</strong><br><em>Vị giám đốc điều hành mới được bổ nhiệm được kính trọng không chỉ vì khả năng lãnh đạo có tầm nhìn mà còn vì sự chính trực của bà.</em>"
    },
    {
        "question": "The shipment of electronic sensors cannot be released from customs ______ the importer provides the certificate of origin.",
        "options": {
            "A": "if",
            "B": "because",
            "C": "unless",
            "D": "since"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. unless</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Liên từ điều kiện phủ định: <strong>Unless = If... not</strong> (Trừ khi / Nếu... không).<br>- Mệnh đề chính có tính phủ định: 'The shipment cannot be released' (Lô hàng không thể được thông quan).<br>- Ý nghĩa logic: Lô hàng không thể được thông quan nếu nhà nhập khẩu không xuất trình giấy chứng nhận xuất xứ (C/O) -> chọn <strong>unless</strong>.<br>- Các phương án A (if), B (because), D (since) đều làm cho câu bị đảo ngược ý nghĩa logic một cách vô lý.<br><br><strong>Dịch câu:</strong><br><em>Lô hàng cảm biến điện tử không thể được thông quan trừ khi nhà nhập khẩu cung cấp được giấy chứng nhận xuất xứ hàng hóa.</em>"
    },
    {
        "question": "The commercial lease contract will remain valid for five years ______ neither party submits a written request for termination.",
        "options": {
            "A": "as for",
            "B": "in order that",
            "C": "even though",
            "D": "provided that"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. provided that</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Liên từ chỉ điều kiện ràng buộc trong hợp đồng thương mại: <strong>provided that / providing that = as long as = if</strong> (với điều kiện là / miễn là...).<br>- Ngữ cảnh: Hợp đồng thuê mặt bằng thương mại sẽ duy trì hiệu lực trong 5 năm với điều kiện là không bên nào nộp yêu cầu chấm dứt bằng văn bản -> chọn <strong>provided that</strong>.<br>- Loại <strong>as for</strong> (giới từ: về phần/đối với).<br>- Loại <strong>in order that</strong> (chỉ mục đích: để mà).<br>- Loại <strong>even though</strong> (tương phản: mặc dù).<br><br><strong>Dịch câu:</strong><br><em>Hợp đồng thuê mặt bằng thương mại sẽ giữ nguyên hiệu lực trong năm năm với điều kiện là không bên nào nộp đơn yêu cầu chấm dứt bằng văn bản.</em>"
    },
    {
        "question": "______ the research department made significant breakthroughs, commercial production remains several months away.",
        "options": {
            "A": "Even though",
            "B": "Because of",
            "C": "Despite",
            "D": "In spite of"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. Even though</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phân biệt liên từ và giới từ chỉ sự tương phản: Theo sau chỗ trống là mệnh đề hoàn chỉnh (<em>the research department made significant breakthroughs</em>).<br>- Cần một liên từ nối hai mệnh đề tương phản: <strong>Even though + S + V</strong> (Mặc dù...).<br>- Ta chọn <strong>Even though</strong>.<br>- Loại <strong>Because of</strong>, <strong>Despite</strong>, và <strong>In spite of</strong> vì đều là giới từ, chỉ đi với Noun Phrase hoặc V-ing.<br><br><strong>Dịch câu:</strong><br><em>Mặc dù phòng nghiên cứu đã tạo ra những bước đột phá đáng kể, việc sản xuất thương mại vẫn còn phải mất vài tháng nữa.</em>"
    },
    {
        "question": "The board of directors has not yet decided ______ to acquire the regional distribution firm or expand existing facilities.",
        "options": {
            "A": "if",
            "B": "whether",
            "C": "neither",
            "D": "either"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. whether</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cặp liên từ lựa chọn với to-V: <strong>whether to do sth or do sth</strong> (liệu nên làm cái này hay làm cái kia).<br>- Trong tiếng Anh chuẩn, <em>if</em> không bao giờ đi trực tiếp với động từ nguyên mẫu có to (không có 'if to do'). Chỉ có <strong>whether to-V</strong>.<br>- 'neither' và 'either' không đi với cấu trúc '...to acquire... or expand'.<br>- Do đó phương án chính xác là <strong>whether</strong>.<br><br><strong>Dịch câu:</strong><br><em>Hội đồng quản trị vẫn chưa quyết định liệu nên mua lại công ty phân phối khu vực hay mở rộng các cơ sở hiện có.</em>"
    },
    {
        "question": "The senior technician was inspecting the control panel ______ the unexpected power surge disrupted the laboratory network.",
        "options": {
            "A": "during",
            "B": "since",
            "C": "when",
            "D": "because of"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. when</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc thì phối hợp với liên từ chỉ thời gian: Một hành động đang xảy ra trong quá khứ (<em>was inspecting</em>) thì một hành động ngắn khác bất ngờ xen vào (<em>disrupted</em>) -> dùng liên từ <strong>when</strong>.<br>- Cấu trúc: <code>S + was/were V-ing + WHEN + S + V2/ed</code>.<br>- Loại <strong>during</strong> và <strong>because of</strong> vì là giới từ (không đứng trước mệnh đề).<br>- Loại <strong>since</strong> vì không phù hợp ngữ cảnh diễn biến hành động xen vào.<br><br><strong>Dịch câu:</strong><br><em>Kỹ thuật viên cao cấp đang kiểm tra bảng điều khiển thì sự cố tăng áp đột ngột đã làm gián đoạn mạng lưới phòng thí nghiệm.</em>"
    },
    {
        "question": "Staff members must submit all travel reimbursement receipts within ten business days; ______, claims will not be processed.",
        "options": {
            "A": "unless",
            "B": "although",
            "C": "instead",
            "D": "otherwise"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. otherwise</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy trạng từ liên kết (Conjunctive Adverb) đi sau dấu chấm phẩy (;) và trước dấu phẩy (,):<br>- <strong>Otherwise</strong> (nếu không thì...) dùng để nối hai mệnh đề độc lập, chỉ hậu quả tiêu cực nếu điều kiện ở mệnh đề trước không được đáp ứng.<br>- <em>Unless</em> và <em>although</em> là liên từ phụ thuộc, không đứng độc lập sau dấu chấm phẩy có dấu phẩy theo sau như vậy.<br>- <em>Instead</em> (thay vào đó) không phù hợp về mặt ngữ nghĩa.<br><br><strong>Dịch câu:</strong><br><em>Nhân viên phải nộp tất cả biên lai hoàn tiền công tác trong vòng mười ngày làm việc; nếu không thì các yêu cầu thanh toán sẽ không được xử lý.</em>"
    },
    {
        "question": "The presentation slides were concise ______ informative, enabling the client to understand the complex proposal easily.",
        "options": {
            "A": "yet",
            "B": "or",
            "C": "so",
            "D": "for"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. yet</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy liên từ đẳng lập đa nghĩa: <strong>Yet</strong> khi đóng vai trò liên từ đẳng lập nối hai tính từ mang nghĩa 'nhưng / tuy vậy mà lại' (tương đương <em>but</em>).<br>- 'concise yet informative' là cách diễn đạt phổ biến và học thuật trong TOEIC (ngắn gọn nhưng lại chứa đựng nhiều thông tin hữu ích).<br>- Các liên từ <em>or</em> (hoặc), <em>so</em> (cho nên), <em>for</em> (bởi vì) không dùng để nối hai tính từ đối lập tinh tế như thế này.<br><br><strong>Dịch câu:</strong><br><em>Các trang trình bày ngắn gọn nhưng vẫn đầy đủ thông tin, giúp khách hàng dễ dàng hiểu được bản đề xuất phức tạp.</em>"
    },
    {
        "question": "The marketing director proposed ______ reducing print advertising expenditures ______ reallocating funds to digital media.",
        "options": {
            "A": "neither - and",
            "B": "not only - but also",
            "C": "both - or",
            "D": "either - but"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. not only - but also</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc liên từ tương quan song hành: Cặp từ đúng ngữ pháp duy nhất là <strong>not only... but also...</strong> (không những... mà còn...).<br>- Hai vế được nối đều là cụm danh động từ: <em>reducing...</em> và <em>reallocating...</em>.<br>- Các lựa chọn A, C, D đều ghép sai cặp liên từ tương quan.<br><br><strong>Dịch câu:</strong><br><em>Giám đốc tiếp thị đã đề xuất không chỉ cắt giảm chi tiêu cho quảng cáo in ấn mà còn tái phân bổ ngân sách sang truyền thông kỹ thuật số.</em>"
    },
    {
        "question": "______ all laboratory test results have been officially verified, the pharmaceutical firm cannot apply for regulatory approval.",
        "options": {
            "A": "As soon as",
            "B": "Because",
            "C": "Until",
            "D": "While"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. Until</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy liên từ thời gian kết hợp phủ định: <strong>Until + S + V, S + cannot / will not + V</strong> mang nghĩa 'Cho đến tận khi... thì mới có thể...'.<br>- Ngữ cảnh: Cho đến khi tất cả kết quả thử nghiệm trong phòng lab được kiểm chứng chính thức, công ty dược phẩm không thể nộp đơn xin cấp phép từ cơ quan quản lý -> chọn <strong>Until</strong>.<br>- Các liên từ <em>As soon as</em> (ngay khi), <em>Because</em> (bởi vì), <em>While</em> (trong khi) nếu đưa vào sẽ tạo thành câu phản logic.<br><br><strong>Dịch câu:</strong><br><em>Cho đến khi tất cả các kết quả xét nghiệm trong phòng thí nghiệm được xác minh chính thức, công ty dược phẩm không thể nộp đơn xin phê duyệt theo quy định.</em>"
    },
    {
        "question": "Candidates must possess ______ a bachelor's degree in accounting ______ a minimum of three years of auditing experience.",
        "options": {
            "A": "neither - or",
            "B": "both - or",
            "C": "not only - or",
            "D": "both - and"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. both - and</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cặp liên từ tương quan đúng: <strong>both A and B</strong> (cả A và B).<br>- Yêu cầu công việc đòi hỏi ứng viên phải có cả hai điều kiện: bằng cử nhân kế toán VÀ tối thiểu ba năm kinh nghiệm kiểm toán -> chọn <strong>both - and</strong>.<br>- Các phương án A, B, C đều ghép sai cặp từ nối.<br><br><strong>Dịch câu:</strong><br><em>Các ứng viên phải có cả bằng cử nhân kế toán và tối thiểu ba năm kinh nghiệm kiểm toán.</em>"
    },
    {
        "question": "The customer care hotline received hundreds of calls ______ the mobile banking application encountered a technical outage.",
        "options": {
            "A": "when",
            "B": "during",
            "C": "despite",
            "D": "because of"
        },
        "answer": "A",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">A. when</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy phân biệt Liên từ vs Giới từ: Phía sau chỗ trống là mệnh đề có chủ ngữ và vị ngữ hoàn chỉnh (<em>the mobile banking application encountered a technical outage</em>).<br>- Do đó ta bắt buộc phải chọn một liên từ chỉ thời gian/sự kiện là <strong>when</strong> (khi/vào lúc).<br>- Các phương án <strong>during</strong>, <strong>despite</strong>, và <strong>because of</strong> đều là giới từ, chỉ đi kèm danh từ/cụm danh từ nên loại.<br><br><strong>Dịch câu:</strong><br><em>Đường dây nóng chăm sóc khách hàng đã nhận được hàng trăm cuộc gọi khi ứng dụng ngân hàng di động gặp sự cố ngừng hoạt động kỹ thuật.</em>"
    },
    {
        "question": "The revised corporate security guidelines are ______ rigorous ______ external auditors commended our compliance efforts.",
        "options": {
            "A": "neither - nor",
            "B": "as - as",
            "C": "such - that",
            "D": "so - that"
        },
        "answer": "D",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">D. so - that</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Cấu trúc chỉ kết quả: Phân biệt <strong>so... that</strong> và <strong>such... that</strong>:<br>  + <code>so + Adjective / Adverb + that + clause</code>.<br>  + <code>such + (a/an) + Adj + Noun + that + clause</code>.<br>- Ở đây sau chỗ trống thứ nhất là tính từ đơn <strong>rigorous</strong> (nghiêm ngặt), không có danh từ theo sau -> bắt buộc dùng cấu trúc <strong>so... that</strong>.<br>- Do đó chọn phương án <strong>so - that</strong>.<br><br><strong>Dịch câu:</strong><br><em>Các hướng dẫn an ninh doanh nghiệp sửa đổi nghiêm ngặt đến mức mà các kiểm toán viên bên ngoài đã khen ngợi nỗ lực tuân thủ của chúng tôi.</em>"
    },
    {
        "question": "The senior management team held an emergency meeting ______ review the quarterly revenue deficit.",
        "options": {
            "A": "so that",
            "B": "in order that",
            "C": "in order to",
            "D": "because"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. in order to</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy động từ nguyên mẫu vs mệnh đề chỉ mục đích: Theo sau chỗ trống là động từ nguyên mẫu (<em>review</em>) cùng tân ngữ của nó.<br>- Cấu trúc chỉ mục đích đi với động từ nguyên mẫu: <strong>in order to / so as to + V-bare</strong> (để làm gì).<br>- Ta chọn phương án <strong>in order to</strong>.<br>- Loại <strong>so that</strong>, <strong>in order that</strong>, và <strong>because</strong> vì tất cả đều là liên từ bắt buộc theo sau bởi một mệnh đề có chủ ngữ và động từ chia thì.<br><br><strong>Dịch câu:</strong><br><em>Đội ngũ quản lý cấp cao đã tổ chức một cuộc họp khẩn cấp để xem xét thâm hụt doanh thu hàng quý.</em>"
    },
    {
        "question": "Employees may work remotely on alternating Fridays, ______ all project milestones are fulfilled on time.",
        "options": {
            "A": "in spite of",
            "B": "as long as",
            "C": "due to",
            "D": "regardless of"
        },
        "answer": "B",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">B. as long as</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Phía sau chỗ trống là mệnh đề điều kiện (<em>all project milestones are fulfilled on time</em>).<br>- Liên từ chỉ điều kiện: <strong>as long as / so long as = provided that = if</strong> (miễn là / với điều kiện là...).<br>- Ta chọn phương án <strong>as long as</strong>.<br>- Các phương án <strong>in spite of</strong>, <strong>due to</strong>, và <strong>regardless of</strong> đều là giới từ, không đi với mệnh đề có động từ chia thì.<br><br><strong>Dịch câu:</strong><br><em>Nhân viên có thể làm việc từ xa vào các ngày thứ Sáu xen kẽ, miễn là tất cả các mốc tiến độ dự án được hoàn thành đúng hạn.</em>"
    },
    {
        "question": "The commercial district experienced a prolonged power disruption; ______, retail businesses suffered substantial sales losses.",
        "options": {
            "A": "although",
            "B": "whereas",
            "C": "consequently",
            "D": "because"
        },
        "answer": "C",
        "explanation": "<strong>Đáp án đúng: <span class=\"hl-green\">C. consequently</span></strong><br><br><strong>Giải thích chi tiết:</strong><br>- Bẫy trạng từ liên kết chỉ kết quả: Đứng sau dấu chấm phẩy (;) và trước dấu phẩy (,) nối hai mệnh đề nguyên nhân - kết quả độc lập.<br>- <strong>Consequently = Therefore = As a result</strong> (Hệ quả là / Do đó...).<br>- Các từ <em>although</em>, <em>whereas</em>, <em>because</em> là liên từ phụ thuộc, không đứng độc lập sau dấu chấm phẩy có dấu phẩy theo sau để ngăn cách mệnh đề chính như vậy.<br>- Do đó chọn phương án <strong>consequently</strong>.<br><br><strong>Dịch câu:</strong><br><em>Khu thương mại đã trải qua tình trạng mất điện kéo dài; hệ quả là, các doanh nghiệp bán lẻ đã chịu tổn thất doanh thu đáng kể.</em>"
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

ch9 = next(c for c in data if c.get("id") == 9)
ch9["questions"] = ch9_questions
print(f"Updated Chapter 9 questions ({len(ch9_questions)} questions).")

ch9_ans = [q["answer"] for q in ch9_questions]
print("Chapter 9 Answer Distribution:", {opt: ch9_ans.count(opt) for opt in ['A', 'B', 'C', 'D']})

new_json_str = json.dumps(data, ensure_ascii=False, indent=2)
new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open(data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Chapter 9 update successfully written to data.js!")
