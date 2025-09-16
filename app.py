import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="토지이용 색상 검색기", page_icon="🎨", layout="wide")

# 엑셀 불러오기
df = pd.read_excel("landuse_colors.xlsx")

# 공백 제거
df.columns = df.columns.str.strip()

# RGB → HEX 변환
def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

df["HEX"] = df.apply(lambda row: rgb_to_hex(row["R"], row["G"], row["B"]), axis=1)

# 이미지 경로 추가 (CAD 코드 기준)
def find_img(code):
    path = f"images/{code}.png"
    return path if os.path.exists(path) else None

df["이미지"] = df["CAD 색상번호"].apply(find_img)

st.title("🎨 토지이용 색상 검색기")
st.write("토지이용 구분을 입력하면 CAD 코드, 색상 코드, 예시 이미지를 알려드립니다.")

# 검색창
query = st.text_input("토지이용 구분 입력 (예: 제1종전용주거지역, 중심상업지역 등):")

if query:
    row = df[df["토지이용 구분"].str.contains(re.escape(query), case=False, na=False)]
    if not row.empty:
        item = row.iloc[0]
        st.success(f"✅ {item['토지이용 구분']} → CAD 코드: {item['CAD 색상번호']} / HEX {item['HEX']}")

        # 색상 박스
        st.markdown(
            f"""
            <div style='width:200px; height:100px;
                        border-radius:10px; border:1px solid #000;
                        background-color:{item['HEX']};'>
            </div>
            """,
            unsafe_allow_html=True
        )

        # PDF 예시 이미지
        if item["이미지"]:
            st.image(item["이미지"], caption=f"{item['토지이용 구분']} 예시", width=150)
    else:
        st.error("❌ 해당 구분을 찾을 수 없습니다. (landuse_colors.xlsx를 확인하세요)")

# 📋 전체 표
st.subheader("📋 토지이용 전체 색상표")

for _, row in df.iterrows():
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <div style="width:200px;"><b>{row['토지이용 구분']}</b></div>
            <div style="width:100px;">CAD {row['CAD 색상번호']}</div>
            <div style="width:100px;">{row['HEX']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if row["이미지"]:
        st.image(row["이미지"], width=80)
    st.markdown("---")
