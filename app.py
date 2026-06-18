import streamlit as st
import google.generativeai as genai

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="초록숲 곰돌이 진로 상담소",
    page_icon="🌿",
    layout="centered"
)

# 2. 귀여운 나뭇잎 & 곰돌이 컨셉 CSS 테마 적용 (안전한 단일 파일 전용 스타일)
st.markdown("""
    <style>
    /* 전체 배경을 편안한 연녹색/아이보리 톤으로 */
    .stApp { background-color: #f6f9f5; }
    
    /* 헤더 폰트 컬러를 싱그러운 숲속 초록색으로 */
    h1, h2, h3 { color: #2e5a27 !important; font-family: 'Nanum Gothic', sans-serif; }
    
    /* 유저 대화창 스타일링 (따뜻한 도토리 갈색 말풍선) */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by user"]) {
        background-color: #f0e3d2 !important; border-radius: 18px; border: 1px solid #dfcfb9; padding: 12px;
    }
    
    /* 챗봇 대화창 스타일링 (싱그러운 새싹 연두색 말풍선) */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by assistant"]) {
        background-color: #e8f3e6 !important; border-radius: 18px; border: 1px solid #cedec9; padding: 12px;
    }
    
    /* 하단 채팅 입력창 디자인 둥글게 */
    div[data-testid="stChatInput"] { border-radius: 25px; }
    </style>
""", unsafe_allow_html=True)

# 3. Streamlit Secrets에서 API 키 확인 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리자 페이지에서 등록해 주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. 사이드바 메뉴 구성 (두 가지 기능을 자유롭게 이동)
st.sidebar.markdown("### 🐻 숲속 메뉴판 🌿")
app_mode = st.sidebar.radio("어떤 이야기를 나누고 싶어?", ["🌱 나의 진로 탐색하기", "🍯 곰돌이에게 고민 털어놓기"])


# =========================================================================
# [기능 1] 메인 진로 탐색 페이지
# =========================================================================
if app_mode == "🌱 나의 진로 탐색하기":
    st.markdown("<h1 style='text-align: center;'>🐻 초록숲 진로 탐색방 🌿</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4a6b42; font-weight: bold;'>"
        "안녕! 네가 좋아하는 과목, 취미, 관심사를 편하게 말해줘. 곰돌이가 멋진 직업을 찾아줄게! 🐾"
        "</p>", 
        unsafe_allow_html=True
    )
    st.write("---")

    # 진로 탐색 대화 기록 세션 초기화
    if "career_messages" not in st.session_state:
        st.session_state.career_messages = []

    # 과거 진로 대화 기록 출력
    for msg in st.session_state.career_messages:
        avatar = "🌿" if msg["role"] == "user" else "🐻"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 입력창 (고유 키 부여)
    if user_input := st.chat_input("예: 난 과학 실험을 좋아하고, 로봇 만드는 것에 관심이 많아!", key="career_input"):
        st.session_state.career_messages.append({"role
