import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import random

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 여러 API 키 값 가져오기
api_keys = [
    secrets.get("gemini_api_key1"),
    secrets.get("gemini_api_key2"),
    secrets.get("gemini_api_key3"),
    secrets.get("gemini_api_key4"),
    secrets.get("gemini_api_key5"),
    secrets.get("gemini_api_key6"),
    secrets.get("gemini_api_key7"),
    secrets.get("gemini_api_key8"),
    secrets.get("gemini_api_key9"),
    secrets.get("gemini_api_key10"),
    secrets.get("gemini_api_key11"),
    secrets.get("gemini_api_key12")
]

# 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
selected_api_key = random.choice(api_keys)

# few-shot 프롬프트 구성 함수
def try_generate_content(api_key, prompt_parts):
    # API 키를 설정
    genai.configure(api_key=api_key)
    
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("교사 주도성 성찰 피드백 시스템")
st.write("""
1. 아래의 질문에 답을 선택하세요.
2. 모든 질문에 답을 완료한 후 "피드백 생성하기" 버튼을 클릭하세요.
3. 인공지능이 여러분의 답변을 바탕으로 평가, 칭찬, 더 생각할 점을 작성해줍니다.
""")

# 학습 주제와 수업 개요 입력란
learning_topic = st.text_input("학습 주제를 입력해주세요:")
lesson_overview = st.text_area("수업 개요를 입력해주세요:")

# 객관식 질문 구성
activity_type = st.selectbox(
    "어떤 유형의 활동을 진행했습니까?",
    ["디지털 마인드맵 작성", "디지털 협력 프로젝트", "AI 기반 맞춤형 학습 경로 설계", "기타"]
)

if activity_type == "기타":
    activity_type_detail = st.text_input("활동 유형을 입력해주세요:")
else:
    activity_type_detail = activity_type

goal_achievement = st.selectbox(
    "활동 목표를 달성했습니까?",
    ["완전히 달성함", "대부분 달성함", "일부 달성함", "달성하지 못함"]
)

student_response = st.selectbox(
    "학생들의 반응은 어땠습니까?",
    ["매우 긍정적", "긍정적", "보통", "부정적"]
)

digital_tool_usage = st.selectbox(
    "디지털 도구를 어느 활동에 넣었습니까?",
    ["결과물 제작", "학생 평가", "수업 주요활동", "맞춤형 과제제시", "기타"]
)

if digital_tool_usage == "기타":
    digital_tool_usage_detail = st.text_input("디지털 도구 사용 활동을 입력해주세요:")
else:
    digital_tool_usage_detail = digital_tool_usage

activity_difficulty = st.selectbox(
    "활동을 진행하면서 어떤 어려움이 있었습니까?",
    ["디지털 도구 사용의 어려움", "학생들의 참여 부족", "기술적인 문제", "기타"]
)

if activity_difficulty == "기타":
    activity_difficulty_detail = st.text_input("어려움을 입력해주세요:")
else:
    activity_difficulty_detail = activity_difficulty

improvement_points = st.selectbox(
    "다음 번에 이 활동을 다시 한다면 어떤 점을 개선하고 싶습니까?",
    ["디지털 도구 활용 방법 개선", "학생 참여 유도 방법 개선", "기술 지원 강화", "기타"]
)

if improvement_points == "기타":
    improvement_points_detail = st.text_input("개선할 점을 입력해주세요:")
else:
    improvement_points_detail = improvement_points

# 주관식 질문
personal_reflection = st.text_area("이 활동을 통해 당신의 교육 철학이나 교수 방법에 어떤 변화가 있었습니까? (예시: 학생 중심 교육으로 전환, 디지털 도구 활용 증가 등)")

# 입력 값 검증 및 인공지능 호출
if st.button("피드백 생성하기"):
    if not all([learning_topic, lesson_overview, activity_type_detail, goal_achievement, student_response, digital_tool_usage_detail, activity_difficulty_detail, improvement_points_detail, personal_reflection]):
        st.warning("모든 질문에 답을 작성해주세요!")
    else:
        # 프롬프트 구성
        prompt = f"""
        다음은 교사가 수행한 교육 활동에 대한 설명과 성찰입니다. 이 설명과 성찰을 바탕으로 활동의 장점과 부족한 점을 평가하고, 개선할 수 있는 방법을 제안해주세요.

        학습 주제: {learning_topic}
        수업 개요: {lesson_overview}
        활동 유형: {activity_type_detail}
        활동 목표 달성 여부: {goal_achievement}
        학생들의 반응: {student_response}
        디지털 도구 사용 활동: {digital_tool_usage_detail}
        활동의 어려움: {activity_difficulty_detail}
        개선할 점: {improvement_points_detail}
        개인적 성찰: {personal_reflection}

        이 답변들을 바탕으로 교사에게 유용한 피드백을 제공해주세요.
        """

        # API 호출 시도
        response_text = try_generate_content(selected_api_key, prompt)
        
        # 첫 번째 API 키 실패 시, 다른 API 키로 재시도
        if response_text is None:
            for api_key in api_keys:
                if api_key != selected_api_key:
                    response_text = try_generate_content(api_key, prompt)
                    if response_text is not None:
                        break
        
        # 결과 출력
        if response_text is not None:
            st.success("피드백 생성 완료!")
            st.text_area("생성된 피드백:", value=response_text, height=300)
            combined_text = f"사용자 입력:\n\n학습 주제: {learning_topic}\n수업 개요: {lesson_overview}\n활동 유형: {activity_type_detail}\n활동 목표 달성 여부: {goal_achievement}\n학생들의 반응: {student_response}\n디지털 도구 사용 활동: {digital_tool_usage_detail}\n활동의 어려움: {activity_difficulty_detail}\n개선할 점: {improvement_points_detail}\n개인적 성찰: {personal_reflection}\n\n인공지능 피드백:\n\n{response_text}"
            st.download_button(label="피드백 다운로드", data=combined_text, file_name="generated_feedback.txt", mime="text/plain")
            st.write("인공지능이 생성한 피드백은 꼭 본인이 확인해야 합니다. 생성된 피드백을 검토하고, 필요한 경우 수정하세요.")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
