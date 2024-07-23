import streamlit as st
import pandas as pd
import random
import toml
import pathlib
import google.generativeai as genai

# GitHub 아이콘 및 기타 UI 요소 숨기기
hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

# secrets.toml 파일 경로 설정 및 파일 읽기
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"
with open(secrets_path, "r", encoding="utf-8") as f:
    secrets = toml.load(f)

# 여러 API 키 값 가져오기
api_keys = [secrets.get(f"gemini_api_key{i}") for i in range(1, 13) if secrets.get(f"gemini_api_key{i}")]

# 인공지능 설정
selected_api_key = api_keys[0]
genai.configure(api_key=selected_api_key)

# 체크리스트 항목 구조화
checklist = {
    "삶과 맥락 & 수업 및 학습자 분석": [
        "학생의 삶과 연계한 학습내용을 평가하도록 설계되었는가?",
        "학습 과정 중 핵심 역량을 평가하고 있는가?",
        "평가가 실생활의 맥락과 연계되거나 적용될 수 있도록 설계되었는가?",
        "학생의 사전 지식 분석을 위한 평가가 설계되었는가?"
    ],
    "맞춤형 & 성찰 기회 제공": [
        "개인별 학습 수준에 맞는 맞춤형 평가 문항을 설계하였는가?",
        "개인 학습 과정별 맞춤형 평가 문항을 설계하였는가?",
        "융합적 사고와 창의적 문제해결력이 요구되는 평가인가?",
        "학생 개별 평가를 통한 맞춤형 피드백이 제공되는가?"
    ],
    "지식 구성 & 상호작용 협력": [
        "학생의 상호작용이 이루어지는 평가 문항을 설계하였는가?",
        "평가를 통해 협력을 위한 개별 학력 향상도가 나타나는가?",
        "학생이 능동적으로 참여하며 협력이 이루어지는 평가인가?",
        "학생 협력 활동을 돕는 맞춤형 피드백이 제공되는가?"
    ]
}

# 수업안 샘플 데이터
sample_lessons = [
    """1) AI 디지털교과서 기반 선수학습
진단평가 학생의 단원 출발점 진단
2) 분수 계산을 위해 원리 기반 방법의 이해 AI 디지털교과서 형성평가
3) 형성평가 결과 분석으로 성취수준 도달점 확인 AI 디지털교과서 제공 개인별 맞춤형 콘텐츠 해결 상황에서 디딤이 필요한 학습자에 대한 교사의 일대일 피드백
4) AI 디지털교과서 기반 성취도평가 일정 성취수준 도달 여부 확인
5) 도달 여부에 따른 맞춤형 수행 활동 제공 디딤 콘텐츠(느린 학습자) 및 도약 프로젝트 활동 제공 및 교사 평가/피드백
6) 단원평가 통한 배움 내용 확인""",
    # 추가 수업안 생략...
]

# 앱 제목
st.title("개별 및 협력학습 설계 시 과정중심평가와 성찰계획 수립을 위한 체크리스트")

# 주의 문구
st.warning("""
⚠️ **주의:** 본 페이지는 개인의 API 키를 사용하고 있으므로 API 한도 초과에 따라 작동이 일정 기간 멈출 수 있습니다.
계속 사용을 원하시는 분은 [F3 (API 입력) 페이지](https://aidt-seondo-2nd.streamlit.app/F3_(API%EC%9E%85%EB%A0%A5)_(%EB%AF%B8%EC%99%84%EC%84%B1))를 참고해주세요.
""")

# 수업안 랜덤 선택 버튼
if st.button("랜덤 뽑기"):
    selected_lesson = random.choice(sample_lessons)
    st.session_state.selected_lesson = selected_lesson

# 선택된 수업안 표시
if "selected_lesson" in st.session_state:
    st.header("평가할 수업안")
    st.write(st.session_state.selected_lesson)

    # 체크리스트 생성
    st.header("체크리스트")
    checklist_responses = {}

    for category, items in checklist.items():
        st.subheader(category)
        for item in items:
            checklist_responses[item] = st.slider(item, 1, 5)

    # 모든 체크리스트 항목을 선택하지 않으면 다음 단계로 진행할 수 없음
    if all(value > 0 for value in checklist_responses.values()):
        if st.button("결과 저장"):
            results_df = pd.DataFrame.from_dict(checklist_responses, orient='index', columns=['평가'])
            st.write("평가 결과:")
            st.dataframe(results_df)
            st.success("평가 결과가 저장되었습니다.")

        if st.button("AI 검토"):
            with st.spinner("AI 검토 중입니다. 잠시만 기다려주세요..."):
                prompt = (
                    f"수업안:\n{st.session_state.selected_lesson}\n\n"
                    "체크리스트 평가 결과:\n" +
                    "\n".join([f"{item}: {response}" for item, response in checklist_responses.items()]) +
                    "\n\n확정된 수업안에 대해 교사가 체크리스트로 평가한 결과입니다. 각 체크리스트는 1점부터 5점까지 이루어져 있으며, 1점은 가장 낮은 점수입니다. "
                    "교사가 실시한 평가 결과를 수업안과 비교하여 비판적으로 인공지능으로 검토해주세요. 교사가 준 점수가 옳지 않다고 여기면 점검해 주고 이유를 꼭 이야기해 주세요. 예를 들어 낮은 점수를 주었는데, 수업안에 반영되어 있는 항목이라면 어느 부분을 살펴본 후 교사가 부여한 점수를 수정하라고 말해주세요."
                )
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 3000,
                    }
                )
                try:
                    response = model.generate_content([prompt])
                    ai_feedback = response.text
                except Exception as e:
                    st.error(f"API 호출 실패: {e}")
                    ai_feedback = "생성 실패"

                st.text_area("AI 검토 피드백", ai_feedback, height=300)

        if st.button("다시 시작하기", key="restart"):
            st.session_state.clear()
            st.experimental_rerun()
    else:
        st.warning("모든 체크리스트 항목을 선택해야 합니다.")
else:
    st.write("랜덤 뽑기를 눌러 수업안을 선택하세요.")
