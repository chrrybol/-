import streamlit as st
st.title('운빨겜')
st.write('welcome')
st.write('from openai import OpenAI')
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일에서 API 키를 읽어옴)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("🚨 환경 변수 오류: .env 파일에 'OPENAI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 2. OpenAI 클라이언트 백엔드 초기화
client = OpenAI(api_key=api_key)

# 3. 웹 앱 UI 및 페이지 설정
st.set_page_config(page_title="Pro AI Chatbot", page_icon="🧠", layout="centered")
st.title("🧠 프로페셔널 AI 챗봇")
st.caption("🚀 스트리밍 기능과 안전한 백엔드 아키텍처가 적용된 완성본 웹앱입니다.")

# 4. [백엔드 데이터베이스 역할] 세션 상태 초기화
# 대화 내역(messages) 저장 공간 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

# AI의 페르소나를 결정하는 시스템 프롬프트 (기본값 설정)
SYSTEM_PROMPT = {"role": "system", "content": "당신은 전문적이고 친절한 AI 조언자입니다. 항상 정확하고 정중하게 답변하세요."}

# 5. [데이터 렌더링] 기존 대화 기록을 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. [사용자 입력 처리 및 API 호출 백엔드 로직]
if user_input := st.chat_input("무엇이든 물어보세요..."):
    
    # 유저 입력 즉시 화면 표시 및 메모리 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI 답변을 출력할 공간을 미리 만들기
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # 스트리밍 텍스트가 채워질 빈 공간
        full_response = ""
        
        try:
            # API 전송용 메시지 조립: [시스템 프롬프트] + [이전 대화 기록 전체]
            api_messages = [SYSTEM_PROMPT] + st.session_state.messages
            
            # [핵심 백엔드] OpenAI API 스트리밍 요청
            # stream=True 옵션을 주면 데이터가 완성될 때까지 기다리지 않고 조각조각 계속 들어옵니다.
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                stream=True,
            )
            
            # 스트리밍 데이터 실시간 수신 및 프론트엔드 전달
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # 실시간으로 빈 공간에 텍스트를 누적하여 업데이트 (타이핑 효과)
                    response_placeholder.markdown(full_response + "▌")
            
            # 커서(▌)를 지우고 최종 텍스트로 확정 표시
            response_placeholder.markdown(full_response)
            
            # [백엔드 저장] 완성된 AI 답변을 대화 기록에 최종 누적
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"백엔드 통신 중 에러가 발생했습니다: {str(e)}")
