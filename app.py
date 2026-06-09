import streamlit as st
import google.generativeai as genai
import random

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="팩맨 고스트 연구소", page_icon="🕹️", layout="centered")

st.title("🕹️ 팩맨(Pac-Man) 텍스트 레트로 챗봇")
st.caption("왁자지껄한 오락실 감성! 유령들을 피해 쿠키를 먹고 최고 점수에 도전하세요.")

# 2. 팩맨 미니 게임 로직 (세션 상태 활용)
if "score" not in st.session_state:
    st.session_state.score = 0
if "pacman_pos" not in st.session_state:
    st.session_state.pacman_pos = [1, 1]  # [y, x]
if "ghost_pos" not in st.session_state:
    st.session_state.ghost_pos = [3, 3]

# 간단한 5x5 미로 데이터 (0: 빈칸, 1: 벽, 2: 쿠키)
# 초기 미로 상태 세션 저장
if "grid" not in st.session_state:
    st.session_state.grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 2, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 2, 0, 1],
        [1, 1, 1, 1, 1]
    ]

def move_pacman(direction):
    """팩맨을 상하좌우로 이동시키고 이벤트를 처리하는 함수"""
    y, x = st.session_state.pacman_pos
    if direction == "위": y -= 1
    elif direction == "아래": y += 1
    elif direction == "왼쪽": x -= 1
    elif direction == "오른쪽": x += 1
    
    # 벽 체크
    if st.session_state.grid[y][x] == 1:
        return "🧱 쾅! 벽에 부딪혔습니다. 이동할 수 없습니다."
    
    # 위치 업데이트
    st.session_state.pacman_pos = [y, x]
    
    # 쿠키 먹기 체크
    event_msg = ""
    if st.session_state.grid[y][x] == 2:
        st.session_state.score += 10
        st.session_state.grid[y][x] = 0
        event_msg = "🍬 냠냠! 쿠키를 먹어 10점을 획득했습니다!\n"
        
    # 유령 AI 임의 이동
    gy, gx = st.session_state.ghost_pos
    st.session_state.ghost_pos = [random.randint(1, 3), random.randint(1, 3)]
    
    # 유령과 충돌 체크
    if st.session_state.pacman_pos == st.session_state.ghost_pos:
        st.session_state.score = max(0, st.session_state.score - 20)
        event_msg += "💀 으악! 유령(Blinky)과 마주쳤습니다! 점수가 20점 감점됩니다. (재배치 중)"
        st.session_state.ghost_pos = [3, 3]
        
    return event_msg

def render_map():
    """현재 미로 상태를 이모지 텍스트로 그리는 함수"""
    map_str = "```\n"
    for y in range(5):
        for x in range(5):
            if [y, x] == st.session_state.pacman_pos:
                map_str += "🍕 "  # 팩맨
            elif [y, x] == st.session_state.ghost_pos:
                map_str += "👻 "  # 유령
            elif st.session_state.grid[y][x] == 1:
                map_str += "🧱 "  # 벽
            elif st.session_state.grid[y][x] == 2:
                map_str += "· "   # 쿠키
            else:
                map_str += "   "  # 빈공간
        map_str += "\n"
    map_str += "
```"
    return map_str

# 3. Streamlit Secrets에서 API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 4. 채팅 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "당신은 고전 게임 '팩맨' 세계관의 안내 AI이자 오락실 주인입니다. "
                "말투는 레트로 감성이 넘치며, 8비트 사운드 효과음('와카와카', '삐비빅')을 추임새로 자주 씁니다. "
                "사용자가 '위', '아래', '왼쪽', '오른쪽'을 입력하여 미니게임을 진행하면 시스템이 맵과 이벤트를 출력합니다. "
                "당신은 그 미니게임 진행 상황(점수 획득, 유령 조우 등)에 맞춰 플레이어를 응원하거나 유령을 조심하라고 훈수를 두는 리액션을 하세요. "
                "게임 외의 일반적인 질문이나 팩맨 역사에 대해 물어봐도 재치 있게 대답해 줍니다."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"🤖 모델 초기화 오류: {e}")
        st.stop()

# 5. 화면 사이드바에 현재 게임 스코어 및 맵 상시 표시
with st.sidebar:
    st.header("🕹️ 아케이드 상태창")
    st.metric(label="현재 스코어", value=f"{st.session_state.score} 점")
    st.markdown("### 🗺️ 미니 미로 상황판")
    st.markdown(render_map())
    st.caption("Tip: 채팅창에 '위', '아래', '왼쪽', '오른쪽'을 입력해 이동해 보세요!")

# 6. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. 사용자 입력 및 게임 이벤트 처리
if user_input := st.chat_input("팩맨에게 말을 걸거나 '오른쪽', '위'를 입력해 이동해보세요!"):
    
    # 사용자 입력 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 게임 이동 키워드 감지
    game_event_text = ""
    clean_input = user_input.strip()
    if clean_input in ["위", "아래", "왼쪽", "오른쪽"]:
        game_event_text = move_pacman(clean_input)
        
        # 이동 결과 및 업데이트된 맵을 대화창에 바로 출력
        game_display = f"🏃‍♂️ **팩맨이 '{clean_input}'으로 이동했습니다!**\n{game_event_text}\n\n{render_map()}"
        with st.chat_message("assistant"):
            st.markdown(game_display)
        st.session_state.messages.append({"role": "assistant", "content": game_display})
        st.rerun() # 사이드바 점수 실시간 갱신을 위한 새로고침

    # Gemini AI 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("👾 *와카와카... 신호 분석 중...*")
        
        # 미니게임 상태를 프롬프트 뒤에 몰래 붙여서 AI가 게임 현황을 완벽히 인지하도록 유도
        ai_prompt = user_input
        if game_event_text:
            ai_prompt += f"\n\n(참고: 유저가 방금 한 행동 결과입니다. 현재 점수는 {st.session_state.score}점입니다. 이 상황에 맞는 오락실 훈수 리액션을 한 줄 내외로 짧고 강렬하게 해주세요: {game_event_text})"
            
        try:
            response = st.session_state.chat_session.send_message(ai_prompt)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"⚠️ 오락실 기계에 동전이 걸렸습니다! 오류: {e}"
            message_placeholder.markdown(error_msg)
