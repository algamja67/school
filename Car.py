import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("10_24_stt.csv", encoding='euc-kr')
    df.columns = df.columns.str.strip()  # 공백 제거
    df['연도'] = df['연도'].astype(str)  # 문자열로 변환
    return df

df_accident = load_data()

# -----------------------------
# HOME 화면
# -----------------------------
def show_home():
    st.header("🚗 전국 교통사고 데이터 분석")
    st.write("10_24_stt.csv 파일 기반의 시각화 웹앱입니다.")
    st.success("데이터 로드 완료!")
    st.subheader("📌 데이터 미리보기")
    st.dataframe(df_accident.head())

# -----------------------------
# 연도 + 컬럼 선택 분석
# -----------------------------
def show_custom_analysis():
    st.header("📊 연도 & 컬럼 선택 분석")

    # 연도 선택
    years = df_accident['연도'].unique()
    selected_year = st.selectbox("연도를 선택하세요", years)

    # 선택된 연도의 데이터 필터링
    filtered_df = df_accident[df_accident['연도'] == selected_year]

    st.info(f"선택한 연도: **{selected_year}년** 데이터 {len(filtered_df)}개")

    # 시각화 가능한 컬럼 목록 만들기
    numeric_cols = ['사고건수', '사고건수 구성비', '사망자수', 
                    '사망자수 구성비', '치사율', '부상자수', '부상자수 구성비']

    selected_col = st.selectbox("분석할 컬럼을 선택하세요", numeric_cols)

    st.subheader(f"📈 {selected_year}년 '{selected_col}' 그래프")

    fig = px.bar(
        filtered_df,
        x="대상사고 구분명",
        y=selected_col,
        title=f"{selected_year}년 {selected_col} 분석",
        labels={"대상사고 구분명": "사고 구분"}
    )
    st.plotly_chart(fig)

    st.subheader("📋 선택한 데이터 테이블")
    st.dataframe(filtered_df[['연도', '대상사고 구분명', selected_col]])

# -----------------------------
# 연도별 전체 분석
# -----------------------------
def show_yearly_total():
    st.header("📆 연도별 전체 사고 분석")

    yearly_data = df_accident.groupby("연도").agg({
        "사고건수": "sum",
        "사망자수": "sum",
        "부상자수": "sum"
    }).reset_index()

    st.dataframe(yearly_data)

    fig = px.line(
        yearly_data,
        x="연도",
        y=["사고건수", "사망자수", "부상자수"],
        title="연도별 사고/사망/부상 추이"
    )
    st.plotly_chart(fig)

# -----------------------------
# 메뉴 선택
# -----------------------------
menu = st.sidebar.selectbox(
    "메뉴를 선택하세요",
    ["HOME", "연도+컬럼 선택 분석", "연도별 전체 분석"]
)

if menu == "HOME":
    show_home()
elif menu == "연도+컬럼 선택 분석":
    show_custom_analysis()
elif menu == "연도별 전체 분석":
    show_yearly_total()
