import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="공부 계획 AI 챗봇", page_icon="📅")
st.title("📅 스마트 공부 계획 챗봇")
st.caption("gemini-2.5-flash-lite 모델을 사용한 AI 학습 플래너입니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
try:
    # Streamlit Cloud 배포 환경이나 로컬 .streamlit/secrets.toml 환경에서 키를 읽어옵니다.
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API 키를 찾을 수 없습니다. Streamlit Secrets에 'GOOGLE_API_KEY'를 설정해주세요.")
    st.stop()

# 3. 채팅 기록 유지(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 당신의 맞춤형 학습 매니저입니다. 어떤 과목이나 시험을 준비하시나요? 목표와 기간을 말씀해주시면 체계적인 공부 계획을 세워드릴게요!"
        }
    ]

# 4. 이전 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. 사용자 입력 받기 및 처리
if user_input := st.chat_input("예: 2주 뒤에 있는 정보처리기사 필기 시험 계획 짜줘"):
    
    # 사용자가 입력한 메시지 화면에 표시 및 세션에 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI 응답 생성 중 표시 (스피너)
    with st.chat_message("assistant"):
        with st.spinner("AI 매니저가 효율적인 계획을 구성하고 있습니다..."):
            try:
                # 지정하신 gemini-2.5-flash-lite 모델 로드
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                # 대화 맥락을 유지하기 위해 이전 대화 기록을 프롬프트에 포함 (페르소나 부여 포함)
                system_instruction = "당신은 학습 계획을 전문적으로 짜주는 든든한 AI 교육 멘토입니다. 친절하고 구체적이며 체계적으로 날짜별/단계별 공부 계획과 실천 팁을 제안해주세요."
                
                # API 전송용 컨텍스트 구성
                full_prompt = f"{system_instruction}\n\n이전 대화 기록:\n"
                for msg in st.session_state.messages[:-1]: # 현재 입력 직전까지의 대화
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += f"user: {user_input}\nassistant:"
                
                # API 호출
                response = model.generate_content(full_prompt)
                ai_response = response.text
                
                # AI 응답 출력 및 세션 저장
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                # 오류 처리 (API 연결 실패, 제한 초과 등)
                error_msg = f"❌ 오류가 발생했습니다: {str(e)}\nAPI 키가 올바른지, 혹은 할당량이 남아있는지 확인해주세요."
                st.error(error_msg)
