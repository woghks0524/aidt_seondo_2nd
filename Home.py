import streamlit as st

# 페이지 제목 설정
st.set_page_config(page_title="교실혁명선도교사 2차연수 보조도구")

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

# 홈 페이지 제목 및 설명
st.title("교실혁명선도교사 2차연수 보조도구")
st.write("🔍 이 도구는 교실혁명 선도교사 2차 연수를 보조하기 위해 설계되었습니다. 아래 링크를 클릭하여 A3 페이지로 이동하세요.")

# A3 페이지로 이동하는 링크
st.markdown("[👉 A3: 교사 주도성 성찰 피드백 시스템으로 이동하기](https://aidt-seondo-2nd.streamlit.app/A3)")

# G3 페이지로 이동하는 링크
st.markdown("[👉 G3: 연구계획서 작성도우미로 이동하기](https://aidt-seondo-2nd.streamlit.app/G3)")

# F3 페이지로 이동하는 링크
st.markdown("[👉 F3: 개별 및 협력학습 설계 시 과정중심평가와 성찰계획 수립을 위한 체크리스트로 이동하기](https://aidt-seondo-2nd.streamlit.app/F3)")

# 2차 집합연수 수업자료 제작 요청 및 문의
st.write("📧 교실혁명선도교사 2차 본연수 수업자료 제작 요청 및 문의:")
st.write("서울특별시융합과학교육원 교사 정용석 [forinnocen@naver.com](mailto:forinnocen@naver.com)")

# API 관련 안내 문구
st.write("""
💡 연수 시 접속자 폭주로 API의 한도량이 초과되어 페이지가 정지될 수 있습니다. 각 사용자가 직접 API를 발급받아 사용하시길 적극 권장합니다. [AI Studio](https://aistudio.google.com/app/apikey)
""")
