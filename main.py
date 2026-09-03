import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(page_title="그래프 도감 2 - 분포와 관계", page_icon="📈", layout="wide")
st.title("📈 영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
    이 페이지는 1년간 박스오피스 10위권에 든 영화 216편의 데이터를 활용하여
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

# =========================================================
# 그래프 1: 장르별 영화 편수 도넛 그래프
# =========================================================
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

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# =========================================================
# 그래프 2: 장르 > 영화 트리맵 (칸 크기 = 총 관객)
# =========================================================
st.header("2. 장르별 영화 트리맵 (크기: 총 관객수)")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안에 속한 영화들의 총 관객수 트리맵"
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# =========================================================
# 그래프 3: 총 관객수 히스토그램
# =========================================================
st.header("3. 총 관객수 히스토그램")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객수 분포"
)

fig3.update_layout(
    xaxis_title="총 관객수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 많이 몰려있는 구간(최빈 구간) 계산
counts, bin_edges = pd.cut(df["total_audi"], bins=30, retbins=True)
most_common_bin = counts.value_counts().idxmax()

# 총 관객이 가장 많은 영화
top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    f"""
    대부분의 영화는 총 관객수 **{int(most_common_bin.left):,} ~ {int(most_common_bin.right):,}명** 구간에 몰려 있습니다.
    가장 총 관객이 많은 영화는 **'{top_movie_row['movieNm']}'**이며, 총 관객수는 **{int(top_movie_row['total_audi']):,}명**입니다.
    """
)

st.divider()

# =========================================================
# 그래프 4: 개봉일 스크린수 vs 총 관객수 산점도 (장르별 색상)
# =========================================================
st.header("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수 (장르별 색상 구분)"
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# =========================================================
# 그래프 5: 영화 10편 이상 장르의 총 관객수 박스플롯
# =========================================================
st.header("5. 장르별 총 관객수 분포 (박스플롯)")

genre_movie_counts = df["genre"].value_counts()
major_genres = genre_movie_counts[genre_movie_counts >= 10].index
df_major_genre = df[df["genre"].isin(major_genres)]

fig5 = px.box(
    df_major_genre,
    x="genre",
    y="total_audi",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상인 장르의 총 관객수 박스플롯"
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객수"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# =========================================================
# 그래프 6: 스크린수 vs 총 관객수 버블 그래프 (크기: 첫 주 관객수)
# =========================================================
st.header("6. 개봉일 스크린수와 총 관객수의 관계 (버블 그래프)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수 (크기: 첫 주 관객수)",
    size_max=40
)

fig6.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

# =========================================================
# 그래프 7: 국가 > 장르 선버스트 그래프 (크기: 영화 편수)
# =========================================================
st.header("7. 제작 국가별 장르 분포 (선버스트 그래프)")

df_count = df.groupby(["nation", "genre"]).size().reset_index(name="count")

fig7 = px.sunburst(
    df_count,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 안에 속한 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 학생이 직접 그래프를 보고 알게 된 점을 한 문장으로 적어보세요.")

st.divider()

st.divider()

# =========================================================
# 그래프 8: 제작 국가별 평균 관객수 막대그래프
# =========================================================
st.header("8. 제작 국가별 평균 관객수")

nation_audi = (
    df.groupby("nation")
    .agg(total_audi_mean=("total_audi", "mean"), movie_count=("movieNm", "count"))
    .reset_index()
    .sort_values("total_audi_mean", ascending=False)
)

fig8 = px.bar(
    nation_audi,
    x="nation",
    y="total_audi_mean",
    hover_data={"movie_count": True, "total_audi_mean": ":,.0f"},
    title="제작 국가별 평균 관객수"
)

fig8.update_layout(
    xaxis_title="제작 국가",
    yaxis_title="평균 관객수"
)

fig8.update_traces(
    hovertemplate="<b>%{x}</b><br>평균 관객수: %{y:,.0f}명<br>영화 편수: %{customdata[0]}편<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True)

top_nation_row = nation_audi.iloc[0]

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    f"""
    제작 국가 중 평균 관객수가 가장 많은 나라는 **{top_nation_row['nation']}**이며,
    이 국가 영화의 평균 관객수는 **{int(top_nation_row['total_audi_mean']):,}명**입니다.
    (해당 국가의 영화 편수: {int(top_nation_row['movie_count'])}편)
    """
)
