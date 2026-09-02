import streamlit as st

st.set_page_config(page_title="나의 데이터 포트폴리오", page_icon="📚", layout="wide")

st.title("나의 데이터 포트폴리오")

st.markdown(
    """
    ### 👋 환영합니다!
    이 앱은 다양한 데이터를 분석하고 시각화한 결과를 모아둔 포트폴리오입니다.
    왼쪽 사이드바에서 원하는 페이지를 선택해 이동해보세요.
    """
)

st.divider()

st.markdown("### 📂 페이지 안내")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### 🌡️ 기온 분석
        기온 데이터를 활용한 분석 결과를 확인할 수 있습니다.
        """
    )
    st.markdown(
        """
        #### 📊 그래프 도감 1
        영화 데이터의 기본적인 특징(비교와 순위 등)을 그래프로 살펴봅니다.
        """
    )

with col2:
    st.markdown(
        """
        #### 🎬 어제의 박스오피스
        최신 박스오피스 순위 데이터를 확인할 수 있습니다.
        """
    )
    st.markdown(
        """
        #### 📈 그래프 도감 2
        영화 데이터의 분포와 관계(도넛, 트리맵, 히스토그램, 산점도, 박스플롯, 버블, 선버스트)를 그래프로 탐구합니다.
        """
    )

st.divider()
st.info("왼쪽 사이드바의 메뉴를 클릭하여 각 페이지로 이동해보세요! 👈")
