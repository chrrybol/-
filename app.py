import streamlit as st
from google import genai
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(
    page_title="달콤살벌 연애상담소 💬",
    page_icon="❤️",
    layout="centered"
)

# 제목 및 설명
st.title("❤️ 달콤살벌 연애상담소")
st.caption("Gemini 2.5 Flash-Lite 기반의 인공지능 연애 상담사입니다. 당신의 연애 고민을 들어드릴게요!")

# Streamlit Secrets에서 API 키 불러오기
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API 키가 설정되지 않았습니다. Streamlit 대시보드의 Secrets에 'GEMINI_API_KEY'를 등록해주세요.")
    st.stop()

# 구글 GenAI 클라이언트 초기화
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 세션 상태(Session State)를 활용한 채팅 기록 유지 설정
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 상담사 콘셉트를 부여하기 위한 첫 환영 인사 추가
    st.session_state.messages.append({
        "role": "model",
        "content": "안녕하세요! 당신의 연애 고민 해결을 도와드릴 연애 상담사입니다. 어떤 고민이 있으신가요? 사소한 이야기라도 편하게 들려주세요. 💕"
    })

# 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력 처리
if user_input := st.chat_input("고민을 입력하세요... (예: 썸녀가 선톡을 안 해요)"):
    # 1. 사용자 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. 챗봇 답변 생성 및 화면 표시
    with st.chat_message("model"):
        with st.spinner("당신의 고민에 귀 기울이는 중..."):
            try:
                # 연애 상담사 콘셉트를 유지하기 위한 시스템 지침(System Instruction) 설정
                system_instruction = (
                    "당신은 전문적이고 공감 능력이 뛰어난 연애 상담사입니다. "
                    "사용자의 고민에 진심으로 공감해주고, 때로는 현실적이고 실용적인 조언을 제공해야 합니다. "
                    "친근하고 다정한 말투를 사용하되, 선을 넘지 않는 선에서 위트 있게 답변하세요."
                )

                # 대화 맥락(History)을 엮어서 보낼 수도 있으나, 
                # 여기서는 API 호출 안정성과 단발성 대화 규칙에 맞추어 최신 입력에 시스템 지침을 결합해 전달합니다.
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_input,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.7,
                    }
                )
                
                # 답변 출력 및 세션 저장
                ai_response = response.text
                st.write(ai_response)
                st.session_state.messages.append({"role": "model", "content": ai_response})

            except APIError as e:
                # Gemini API 자체 오류 처리 (할당량 초과, 잘못된 키 등)
                st.error(f"❌ Gemini API 오류가 발생했습니다: {e.message}")
            except Exception as e:
                # 기타 일반 예외 처리
                st.error(f"⚠️ 에러가 발생했습니다: {e}")
