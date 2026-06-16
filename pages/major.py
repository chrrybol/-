import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="학과 찾기 나침반",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 학과 찾기 나침반")
st.subheader("좋아하는 과목으로 알아보는 학과 추천")

st.markdown("---")

subjects = [
    "국어",
    "영어",
    "수학",
    "과학",
    "사회",
    "역사",
    "정보",
    "미술",
    "음악",
    "체육"
]

major_data = {
    "컴퓨터공학과": {
        "subjects": ["수학", "과학", "정보"],
        "description": "소프트웨어와 컴퓨터 시스템을 공부합니다.",
        "fit": "논리적 사고와 문제 해결을 좋아하는 학생",
        "career": "개발자, AI 엔지니어, 데이터 분석가"
    },
    "소프트웨어학과": {
        "subjects": ["정보", "수학"],
        "description": "프로그래밍과 소프트웨어 개발을 배웁니다.",
        "fit": "코딩에 흥미가 있는 학생",
        "career": "앱 개발자, 웹 개발자"
    },
    "전자공학과": {
        "subjects": ["수학", "과학"],
        "description": "전자기기와 반도체 기술을 공부합니다.",
        "fit": "기술과 기계에 관심 있는 학생",
        "career": "반도체 엔지니어, 연구원"
    },
    "기계공학과": {
        "subjects": ["수학", "과학"],
        "description": "기계 설계와 제조 기술을 배웁니다.",
        "fit": "공학적 사고를 좋아하는 학생",
        "career": "기계 엔지니어"
    },
    "경영학과": {
        "subjects": ["사회", "수학"],
        "description": "기업 운영과 경영 전략을 공부합니다.",
        "fit": "기획과 리더십에 관심 있는 학생",
        "career": "경영인, 마케터"
    },
    "경제학과": {
        "subjects": ["수학", "사회"],
        "description": "경제 현상과 시장 구조를 분석합니다.",
        "fit": "분석을 좋아하는 학생",
        "career": "경제연구원, 금융 전문가"
    },
    "심리학과": {
        "subjects": ["사회", "국어"],
        "description": "인간의 마음과 행동을 연구합니다.",
        "fit": "사람에 관심이 많은 학생",
        "career": "상담사, 심리전문가"
    },
    "교육학과": {
        "subjects": ["국어", "사회"],
        "description": "교육 이론과 방법을 공부합니다.",
        "fit": "가르치는 것을 좋아하는 학생",
        "career": "교사, 교육연구원"
    },
    "간호학과": {
        "subjects": ["과학"],
        "description": "환자 간호와 건강관리를 배웁니다.",
        "fit": "배려심이 많은 학생",
        "career": "간호사"
    },
    "의예과": {
        "subjects": ["과학", "수학"],
        "description": "의학 공부를 위한 기초 과정을 배웁니다.",
        "fit": "생명과 건강에 관심 있는 학생",
        "career": "의사"
    },
    "생명과학과": {
        "subjects": ["과학"],
        "description": "생명 현상을 연구합니다.",
        "fit": "탐구를 좋아하는 학생",
        "career": "연구원"
    },
    "디자인학과": {
        "subjects": ["미술"],
        "description": "제품 및 시각 디자인을 공부합니다.",
        "fit": "창의적인 학생",
        "career": "디자이너"
    },
    "시각디자인학과": {
        "subjects": ["미술"],
        "description": "브랜드와 콘텐츠 디자인을 공부합니다.",
        "fit": "창작 활동을 좋아하는 학생",
        "career": "그래픽 디자이너"
    },
    "체육교육과": {
        "subjects": ["체육"],
        "description": "체육 교육 방법을 배웁니다.",
        "fit": "운동을 좋아하는 학생",
        "career": "체육교사"
    },
    "스포츠과학과": {
        "subjects": ["체육", "과학"],
        "description": "운동과 인체를 과학적으로 연구합니다.",
        "fit": "스포츠에 관심 있는 학생",
        "career": "운동처방사"
    },
    "국어국문학과": {
        "subjects": ["국어"],
        "description": "국어와 문학을 연구합니다.",
        "fit": "독서와 글쓰기를 좋아하는 학생",
        "career": "작가, 기자"
    },
    "영어영문학과": {
        "subjects": ["영어"],
        "description": "영어와 영미 문화를 공부합니다.",
        "fit": "외국어를 좋아하는 학생",
        "career": "통번역사"
    },
    "역사학과": {
        "subjects": ["역사", "사회"],
        "description": "역사와 문화를 연구합니다.",
        "fit": "과거 사건에 관심 있는 학생",
        "career": "연구원, 학예사"
    }
}

st.header("📚 좋아하는 과목 선택")

selected_subjects = st.multiselect(
    "흥미를 느끼는 과목을 선택하세요 (여러 개 선택 가능)",
    subjects
)

if st.button("🎯 학과 추천 받기"):

    try:
        if not selected_subjects:
            st.warning("과목을 1개 이상 선택해주세요.")
            st.stop()

        scores = {}

        for major, info in major_data.items():
            score = 0

            for subject in selected_subjects:
                if subject in info["subjects"]:
                    score += 10

            scores[major] = score

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top5 = ranked[:5]

        st.success("추천 결과가 나왔습니다!")

        st.subheader("🏆 추천 학과 TOP 5")

        for rank, (major, score) in enumerate(top5, start=1):
            st.markdown(
                f"### {rank}위. {major} ({score}점)"
            )

            st.write(f"**배우는 내용:** {major_data[major]['description']}")
            st.write(f"**잘 맞는 학생:** {major_data[major]['fit']}")
            st.write(f"**추천 진로:** {major_data[major]['career']}")

            st.markdown("---")

        chart_df = pd.DataFrame(
            top5,
            columns=["학과", "점수"]
        ).set_index("학과")

        st.subheader("📊 학과 적합도 그래프")
        st.bar_chart(chart_df)

    except Exception as e:
        st.error(f"오류가 발생했습니다.\n\n{e}")

st.markdown("---")
st.caption("※ 본 결과는 참고용 진로 탐색 자료입니다.")
