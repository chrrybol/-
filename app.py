import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 부드러운 숲속 테마 스타일 적용
st.set_page_config(
    page_title="초록숲 진로 탐색: 곰돌이 멘토와 함께", 
    page_icon="🌿", 
    layout="centered"
)

# 커스텀 CSS로 프론트엔드 귀엽게 꾸미기
st.markdown("""
    <style>
    /* 전체 배경색을 따뜻하고 밝은 아이보리/연녹색 톤으로 */
    .stApp {
        background-color: #f7f9f6;
    }
    
    /* 타이틀 및 메인 텍스트 컬러 변경 */
    h1 {
        color: #2d5a27 !important; /* 짙은 나뭇잎 색 */
        font-family: 'Nanum Gothic', sans-serif;
    }
    
    /* 유저 대화창 스타일 (부드러운 갈색 톤) */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by user"]) {
        background-color: #f1e4d3 !important;
        border-radius: 15px;
        border: 1px solid #e0cfb8;
        padding: 10px 15px;
    }
    
    /* 챗봇 대화창 스타일 (싱그러운 연두색 톤) */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by assistant"]) {
        background-color: #eaf2e8 !important;
        border-radius: 15px;
        border: 1px solid #cfe2cc;
        padding: 10px 15px;
    }
    
    /* 채팅창 입력 바 스타일 조절 */
    div[data-testid="stChatInput"] {
        border-radius: 20px;
    }
    
    /* 상단 장식 바 제거 및 깔끔한 마무리 */
    header {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# 2. API 키 확인 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 상단 헤더 꾸미기 (나뭇잎과 곰돌이)
st.markdown("<h1 style='text-align: center;'>🐻 초록숲 진로 탐색 소 가이드 🌿</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #556b2f; font-size: 1.1rem; font-weight: bold;'>"
    "안녕! 네가 좋아하는 일과 관심사를 들려주면, 멋진 미래 직업을 함께 찾아줄게! 🐾"
    "</p>", 
    unsafe_allow_html=True
)
st.write("---")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 화면에 표시 (커스텀 이모지 아이콘 적용)
for message in st.session_state.messages:
    # 유저는 나뭇잎(🌿), 챗봇은 곰돌이(🐻) 아이콘을 사용하도록 지정
    avatar_icon = "🌿" if message["role"] == "user" else "🐻"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("예: 나는 동물 돌보는 걸 좋아하고, 그림 그리는 것도 재밌어!"):
    
    # 1. 사용자 메시지 저장 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🌿"):
        st.markdown(user_input)

    # 2. 챗봇 답변 생성 및 화면 표시
    with st.chat_message("assistant", avatar="🐻"):
        message_placeholder = st.empty()
        
        try:
            # 모델 설정 및 숲속 곰돌이 멘토 컨셉 부여
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=(
                    "당신은 청소년들을 위한 친근하고 따뜻한 숲속 곰돌이 진로 상담사입니다. "
                    "말투는 다정하고 상냥한 반말(예: ~했구나!, ~해보는 건 어때?, 최고야! 🐾)을 사용해 주세요. "
                    "답변 중간중간에 곰돌이(🐻, 🐾)나 나뭇잎(🌿, 🌱) 이모지를 적절히 섞어 귀엽게 표현해 주고, "
                    "청소년의 고민을 적극적으로 공감하며 구체적인 진로 로드맵을 제안해 주세요."
                )
            )

            # 대화 기록 포맷팅
            history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})

            chat = model.start_chat(history=history)
            
            # 스트리밍 답변 출력
            full_response = ""
            response_stream = chat.send_message(user_input, stream=True)
            
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "🐾") # 로딩 중 발자국 표시
                
            message_placeholder.markdown(full_response)
            
            # 생성된 답변 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = "🐻 에구, 대화 중에 잠시 꿀단지가 넘쳤나 봐! 잠시 후 다시 말해줄래? 🍯"
            message_placeholder.markdown(error_msg)
            st.sidebar.error(f"상세 에러 로그: {e}")
