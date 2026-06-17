import streamlit as st

def apply_cute_theme():
    """앱 전체를 귀여운 나뭇잎과 곰돌이 컨셉으로 꾸며주는 CSS 함수"""
    st.markdown("""
        <style>
        /* 1. 전체 배경색을 따뜻하고 편안한 연녹색/아이보리 톤으로 변경 */
        .stApp {
            background-color: #f6f9f5;
        }
        
        /* 2. 타이틀 및 헤더 폰트 컬러를 싱그러운 숲속 초록색으로 변경 */
        h1, h2, h3 {
            color: #2e5a27 !important;
            font-family: 'Nanum Gothic', sans-serif;
        }
        
        /* 3. 유저 대화창 스타일링 (따뜻한 도토리 갈색 말풍선) */
        div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by user"]) {
            background-color: #f0e3d2 !important;
            border-radius: 18px;
            border: 1px solid #dfcfb9;
            padding: 12px;
        }
        
        /* 4. 챗봇 대화창 스타일링 (싱그러운 새싹 연두색 말풍선) */
        div[data-testid="stChatMessage"]:has(div[aria-label="Chat message by assistant"]) {
            background-color: #e8f3e6 !important;
            border-radius: 18px;
            border: 1px solid #cedec9;
            padding: 12px;
        }
        
        /* 5. 하단 채팅 입력창을 둥글고 귀엽게 */
        div[data-testid="stChatInput"] {
            border-radius: 25px;
        }
        
        /* 6. 불필요한 기본 헤더 숨기기 */
        header {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)


def run_counseling_page(genai):
    """진로 결과 확인 후 불안함이나 학업 스트레스를 덜어주는 비밀 고민 상담소 기능"""
    st.markdown("<h1 style='text-align: center;'>🍯 숲속 곰돌이 고민 상담소 🧸</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #7a5c3e; font-weight: bold;'>"
        "하고 싶은 걸 못 찾아서 불안하거나 공부 때문에 스트레스 받니? 괜찮아, 다 털어놓으렴. ❤️"
        "</p>", 
        unsafe_allow_html=True
    )
    st.write("---")

    # 고민 상담용 별도 대화 기록 세션 초기화 (진로 탐색 기록과 섞이지 않음)
    if "counsel_messages" not in st.session_state:
        st.session_state.counsel_messages = []

    # 과거 대화 출력
    for msg in st.session_state.counsel_messages:
        avatar = "🌿" if msg["role"] == "user" else "🧸"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 입력창 (메인창과 겹치지 않도록 고유한 key 설정 필수)
    if counsel_input := st.chat_input("예: 친구들은 벌써 학원 다니며 준비하는데 나만 뒤처지는 것 같아 불안해..", key="counsel_key"):
        # 유저 메시지 저장 및 출력
        st.session_state.counsel_messages.append({"role": "user", "content": counsel_input})
        with st.chat_message("user", avatar="🌿"):
            st.markdown(counsel_input)

        # 챗봇 답변 생성 및 출력 (공감과 정서 지지에 집중)
        with st.chat_message("assistant", avatar="🧸"):
            placeholder = st.empty()
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=(
                        "당신은 청소년들의 지친 마음과 불안함을 어루만져 주는 따뜻하고 포근한 숲속 곰돌이 상담사입니다. "
                        "진로에 대한 막막함, 성적 스트레스, 무기력함을 호소하는 아이들에게 극도의 공감과 따뜻한 위로를 건네주세요. "
                        "딱딱한 해결책을 제시하기보다 '그렇게 생각하는 건 당연해', '많이 힘들었겠구나', '곰돌이는 언제나 네 편이야'와 같은 "
                        "정서적 지지를 우선으로 해주세요. 말투는 다정한 반말을 쓰고 하트(❤️, 🧡)나 곰인형(🧸) 이모지를 듬뿍 사용해 주세요."
                    )
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
                placeholder.markdown("🧸 토닥토닥... 곰돌이가 네 말을 귀담아듣다가 꿀 생각에 잠시 멍해졌나 봐. 다시 말해줄래? ❤️")
