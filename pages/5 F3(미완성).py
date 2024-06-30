import streamlit as st
import pandas as pd
import random
import toml
import pathlib
import google.generativeai as genai

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
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

# 수업안 샘플
sample_lessons = [
    """1) AI 디지털교과서 기반 선수학습
진단평가 학생의 단원 출발점 진단
2) 분수 계산을 위해 원리 기반 방법의 이해 AI 디지털교과서 형성평가
3) 형성평가 결과 분석으로 성취수준 도달점 확인 AI 디지털교과서 제공 개인별 맞춤형 콘텐츠 해결 상황에서 디딤이 필요한 학습자에 대한 교사의 일대일 피드백
4) AI 디지털교과서 기반 성취도평가 일정 성취수준 도달 여부 확인
5) 도달 여부에 따른 맞춤형 수행 활동 제공 디딤 콘텐츠(느린 학습자) 및 도약 프로젝트 활동 제공 및 교사 평가/피드백
6) 단원평가 통한 배움 내용 확인""",
    
    """1) 우리 몸의 다양한 기관에 대한 주요 용어 확인 AI 챗봇 활용
2) 용어 이해하기 AI 디지털교과서 기반 인체 기관 내 주요 부분에 대한 조사 후 교사 피드백
3) 개념 공유하기 조사 내용 동료 학생과 공유하고 피드백 주고받기
4) 주제 정하기 AI 디지털교과서 데이터 기반 모둠 구성한 후 인체 기관 간 연관성이 드러나는 발표 자료 조직하고 교사 및 동료 피드백 받기
5) 발표 내용 구성하기 동영상으로 구성할 발표 내용 모둠별 구성하고 동료 피드백 주고받기
6) 발표하기 인체 내 두세 기관 간 연관성이 드러나는 인체 기관 발표하기 최종 평가""",

    """1) 한국 문화 관련 주제 선정 브레인스토밍하기 디딤 콘텐츠(느린 학습자) 및 도약 프로젝트 활동 제공 및 교사 평가/피드백
2) 세부 주제 관련 자료 조사하기 AI 챗봇 활용하기
3) 영어 대본 작성 후 피드백 받기 AI 디지털교과서로부터 쓰기 피드백 받기(영작)
4) 영어 말하기 발표 개별 연습하기 AI 디지털교과서로부터 말하기 피드백 받기(녹음 및 발음 교정, 개별 맞춤 학습 및 보충심화 과제 제시) 느린 학습자에 대한 교사 피드백
5) 영어 말하기 발표 모둠 연습하기 모둠원 피드백
6) 영어 말하기 발표하기 교사 평가 및 피드백""",

    """1) 주제 정하기 모둠원 협력 - AI 챗봇 활용하기
2) 대본 작성하기 교사가 제작한 챗봇 활용 혹은 AI 디지털교과서로부터 쓰기 피드백 받기
3) 대본 작성 후 피드백 받기 완성도가 높아 챗봇이 통과시킨 학생은 교사의 피드백 제공
4) 짝지어 발표 연습하기 짝에게 평가 받기(평가 기준을 근거로 감점 요인에 대한 동료 피드백)
5) 발표하기 교사의 채점 및 감점 요인에 대한 피드백 제공
6) 발표하기 재도전 최종 평가"""
]

# 앱 제목
st.title("수업안 평가 체크리스트")

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
            prompt = (
                f"수업안:\n{st.session_state.selected_lesson}\n\n"
                "체크리스트 평가 결과:\n" +
                "\n".join([f"{item}: {response}" for item, response in checklist_responses.items()]) +
                "\n\n수업안에 대해 교사가 체크리스트로 평가한 결과입니다. 체크리스트는 1점부터 5점까지 이루어져 있으며, 1점의 낮은 점수입니다. "
                "교사가 평가를 결과를 수업안과 비교하여 비판적으로 검토하여 인공지능으로 검토해주세요. 교사가 준 점수가 옳지 않다고 여기면 점검해 주고 이유를 꼭 이야기해 주세요."
            )
            model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                          generation_config={
                                              "temperature": 0.7,
                                              "max_output_tokens": 3000,
                                          })
            try:
                response = model.generate_content([prompt])
                ai_feedback = response.text
            except Exception as e:
                st.error(f"API 호출 실패: {e}")
                ai_feedback = "생성 실패"

            st.text_area("AI 검토 피드백", ai_feedback, height=300)

        if st.button("결과 분석"):
            avg_score = sum(checklist_responses.values()) / len(checklist_responses)
            st.write(f"평균 점수: {avg_score:.2f}")

        if st.button("다시 시작하기", key="restart"):
            st.session_state.clear()
            st.experimental_rerun()
    else:
        st.warning("모든 체크리스트 항목을 선택해야 합니다.")
else:
    st.write("랜덤 뽑기를 눌러 수업안을 선택하세요.")
