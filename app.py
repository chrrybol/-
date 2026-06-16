import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="내일의 나: 청소년 진로 탐색 챗봇", page_icon="🚀", layout="centered")

# Streamlit Secrets에서 API 키 불러오기 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관라지 페이지에서 설정해 주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 제목 및 설명
st.title("🚀 내일의 나: 청소년 진로 탐색 챗봇")
st.caption("관심사, 취미, 좋아하는 과목을 말씀해 주시면 멋진 진로와 직업을 추천해 드려요!")

# 대화 기록 초기화 (Streamlit Session State 이용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("예: 나는 과학 실험을 좋아하고 사람들을 돕는 일을 하고 싶어!"):
    
    # 사용자가 입력한 메시지 저장 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 챗봇 답변 생성 및 화면 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # gemini-2.5-flash-lite 모델 인스턴스 생성
            # 청소년 상담원 역할을 하도록 system_instruction 설정
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=(
                    "당신은 청소년들을 위한 친절하고 따뜻한 진로 상담 전문가입니다. "
                    "청소년의 눈높이에 맞춰 이해하기 쉽게 설명하고, 긍정적이고 구체적인 조언을 제공해 주세요. "
                    "답변은 친근한 반말(예: ~했어?, ~해보는 건 어때?) 또는 상냥한 존댓말을 일관되게 사용해 주세요."
                )
            )

            # 이전 대화 기록을 Gemini API가 이해할 수 있는 형태로 변환
            history = []
            for msg in st.session_state.messages[:-1]:  # 현재 입력 제외한 이전 기록
                # Gemini API는 'user'와 'model' 역할을 사용합니다.
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})

            # 채팅 세션 시작 (과거 기록 포함)
            chat = model.start_chat(history=history)
            
            # 답변 생성 (스트리밍 방식 적용으로 실시간 글자 출력)
            full_response = ""
            response_stream = chat.send_message(user_input, stream=True)
            
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            
            # 생성된 답변을 대화 기록에 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # 오류 처리
            error_msg = "죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
            message_placeholder.markdown(error_msg)
            # 개발자가 로그를 확인할 수 있도록 세부 에러 출력 (사용자 화면에는 안 보임)
            st.sidebar.error(f"상세 에러 로그: {e}")
