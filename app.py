import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="살인연구소 (Murder Lab)", page_icon="🕵️‍♂️", layout="centered")

st.title("🕵️‍♂️ 살인연구소 (Murder Lab) Chatbot")
st.caption("미스터리, 범죄 심리, 그리고 사건 추리의 세계에 오신 것을 환영합니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관관리자 설정을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 및 모델 객체 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    try:
        # gemini-2.5-flash-lite 모델 설정 및 컨셉 부여
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "당신은 '살인연구소'의 수석 연구원 AI입니다. "
                "사용자는 범죄 심리학, 추리 소설 기법, 역사적 사건 등에 관심이 있는 탐정들입니다. "
                "어둡고 미스터리하면서도 지적이고 정중한 톤앤매너를 유지하세요. "
                "단, 실제 범죄를 모의하거나 잔혹하고 고어한 묘사를 구체적으로 유도하는 질문에는 "
                "안전 가이드라인을 준수하며 부드럽게 거절해야 합니다."
            )
        )
        # 빈 대화 기록으로 채팅 세션 시작
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"🤖 모델을 초기화하는 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("연구소장에게 물어볼 사건을 입력하세요..."):
    
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🕵️‍♂️ *단서를 분석 중입니다...*")
        
        try:
            # Gemini API로 메시지 전송
            response = st.session_state.chat_session.send_message(user_input)
            full_response = response.text
            
            # 답변 화면에 업데이트 및 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # API 호출 오류 예외 처리
            error_msg = f"⚠️ 답변을 생성하는 동안 오류가 발생했습니다: {e}\n(API 키 상태나 요청 내용을 확인해 주세요.)"
            message_placeholder.markdown(error_msg)
