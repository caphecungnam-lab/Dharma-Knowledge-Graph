window.DHARMA_GRAPH_SCOPES = {
  "default_mode": "giac_khang",
  "modes": {
    "giac_khang": {
      "metadata": {
        "title": "Dharma Knowledge Graph: Giác Khang Corpus",
        "version": "0.1",
        "mode": "giac_khang",
        "content_hash": "5c453319f08e887b114988a043ff59e6c7e1b969bd1ebc4d1bc5af8e08fca431",
        "source_files": [
          "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json"
        ]
      },
      "summary": {
        "node_count": 20,
        "relationship_count": 25,
        "node_type_counts": {
          "Citation": 1,
          "Concept": 5,
          "Corpus": 1,
          "Document": 1,
          "Evidence": 5,
          "Source": 1,
          "Term": 6
        },
        "relationship_type_counts": {
          "BELONGS_TO_CORPUS": 2,
          "DENOTES": 6,
          "DERIVED_FROM": 7,
          "HAS_CITATION": 5,
          "HAS_DOCUMENT": 1,
          "RELATED_TO": 4
        },
        "source_badge_counts": {
          "corpus": 1,
          "reviewed": 5,
          "seed": 14
        }
      },
      "nodes": [
        {
          "id": "citation_youtube_fisp_arohzy8",
          "type": "Citation",
          "name": "YouTube citation for FISpARohzy8",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "locator": "video root",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_kinh_sau_sau",
          "type": "Concept",
          "name": "Kinh Sáu Sáu",
          "language": "vi",
          "category": "text_topic",
          "description": "Pilot topic concept for Giác Khang teachings on Kinh Sáu Sáu.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_luc_can_luc_tran_luc_thuc",
          "type": "Concept",
          "name": "Lục căn, lục trần, lục thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Grouping concept for six faculties, six objects, and six consciousnesses.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_can",
          "type": "Concept",
          "name": "Sáu căn",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense faculties in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_thuc",
          "type": "Concept",
          "name": "Sáu thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six consciousnesses in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_tran",
          "type": "Concept",
          "name": "Sáu trần",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense objects in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "corpus_giac_khang",
          "type": "Corpus",
          "name": "Giác Khang Corpus",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "corpus"
        },
        {
          "id": "document_transcript_fisp_arohzy8",
          "type": "Document",
          "name": "Transcript placeholder for 1A. KINH 6 6 L2CÂU 1 P1",
          "document_kind": "transcript",
          "language": "vi",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "source_kind": "youtube",
          "review_status": "unreviewed",
          "notes": "Transcript not yet imported. Evidence must not be created without real excerpt text and timestamp.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_fisp_arohzy8_0001",
          "type": "Evidence",
          "name": "VTT caption excerpt 0001 from FISpARohzy8",
          "evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:18.720",
          "end_time": "00:01:39.030",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "reviewed_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0002",
          "type": "Evidence",
          "name": "VTT caption excerpt 0002 from FISpARohzy8",
          "evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:39.040",
          "end_time": "00:01:53.190",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "reviewed_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0003",
          "type": "Evidence",
          "name": "VTT caption excerpt 0003 from FISpARohzy8",
          "evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:53.200",
          "end_time": "00:02:16.110",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "reviewed_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0004",
          "type": "Evidence",
          "name": "VTT caption excerpt 0004 from FISpARohzy8",
          "evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:02:16.120",
          "end_time": "00:02:37.949",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "reviewed_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0005",
          "type": "Evidence",
          "name": "VTT caption excerpt 0005 from FISpARohzy8",
          "evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:02:37.959",
          "end_time": "00:02:54.470",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "reviewed_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "source_youtube_fisp_arohzy8",
          "type": "Source",
          "name": "YouTube video FISpARohzy8",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "channel": "PHÁP ÂM SƯ KHANG",
          "title": "1A. KINH 6 6 L2CÂU 1 P1",
          "speaker": "HT. Thích Giác Khang",
          "topic": "Kinh Sáu Sáu",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_can_hv",
          "type": "Term",
          "name": "lục căn",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_thuc_hv",
          "type": "Term",
          "name": "lục thức",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_tran_hv",
          "type": "Term",
          "name": "lục trần",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_can_vi",
          "type": "Term",
          "name": "sáu căn",
          "language": "vi",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_thuc_vi",
          "type": "Term",
          "name": "sáu thức",
          "language": "vi",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_tran_vi",
          "type": "Term",
          "name": "sáu trần",
          "language": "vi",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        }
      ],
      "relationships": [
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_can_hv",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_thuc_hv",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_tran_hv",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_can_vi",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_thuc_vi",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_tran_vi",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_youtube_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_fisp_arohzy8_0001",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0002",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0003",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0004",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0005",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0001",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0002",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0003",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0004",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0005",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "HAS_DOCUMENT",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_luc_can_luc_tran_luc_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_can",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_tran",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        }
      ]
    },
    "seeds_only": {
      "metadata": {
        "title": "Dharma Knowledge Graph: Seeds",
        "version": "0.1",
        "mode": "seeds_only",
        "content_hash": "be3c8509bc22146dbdb4318d3edb5a1db567757c1e1a8dbf2b7e4902623c66fa",
        "source_files": [
          "data/seeds/concepts.json",
          "data/seeds/core.json",
          "data/seeds/dhammapada.json",
          "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "data/seeds/giac_khang_pilot.json",
          "data/seeds/giac_khang_real_evidence_sample.json",
          "data/seeds/heart_sutra.json",
          "data/seeds/places_traditions.json",
          "data/seeds/terms.json",
          "data/seeds/terms_extended.json",
          "data/seeds/terms_remaining.json"
        ]
      },
      "summary": {
        "node_count": 148,
        "relationship_count": 228,
        "node_type_counts": {
          "Citation": 21,
          "Concept": 42,
          "Corpus": 2,
          "Document": 2,
          "Evidence": 4,
          "Person": 1,
          "Place": 6,
          "School": 5,
          "Source": 2,
          "Term": 59,
          "Text": 3,
          "Work": 1
        },
        "relationship_type_counts": {
          "AUTHORED_BY": 1,
          "BELONGS_TO_CORPUS": 8,
          "BELONGS_TO_SCHOOL": 13,
          "CITES": 17,
          "DEFINES": 60,
          "DENOTES": 6,
          "DERIVED_FROM": 7,
          "EVIDENCES": 3,
          "HAS_CITATION": 3,
          "HAS_DOCUMENT": 3,
          "HAS_EVIDENCE": 3,
          "LOCATED_IN": 4,
          "MENTIONS": 59,
          "RELATED_TO": 41
        },
        "source_badge_counts": {
          "corpus": 2,
          "seed": 146
        }
      },
      "nodes": [
        {
          "id": "citation_dhammapada_1",
          "type": "Citation",
          "name": "Dhammapada 1",
          "source": "Dhammapada",
          "locator": "Verse 1",
          "notes": "Pilot citation for the relation between mind, intention, and suffering.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_129",
          "type": "Citation",
          "name": "Dhammapada 129",
          "source": "Dhammapada",
          "locator": "Verse 129",
          "notes": "Pilot citation for non-harming and empathy toward beings.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_183",
          "type": "Citation",
          "name": "Dhammapada 183",
          "source": "Dhammapada",
          "locator": "Verse 183",
          "notes": "Pilot citation for ethical restraint, wholesome cultivation, and mental purification.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_2",
          "type": "Citation",
          "name": "Dhammapada 2",
          "source": "Dhammapada",
          "locator": "Verse 2",
          "notes": "Pilot citation for the relation between mind, intention, and well-being.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_21",
          "type": "Citation",
          "name": "Dhammapada 21",
          "source": "Dhammapada",
          "locator": "Verse 21",
          "notes": "Pilot citation for heedfulness as a path quality.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_277",
          "type": "Citation",
          "name": "Dhammapada 277",
          "source": "Dhammapada",
          "locator": "Verse 277",
          "notes": "Pilot citation for impermanence.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_279",
          "type": "Citation",
          "name": "Dhammapada 279",
          "source": "Dhammapada",
          "locator": "Verse 279",
          "notes": "Pilot citation for not-self.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_35",
          "type": "Citation",
          "name": "Dhammapada 35",
          "source": "Dhammapada",
          "locator": "Verse 35",
          "notes": "Pilot citation for the training and restraint of mind.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_5",
          "type": "Citation",
          "name": "Dhammapada 5",
          "source": "Dhammapada",
          "locator": "Verse 5",
          "notes": "Pilot citation for non-hatred and reconciliation.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_50",
          "type": "Citation",
          "name": "Dhammapada 50",
          "source": "Dhammapada",
          "locator": "Verse 50",
          "notes": "Pilot citation for self-examination in ethical practice.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_pratityasamutpada",
          "type": "Citation",
          "name": "Giac Khang notes, Dependent arising excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#dependent-arising",
          "notes": "Pilot citation for evidence about dependent arising.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_middle_way",
          "type": "Citation",
          "name": "Giac Khang notes, Middle Way excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#middle-way",
          "notes": "Pilot citation for evidence about the middle way.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_sunyata",
          "type": "Citation",
          "name": "Giac Khang notes, Sunyata excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#sunyata",
          "notes": "Pilot citation for evidence about emptiness.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_dharmas",
          "type": "Citation",
          "name": "Heart Sutra Dharmas Passage",
          "source": "Heart Sutra",
          "locator": "Dharmas and categories passage",
          "notes": "Pilot citation for sense bases, elements, dependent arising categories, and the four truths.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_mantra",
          "type": "Citation",
          "name": "Heart Sutra Mantra Passage",
          "source": "Heart Sutra",
          "locator": "Mantra passage",
          "notes": "Pilot citation for mantra and prajnaparamita as a practice expression.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_opening",
          "type": "Citation",
          "name": "Heart Sutra Opening",
          "source": "Heart Sutra",
          "locator": "Opening scene",
          "notes": "Pilot citation for Avalokitesvara, prajnaparamita, and the five aggregates.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_skandhas",
          "type": "Citation",
          "name": "Heart Sutra Skandhas Passage",
          "source": "Heart Sutra",
          "locator": "Five aggregates passage",
          "notes": "Pilot citation for the relationship between form, the aggregates, and emptiness.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_24_18",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 24.18",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 24, verse 18",
          "notes": "Pilot citation for dependent designation, emptiness, and the middle way.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_24_19",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 24.19",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 24, verse 19",
          "notes": "Pilot citation for the relation between dependent arising and emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_25_19",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 25.19",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 25, verse 19",
          "notes": "Pilot citation for the relation between samsara and nirvana in Madhyamaka analysis.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_youtube_fisp_arohzy8",
          "type": "Citation",
          "name": "YouTube citation for FISpARohzy8",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "locator": "video root",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_ahimsa",
          "type": "Concept",
          "name": "Ahimsa",
          "pali": "avihimsa",
          "sanskrit": "ahimsa",
          "category": "ethics",
          "description": "Non-harming; an ethical orientation of restraint from violence and injury.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_anatta",
          "type": "Concept",
          "name": "Anatta",
          "pali": "anatta",
          "sanskrit": "anatman",
          "category": "doctrine",
          "description": "Not-self; the absence of a permanent, independent self in conditioned phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_anicca",
          "type": "Concept",
          "name": "Anicca",
          "pali": "anicca",
          "sanskrit": "anitya",
          "category": "doctrine",
          "description": "Impermanence; the conditioned nature of phenomena as changing and unstable.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_appamada",
          "type": "Concept",
          "name": "Appamada",
          "pali": "appamada",
          "sanskrit": "apramada",
          "category": "practice",
          "description": "Heedfulness or diligent care in practice.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_avalokitesvara",
          "type": "Concept",
          "name": "Avalokitesvara",
          "sanskrit": "avalokitesvara",
          "category": "mahayana",
          "description": "A bodhisattva associated with compassion and prominent in the Heart Sutra setting.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_avidya",
          "type": "Concept",
          "name": "Avidya",
          "pali": "avijja",
          "sanskrit": "avidya",
          "category": "psychology",
          "description": "Ignorance or misknowing, especially regarding the nature of reality and the path.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_bodhicitta",
          "type": "Concept",
          "name": "Bodhicitta",
          "sanskrit": "bodhicitta",
          "category": "mahayana",
          "description": "The awakened mind or aspiration to attain awakening for the benefit of all beings.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_bodhisattva",
          "type": "Concept",
          "name": "Bodhisattva",
          "pali": "bodhisatta",
          "sanskrit": "bodhisattva",
          "category": "mahayana",
          "description": "A being oriented toward awakening, especially for the liberation of all beings in Mahayana contexts.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_brahmaviharas",
          "type": "Concept",
          "name": "Brahmaviharas",
          "pali": "brahmavihara",
          "sanskrit": "brahmavihara",
          "category": "practice",
          "description": "The four divine abodes: loving-kindness, compassion, sympathetic joy, and equanimity.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_citta",
          "type": "Concept",
          "name": "Citta",
          "pali": "citta",
          "sanskrit": "citta",
          "category": "psychology",
          "description": "Mind, heart, or mental orientation; a key term for understanding intention and experience.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_dukkha",
          "type": "Concept",
          "name": "Dukkha",
          "pali": "dukkha",
          "sanskrit": "duhkha",
          "description": "A central Dharma concept often translated as suffering, unsatisfactoriness, or stress.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_dhatu",
          "type": "Concept",
          "name": "Elements",
          "pali": "dhatu",
          "sanskrit": "dhatu",
          "category": "analysis",
          "description": "Elements or domains used to analyze experience and phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_skandhas",
          "type": "Concept",
          "name": "Five Aggregates",
          "pali": "khandha",
          "sanskrit": "skandha",
          "category": "analysis",
          "description": "Form, feeling, perception, formations, and consciousness as a framework for analyzing experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_form",
          "type": "Concept",
          "name": "Form",
          "pali": "rupa",
          "sanskrit": "rupa",
          "category": "analysis",
          "description": "Material form; one of the five aggregates.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_four_noble_truths",
          "type": "Concept",
          "name": "Four Noble Truths",
          "pali": "cattari ariyasaccani",
          "sanskrit": "catvari aryasatyani",
          "category": "doctrine",
          "description": "The teaching of suffering, its origin, its cessation, and the path leading to cessation.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_karma",
          "type": "Concept",
          "name": "Karma",
          "pali": "kamma",
          "sanskrit": "karma",
          "category": "ethics",
          "description": "Intentional action and its ethical consequences.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_karuna",
          "type": "Concept",
          "name": "Karuna",
          "pali": "karuna",
          "sanskrit": "karuna",
          "category": "practice",
          "description": "Compassion; the wish for beings to be free from suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_kinh_sau_sau",
          "type": "Concept",
          "name": "Kinh Sáu Sáu",
          "language": "vi",
          "category": "text_topic",
          "description": "Pilot topic concept for Giác Khang teachings on Kinh Sáu Sáu.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_klesha",
          "type": "Concept",
          "name": "Klesha",
          "pali": "kilesa",
          "sanskrit": "klesa",
          "category": "psychology",
          "description": "Afflictive mental states that disturb the mind and condition suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_luc_can_luc_tran_luc_thuc",
          "type": "Concept",
          "name": "Lục căn, lục trần, lục thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Grouping concept for six faculties, six objects, and six consciousnesses.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_mantra",
          "type": "Concept",
          "name": "Mantra",
          "sanskrit": "mantra",
          "category": "practice",
          "description": "A sacred utterance or formula used in contemplative and ritual contexts.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_metta",
          "type": "Concept",
          "name": "Metta",
          "pali": "metta",
          "sanskrit": "maitri",
          "category": "practice",
          "description": "Loving-kindness; the cultivation of goodwill and friendliness.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_middle_way",
          "type": "Concept",
          "name": "Middle Way",
          "pali": "majjhima patipada",
          "sanskrit": "madhyama pratipad",
          "category": "practice",
          "description": "A path avoiding extremes, often framed as avoiding indulgence and self-mortification or eternalism and nihilism.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_mudita",
          "type": "Concept",
          "name": "Mudita",
          "pali": "mudita",
          "sanskrit": "mudita",
          "category": "practice",
          "description": "Sympathetic joy; delight in the welfare and happiness of others.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_nirvana",
          "type": "Concept",
          "name": "Nirvana",
          "pali": "nibbana",
          "sanskrit": "nirvana",
          "category": "liberation",
          "description": "Liberation; the extinguishing of greed, hatred, and delusion.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_noble_eightfold_path",
          "type": "Concept",
          "name": "Noble Eightfold Path",
          "pali": "ariya atthangika magga",
          "sanskrit": "arya astangika marga",
          "category": "practice",
          "description": "The path of right view, intention, speech, action, livelihood, effort, mindfulness, and concentration.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_paramita",
          "type": "Concept",
          "name": "Paramita",
          "pali": "parami",
          "sanskrit": "paramita",
          "category": "mahayana",
          "description": "Perfection or transcendent virtue cultivated on the bodhisattva path.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_prajna",
          "type": "Concept",
          "name": "Prajna",
          "pali": "panna",
          "sanskrit": "prajna",
          "category": "wisdom",
          "description": "Wisdom or liberating insight into the nature of phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_prajnaparamita",
          "type": "Concept",
          "name": "Prajnaparamita",
          "sanskrit": "prajnaparamita",
          "category": "mahayana",
          "description": "The perfection of wisdom; a central theme in Mahayana sutra literature.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_pratityasamutpada",
          "type": "Concept",
          "name": "Pratityasamutpada",
          "pali": "paticcasamuppada",
          "sanskrit": "pratityasamutpada",
          "category": "doctrine",
          "description": "Dependent arising; the principle that phenomena arise in dependence on causes and conditions.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_samadhi",
          "type": "Concept",
          "name": "Samadhi",
          "pali": "samadhi",
          "sanskrit": "samadhi",
          "category": "practice",
          "description": "Collectedness, concentration, or meditative absorption.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_samsara",
          "type": "Concept",
          "name": "Samsara",
          "pali": "samsara",
          "sanskrit": "samsara",
          "category": "cosmology",
          "description": "The cycle of birth, death, and rebirth conditioned by ignorance and craving.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sila",
          "type": "Concept",
          "name": "Sila",
          "pali": "sila",
          "sanskrit": "sila",
          "category": "ethics",
          "description": "Ethical conduct or moral discipline.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_ayatana",
          "type": "Concept",
          "name": "Six Sense Bases",
          "pali": "ayatana",
          "sanskrit": "ayatana",
          "category": "analysis",
          "description": "The internal and external sense bases involved in perceptual experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sunyata",
          "type": "Concept",
          "name": "Sunyata",
          "sanskrit": "sunyata",
          "description": "A Mahayana concept commonly translated as emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_can",
          "type": "Concept",
          "name": "Sáu căn",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense faculties in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_thuc",
          "type": "Concept",
          "name": "Sáu thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six consciousnesses in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_tran",
          "type": "Concept",
          "name": "Sáu trần",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense objects in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_tanha",
          "type": "Concept",
          "name": "Tanha",
          "pali": "tanha",
          "sanskrit": "trsna",
          "category": "psychology",
          "description": "Craving or thirst; a central condition in the arising of suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_three_marks",
          "type": "Concept",
          "name": "Three Marks of Existence",
          "pali": "tilakkhana",
          "sanskrit": "trilaksana",
          "category": "doctrine",
          "description": "The marks of impermanence, suffering or unsatisfactoriness, and not-self.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_two_truths",
          "type": "Concept",
          "name": "Two Truths",
          "sanskrit": "satya-dvaya",
          "category": "mahayana",
          "description": "The distinction between conventional truth and ultimate truth.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_upekkha",
          "type": "Concept",
          "name": "Upekkha",
          "pali": "upekkha",
          "sanskrit": "upeksa",
          "category": "practice",
          "description": "Equanimity; balanced presence toward changing experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "corpus_giac_khang_pilot",
          "type": "Corpus",
          "name": "Giac Khang Pilot Corpus",
          "language": "Vietnamese",
          "scope": "21-day MVP evidence-first pilot",
          "description": "A bounded pilot corpus for testing evidence-first Dharma Knowledge Graph ingestion.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "corpus"
        },
        {
          "id": "corpus_giac_khang",
          "type": "Corpus",
          "name": "Giác Khang Corpus",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "corpus"
        },
        {
          "id": "document_giac_khang_mvp_notes",
          "type": "Document",
          "name": "Giac Khang MVP Notes",
          "document_type": "study_note",
          "language": "Vietnamese",
          "locator": "pilot-note-001",
          "description": "A single pilot document used to test document-to-evidence modeling.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "document_transcript_fisp_arohzy8",
          "type": "Document",
          "name": "Transcript placeholder for 1A. KINH 6 6 L2CÂU 1 P1",
          "document_kind": "transcript",
          "language": "vi",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "source_kind": "youtube",
          "review_status": "unreviewed",
          "notes": "Transcript not yet imported. Evidence must not be created without real excerpt text and timestamp.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_pratityasamutpada_001",
          "type": "Evidence",
          "name": "Evidence: Dependent arising as relational explanation",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#dependent-arising",
          "evidence_text": "Dependent arising is represented as the principle that phenomena appear through conditions and relationships.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_middle_way_001",
          "type": "Evidence",
          "name": "Evidence: Middle Way avoids extremes",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#middle-way",
          "evidence_text": "The middle way is represented as avoiding fixed extremes while preserving practical conventional meaning.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_sunyata_001",
          "type": "Evidence",
          "name": "Evidence: Sunyata as non-independent existence",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#sunyata",
          "evidence_text": "Emptiness is represented as the absence of independent, self-existing nature rather than simple nothingness.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_real_sample_001",
          "type": "Evidence",
          "name": "Unreviewed Giac Khang transcript evidence sample",
          "evidence_text": "Placeholder transcript excerpt for DKG-002 schema validation. This text is not reviewed and must be replaced with a real transcript excerpt before use.",
          "evidence_type": "transcript_excerpt",
          "language": "Vietnamese",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=placeholder_unreviewed",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "youtube-placeholder#t=00:00:00",
          "start_time": "00:00:00",
          "end_time": "00:00:30",
          "speaker": "Giac Khang",
          "review_status": "unreviewed",
          "notes": "Unreviewed placeholder node for DKG-002. Do not treat as verified teaching evidence.",
          "source_file": "data/seeds/giac_khang_real_evidence_sample.json",
          "source_badge": "seed"
        },
        {
          "id": "person_nagarjuna",
          "type": "Person",
          "name": "Nagarjuna",
          "tradition": "Mahayana",
          "description": "A major Buddhist philosopher associated with Madhyamaka.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "place_bodh_gaya",
          "type": "Place",
          "name": "Bodh Gaya",
          "country": "India",
          "region": "Bihar",
          "description": "A major Buddhist pilgrimage place associated with the Buddha's awakening.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_gandhara",
          "type": "Place",
          "name": "Gandhara",
          "country": "Historical region",
          "region": "Northwest South Asia",
          "description": "A historical Buddhist region important for textual and artistic transmission.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_magadha",
          "type": "Place",
          "name": "Magadha",
          "country": "India",
          "region": "Eastern India",
          "description": "An ancient region important in early Buddhist history.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_nalanda",
          "type": "Place",
          "name": "Nalanda",
          "country": "India",
          "region": "Bihar",
          "description": "A historic center of Buddhist monastic learning.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_sarnath",
          "type": "Place",
          "name": "Sarnath",
          "country": "India",
          "region": "Uttar Pradesh",
          "description": "A major Buddhist pilgrimage place associated with the first teaching.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_sri_lanka",
          "type": "Place",
          "name": "Sri Lanka",
          "country": "Sri Lanka",
          "region": "South Asia",
          "description": "A major historical center for Theravada Buddhist transmission.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_early_buddhism",
          "type": "School",
          "name": "Early Buddhism",
          "description": "A working category for early Buddhist teachings and textual layers.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_madhyamaka",
          "type": "School",
          "name": "Madhyamaka",
          "description": "A Mahayana philosophical school associated with analysis of emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "school_mahayana",
          "type": "School",
          "name": "Mahayana",
          "description": "A broad family of Buddhist traditions emphasizing the bodhisattva path.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_pali_canon",
          "type": "School",
          "name": "Pali Canon",
          "description": "A textual tradition preserving canonical materials in Pali.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_theravada",
          "type": "School",
          "name": "Theravada",
          "description": "A Buddhist tradition preserving the Pali Canon.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "source_giac_khang_notes",
          "type": "Source",
          "name": "Giac Khang Study Notes",
          "source_type": "local_notes",
          "language": "Vietnamese",
          "description": "Pilot source material used to model evidence before API, embeddings, or LLM extraction.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "source_youtube_fisp_arohzy8",
          "type": "Source",
          "name": "YouTube video FISpARohzy8",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "channel": "PHÁP ÂM SƯ KHANG",
          "title": "1A. KINH 6 6 L2CÂU 1 P1",
          "speaker": "HT. Thích Giác Khang",
          "topic": "Kinh Sáu Sáu",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ahimsa_sanskrit",
          "type": "Term",
          "name": "ahimsa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "ahimsa",
          "translation": "non-harming",
          "notes": "Sanskrit term for non-harming.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anatman_sanskrit",
          "type": "Term",
          "name": "anatman",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "anatman",
          "translation": "not-self; no self",
          "notes": "Sanskrit form corresponding to Pali anatta.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anatta_pali",
          "type": "Term",
          "name": "anatta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "anatta",
          "translation": "not-self",
          "notes": "Pali form used for the doctrine of not-self.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anicca_pali",
          "type": "Term",
          "name": "anicca",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "anicca",
          "translation": "impermanent",
          "notes": "Pali form used for impermanence.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anitya_sanskrit",
          "type": "Term",
          "name": "anitya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "anitya",
          "translation": "impermanent",
          "notes": "Sanskrit form used for impermanence.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_appamada_pali",
          "type": "Term",
          "name": "appamada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "appamada",
          "translation": "heedfulness; diligence",
          "notes": "A central practice quality highlighted in the Dhammapada.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ariya_atthangika_magga_pali",
          "type": "Term",
          "name": "ariya atthangika magga",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "ariya atthangika magga",
          "translation": "noble eightfold path",
          "notes": "Pali phrase for the Noble Eightfold Path.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_arya_astangika_marga_sanskrit",
          "type": "Term",
          "name": "arya astangika marga",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "arya astangika marga",
          "translation": "noble eightfold path",
          "notes": "Sanskrit phrase for the Noble Eightfold Path.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avalokitesvara_sanskrit",
          "type": "Term",
          "name": "avalokitesvara",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "avalokitesvara",
          "translation": "Avalokitesvara",
          "notes": "Sanskrit name of the bodhisattva associated with compassion.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avidya_sanskrit",
          "type": "Term",
          "name": "avidya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "avidya",
          "translation": "ignorance",
          "notes": "Sanskrit term for ignorance or misknowing.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avihimsa_pali",
          "type": "Term",
          "name": "avihimsa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "avihimsa",
          "translation": "non-harming",
          "notes": "Pali term related to non-harming.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avijja_pali",
          "type": "Term",
          "name": "avijja",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "avijja",
          "translation": "ignorance",
          "notes": "Pali term for ignorance or misknowing.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ayatana_pali",
          "type": "Term",
          "name": "ayatana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "ayatana",
          "translation": "sense base",
          "notes": "Pali and Sanskrit term for sense base.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_bodhicitta_sanskrit",
          "type": "Term",
          "name": "bodhicitta",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "bodhicitta",
          "translation": "awakening mind",
          "notes": "Sanskrit term for the awakened mind or aspiration toward awakening.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_bodhisattva_sanskrit",
          "type": "Term",
          "name": "bodhisattva",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "bodhisattva",
          "translation": "awakening being",
          "notes": "Sanskrit term for a being oriented toward awakening.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_brahmavihara_pali",
          "type": "Term",
          "name": "brahmavihara",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "brahmavihara",
          "translation": "divine abode",
          "notes": "Pali term for the divine abodes.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_cattari_ariyasaccani_pali",
          "type": "Term",
          "name": "cattari ariyasaccani",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "cattari ariyasaccani",
          "translation": "four noble truths",
          "notes": "Pali phrase for the Four Noble Truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_catvari_aryasatyani_sanskrit",
          "type": "Term",
          "name": "catvari aryasatyani",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "catvari aryasatyani",
          "translation": "four noble truths",
          "notes": "Sanskrit phrase for the Four Noble Truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_citta_pali",
          "type": "Term",
          "name": "citta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "citta",
          "translation": "mind; heart",
          "notes": "A term for mind, heart, or mental orientation.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_dhatu_pali",
          "type": "Term",
          "name": "dhatu",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "dhatu",
          "translation": "element; domain",
          "notes": "Pali and Sanskrit term for element or domain.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_duhkha_sanskrit",
          "type": "Term",
          "name": "duhkha",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "duhkha",
          "translation": "suffering; unsatisfactoriness",
          "notes": "Sanskrit cognate of Pali dukkha.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_dukkha_pali",
          "type": "Term",
          "name": "dukkha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "dukkha",
          "translation": "suffering; unsatisfactoriness; stress",
          "notes": "A core Pali term in the analysis of conditioned experience.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_kamma_pali",
          "type": "Term",
          "name": "kamma",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "kamma",
          "translation": "intentional action",
          "notes": "Pali form corresponding to Sanskrit karma.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_karma_sanskrit",
          "type": "Term",
          "name": "karma",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "karma",
          "translation": "intentional action",
          "notes": "Sanskrit form for intentional action and its consequences.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_karuna_pali",
          "type": "Term",
          "name": "karuna",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "karuna",
          "translation": "compassion",
          "notes": "Pali and Sanskrit term for compassion.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_kilesa_pali",
          "type": "Term",
          "name": "kilesa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "kilesa",
          "translation": "affliction; defilement",
          "notes": "Pali term for afflictive mental states.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_klesa_sanskrit",
          "type": "Term",
          "name": "klesa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "klesa",
          "translation": "affliction",
          "notes": "Sanskrit term for afflictive mental states.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_can_hv",
          "type": "Term",
          "name": "lục căn",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_thuc_hv",
          "type": "Term",
          "name": "lục thức",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_tran_hv",
          "type": "Term",
          "name": "lục trần",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_madhyama_pratipad_sanskrit",
          "type": "Term",
          "name": "madhyama pratipad",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "madhyama pratipad",
          "translation": "middle way",
          "notes": "Sanskrit phrase for the middle way.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_majjhima_patipada_pali",
          "type": "Term",
          "name": "majjhima patipada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "majjhima patipada",
          "translation": "middle way",
          "notes": "Pali phrase for the middle way.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_mantra_sanskrit",
          "type": "Term",
          "name": "mantra",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "mantra",
          "translation": "sacred utterance",
          "notes": "Sanskrit term for a sacred utterance or formula.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_metta_pali",
          "type": "Term",
          "name": "metta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "metta",
          "translation": "loving-kindness",
          "notes": "Pali term for loving-kindness.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_mudita_pali",
          "type": "Term",
          "name": "mudita",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "mudita",
          "translation": "sympathetic joy",
          "notes": "Pali and Sanskrit term for sympathetic joy.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_nibbana_pali",
          "type": "Term",
          "name": "nibbana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "nibbana",
          "translation": "liberation; extinguishing",
          "notes": "Pali term commonly rendered as nirvana.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_nirvana_sanskrit",
          "type": "Term",
          "name": "nirvana",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "nirvana",
          "translation": "liberation; extinguishing",
          "notes": "Sanskrit form corresponding to Pali nibbana.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_panna_pali",
          "type": "Term",
          "name": "panna",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "panna",
          "translation": "wisdom",
          "notes": "Pali term corresponding to Sanskrit prajna.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_paramita_sanskrit",
          "type": "Term",
          "name": "paramita",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "paramita",
          "translation": "perfection",
          "notes": "Sanskrit term for perfection or transcendent virtue.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_paticcasamuppada_pali",
          "type": "Term",
          "name": "paticcasamuppada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "paticcasamuppada",
          "translation": "dependent arising",
          "notes": "Pali term for dependent arising.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_prajna_sanskrit",
          "type": "Term",
          "name": "prajna",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "prajna",
          "translation": "wisdom",
          "notes": "Sanskrit term for wisdom or liberating insight.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_prajnaparamita_sanskrit",
          "type": "Term",
          "name": "prajnaparamita",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "prajnaparamita",
          "translation": "perfection of wisdom",
          "notes": "Sanskrit term for the perfection of wisdom.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_pratityasamutpada_sanskrit",
          "type": "Term",
          "name": "pratityasamutpada",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "pratityasamutpada",
          "translation": "dependent arising",
          "notes": "Sanskrit term for dependent arising.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_rupa_pali",
          "type": "Term",
          "name": "rupa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "rupa",
          "translation": "form; material form",
          "notes": "Pali and Sanskrit term for form.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_samadhi_pali",
          "type": "Term",
          "name": "samadhi",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "samadhi",
          "translation": "concentration; collectedness",
          "notes": "Pali and Sanskrit term for meditative collectedness.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_samsara_pali",
          "type": "Term",
          "name": "samsara",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "samsara",
          "translation": "cycle of rebirth",
          "notes": "Pali form for the cycle of conditioned existence.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_satya_dvaya_sanskrit",
          "type": "Term",
          "name": "satya-dvaya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "satya-dvaya",
          "translation": "two truths",
          "notes": "Sanskrit phrase for the two truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sila_pali",
          "type": "Term",
          "name": "sila",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "sila",
          "translation": "ethical conduct",
          "notes": "Pali term for moral discipline or ethical conduct.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_skandha_sanskrit",
          "type": "Term",
          "name": "skandha",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "skandha",
          "translation": "aggregate",
          "notes": "Sanskrit term for aggregate.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sunyata_sanskrit",
          "type": "Term",
          "name": "sunyata",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "sunyata",
          "translation": "emptiness",
          "notes": "A key Mahayana term, especially important in Madhyamaka contexts.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_can_vi",
          "type": "Term",
          "name": "sáu căn",
          "language": "vi",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_thuc_vi",
          "type": "Term",
          "name": "sáu thức",
          "language": "vi",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_tran_vi",
          "type": "Term",
          "name": "sáu trần",
          "language": "vi",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_tanha_pali",
          "type": "Term",
          "name": "tanha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "tanha",
          "translation": "craving; thirst",
          "notes": "Pali term for craving.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_tilakkhana_pali",
          "type": "Term",
          "name": "tilakkhana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "tilakkhana",
          "translation": "three marks",
          "notes": "Pali term for the three marks of existence.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_trilaksana_sanskrit",
          "type": "Term",
          "name": "trilaksana",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "trilaksana",
          "translation": "three marks",
          "notes": "Sanskrit term for the three marks of existence.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_trsna_sanskrit",
          "type": "Term",
          "name": "trsna",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "trsna",
          "translation": "craving; thirst",
          "notes": "Sanskrit term corresponding to Pali tanha.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_upekkha_pali",
          "type": "Term",
          "name": "upekkha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "upekkha",
          "translation": "equanimity",
          "notes": "Pali term for equanimity.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_upeksa_sanskrit",
          "type": "Term",
          "name": "upeksa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "upeksa",
          "translation": "equanimity",
          "notes": "Sanskrit term corresponding to Pali upekkha.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "text_dhammapada",
          "type": "Text",
          "name": "Dhammapada",
          "language": "Pali",
          "tradition": "Theravada",
          "description": "A collection of verses from the Pali Canon, traditionally arranged into 26 chapters.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "text_heart_sutra",
          "type": "Text",
          "name": "Heart Sutra",
          "alternate_names": [
            "Prajnaparamita Hrdaya",
            "Heart of the Perfection of Wisdom"
          ],
          "language": "Sanskrit",
          "tradition": "Mahayana",
          "description": "A short Mahayana sutra associated with the perfection of wisdom literature and the teaching of emptiness.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "text_mulamadhyamakakarika",
          "type": "Text",
          "name": "Mulamadhyamakakarika",
          "language": "Sanskrit",
          "tradition": "Mahayana",
          "description": "A foundational Madhyamaka text attributed to Nagarjuna.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "work_giac_khang_pilot_teachings",
          "type": "Work",
          "name": "Giac Khang Pilot Teachings",
          "language": "Vietnamese",
          "description": "A pilot work grouping selected notes for the evidence-first MVP.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        }
      ],
      "relationships": [
        {
          "source": "text_mulamadhyamakakarika",
          "type": "AUTHORED_BY",
          "target": "person_nagarjuna",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_middle_way",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_pratityasamutpada",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_sunyata",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "source_giac_khang_notes",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_avalokitesvara",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhicitta",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "person_nagarjuna",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_madhyamaka",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "person_nagarjuna",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_madhyamaka",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_early_buddhism",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_pali_canon",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_theravada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_madhyamaka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_1",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_129",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_183",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_2",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_21",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_277",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_279",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_35",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_5",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_50",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_dharmas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_mantra",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_opening",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_24_18",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_24_19",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_25_19",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_karuna",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_metta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_mudita",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ahimsa_sanskrit",
          "type": "DEFINES",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatman_sanskrit",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatta_pali",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anicca_pali",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anitya_sanskrit",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_appamada_pali",
          "type": "DEFINES",
          "target": "concept_appamada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ariya_atthangika_magga_pali",
          "type": "DEFINES",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_arya_astangika_marga_sanskrit",
          "type": "DEFINES",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avalokitesvara_sanskrit",
          "type": "DEFINES",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avidya_sanskrit",
          "type": "DEFINES",
          "target": "concept_avidya",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avihimsa_pali",
          "type": "DEFINES",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avijja_pali",
          "type": "DEFINES",
          "target": "concept_avidya",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ayatana_pali",
          "type": "DEFINES",
          "target": "concept_ayatana",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_bodhicitta_sanskrit",
          "type": "DEFINES",
          "target": "concept_bodhicitta",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_bodhisattva_sanskrit",
          "type": "DEFINES",
          "target": "concept_bodhisattva",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_brahmavihara_pali",
          "type": "DEFINES",
          "target": "concept_brahmaviharas",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_cattari_ariyasaccani_pali",
          "type": "DEFINES",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_catvari_aryasatyani_sanskrit",
          "type": "DEFINES",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_citta_pali",
          "type": "DEFINES",
          "target": "concept_citta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dhatu_pali",
          "type": "DEFINES",
          "target": "concept_dhatu",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_duhkha_sanskrit",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dukkha_pali",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kamma_pali",
          "type": "DEFINES",
          "target": "concept_karma",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_karma_sanskrit",
          "type": "DEFINES",
          "target": "concept_karma",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_karuna_pali",
          "type": "DEFINES",
          "target": "concept_karuna",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kilesa_pali",
          "type": "DEFINES",
          "target": "concept_klesha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_klesa_sanskrit",
          "type": "DEFINES",
          "target": "concept_klesha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_madhyama_pratipad_sanskrit",
          "type": "DEFINES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_majjhima_patipada_pali",
          "type": "DEFINES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_mantra_sanskrit",
          "type": "DEFINES",
          "target": "concept_mantra",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_metta_pali",
          "type": "DEFINES",
          "target": "concept_metta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_mudita_pali",
          "type": "DEFINES",
          "target": "concept_mudita",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nibbana_pali",
          "type": "DEFINES",
          "target": "concept_nirvana",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nirvana_sanskrit",
          "type": "DEFINES",
          "target": "concept_nirvana",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_panna_pali",
          "type": "DEFINES",
          "target": "concept_prajna",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paramita_sanskrit",
          "type": "DEFINES",
          "target": "concept_paramita",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paticcasamuppada_pali",
          "type": "DEFINES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_prajna_sanskrit",
          "type": "DEFINES",
          "target": "concept_prajna",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_prajnaparamita_sanskrit",
          "type": "DEFINES",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_pratityasamutpada_sanskrit",
          "type": "DEFINES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_rupa_pali",
          "type": "DEFINES",
          "target": "concept_form",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_samadhi_pali",
          "type": "DEFINES",
          "target": "concept_samadhi",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_samsara_pali",
          "type": "DEFINES",
          "target": "concept_samsara",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_satya_dvaya_sanskrit",
          "type": "DEFINES",
          "target": "concept_two_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sila_pali",
          "type": "DEFINES",
          "target": "concept_sila",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_skandha_sanskrit",
          "type": "DEFINES",
          "target": "concept_skandhas",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sunyata_sanskrit",
          "type": "DEFINES",
          "target": "concept_sunyata",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tanha_pali",
          "type": "DEFINES",
          "target": "concept_tanha",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tilakkhana_pali",
          "type": "DEFINES",
          "target": "concept_three_marks",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_trilaksana_sanskrit",
          "type": "DEFINES",
          "target": "concept_three_marks",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_trsna_sanskrit",
          "type": "DEFINES",
          "target": "concept_tanha",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upekkha_pali",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upeksa_sanskrit",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_can_hv",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_thuc_hv",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_tran_hv",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_can_vi",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_thuc_vi",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_tran_vi",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_youtube_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "DERIVED_FROM",
          "target": "source_giac_khang_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "DERIVED_FROM",
          "target": "source_giac_khang_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "EVIDENCES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "EVIDENCES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "EVIDENCES",
          "target": "concept_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_giac_khang_notes",
          "type": "HAS_DOCUMENT",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "HAS_DOCUMENT",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "HAS_DOCUMENT",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_middle_way_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_pratityasamutpada_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_sunyata_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "place_bodh_gaya",
          "type": "LOCATED_IN",
          "target": "place_magadha",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "place_nalanda",
          "type": "LOCATED_IN",
          "target": "place_magadha",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_pali_canon",
          "type": "LOCATED_IN",
          "target": "place_sri_lanka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_theravada",
          "type": "LOCATED_IN",
          "target": "place_sri_lanka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_dukkha",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_karma",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_129",
          "type": "MENTIONS",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_129",
          "type": "MENTIONS",
          "target": "concept_karuna",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_183",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_183",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_2",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_2",
          "type": "MENTIONS",
          "target": "concept_karma",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_21",
          "type": "MENTIONS",
          "target": "concept_appamada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_277",
          "type": "MENTIONS",
          "target": "concept_anicca",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_279",
          "type": "MENTIONS",
          "target": "concept_anatta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_35",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_5",
          "type": "MENTIONS",
          "target": "concept_metta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_50",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_middle_way",
          "type": "MENTIONS",
          "target": "concept_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_pratityasamutpada",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_sunyata",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_ayatana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_dhatu",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_mantra",
          "type": "MENTIONS",
          "target": "concept_mantra",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_mantra",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_form",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_middle_way",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_two_truths",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_25_19",
          "type": "MENTIONS",
          "target": "concept_nirvana",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_25_19",
          "type": "MENTIONS",
          "target": "concept_samsara",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_dukkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_nirvana",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_prajna",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_samadhi",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_anatta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_anicca",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_appamada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_ayatana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_dhatu",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_two_truths",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_avalokitesvara",
          "type": "RELATED_TO",
          "target": "concept_karuna",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "RELATED_TO",
          "target": "concept_bodhicitta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "RELATED_TO",
          "target": "concept_paramita",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_form",
          "type": "RELATED_TO",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "RELATED_TO",
          "target": "place_sarnath",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_klesha",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_klesha",
          "type": "RELATED_TO",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_luc_can_luc_tran_luc_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_middle_way",
          "type": "RELATED_TO",
          "target": "concept_two_truths",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_nirvana",
          "type": "RELATED_TO",
          "target": "place_bodh_gaya",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "RELATED_TO",
          "target": "concept_paramita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "RELATED_TO",
          "target": "concept_prajna",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_karma",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_karma",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_nirvana",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_can",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_tran",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "RELATED_TO",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "RELATED_TO",
          "target": "concept_two_truths",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "school_mahayana",
          "type": "RELATED_TO",
          "target": "place_gandhara",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_pali_canon",
          "type": "RELATED_TO",
          "target": "school_theravada",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatta_pali",
          "type": "RELATED_TO",
          "target": "term_anatman_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anicca_pali",
          "type": "RELATED_TO",
          "target": "term_anitya_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ariya_atthangika_magga_pali",
          "type": "RELATED_TO",
          "target": "term_arya_astangika_marga_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avihimsa_pali",
          "type": "RELATED_TO",
          "target": "term_ahimsa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avijja_pali",
          "type": "RELATED_TO",
          "target": "term_avidya_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_cattari_ariyasaccani_pali",
          "type": "RELATED_TO",
          "target": "term_catvari_aryasatyani_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dukkha_pali",
          "type": "RELATED_TO",
          "target": "term_duhkha_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kamma_pali",
          "type": "RELATED_TO",
          "target": "term_karma_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kilesa_pali",
          "type": "RELATED_TO",
          "target": "term_klesa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_majjhima_patipada_pali",
          "type": "RELATED_TO",
          "target": "term_madhyama_pratipad_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nibbana_pali",
          "type": "RELATED_TO",
          "target": "term_nirvana_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_panna_pali",
          "type": "RELATED_TO",
          "target": "term_prajna_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paticcasamuppada_pali",
          "type": "RELATED_TO",
          "target": "term_pratityasamutpada_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tanha_pali",
          "type": "RELATED_TO",
          "target": "term_trsna_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tilakkhana_pali",
          "type": "RELATED_TO",
          "target": "term_trilaksana_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upekkha_pali",
          "type": "RELATED_TO",
          "target": "term_upeksa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        }
      ]
    },
    "all_data": {
      "metadata": {
        "title": "Dharma Knowledge Graph: All Data",
        "version": "0.1",
        "mode": "all_data",
        "content_hash": "a71739ba126b977a3507406f899d3d2696e43a8d63467094990ad23fba75f31b",
        "source_files": [
          "data/seeds/concepts.json",
          "data/seeds/core.json",
          "data/seeds/dhammapada.json",
          "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "data/seeds/giac_khang_pilot.json",
          "data/seeds/giac_khang_real_evidence_sample.json",
          "data/seeds/heart_sutra.json",
          "data/seeds/places_traditions.json",
          "data/seeds/terms.json",
          "data/seeds/terms_extended.json",
          "data/seeds/terms_remaining.json",
          "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json"
        ]
      },
      "summary": {
        "node_count": 153,
        "relationship_count": 238,
        "node_type_counts": {
          "Citation": 21,
          "Concept": 42,
          "Corpus": 2,
          "Document": 2,
          "Evidence": 9,
          "Person": 1,
          "Place": 6,
          "School": 5,
          "Source": 2,
          "Term": 59,
          "Text": 3,
          "Work": 1
        },
        "relationship_type_counts": {
          "AUTHORED_BY": 1,
          "BELONGS_TO_CORPUS": 8,
          "BELONGS_TO_SCHOOL": 13,
          "CITES": 17,
          "DEFINES": 60,
          "DENOTES": 6,
          "DERIVED_FROM": 12,
          "EVIDENCES": 3,
          "HAS_CITATION": 8,
          "HAS_DOCUMENT": 3,
          "HAS_EVIDENCE": 3,
          "LOCATED_IN": 4,
          "MENTIONS": 59,
          "RELATED_TO": 41
        },
        "source_badge_counts": {
          "corpus": 2,
          "reviewed": 5,
          "seed": 146
        }
      },
      "nodes": [
        {
          "id": "citation_dhammapada_1",
          "type": "Citation",
          "name": "Dhammapada 1",
          "source": "Dhammapada",
          "locator": "Verse 1",
          "notes": "Pilot citation for the relation between mind, intention, and suffering.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_129",
          "type": "Citation",
          "name": "Dhammapada 129",
          "source": "Dhammapada",
          "locator": "Verse 129",
          "notes": "Pilot citation for non-harming and empathy toward beings.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_183",
          "type": "Citation",
          "name": "Dhammapada 183",
          "source": "Dhammapada",
          "locator": "Verse 183",
          "notes": "Pilot citation for ethical restraint, wholesome cultivation, and mental purification.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_2",
          "type": "Citation",
          "name": "Dhammapada 2",
          "source": "Dhammapada",
          "locator": "Verse 2",
          "notes": "Pilot citation for the relation between mind, intention, and well-being.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_21",
          "type": "Citation",
          "name": "Dhammapada 21",
          "source": "Dhammapada",
          "locator": "Verse 21",
          "notes": "Pilot citation for heedfulness as a path quality.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_277",
          "type": "Citation",
          "name": "Dhammapada 277",
          "source": "Dhammapada",
          "locator": "Verse 277",
          "notes": "Pilot citation for impermanence.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_279",
          "type": "Citation",
          "name": "Dhammapada 279",
          "source": "Dhammapada",
          "locator": "Verse 279",
          "notes": "Pilot citation for not-self.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_35",
          "type": "Citation",
          "name": "Dhammapada 35",
          "source": "Dhammapada",
          "locator": "Verse 35",
          "notes": "Pilot citation for the training and restraint of mind.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_5",
          "type": "Citation",
          "name": "Dhammapada 5",
          "source": "Dhammapada",
          "locator": "Verse 5",
          "notes": "Pilot citation for non-hatred and reconciliation.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_dhammapada_50",
          "type": "Citation",
          "name": "Dhammapada 50",
          "source": "Dhammapada",
          "locator": "Verse 50",
          "notes": "Pilot citation for self-examination in ethical practice.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_pratityasamutpada",
          "type": "Citation",
          "name": "Giac Khang notes, Dependent arising excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#dependent-arising",
          "notes": "Pilot citation for evidence about dependent arising.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_middle_way",
          "type": "Citation",
          "name": "Giac Khang notes, Middle Way excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#middle-way",
          "notes": "Pilot citation for evidence about the middle way.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_giac_khang_notes_sunyata",
          "type": "Citation",
          "name": "Giac Khang notes, Sunyata excerpt",
          "source": "Giac Khang MVP Notes",
          "locator": "pilot-note-001#sunyata",
          "notes": "Pilot citation for evidence about emptiness.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_dharmas",
          "type": "Citation",
          "name": "Heart Sutra Dharmas Passage",
          "source": "Heart Sutra",
          "locator": "Dharmas and categories passage",
          "notes": "Pilot citation for sense bases, elements, dependent arising categories, and the four truths.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_mantra",
          "type": "Citation",
          "name": "Heart Sutra Mantra Passage",
          "source": "Heart Sutra",
          "locator": "Mantra passage",
          "notes": "Pilot citation for mantra and prajnaparamita as a practice expression.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_opening",
          "type": "Citation",
          "name": "Heart Sutra Opening",
          "source": "Heart Sutra",
          "locator": "Opening scene",
          "notes": "Pilot citation for Avalokitesvara, prajnaparamita, and the five aggregates.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_heart_sutra_skandhas",
          "type": "Citation",
          "name": "Heart Sutra Skandhas Passage",
          "source": "Heart Sutra",
          "locator": "Five aggregates passage",
          "notes": "Pilot citation for the relationship between form, the aggregates, and emptiness.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_24_18",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 24.18",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 24, verse 18",
          "notes": "Pilot citation for dependent designation, emptiness, and the middle way.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_24_19",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 24.19",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 24, verse 19",
          "notes": "Pilot citation for the relation between dependent arising and emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_mmkv_25_19",
          "type": "Citation",
          "name": "Mulamadhyamakakarika 25.19",
          "source": "Mulamadhyamakakarika",
          "locator": "Chapter 25, verse 19",
          "notes": "Pilot citation for the relation between samsara and nirvana in Madhyamaka analysis.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "citation_youtube_fisp_arohzy8",
          "type": "Citation",
          "name": "YouTube citation for FISpARohzy8",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "locator": "video root",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_ahimsa",
          "type": "Concept",
          "name": "Ahimsa",
          "pali": "avihimsa",
          "sanskrit": "ahimsa",
          "category": "ethics",
          "description": "Non-harming; an ethical orientation of restraint from violence and injury.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_anatta",
          "type": "Concept",
          "name": "Anatta",
          "pali": "anatta",
          "sanskrit": "anatman",
          "category": "doctrine",
          "description": "Not-self; the absence of a permanent, independent self in conditioned phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_anicca",
          "type": "Concept",
          "name": "Anicca",
          "pali": "anicca",
          "sanskrit": "anitya",
          "category": "doctrine",
          "description": "Impermanence; the conditioned nature of phenomena as changing and unstable.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_appamada",
          "type": "Concept",
          "name": "Appamada",
          "pali": "appamada",
          "sanskrit": "apramada",
          "category": "practice",
          "description": "Heedfulness or diligent care in practice.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_avalokitesvara",
          "type": "Concept",
          "name": "Avalokitesvara",
          "sanskrit": "avalokitesvara",
          "category": "mahayana",
          "description": "A bodhisattva associated with compassion and prominent in the Heart Sutra setting.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_avidya",
          "type": "Concept",
          "name": "Avidya",
          "pali": "avijja",
          "sanskrit": "avidya",
          "category": "psychology",
          "description": "Ignorance or misknowing, especially regarding the nature of reality and the path.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_bodhicitta",
          "type": "Concept",
          "name": "Bodhicitta",
          "sanskrit": "bodhicitta",
          "category": "mahayana",
          "description": "The awakened mind or aspiration to attain awakening for the benefit of all beings.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_bodhisattva",
          "type": "Concept",
          "name": "Bodhisattva",
          "pali": "bodhisatta",
          "sanskrit": "bodhisattva",
          "category": "mahayana",
          "description": "A being oriented toward awakening, especially for the liberation of all beings in Mahayana contexts.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_brahmaviharas",
          "type": "Concept",
          "name": "Brahmaviharas",
          "pali": "brahmavihara",
          "sanskrit": "brahmavihara",
          "category": "practice",
          "description": "The four divine abodes: loving-kindness, compassion, sympathetic joy, and equanimity.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_citta",
          "type": "Concept",
          "name": "Citta",
          "pali": "citta",
          "sanskrit": "citta",
          "category": "psychology",
          "description": "Mind, heart, or mental orientation; a key term for understanding intention and experience.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_dukkha",
          "type": "Concept",
          "name": "Dukkha",
          "pali": "dukkha",
          "sanskrit": "duhkha",
          "description": "A central Dharma concept often translated as suffering, unsatisfactoriness, or stress.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_dhatu",
          "type": "Concept",
          "name": "Elements",
          "pali": "dhatu",
          "sanskrit": "dhatu",
          "category": "analysis",
          "description": "Elements or domains used to analyze experience and phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_skandhas",
          "type": "Concept",
          "name": "Five Aggregates",
          "pali": "khandha",
          "sanskrit": "skandha",
          "category": "analysis",
          "description": "Form, feeling, perception, formations, and consciousness as a framework for analyzing experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_form",
          "type": "Concept",
          "name": "Form",
          "pali": "rupa",
          "sanskrit": "rupa",
          "category": "analysis",
          "description": "Material form; one of the five aggregates.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_four_noble_truths",
          "type": "Concept",
          "name": "Four Noble Truths",
          "pali": "cattari ariyasaccani",
          "sanskrit": "catvari aryasatyani",
          "category": "doctrine",
          "description": "The teaching of suffering, its origin, its cessation, and the path leading to cessation.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_karma",
          "type": "Concept",
          "name": "Karma",
          "pali": "kamma",
          "sanskrit": "karma",
          "category": "ethics",
          "description": "Intentional action and its ethical consequences.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_karuna",
          "type": "Concept",
          "name": "Karuna",
          "pali": "karuna",
          "sanskrit": "karuna",
          "category": "practice",
          "description": "Compassion; the wish for beings to be free from suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_kinh_sau_sau",
          "type": "Concept",
          "name": "Kinh Sáu Sáu",
          "language": "vi",
          "category": "text_topic",
          "description": "Pilot topic concept for Giác Khang teachings on Kinh Sáu Sáu.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_klesha",
          "type": "Concept",
          "name": "Klesha",
          "pali": "kilesa",
          "sanskrit": "klesa",
          "category": "psychology",
          "description": "Afflictive mental states that disturb the mind and condition suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_luc_can_luc_tran_luc_thuc",
          "type": "Concept",
          "name": "Lục căn, lục trần, lục thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Grouping concept for six faculties, six objects, and six consciousnesses.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_mantra",
          "type": "Concept",
          "name": "Mantra",
          "sanskrit": "mantra",
          "category": "practice",
          "description": "A sacred utterance or formula used in contemplative and ritual contexts.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_metta",
          "type": "Concept",
          "name": "Metta",
          "pali": "metta",
          "sanskrit": "maitri",
          "category": "practice",
          "description": "Loving-kindness; the cultivation of goodwill and friendliness.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_middle_way",
          "type": "Concept",
          "name": "Middle Way",
          "pali": "majjhima patipada",
          "sanskrit": "madhyama pratipad",
          "category": "practice",
          "description": "A path avoiding extremes, often framed as avoiding indulgence and self-mortification or eternalism and nihilism.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_mudita",
          "type": "Concept",
          "name": "Mudita",
          "pali": "mudita",
          "sanskrit": "mudita",
          "category": "practice",
          "description": "Sympathetic joy; delight in the welfare and happiness of others.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_nirvana",
          "type": "Concept",
          "name": "Nirvana",
          "pali": "nibbana",
          "sanskrit": "nirvana",
          "category": "liberation",
          "description": "Liberation; the extinguishing of greed, hatred, and delusion.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_noble_eightfold_path",
          "type": "Concept",
          "name": "Noble Eightfold Path",
          "pali": "ariya atthangika magga",
          "sanskrit": "arya astangika marga",
          "category": "practice",
          "description": "The path of right view, intention, speech, action, livelihood, effort, mindfulness, and concentration.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_paramita",
          "type": "Concept",
          "name": "Paramita",
          "pali": "parami",
          "sanskrit": "paramita",
          "category": "mahayana",
          "description": "Perfection or transcendent virtue cultivated on the bodhisattva path.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_prajna",
          "type": "Concept",
          "name": "Prajna",
          "pali": "panna",
          "sanskrit": "prajna",
          "category": "wisdom",
          "description": "Wisdom or liberating insight into the nature of phenomena.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_prajnaparamita",
          "type": "Concept",
          "name": "Prajnaparamita",
          "sanskrit": "prajnaparamita",
          "category": "mahayana",
          "description": "The perfection of wisdom; a central theme in Mahayana sutra literature.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_pratityasamutpada",
          "type": "Concept",
          "name": "Pratityasamutpada",
          "pali": "paticcasamuppada",
          "sanskrit": "pratityasamutpada",
          "category": "doctrine",
          "description": "Dependent arising; the principle that phenomena arise in dependence on causes and conditions.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_samadhi",
          "type": "Concept",
          "name": "Samadhi",
          "pali": "samadhi",
          "sanskrit": "samadhi",
          "category": "practice",
          "description": "Collectedness, concentration, or meditative absorption.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_samsara",
          "type": "Concept",
          "name": "Samsara",
          "pali": "samsara",
          "sanskrit": "samsara",
          "category": "cosmology",
          "description": "The cycle of birth, death, and rebirth conditioned by ignorance and craving.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sila",
          "type": "Concept",
          "name": "Sila",
          "pali": "sila",
          "sanskrit": "sila",
          "category": "ethics",
          "description": "Ethical conduct or moral discipline.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_ayatana",
          "type": "Concept",
          "name": "Six Sense Bases",
          "pali": "ayatana",
          "sanskrit": "ayatana",
          "category": "analysis",
          "description": "The internal and external sense bases involved in perceptual experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sunyata",
          "type": "Concept",
          "name": "Sunyata",
          "sanskrit": "sunyata",
          "description": "A Mahayana concept commonly translated as emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_can",
          "type": "Concept",
          "name": "Sáu căn",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense faculties in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_thuc",
          "type": "Concept",
          "name": "Sáu thức",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six consciousnesses in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_sau_tran",
          "type": "Concept",
          "name": "Sáu trần",
          "language": "vi",
          "category": "doctrine",
          "description": "Vietnamese concept placeholder for the six sense objects in the Kinh Sáu Sáu pilot.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_tanha",
          "type": "Concept",
          "name": "Tanha",
          "pali": "tanha",
          "sanskrit": "trsna",
          "category": "psychology",
          "description": "Craving or thirst; a central condition in the arising of suffering.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_three_marks",
          "type": "Concept",
          "name": "Three Marks of Existence",
          "pali": "tilakkhana",
          "sanskrit": "trilaksana",
          "category": "doctrine",
          "description": "The marks of impermanence, suffering or unsatisfactoriness, and not-self.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_two_truths",
          "type": "Concept",
          "name": "Two Truths",
          "sanskrit": "satya-dvaya",
          "category": "mahayana",
          "description": "The distinction between conventional truth and ultimate truth.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "concept_upekkha",
          "type": "Concept",
          "name": "Upekkha",
          "pali": "upekkha",
          "sanskrit": "upeksa",
          "category": "practice",
          "description": "Equanimity; balanced presence toward changing experience.",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "id": "corpus_giac_khang_pilot",
          "type": "Corpus",
          "name": "Giac Khang Pilot Corpus",
          "language": "Vietnamese",
          "scope": "21-day MVP evidence-first pilot",
          "description": "A bounded pilot corpus for testing evidence-first Dharma Knowledge Graph ingestion.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "corpus"
        },
        {
          "id": "corpus_giac_khang",
          "type": "Corpus",
          "name": "Giác Khang Corpus",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "corpus"
        },
        {
          "id": "document_giac_khang_mvp_notes",
          "type": "Document",
          "name": "Giac Khang MVP Notes",
          "document_type": "study_note",
          "language": "Vietnamese",
          "locator": "pilot-note-001",
          "description": "A single pilot document used to test document-to-evidence modeling.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "document_transcript_fisp_arohzy8",
          "type": "Document",
          "name": "Transcript placeholder for 1A. KINH 6 6 L2CÂU 1 P1",
          "document_kind": "transcript",
          "language": "vi",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "source_kind": "youtube",
          "review_status": "unreviewed",
          "notes": "Transcript not yet imported. Evidence must not be created without real excerpt text and timestamp.",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_pratityasamutpada_001",
          "type": "Evidence",
          "name": "Evidence: Dependent arising as relational explanation",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#dependent-arising",
          "evidence_text": "Dependent arising is represented as the principle that phenomena appear through conditions and relationships.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_middle_way_001",
          "type": "Evidence",
          "name": "Evidence: Middle Way avoids extremes",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#middle-way",
          "evidence_text": "The middle way is represented as avoiding fixed extremes while preserving practical conventional meaning.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_sunyata_001",
          "type": "Evidence",
          "name": "Evidence: Sunyata as non-independent existence",
          "evidence_type": "human_note",
          "language": "Vietnamese",
          "confidence": "medium",
          "review_status": "human_reviewed",
          "source_kind": "local_notes",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "pilot-note-001#sunyata",
          "evidence_text": "Emptiness is represented as the absence of independent, self-existing nature rather than simple nothingness.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_giac_khang_real_sample_001",
          "type": "Evidence",
          "name": "Unreviewed Giac Khang transcript evidence sample",
          "evidence_text": "Placeholder transcript excerpt for DKG-002 schema validation. This text is not reviewed and must be replaced with a real transcript excerpt before use.",
          "evidence_type": "transcript_excerpt",
          "language": "Vietnamese",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=placeholder_unreviewed",
          "document_id": "document_giac_khang_mvp_notes",
          "locator": "youtube-placeholder#t=00:00:00",
          "start_time": "00:00:00",
          "end_time": "00:00:30",
          "speaker": "Giac Khang",
          "review_status": "unreviewed",
          "notes": "Unreviewed placeholder node for DKG-002. Do not treat as verified teaching evidence.",
          "source_file": "data/seeds/giac_khang_real_evidence_sample.json",
          "source_badge": "seed"
        },
        {
          "id": "evidence_fisp_arohzy8_0001",
          "type": "Evidence",
          "name": "VTT caption excerpt 0001 from FISpARohzy8",
          "evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:18.720",
          "end_time": "00:01:39.030",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "reviewed_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0002",
          "type": "Evidence",
          "name": "VTT caption excerpt 0002 from FISpARohzy8",
          "evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:39.040",
          "end_time": "00:01:53.190",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "reviewed_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0003",
          "type": "Evidence",
          "name": "VTT caption excerpt 0003 from FISpARohzy8",
          "evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:01:53.200",
          "end_time": "00:02:16.110",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "reviewed_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0004",
          "type": "Evidence",
          "name": "VTT caption excerpt 0004 from FISpARohzy8",
          "evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:02:16.120",
          "end_time": "00:02:37.949",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "reviewed_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "evidence_fisp_arohzy8_0005",
          "type": "Evidence",
          "name": "VTT caption excerpt 0005 from FISpARohzy8",
          "evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "evidence_type": "transcript_excerpt",
          "language": "vi",
          "confidence": "low",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "document_id": "document_transcript_fisp_arohzy8",
          "start_time": "00:02:37.959",
          "end_time": "00:02:54.470",
          "speaker": "HT. Thích Giác Khang",
          "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
          "original_review_status": "unreviewed",
          "original_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "reviewed_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
          "reviewer": "",
          "reviewed_at": "",
          "review_notes": "",
          "review_status": "human_reviewed",
          "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
          "source_badge": "reviewed"
        },
        {
          "id": "person_nagarjuna",
          "type": "Person",
          "name": "Nagarjuna",
          "tradition": "Mahayana",
          "description": "A major Buddhist philosopher associated with Madhyamaka.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "place_bodh_gaya",
          "type": "Place",
          "name": "Bodh Gaya",
          "country": "India",
          "region": "Bihar",
          "description": "A major Buddhist pilgrimage place associated with the Buddha's awakening.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_gandhara",
          "type": "Place",
          "name": "Gandhara",
          "country": "Historical region",
          "region": "Northwest South Asia",
          "description": "A historical Buddhist region important for textual and artistic transmission.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_magadha",
          "type": "Place",
          "name": "Magadha",
          "country": "India",
          "region": "Eastern India",
          "description": "An ancient region important in early Buddhist history.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_nalanda",
          "type": "Place",
          "name": "Nalanda",
          "country": "India",
          "region": "Bihar",
          "description": "A historic center of Buddhist monastic learning.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_sarnath",
          "type": "Place",
          "name": "Sarnath",
          "country": "India",
          "region": "Uttar Pradesh",
          "description": "A major Buddhist pilgrimage place associated with the first teaching.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "place_sri_lanka",
          "type": "Place",
          "name": "Sri Lanka",
          "country": "Sri Lanka",
          "region": "South Asia",
          "description": "A major historical center for Theravada Buddhist transmission.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_early_buddhism",
          "type": "School",
          "name": "Early Buddhism",
          "description": "A working category for early Buddhist teachings and textual layers.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_madhyamaka",
          "type": "School",
          "name": "Madhyamaka",
          "description": "A Mahayana philosophical school associated with analysis of emptiness.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "school_mahayana",
          "type": "School",
          "name": "Mahayana",
          "description": "A broad family of Buddhist traditions emphasizing the bodhisattva path.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_pali_canon",
          "type": "School",
          "name": "Pali Canon",
          "description": "A textual tradition preserving canonical materials in Pali.",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "id": "school_theravada",
          "type": "School",
          "name": "Theravada",
          "description": "A Buddhist tradition preserving the Pali Canon.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "source_giac_khang_notes",
          "type": "Source",
          "name": "Giac Khang Study Notes",
          "source_type": "local_notes",
          "language": "Vietnamese",
          "description": "Pilot source material used to model evidence before API, embeddings, or LLM extraction.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "id": "source_youtube_fisp_arohzy8",
          "type": "Source",
          "name": "YouTube video FISpARohzy8",
          "source_kind": "youtube",
          "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
          "channel": "PHÁP ÂM SƯ KHANG",
          "title": "1A. KINH 6 6 L2CÂU 1 P1",
          "speaker": "HT. Thích Giác Khang",
          "topic": "Kinh Sáu Sáu",
          "review_status": "unreviewed",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ahimsa_sanskrit",
          "type": "Term",
          "name": "ahimsa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "ahimsa",
          "translation": "non-harming",
          "notes": "Sanskrit term for non-harming.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anatman_sanskrit",
          "type": "Term",
          "name": "anatman",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "anatman",
          "translation": "not-self; no self",
          "notes": "Sanskrit form corresponding to Pali anatta.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anatta_pali",
          "type": "Term",
          "name": "anatta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "anatta",
          "translation": "not-self",
          "notes": "Pali form used for the doctrine of not-self.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anicca_pali",
          "type": "Term",
          "name": "anicca",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "anicca",
          "translation": "impermanent",
          "notes": "Pali form used for impermanence.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_anitya_sanskrit",
          "type": "Term",
          "name": "anitya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "anitya",
          "translation": "impermanent",
          "notes": "Sanskrit form used for impermanence.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_appamada_pali",
          "type": "Term",
          "name": "appamada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "appamada",
          "translation": "heedfulness; diligence",
          "notes": "A central practice quality highlighted in the Dhammapada.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ariya_atthangika_magga_pali",
          "type": "Term",
          "name": "ariya atthangika magga",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "ariya atthangika magga",
          "translation": "noble eightfold path",
          "notes": "Pali phrase for the Noble Eightfold Path.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_arya_astangika_marga_sanskrit",
          "type": "Term",
          "name": "arya astangika marga",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "arya astangika marga",
          "translation": "noble eightfold path",
          "notes": "Sanskrit phrase for the Noble Eightfold Path.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avalokitesvara_sanskrit",
          "type": "Term",
          "name": "avalokitesvara",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "avalokitesvara",
          "translation": "Avalokitesvara",
          "notes": "Sanskrit name of the bodhisattva associated with compassion.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avidya_sanskrit",
          "type": "Term",
          "name": "avidya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "avidya",
          "translation": "ignorance",
          "notes": "Sanskrit term for ignorance or misknowing.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avihimsa_pali",
          "type": "Term",
          "name": "avihimsa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "avihimsa",
          "translation": "non-harming",
          "notes": "Pali term related to non-harming.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_avijja_pali",
          "type": "Term",
          "name": "avijja",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "avijja",
          "translation": "ignorance",
          "notes": "Pali term for ignorance or misknowing.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_ayatana_pali",
          "type": "Term",
          "name": "ayatana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "ayatana",
          "translation": "sense base",
          "notes": "Pali and Sanskrit term for sense base.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_bodhicitta_sanskrit",
          "type": "Term",
          "name": "bodhicitta",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "bodhicitta",
          "translation": "awakening mind",
          "notes": "Sanskrit term for the awakened mind or aspiration toward awakening.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_bodhisattva_sanskrit",
          "type": "Term",
          "name": "bodhisattva",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "bodhisattva",
          "translation": "awakening being",
          "notes": "Sanskrit term for a being oriented toward awakening.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_brahmavihara_pali",
          "type": "Term",
          "name": "brahmavihara",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "brahmavihara",
          "translation": "divine abode",
          "notes": "Pali term for the divine abodes.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_cattari_ariyasaccani_pali",
          "type": "Term",
          "name": "cattari ariyasaccani",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "cattari ariyasaccani",
          "translation": "four noble truths",
          "notes": "Pali phrase for the Four Noble Truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_catvari_aryasatyani_sanskrit",
          "type": "Term",
          "name": "catvari aryasatyani",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "catvari aryasatyani",
          "translation": "four noble truths",
          "notes": "Sanskrit phrase for the Four Noble Truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_citta_pali",
          "type": "Term",
          "name": "citta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "citta",
          "translation": "mind; heart",
          "notes": "A term for mind, heart, or mental orientation.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_dhatu_pali",
          "type": "Term",
          "name": "dhatu",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "dhatu",
          "translation": "element; domain",
          "notes": "Pali and Sanskrit term for element or domain.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_duhkha_sanskrit",
          "type": "Term",
          "name": "duhkha",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "duhkha",
          "translation": "suffering; unsatisfactoriness",
          "notes": "Sanskrit cognate of Pali dukkha.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_dukkha_pali",
          "type": "Term",
          "name": "dukkha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "dukkha",
          "translation": "suffering; unsatisfactoriness; stress",
          "notes": "A core Pali term in the analysis of conditioned experience.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_kamma_pali",
          "type": "Term",
          "name": "kamma",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "kamma",
          "translation": "intentional action",
          "notes": "Pali form corresponding to Sanskrit karma.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_karma_sanskrit",
          "type": "Term",
          "name": "karma",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "karma",
          "translation": "intentional action",
          "notes": "Sanskrit form for intentional action and its consequences.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_karuna_pali",
          "type": "Term",
          "name": "karuna",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "karuna",
          "translation": "compassion",
          "notes": "Pali and Sanskrit term for compassion.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_kilesa_pali",
          "type": "Term",
          "name": "kilesa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "kilesa",
          "translation": "affliction; defilement",
          "notes": "Pali term for afflictive mental states.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_klesa_sanskrit",
          "type": "Term",
          "name": "klesa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "klesa",
          "translation": "affliction",
          "notes": "Sanskrit term for afflictive mental states.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_can_hv",
          "type": "Term",
          "name": "lục căn",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_thuc_hv",
          "type": "Term",
          "name": "lục thức",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_luc_tran_hv",
          "type": "Term",
          "name": "lục trần",
          "language": "vi",
          "script": "Hán-Việt",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_madhyama_pratipad_sanskrit",
          "type": "Term",
          "name": "madhyama pratipad",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "madhyama pratipad",
          "translation": "middle way",
          "notes": "Sanskrit phrase for the middle way.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_majjhima_patipada_pali",
          "type": "Term",
          "name": "majjhima patipada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "majjhima patipada",
          "translation": "middle way",
          "notes": "Pali phrase for the middle way.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_mantra_sanskrit",
          "type": "Term",
          "name": "mantra",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "mantra",
          "translation": "sacred utterance",
          "notes": "Sanskrit term for a sacred utterance or formula.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_metta_pali",
          "type": "Term",
          "name": "metta",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "metta",
          "translation": "loving-kindness",
          "notes": "Pali term for loving-kindness.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_mudita_pali",
          "type": "Term",
          "name": "mudita",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "mudita",
          "translation": "sympathetic joy",
          "notes": "Pali and Sanskrit term for sympathetic joy.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_nibbana_pali",
          "type": "Term",
          "name": "nibbana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "nibbana",
          "translation": "liberation; extinguishing",
          "notes": "Pali term commonly rendered as nirvana.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_nirvana_sanskrit",
          "type": "Term",
          "name": "nirvana",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "nirvana",
          "translation": "liberation; extinguishing",
          "notes": "Sanskrit form corresponding to Pali nibbana.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_panna_pali",
          "type": "Term",
          "name": "panna",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "panna",
          "translation": "wisdom",
          "notes": "Pali term corresponding to Sanskrit prajna.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_paramita_sanskrit",
          "type": "Term",
          "name": "paramita",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "paramita",
          "translation": "perfection",
          "notes": "Sanskrit term for perfection or transcendent virtue.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_paticcasamuppada_pali",
          "type": "Term",
          "name": "paticcasamuppada",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "paticcasamuppada",
          "translation": "dependent arising",
          "notes": "Pali term for dependent arising.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_prajna_sanskrit",
          "type": "Term",
          "name": "prajna",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "prajna",
          "translation": "wisdom",
          "notes": "Sanskrit term for wisdom or liberating insight.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_prajnaparamita_sanskrit",
          "type": "Term",
          "name": "prajnaparamita",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "prajnaparamita",
          "translation": "perfection of wisdom",
          "notes": "Sanskrit term for the perfection of wisdom.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_pratityasamutpada_sanskrit",
          "type": "Term",
          "name": "pratityasamutpada",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "pratityasamutpada",
          "translation": "dependent arising",
          "notes": "Sanskrit term for dependent arising.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_rupa_pali",
          "type": "Term",
          "name": "rupa",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "rupa",
          "translation": "form; material form",
          "notes": "Pali and Sanskrit term for form.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_samadhi_pali",
          "type": "Term",
          "name": "samadhi",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "samadhi",
          "translation": "concentration; collectedness",
          "notes": "Pali and Sanskrit term for meditative collectedness.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_samsara_pali",
          "type": "Term",
          "name": "samsara",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "samsara",
          "translation": "cycle of rebirth",
          "notes": "Pali form for the cycle of conditioned existence.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_satya_dvaya_sanskrit",
          "type": "Term",
          "name": "satya-dvaya",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "satya-dvaya",
          "translation": "two truths",
          "notes": "Sanskrit phrase for the two truths.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sila_pali",
          "type": "Term",
          "name": "sila",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "sila",
          "translation": "ethical conduct",
          "notes": "Pali term for moral discipline or ethical conduct.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_skandha_sanskrit",
          "type": "Term",
          "name": "skandha",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "skandha",
          "translation": "aggregate",
          "notes": "Sanskrit term for aggregate.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sunyata_sanskrit",
          "type": "Term",
          "name": "sunyata",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "sunyata",
          "translation": "emptiness",
          "notes": "A key Mahayana term, especially important in Madhyamaka contexts.",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_can_vi",
          "type": "Term",
          "name": "sáu căn",
          "language": "vi",
          "translation": "six sense faculties",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_thuc_vi",
          "type": "Term",
          "name": "sáu thức",
          "language": "vi",
          "translation": "six consciousnesses",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_sau_tran_vi",
          "type": "Term",
          "name": "sáu trần",
          "language": "vi",
          "translation": "six sense objects",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "id": "term_tanha_pali",
          "type": "Term",
          "name": "tanha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "tanha",
          "translation": "craving; thirst",
          "notes": "Pali term for craving.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_tilakkhana_pali",
          "type": "Term",
          "name": "tilakkhana",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "tilakkhana",
          "translation": "three marks",
          "notes": "Pali term for the three marks of existence.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_trilaksana_sanskrit",
          "type": "Term",
          "name": "trilaksana",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "trilaksana",
          "translation": "three marks",
          "notes": "Sanskrit term for the three marks of existence.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_trsna_sanskrit",
          "type": "Term",
          "name": "trsna",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "trsna",
          "translation": "craving; thirst",
          "notes": "Sanskrit term corresponding to Pali tanha.",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "id": "term_upekkha_pali",
          "type": "Term",
          "name": "upekkha",
          "language": "Pali",
          "script": "Latin",
          "transliteration": "upekkha",
          "translation": "equanimity",
          "notes": "Pali term for equanimity.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "term_upeksa_sanskrit",
          "type": "Term",
          "name": "upeksa",
          "language": "Sanskrit",
          "script": "Latin",
          "transliteration": "upeksa",
          "translation": "equanimity",
          "notes": "Sanskrit term corresponding to Pali upekkha.",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "id": "text_dhammapada",
          "type": "Text",
          "name": "Dhammapada",
          "language": "Pali",
          "tradition": "Theravada",
          "description": "A collection of verses from the Pali Canon, traditionally arranged into 26 chapters.",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "id": "text_heart_sutra",
          "type": "Text",
          "name": "Heart Sutra",
          "alternate_names": [
            "Prajnaparamita Hrdaya",
            "Heart of the Perfection of Wisdom"
          ],
          "language": "Sanskrit",
          "tradition": "Mahayana",
          "description": "A short Mahayana sutra associated with the perfection of wisdom literature and the teaching of emptiness.",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "id": "text_mulamadhyamakakarika",
          "type": "Text",
          "name": "Mulamadhyamakakarika",
          "language": "Sanskrit",
          "tradition": "Mahayana",
          "description": "A foundational Madhyamaka text attributed to Nagarjuna.",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "id": "work_giac_khang_pilot_teachings",
          "type": "Work",
          "name": "Giac Khang Pilot Teachings",
          "language": "Vietnamese",
          "description": "A pilot work grouping selected notes for the evidence-first MVP.",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        }
      ],
      "relationships": [
        {
          "source": "text_mulamadhyamakakarika",
          "type": "AUTHORED_BY",
          "target": "person_nagarjuna",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_middle_way",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_pratityasamutpada",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_sunyata",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "source_giac_khang_notes",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "BELONGS_TO_CORPUS",
          "target": "corpus_giac_khang_pilot",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_avalokitesvara",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhicitta",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "person_nagarjuna",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_madhyamaka",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "person_nagarjuna",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_madhyamaka",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_early_buddhism",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_pali_canon",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_theravada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_mahayana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "BELONGS_TO_SCHOOL",
          "target": "school_madhyamaka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_1",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_129",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_183",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_2",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_21",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_277",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_279",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_35",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_5",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "CITES",
          "target": "citation_dhammapada_50",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_dharmas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_mantra",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_opening",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "CITES",
          "target": "citation_heart_sutra_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_24_18",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_24_19",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "CITES",
          "target": "citation_mmkv_25_19",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_karuna",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_metta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_mudita",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_brahmaviharas",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_three_marks",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ahimsa_sanskrit",
          "type": "DEFINES",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatman_sanskrit",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatta_pali",
          "type": "DEFINES",
          "target": "concept_anatta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anicca_pali",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anitya_sanskrit",
          "type": "DEFINES",
          "target": "concept_anicca",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_appamada_pali",
          "type": "DEFINES",
          "target": "concept_appamada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ariya_atthangika_magga_pali",
          "type": "DEFINES",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_arya_astangika_marga_sanskrit",
          "type": "DEFINES",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avalokitesvara_sanskrit",
          "type": "DEFINES",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avidya_sanskrit",
          "type": "DEFINES",
          "target": "concept_avidya",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avihimsa_pali",
          "type": "DEFINES",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avijja_pali",
          "type": "DEFINES",
          "target": "concept_avidya",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ayatana_pali",
          "type": "DEFINES",
          "target": "concept_ayatana",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_bodhicitta_sanskrit",
          "type": "DEFINES",
          "target": "concept_bodhicitta",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_bodhisattva_sanskrit",
          "type": "DEFINES",
          "target": "concept_bodhisattva",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_brahmavihara_pali",
          "type": "DEFINES",
          "target": "concept_brahmaviharas",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_cattari_ariyasaccani_pali",
          "type": "DEFINES",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_catvari_aryasatyani_sanskrit",
          "type": "DEFINES",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_citta_pali",
          "type": "DEFINES",
          "target": "concept_citta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dhatu_pali",
          "type": "DEFINES",
          "target": "concept_dhatu",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_duhkha_sanskrit",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dukkha_pali",
          "type": "DEFINES",
          "target": "concept_dukkha",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kamma_pali",
          "type": "DEFINES",
          "target": "concept_karma",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_karma_sanskrit",
          "type": "DEFINES",
          "target": "concept_karma",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_karuna_pali",
          "type": "DEFINES",
          "target": "concept_karuna",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kilesa_pali",
          "type": "DEFINES",
          "target": "concept_klesha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_klesa_sanskrit",
          "type": "DEFINES",
          "target": "concept_klesha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_madhyama_pratipad_sanskrit",
          "type": "DEFINES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_majjhima_patipada_pali",
          "type": "DEFINES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_mantra_sanskrit",
          "type": "DEFINES",
          "target": "concept_mantra",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_metta_pali",
          "type": "DEFINES",
          "target": "concept_metta",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_mudita_pali",
          "type": "DEFINES",
          "target": "concept_mudita",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nibbana_pali",
          "type": "DEFINES",
          "target": "concept_nirvana",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nirvana_sanskrit",
          "type": "DEFINES",
          "target": "concept_nirvana",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_panna_pali",
          "type": "DEFINES",
          "target": "concept_prajna",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paramita_sanskrit",
          "type": "DEFINES",
          "target": "concept_paramita",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paticcasamuppada_pali",
          "type": "DEFINES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_prajna_sanskrit",
          "type": "DEFINES",
          "target": "concept_prajna",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_prajnaparamita_sanskrit",
          "type": "DEFINES",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_pratityasamutpada_sanskrit",
          "type": "DEFINES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_rupa_pali",
          "type": "DEFINES",
          "target": "concept_form",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_samadhi_pali",
          "type": "DEFINES",
          "target": "concept_samadhi",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_samsara_pali",
          "type": "DEFINES",
          "target": "concept_samsara",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_satya_dvaya_sanskrit",
          "type": "DEFINES",
          "target": "concept_two_truths",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sila_pali",
          "type": "DEFINES",
          "target": "concept_sila",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_skandha_sanskrit",
          "type": "DEFINES",
          "target": "concept_skandhas",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sunyata_sanskrit",
          "type": "DEFINES",
          "target": "concept_sunyata",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tanha_pali",
          "type": "DEFINES",
          "target": "concept_tanha",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tilakkhana_pali",
          "type": "DEFINES",
          "target": "concept_three_marks",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_trilaksana_sanskrit",
          "type": "DEFINES",
          "target": "concept_three_marks",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_trsna_sanskrit",
          "type": "DEFINES",
          "target": "concept_tanha",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upekkha_pali",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upeksa_sanskrit",
          "type": "DEFINES",
          "target": "concept_upekkha",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_can_hv",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_thuc_hv",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_luc_tran_hv",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_can_vi",
          "type": "DENOTES",
          "target": "concept_sau_can",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_thuc_vi",
          "type": "DENOTES",
          "target": "concept_sau_thuc",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "term_sau_tran_vi",
          "type": "DENOTES",
          "target": "concept_sau_tran",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_youtube_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "DERIVED_FROM",
          "target": "source_giac_khang_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_transcript_fisp_arohzy8",
          "type": "DERIVED_FROM",
          "target": "source_youtube_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_fisp_arohzy8_0001",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0002",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0003",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0004",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0005",
          "type": "DERIVED_FROM",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "DERIVED_FROM",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "DERIVED_FROM",
          "target": "source_giac_khang_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "EVIDENCES",
          "target": "concept_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "EVIDENCES",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "EVIDENCES",
          "target": "concept_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_fisp_arohzy8_0001",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0002",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0003",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0004",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_fisp_arohzy8_0005",
          "type": "HAS_CITATION",
          "target": "citation_youtube_fisp_arohzy8",
          "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
          "source_badge": "processed"
        },
        {
          "source": "evidence_giac_khang_middle_way_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_pratityasamutpada_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "evidence_giac_khang_sunyata_001",
          "type": "HAS_CITATION",
          "target": "citation_giac_khang_notes_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_giac_khang_notes",
          "type": "HAS_DOCUMENT",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "source_youtube_fisp_arohzy8",
          "type": "HAS_DOCUMENT",
          "target": "document_transcript_fisp_arohzy8",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "work_giac_khang_pilot_teachings",
          "type": "HAS_DOCUMENT",
          "target": "document_giac_khang_mvp_notes",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_middle_way_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_pratityasamutpada_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "document_giac_khang_mvp_notes",
          "type": "HAS_EVIDENCE",
          "target": "evidence_giac_khang_sunyata_001",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "place_bodh_gaya",
          "type": "LOCATED_IN",
          "target": "place_magadha",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "place_nalanda",
          "type": "LOCATED_IN",
          "target": "place_magadha",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_pali_canon",
          "type": "LOCATED_IN",
          "target": "place_sri_lanka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_theravada",
          "type": "LOCATED_IN",
          "target": "place_sri_lanka",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_dukkha",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_1",
          "type": "MENTIONS",
          "target": "concept_karma",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_129",
          "type": "MENTIONS",
          "target": "concept_ahimsa",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_129",
          "type": "MENTIONS",
          "target": "concept_karuna",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_183",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_183",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_2",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_2",
          "type": "MENTIONS",
          "target": "concept_karma",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_21",
          "type": "MENTIONS",
          "target": "concept_appamada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_277",
          "type": "MENTIONS",
          "target": "concept_anicca",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_279",
          "type": "MENTIONS",
          "target": "concept_anatta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_35",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_5",
          "type": "MENTIONS",
          "target": "concept_metta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_dhammapada_50",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_middle_way",
          "type": "MENTIONS",
          "target": "concept_middle_way",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_pratityasamutpada",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_giac_khang_notes_sunyata",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/giac_khang_pilot.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_ayatana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_dhatu",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_four_noble_truths",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_dharmas",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_mantra",
          "type": "MENTIONS",
          "target": "concept_mantra",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_mantra",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_opening",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_form",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_heart_sutra_skandhas",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_middle_way",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_18",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_24_19",
          "type": "MENTIONS",
          "target": "concept_two_truths",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_25_19",
          "type": "MENTIONS",
          "target": "concept_nirvana",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "citation_mmkv_25_19",
          "type": "MENTIONS",
          "target": "concept_samsara",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_dukkha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_nirvana",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_noble_eightfold_path",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "MENTIONS",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_prajna",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_samadhi",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_noble_eightfold_path",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_anatta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_anicca",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_appamada",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_citta",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_dhammapada",
          "type": "MENTIONS",
          "target": "concept_sila",
          "source_file": "data/seeds/dhammapada.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_avalokitesvara",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_ayatana",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_dhatu",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_prajnaparamita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_heart_sutra",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_sunyata",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "text_mulamadhyamakakarika",
          "type": "MENTIONS",
          "target": "concept_two_truths",
          "source_file": "data/seeds/core.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_avalokitesvara",
          "type": "RELATED_TO",
          "target": "concept_karuna",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "RELATED_TO",
          "target": "concept_bodhicitta",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_bodhisattva",
          "type": "RELATED_TO",
          "target": "concept_paramita",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_form",
          "type": "RELATED_TO",
          "target": "concept_skandhas",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_four_noble_truths",
          "type": "RELATED_TO",
          "target": "place_sarnath",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_klesha",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_klesha",
          "type": "RELATED_TO",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_luc_can_luc_tran_luc_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_middle_way",
          "type": "RELATED_TO",
          "target": "concept_two_truths",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_nirvana",
          "type": "RELATED_TO",
          "target": "place_bodh_gaya",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "RELATED_TO",
          "target": "concept_paramita",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_prajnaparamita",
          "type": "RELATED_TO",
          "target": "concept_prajna",
          "source_file": "data/seeds/heart_sutra.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_karma",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_pratityasamutpada",
          "type": "RELATED_TO",
          "target": "concept_tanha",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_avidya",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_karma",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_samsara",
          "type": "RELATED_TO",
          "target": "concept_nirvana",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_can",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_thuc",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sau_tran",
          "type": "RELATED_TO",
          "target": "concept_kinh_sau_sau",
          "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "RELATED_TO",
          "target": "concept_pratityasamutpada",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "concept_sunyata",
          "type": "RELATED_TO",
          "target": "concept_two_truths",
          "source_file": "data/seeds/concepts.json",
          "source_badge": "seed"
        },
        {
          "source": "school_mahayana",
          "type": "RELATED_TO",
          "target": "place_gandhara",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "school_pali_canon",
          "type": "RELATED_TO",
          "target": "school_theravada",
          "source_file": "data/seeds/places_traditions.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anatta_pali",
          "type": "RELATED_TO",
          "target": "term_anatman_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_anicca_pali",
          "type": "RELATED_TO",
          "target": "term_anitya_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_ariya_atthangika_magga_pali",
          "type": "RELATED_TO",
          "target": "term_arya_astangika_marga_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avihimsa_pali",
          "type": "RELATED_TO",
          "target": "term_ahimsa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_avijja_pali",
          "type": "RELATED_TO",
          "target": "term_avidya_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_cattari_ariyasaccani_pali",
          "type": "RELATED_TO",
          "target": "term_catvari_aryasatyani_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_dukkha_pali",
          "type": "RELATED_TO",
          "target": "term_duhkha_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kamma_pali",
          "type": "RELATED_TO",
          "target": "term_karma_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_kilesa_pali",
          "type": "RELATED_TO",
          "target": "term_klesa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_majjhima_patipada_pali",
          "type": "RELATED_TO",
          "target": "term_madhyama_pratipad_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_nibbana_pali",
          "type": "RELATED_TO",
          "target": "term_nirvana_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_panna_pali",
          "type": "RELATED_TO",
          "target": "term_prajna_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_paticcasamuppada_pali",
          "type": "RELATED_TO",
          "target": "term_pratityasamutpada_sanskrit",
          "source_file": "data/seeds/terms.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tanha_pali",
          "type": "RELATED_TO",
          "target": "term_trsna_sanskrit",
          "source_file": "data/seeds/terms_extended.json",
          "source_badge": "seed"
        },
        {
          "source": "term_tilakkhana_pali",
          "type": "RELATED_TO",
          "target": "term_trilaksana_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        },
        {
          "source": "term_upekkha_pali",
          "type": "RELATED_TO",
          "target": "term_upeksa_sanskrit",
          "source_file": "data/seeds/terms_remaining.json",
          "source_badge": "seed"
        }
      ]
    }
  }
};
window.DHARMA_GRAPH = {
  "metadata": {
    "title": "Dharma Knowledge Graph: Giác Khang Corpus",
    "version": "0.1",
    "mode": "giac_khang",
    "content_hash": "5c453319f08e887b114988a043ff59e6c7e1b969bd1ebc4d1bc5af8e08fca431",
    "source_files": [
      "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json"
    ]
  },
  "summary": {
    "node_count": 20,
    "relationship_count": 25,
    "node_type_counts": {
      "Citation": 1,
      "Concept": 5,
      "Corpus": 1,
      "Document": 1,
      "Evidence": 5,
      "Source": 1,
      "Term": 6
    },
    "relationship_type_counts": {
      "BELONGS_TO_CORPUS": 2,
      "DENOTES": 6,
      "DERIVED_FROM": 7,
      "HAS_CITATION": 5,
      "HAS_DOCUMENT": 1,
      "RELATED_TO": 4
    },
    "source_badge_counts": {
      "corpus": 1,
      "reviewed": 5,
      "seed": 14
    }
  },
  "nodes": [
    {
      "id": "citation_youtube_fisp_arohzy8",
      "type": "Citation",
      "name": "YouTube citation for FISpARohzy8",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "locator": "video root",
      "review_status": "unreviewed",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "concept_kinh_sau_sau",
      "type": "Concept",
      "name": "Kinh Sáu Sáu",
      "language": "vi",
      "category": "text_topic",
      "description": "Pilot topic concept for Giác Khang teachings on Kinh Sáu Sáu.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "concept_luc_can_luc_tran_luc_thuc",
      "type": "Concept",
      "name": "Lục căn, lục trần, lục thức",
      "language": "vi",
      "category": "doctrine",
      "description": "Grouping concept for six faculties, six objects, and six consciousnesses.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "concept_sau_can",
      "type": "Concept",
      "name": "Sáu căn",
      "language": "vi",
      "category": "doctrine",
      "description": "Vietnamese concept placeholder for the six sense faculties in the Kinh Sáu Sáu pilot.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "concept_sau_thuc",
      "type": "Concept",
      "name": "Sáu thức",
      "language": "vi",
      "category": "doctrine",
      "description": "Vietnamese concept placeholder for the six consciousnesses in the Kinh Sáu Sáu pilot.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "concept_sau_tran",
      "type": "Concept",
      "name": "Sáu trần",
      "language": "vi",
      "category": "doctrine",
      "description": "Vietnamese concept placeholder for the six sense objects in the Kinh Sáu Sáu pilot.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "corpus_giac_khang",
      "type": "Corpus",
      "name": "Giác Khang Corpus",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "corpus"
    },
    {
      "id": "document_transcript_fisp_arohzy8",
      "type": "Document",
      "name": "Transcript placeholder for 1A. KINH 6 6 L2CÂU 1 P1",
      "document_kind": "transcript",
      "language": "vi",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "source_kind": "youtube",
      "review_status": "unreviewed",
      "notes": "Transcript not yet imported. Evidence must not be created without real excerpt text and timestamp.",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "evidence_fisp_arohzy8_0001",
      "type": "Evidence",
      "name": "VTT caption excerpt 0001 from FISpARohzy8",
      "evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
      "evidence_type": "transcript_excerpt",
      "language": "vi",
      "confidence": "low",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "document_id": "document_transcript_fisp_arohzy8",
      "start_time": "00:01:18.720",
      "end_time": "00:01:39.030",
      "speaker": "HT. Thích Giác Khang",
      "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
      "original_review_status": "unreviewed",
      "original_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
      "reviewed_evidence_text": "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước rồi hai vị Phật tử sẽ nhắc lại rồi chúng ta sẽ đi vào trả lời bài câu hỏi số 1 thì ở đây bài kinh 66 gồm tất cả là sáu phần. Phần nhập đề tức",
      "reviewer": "",
      "reviewed_at": "",
      "review_notes": "",
      "review_status": "human_reviewed",
      "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
      "source_badge": "reviewed"
    },
    {
      "id": "evidence_fisp_arohzy8_0002",
      "type": "Evidence",
      "name": "VTT caption excerpt 0002 from FISpARohzy8",
      "evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
      "evidence_type": "transcript_excerpt",
      "language": "vi",
      "confidence": "low",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "document_id": "document_transcript_fisp_arohzy8",
      "start_time": "00:01:39.040",
      "end_time": "00:01:53.190",
      "speaker": "HT. Thích Giác Khang",
      "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
      "original_review_status": "unreviewed",
      "original_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
      "reviewed_evidence_text": "là phần dẫn nhập, phần kết luận là hai còn phần thân bài là bốn. Thì ở đây chúng ta thường thấy kinh Phật nói chung đó là có sáu cái ấn chứng, sáu cái chứng để đi vào bài giảng.",
      "reviewer": "",
      "reviewed_at": "",
      "review_notes": "",
      "review_status": "human_reviewed",
      "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
      "source_badge": "reviewed"
    },
    {
      "id": "evidence_fisp_arohzy8_0003",
      "type": "Evidence",
      "name": "VTT caption excerpt 0003 from FISpARohzy8",
      "evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
      "evidence_type": "transcript_excerpt",
      "language": "vi",
      "confidence": "low",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "document_id": "document_transcript_fisp_arohzy8",
      "start_time": "00:01:53.200",
      "end_time": "00:02:16.110",
      "speaker": "HT. Thích Giác Khang",
      "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
      "original_review_status": "unreviewed",
      "original_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
      "reviewed_evidence_text": "Vì chúng ta thấy đây là cái ấn chứng thứ nhất là không gian, thứ nhì là thời gian và cái thứ ba là ai giảng, cái thứ tư là giảng cho ai nghe và cái thứ năm là giảng về kinh gì và cái thứ sáu là nội dung của bài kinh đó. Thì chúng ta thấy đây không gian thời gian là tại thành Xá Vệ cái giường của ông thái tử Kiều Đà và",
      "reviewer": "",
      "reviewed_at": "",
      "review_notes": "",
      "review_status": "human_reviewed",
      "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
      "source_badge": "reviewed"
    },
    {
      "id": "evidence_fisp_arohzy8_0004",
      "type": "Evidence",
      "name": "VTT caption excerpt 0004 from FISpARohzy8",
      "evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
      "evidence_type": "transcript_excerpt",
      "language": "vi",
      "confidence": "low",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "document_id": "document_transcript_fisp_arohzy8",
      "start_time": "00:02:16.120",
      "end_time": "00:02:37.949",
      "speaker": "HT. Thích Giác Khang",
      "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
      "original_review_status": "unreviewed",
      "original_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
      "reviewed_evidence_text": "Tịnh xá của cấp cô độc. Đó là phần không gian thời gian hai phần. Phần thứ ba là Đức Phật Thích Ca Mâu Ni tức là đức Thế Tôn của chúng ta giảng và giảng cho các vị tỳ kheo nghe. Đó là bốn phần. Và phần thứ năm là giảng về bài kinh 66 và nội dung đó là sơ thiện, trung thiện, hậu thiện có văn có nghĩa",
      "reviewer": "",
      "reviewed_at": "",
      "review_notes": "",
      "review_status": "human_reviewed",
      "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
      "source_badge": "reviewed"
    },
    {
      "id": "evidence_fisp_arohzy8_0005",
      "type": "Evidence",
      "name": "VTT caption excerpt 0005 from FISpARohzy8",
      "evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
      "evidence_type": "transcript_excerpt",
      "language": "vi",
      "confidence": "low",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "document_id": "document_transcript_fisp_arohzy8",
      "start_time": "00:02:37.959",
      "end_time": "00:02:54.470",
      "speaker": "HT. Thích Giác Khang",
      "notes": "Imported from YouTube VTT caption. Needs human review for Buddhist terminology.",
      "original_review_status": "unreviewed",
      "original_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
      "reviewed_evidence_text": "phạm hạnh thanh tịnh rồi đưa đến giải thoát. Đó là hình. Còn sau đây là bốn phần là thân bài. Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
      "reviewer": "",
      "reviewed_at": "",
      "review_notes": "",
      "review_status": "human_reviewed",
      "source_file": "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
      "source_badge": "reviewed"
    },
    {
      "id": "source_youtube_fisp_arohzy8",
      "type": "Source",
      "name": "YouTube video FISpARohzy8",
      "source_kind": "youtube",
      "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
      "channel": "PHÁP ÂM SƯ KHANG",
      "title": "1A. KINH 6 6 L2CÂU 1 P1",
      "speaker": "HT. Thích Giác Khang",
      "topic": "Kinh Sáu Sáu",
      "review_status": "unreviewed",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_luc_can_hv",
      "type": "Term",
      "name": "lục căn",
      "language": "vi",
      "script": "Hán-Việt",
      "translation": "six sense faculties",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_luc_thuc_hv",
      "type": "Term",
      "name": "lục thức",
      "language": "vi",
      "script": "Hán-Việt",
      "translation": "six consciousnesses",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_luc_tran_hv",
      "type": "Term",
      "name": "lục trần",
      "language": "vi",
      "script": "Hán-Việt",
      "translation": "six sense objects",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_sau_can_vi",
      "type": "Term",
      "name": "sáu căn",
      "language": "vi",
      "translation": "six sense faculties",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_sau_thuc_vi",
      "type": "Term",
      "name": "sáu thức",
      "language": "vi",
      "translation": "six consciousnesses",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "id": "term_sau_tran_vi",
      "type": "Term",
      "name": "sáu trần",
      "language": "vi",
      "translation": "six sense objects",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    }
  ],
  "relationships": [
    {
      "source": "document_transcript_fisp_arohzy8",
      "type": "BELONGS_TO_CORPUS",
      "target": "corpus_giac_khang",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "source_youtube_fisp_arohzy8",
      "type": "BELONGS_TO_CORPUS",
      "target": "corpus_giac_khang",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_luc_can_hv",
      "type": "DENOTES",
      "target": "concept_sau_can",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_luc_thuc_hv",
      "type": "DENOTES",
      "target": "concept_sau_thuc",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_luc_tran_hv",
      "type": "DENOTES",
      "target": "concept_sau_tran",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_sau_can_vi",
      "type": "DENOTES",
      "target": "concept_sau_can",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_sau_thuc_vi",
      "type": "DENOTES",
      "target": "concept_sau_thuc",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "term_sau_tran_vi",
      "type": "DENOTES",
      "target": "concept_sau_tran",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "citation_youtube_fisp_arohzy8",
      "type": "DERIVED_FROM",
      "target": "source_youtube_fisp_arohzy8",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "document_transcript_fisp_arohzy8",
      "type": "DERIVED_FROM",
      "target": "source_youtube_fisp_arohzy8",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "evidence_fisp_arohzy8_0001",
      "type": "DERIVED_FROM",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0002",
      "type": "DERIVED_FROM",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0003",
      "type": "DERIVED_FROM",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0004",
      "type": "DERIVED_FROM",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0005",
      "type": "DERIVED_FROM",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0001",
      "type": "HAS_CITATION",
      "target": "citation_youtube_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0002",
      "type": "HAS_CITATION",
      "target": "citation_youtube_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0003",
      "type": "HAS_CITATION",
      "target": "citation_youtube_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0004",
      "type": "HAS_CITATION",
      "target": "citation_youtube_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "evidence_fisp_arohzy8_0005",
      "type": "HAS_CITATION",
      "target": "citation_youtube_fisp_arohzy8",
      "source_file": "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
      "source_badge": "processed"
    },
    {
      "source": "source_youtube_fisp_arohzy8",
      "type": "HAS_DOCUMENT",
      "target": "document_transcript_fisp_arohzy8",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "concept_luc_can_luc_tran_luc_thuc",
      "type": "RELATED_TO",
      "target": "concept_kinh_sau_sau",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "concept_sau_can",
      "type": "RELATED_TO",
      "target": "concept_kinh_sau_sau",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "concept_sau_thuc",
      "type": "RELATED_TO",
      "target": "concept_kinh_sau_sau",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    },
    {
      "source": "concept_sau_tran",
      "type": "RELATED_TO",
      "target": "concept_kinh_sau_sau",
      "source_file": "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
      "source_badge": "seed"
    }
  ]
};
