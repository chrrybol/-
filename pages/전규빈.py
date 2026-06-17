
import streamlit as st
from google import genai

st.set_page_config(page_title="진로 탐색 도우미", page_icon="🎯")

st.title("🎯 진로 탐색 도우미")

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

interest = st.multiselect(
    "관심 분야",
    ["과학", "기술", "예술", "음악", "디자인", "교육", "의료", "심리", "경영", "IT"]
)

activity = st.multiselect(
    "좋아하는 활동",
    ["문제 해결", "사람 돕기", "발표하기", "글쓰기", "코딩", "연구하기"]
)

strength = st.text_area("내 강점")

if st.button("진로 추천 받기"):

    if not interest and not activity and not strength.strip():
        st.warning("내용을 입력해주세요.")
    else:
        prompt = f"""
관심 분야: {', '.join(interest)}
좋아하는 활동: {', '.join(activity)}
강점: {strength}

학생에게 적합한 진로 3가지와 추천 이유,
관련 학과, 준비 방법을 알려주세요.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            result = response.text

            st.session_state.history.append(result)

            st.success("분석 완료!")
            st.markdown(result)

        except Exception as e:
            st.error("오류가 발생했습니다.")
            st.exception(e)

if st.session_state.history:
    st.subheader("이전 결과")
    for item in reversed(st.session_state.history):
        st.markdown(item)
