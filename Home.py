import streamlit as st

# 페이지 제목 설정
st.set_page_config(page_title="교실혁명 선도교사 2차 연수 보조도구")

# 홈 페이지 제목 및 설명
st.title("교실혁명 선도교사 2차 연수 보조도구")
st.write("🔍 이 도구는 교실혁명 선도교사 2차 연수를 보조하기 위해 설계되었습니다. 아래 링크를 클릭하여 A3 페이지로 이동하세요.")

# A3 페이지로 이동하는 링크
st.markdown("[👉 A3: 교사 주도성 성찰 피드백 시스템으로 이동하기](https://aidt-seondo-2nd.streamlit.app/A3)")

# 2차 집합연수 수업자료 제작 요청 및 문의
st.write("📧 2차 집합연수 수업자료 제작 요청 및 문의: [forinnocen@naver.com](mailto:forinnocen@naver.com)")

# API 관련 안내 문구
st.write("""
💡 집합연수 시에는 [AI Studio](https://aistudio.google.com/app/)에서 직접 API 키를 받아서 사용할 예정입니다. 
이는 접속자 폭주로 인해 자체 API 사용 시 서버 과부하 문제를 방지하기 위함입니다.
""")
