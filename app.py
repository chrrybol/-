iimport streamlit as st
import google.generativeai as genai

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="초록숲 곰돌이 진로 상담소",
    page_icon="🌿",
    layout="centered"
)

# 2. 귀여운 나뭇잎 & 곰돌이 컨셉 테마 적용
st.markdown("""
    <style>
    .stApp { background-color: #f6f9f5; }
    h1, h2, h3 { color: #2e5a27 !important; font-family: 'Nanum Gothic', sans-serif; }
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by user"]) {
        background-color: #f0e3d2 !important; border-radius: 18px; border: 1px solid #dfcfb9; padding: 12px;
    }
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by assistant"]) {
        background-color: #e8f3e6 !important; border-radius: 18px; border: 1px solid #cedec9; padding: 12px;
    }
    div[data-testid="stChatInput"] { border-radius: 25px; }
    </style>
""", unsafe_allow_html=True)

# 3. Streamlit Secrets에서 API 키 확인 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리자 페이지에서 등록해 주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. 사이드바 메뉴 구성
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

    if "career_messages" not in st.session_state:
        st.session_state.career_messages = []

    for msg in st.session_state.career_messages:
        avatar = "🌿" if msg["role"] == "user" else "🐻"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 입력창 받기
    user_input = st.chat_input("예: 난 과학 실험을 좋아하고, 로봇 만드는 것에 관심이 많아!", key="career_input")
    
    if user_input:
        # 이 부분이 잘리지 않도록 안전하게 한 줄로 정돈했습니다.
        st.session_state.career_messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user", avatar="🌿"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🐻"):
            placeholder = st.empty()
            try:
                # 시스템 지침을 한 줄로 길게 늘어뜨리지 않고 안전하게 결합
                sys_instruction = (
                    "당신은 청소년들의 소질과 적성을 찾아주는 친절한 숲속 곰돌이 진로 전문가입니다. "
                    "상냥하고 다정한 반말을 사용해 주세요. 사용자의 흥미를 바탕으로 구체적인 직업을 추천하고 "
                    "나뭇잎(🌿)이나 곰(🐻) 이모지를 풍부하게 섞어 귀엽게 작성해 주세요."
                )
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=sys_instruction
                )
                
                history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.career_messages[:-1]]
                chat = model.start_chat(history=history)
                
                full_response = ""
                for chunk in chat.send_message(user_input, stream=True):
                    full_response += chunk.text
                    placeholder.markdown(full_response + "🐾")
                placeholder.markdown(full_response)
                
                st.session_state.career_messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                placeholder.markdown("🐻 에구, 대화 중에 꿀단지를 쏟았나 봐! 잠시 후 다시 이야기해 줄래? 🍯")

    # 대화가 시작되면 하단에 고민상담소 제안 버튼 출력
    if len(st.session_state.career_messages) >= 2:
        st.write("---")
        st.markdown("<p style='text-align: center; color: #7a6248;'> 혹시 미래에 대한 걱정이나 남모를 고민이 생겼니? </p>", unsafe_allow_html=True)
        if st.button("🐻 곰돌이에게 비밀 고민 상담하러 가기 🍯", use_container_width=True):
            st.info("왼쪽 사이드바 메뉴에서 '🍯 곰돌이에게 고민 털어놓기'를 선택해줘! 대피소에서 기다리고 있을게.")

# =========================================================================
# [기능 2] 고민 상담 페이지
# =========================================================================
else:
    st.markdown("<h1 style='text-align: center;'>🍯 숲속 곰돌이 고민 상담소 🧸</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #7a5c3e; font-weight: bold;'>"
        "하고 싶은 걸 못 찾아서 불안하거나 공부 때문에 스트레스 받니? 괜찮아, 다 털어놓으렴. ❤️"
        "</p>", 
        unsafe_allow_html=True
    )
    st.write("---")

    if "counsel_messages" not in st.session_state:
        st.session_state.counsel_messages = []

    for msg in st.session_state.counsel_messages:
        avatar = "🌿" if msg["role"] == "user" else "🧸"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    counsel_input = st.chat_input("예: 친구들은 벌써 진로를 정한 것 같아 나만 뒤처지는 기분이야..", key="counsel_input")

    if counsel_input:
        st.session_state.counsel_messages.append({"role": "user", "content": counsel_input})
        
        with st.chat_message("user", avatar="🌿"):
            st.markdown(counsel_input)

        with st.chat_message("assistant", avatar="🧸"):
            placeholder = st.empty()
            try:
                sys_instruction_counsel = (
                    "당신은 청소년들의 지친 마음과 불안함을 어루만져 주는 따뜻하고 포근한 숲속 곰돌이 상담사입니다. "
                    "진로 막막함, 성적 스트레스를 호소하는 아이들에게 극도의 공감과 따뜻한 위로를 건네주세요. "
                    "정서적 지지를 우선으로 하고 말투는 다정한 반말을 쓰며 하트(❤️)나 곰인형(🧸) 이모지를 사용해 주세요."
                )
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=sys_instruction_counsel
                )
                
                history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.counsel_messages[:-1]]
                chat = model.start_chat(history=history)
                
                full_response = ""
                for chunk in chat.send_message(counsel_input, stream=True):
                    full_response += chunk.text
                    placeholder.markdown(full_response + "🧸")
                placeholder.markdown(full_response)
                
                st.session_state.counsel_messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                placeholder.markdown("🧸 토닥토닥... 곰돌이가 네 말을 귀담아듣다가 꿀 생각에 잠깐 멍해졌나 봐. 다시 말해줄래? ❤️")
