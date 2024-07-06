import streamlit as st
import random
import toml
import pathlib
from openai import OpenAI
import pandas as pd

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# 여러 API 키 값 가져오기
api_keys = [secrets.get(f"api_key{i}") for i in range(1, 13)]

# 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)

# 페르소나 특성 정의
persona_traits = ["집중력", "기기친숙도", "구두언어 사용 빈도", "과제집착력", "학업스트레스", "자기조절", "가정환경", "학업성취도", "메타인지"]
genders = ["boy", "girl"]

# Streamlit 앱 인터페이스 구성
st.title("하이터치 시뮬레이션 🎨")
st.write("학생의 페르소나가 무작위로 생성됩니다. AIDT 카드를 이용해 하이터치를 시도해보세요.")

# 게임방법 강조
st.markdown("""
<div style='border: 2px solid #f39c12; padding: 10px; border-radius: 5px;'>
    <h3>게임방법 🎮</h3>
    <ul>
        <li>👥 인원수: 2~6</li>
        <li>📦 준비물: AIDT카드, 종</li>
        <li>🃏 한 사람당 AIDT카드를 7장씩 받습니다.</li>
        <li>🔍 모둠 가운데에 디지털도구를 놓고, '어떤 학생이 나타날까요?' 버튼을 누릅니다.</li>
        <li>🕒 오른쪽 위의 RUNNING이 끝나면 그림과 함께 학생의 정보가 나타납니다.</li>
        <li>👀 학생의 정보를 보고 나의 AIDT 기능카드를 본 후 어떤 하이터치를 할 수 있을지 생각합니다.</li>
        <li>🔔 모둠 가운데 종을 치고 해당되는 AIDT 카드를 내려놓으며 하이터치 계획을 말합니다.</li>
        <li>👍 모둠원의 과반수가 하이터치 계획에 동의할 경우 자신의 AIDT 카드를 중앙의 카드덱에 버립니다.</li>
        <li>🏆 위 과정을 반복하여 자신의 카드덱이 모두 없어진 사람이 승리합니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("이 이미지생성도구의 사용 비용은 서울특별시교육청 AI 에듀테크 선도교사 운영비로 지출됩니다.")
st.markdown("제작자: 서울특별시교육청융합과학교육원 정용석, 함현초등학교 권혜영")


# 입력 값 검증 및 이미지 생성
if st.button("어떤 학생이 나타날까요?"):
    # 무작위로 3개의 페르소나 특성 선택
    selected_traits = random.sample(persona_traits, 3)
    selected_gauges = {trait: random.choice([1, 2, 3, 4, 5]) for trait in selected_traits}
    gender = random.choice(genders)

    # 프롬프트 구성
    trait_descriptions = ", ".join([f"{trait} {gauge} out of 5" for trait, gauge in selected_gauges.items()])
    prompt = f"Caricature of an elementary school {gender}, cartoon style, reflecting traits such as {trait_descriptions}. The image should not contain any text."

    # 컨테이너 생성
    container = st.container()

    with container:
        # DALL-E API 호출 시도
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url

            # 생성된 이미지 출력
            st.image(image_url, caption="생성된 학생 페르소나 이미지")

        except Exception as e:
            st.error(f"이미지 생성에 실패했습니다: {e}")

        # 선택된 페르소나 특성 및 게이지 시각화
        traits_df = pd.DataFrame(list(selected_gauges.items()), columns=['Trait', 'Gauge'])
        st.bar_chart(traits_df.set_index('Trait'))

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()

st.markdown("[AIDT 카드 다운로드(준비중)](https://drive.google.com/file/d/1F7_E5cXGg3W3j8o6nJHfT6aD3d0QYZfP/view?usp=sharing)")
