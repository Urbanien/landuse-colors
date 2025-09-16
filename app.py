import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="토지이용 색상 검색기", page_icon="🎨", layout="wide")

# 엑셀 불러오기
df = pd.read_excel("landuse_colors.xlsx")

st.title("🎨 토지이용 색상 검색기")
st.write("토지이용 구분을 입력하면 CAD 코드, RGB, HEX, 예시 이미지를 보여줍니다.")

# 검색창
query = st.text_input("토지이용 구분 입력 (예: 제1종전용주거지역, 단독주택, 중심상업지역 등):").strip()

if query:
    # 부분 일치 검색 (대소문자 무시)
    results = df[df["토지이용 구분"].str.contains(re.escape(query), case=False, na=False)]

    if not results.empty:
        st.success(f"🔍 검색 결과: {len(results)}건")

        for _, item in results.iterrows():
            st.markdown(
                f"""
                **{item['토지이용 구분']}**  
                CAD 코드: {item['CAD 색상번호']}  
                RGB: ({item['R']}, {item['G']}, {item['B']})  
                HEX: {item['HEX']}  
                """
            )
        # 색상 박스 미리보기
        if pd.notna(item["HEX"]):
            st.markdown(
                f"""
                <div style='width:200px; height:100px;
                            border-radius:10px; border:1px solid #000;
                            background-color:{item["HEX"]};'>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 이미지 표시
        if pd.notna(item["이미지 경로"]) and os.path.exists(item["이미지 경로"]):
            st.image(item["이미지 경로"], caption=f"{item['토지이용 구분']} 예시", width=200)
        else:
            st.info("이미지 파일이 없습니다. (images/ 폴더 확인)")

    else:
        st.error("❌ 해당 구분을 찾을 수 없습니다.")

# 전체 표 + 이미지
st.subheader("📋 토지이용 전체 색상표")

for _, row in df.iterrows():
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <div style="width:220px;"><b>{row['토지이용 구분']}</b></div>
            <div style="width:100px;">CAD {row['CAD 색상번호']}</div>
            <div style="width:120px;">{row['HEX']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if pd.notna(row["이미지 경로"]) and os.path.exists(row["이미지 경로"]):
        st.image(row["이미지 경로"], width=100)
    st.markdown("---")
