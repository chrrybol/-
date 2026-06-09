import streamlit as st
import google.generativeai as genai
import random

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="쿠키런 킹덤 뽑기 연구소", page_icon="🍪", layout="centered")

st.title("🍪 쿠키런 킹덤 뽑기 시뮬레이터 Chatbot")
st.caption("용감한 쿠키와 함께 대화하고, 행운의 쿠키 뽑기에 도전해보세요!")

# 2. 쿠키 데이터베이스 (뽑기용)
COOKIES = {
    "ANCIENT/BEAST": ["퓨어바닐라 쿠키", "홀리베리 쿠키", "다크카카오 쿠키", "골드치즈 쿠키", "화이트릴리 쿠키", "미스 flour 쿠키", "버닝스파이스 쿠키"],
    "LEGENDARY": ["바다요정 쿠키", "서리여왕 쿠키", "블랙펄 쿠키", "달빛술사 쿠키", "스타더스트 쿠키"],
    "SUPER EPIC": ["클로티드 크림 쿠키", "오이스터 쿠키", "캡사이신맛 쿠키", "샤이닝글리터맛 쿠키", "크림스프 쿠키"],
    "EPIC": ["에스프레소맛 쿠키", "감초맛 쿠키", "다크초코 쿠키", "석류맛 쿠키", "허브맛 쿠키", "샤벳상어맛 쿠키", "소르베맛 쿠키", "와일드베리 쿠키", "휘낭시에맛 쿠키", "타트체리맛 쿠키", "페페론치노맛 쿠키", "민트초코 쿠키", "마들렌맛 쿠키", "호밀맛 쿠키", "뱀파이어맛 쿠키"],
    "RARE": ["커스터드 3세맛 쿠키", "클로버맛 쿠키", "실론나이트 쿠키", "양파맛 쿠키", "당근맛 쿠키", "아보카도맛 쿠키", "연금술사맛 쿠키"],
    "COMMON": ["용감한 쿠키", "딸기맛 쿠키", "마법사맛 쿠키", "비트맛 쿠키", "근육맛 쿠키", "천사맛 쿠키"]
}

# 등급별 확률 설정 (총합 100%)
GRADES = ["ANCIENT/BEAST", "LEGENDARY", "SUPER EPIC", "EPIC", "RARE", "COMMON"]
PROBABILITIES = [0.005, 0.015, 0.03, 0.15, 0.30, 0.50]  # 에인션트 0.5%, 레전더리 1.5% 등등

def draw_cookie():
    """확률에 따라 쿠키 1종을 무작위로 뽑는 함수"""
    grade = random.choices(GRADES, weights=PROBABILITIES, k=1)[0]
    cookie_name = random.choice(COOKIES[grade])
    
    # 등급별 이펙트 부여
    if grade in ["ANCIENT/BEAST", "LEGENDARY"]:
        effect = "✨👑 [엄청난 영웅의 기운!] 👑✨"
    elif grade == "SUPER EPIC":
        effect = "🌟✨ [빛나는 특별함!] ✨🌟"
    elif grade == "EPIC":
        effect = "💜 [보라색 마녀의 눈빛!] 💜"
    else:
        effect = "🍪"
        
    return f"{effect} **{cookie_name}** ({grade})"

# 3. Streamlit Secrets에서 API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 4. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "당신은 '쿠키런 킹덤 뽑기 연구소'의 대리인, '용감한 쿠키'입니다. "
                "말투는 밝고, 활기차며, '쿠키', '설탕노움' 같은 쿠키런 세계관 단어를 자주 씁니다. "
                "사용자가 쿠키 추천을 달라고 하거나 조합을 물어보면 친절하게 답해주세요. "
                "만약 사용자가 '뽑기'나 '가챠'를 요청하면, 시스템이 뽑기 결과를 먼저 보여줄 테니 "
                "당신은 그 결과(예: 에인션트 쿠키 당첨 등)를 보고 엄청나게 축하해주거나 아쉬워하는 리액션을 해주면 됩니다."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"🤖 모델 초기화 오류: {e}")
        st.stop()

# 5. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 가챠 시스템 작동
if user_input := st.chat_input("용쿠에게 말을 걸거나 '10연뽑 해줘!'라고 해보세요!"):
    
    # 사용자 입력 화면 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 뽑기 명령어 감지 및 가챠 처리
    gacha_result_text = ""
    if any(keyword in user_input for keyword in ["뽑기", "가챠", "단뽑", "연뽑", "10회"]):
        # 10회 뽑기인지 1회 뽑기인지 판별
        count = 10 if "10" in user_input else 1
        
        results = [draw_cookie() for _ in range(count)]
        gacha_result_text = f"### 🔮 오븐이 뜨거워집니다...! ({count}회 뽑기 결과)\n"
        for i, res in enumerate(results, 1):
            gacha_result_text += f"{i}. {res}\n"
        
        # 뽑기 결과를 대화창에 즉시 띄우기
        with st.chat_message("assistant"):
            st.markdown(gacha_result_text)
        st.session_state.messages.append({"role": "assistant", "content": gacha_result_text})

    # AI 답변 생성 (Gemini-2.5-flash-lite)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🍪 *쿠키 굽는 중...*")
        
        # 뽑기를 진행했다면 프롬프트에 결과를 알려주어 AI가 맞춤 리액션을 하도록 유도
        ai_prompt = user_input
        if gacha_result_text:
            ai_prompt += f"\n\n(참고: 시스템이 유저에게 다음과 같은 뽑기 결과를 전달했으니 이에 맞는 리액션을 하세요:\n{gacha_result_text})"
            
        try:
            response = st.session_state.chat_session.send_message(ai_prompt)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"⚠️ 설탕노움이 일하다가 실수를 대만했습니다! 오류: {e}"
            message_placeholder.markdown(error_msg)
