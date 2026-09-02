import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
    이 앱은 1년간 박스오피스 10위권에 든 영화 216편의 데이터를 활용하여
    다양한 그래프로 데이터의 **분포와 관계**를 탐구합니다.
    """
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # genre 열에 세로막대(|)로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    # 개봉일(openDt)을 날짜 형식으로 변환 (여덟 자리 숫자 -> YYYY-MM-DD)
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    return df

df = load_data()

# -----------------------------
# 원본 데이터 미리보기
# -----------------------------
with st.expander("원본 데이터 미리보기"):
    st.dataframe(df)

st.divider()

# -----------------------------
# 그래프 1: 장르별 영화 편수 도넛 그래프
# -----------------------------
st.header("1. 장르별 영화 편수 (도넛 그래프)")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
    title="장르별 영화 편수 분포"
)

# 마우스를 올리면 편수와 비율이 함께 보이도록 설정
fig1.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# -----------------------------
# (추가 그래프를 위한 구역 예시)
# -----------------------------
st.header("2. 추가 그래프 영역 (자유롭게 확장해보세요)")
st.write("이 아래에 다른 그래프(예: 국가별 분포, 스크린수와 관객수의 관계 등)를 추가해볼 수 있습니다.")

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")
