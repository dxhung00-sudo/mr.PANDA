import streamlit as st
import google.generativeai as genai
import json

# --- CẤU HÌNH API ---
# Thầy dán API Key lấy từ Google AI Studio vào đây
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- HÀM GỌI AI SOẠN ĐỀ ---
def generate_quiz(topic):
    prompt = r"""
    Bạn là chuyên gia soạn đề Toán. Hãy soạn 3 câu hỏi trắc nghiệm về chủ đề: """ + topic + r""".
    Yêu cầu xuất JSON chuẩn với cấu trúc:
    [
      {"type": "multiple_choice", "question": "...", "options": {"A": "..", "B": "..", "C": "..", "D": ".."}, "answer": "B"},
      {"type": "true_false", "context": "...", "sub_questions": [{"id": "a", "content": "..", "answer": "Đúng"}], "explanation": ".."},
      {"type": "short_answer", "context": "...", "sub_questions": [{"id": "1", "content": "..", "answer": "5"}], "explanation": ".."}
    ]
    Lưu ý: Dùng LaTeX cho công thức toán. Chỉ trả về JSON, không nói thêm.
    """
    response = model.generate_content(prompt)
    # Làm sạch dữ liệu trả về (xóa các ký tự thừa như ```json)
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# --- GIAO DIỆN APP ---
st.set_page_config(page_title="App Toán Thầy Hùng", layout="wide")
st.title("🎓 Hệ Thống Tạo Bài Tập Toán Tự Động")

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

# Ô nhập liệu
topic_input = st.text_input("Nhập chủ đề bài tập (Ví dụ: Hệ thức lượng trong tam giác vuông):")
if st.button("Tạo đề ngay"):
    with st.spinner("AI đang soạn đề, thầy chờ xíu nhé..."):
        st.session_state.quiz_data = generate_quiz(topic_input)

# Hiển thị đề thi
if st.session_state.quiz_data:
    with st.form("quiz_form"):
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"### Câu {i+1}")
            if q['type'] == 'multiple_choice':
                st.write(q['question'])
                st.radio("Chọn đáp án:", list(q['options'].values()), key=f"q_{i}")
            # ... (Thêm code hiển thị True/False và Short Answer như bài trước) ...
        
        if st.form_submit_button("Nộp bài"):
            st.balloons()
            st.success("Hợp lệ! Thầy có thể thêm logic chấm điểm tại đây.")
