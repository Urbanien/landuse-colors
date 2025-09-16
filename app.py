import streamlit as st
import pandas as pd

# 엑셀 파일 불러오기 (같은 폴더에 landuse_colors.xlsx 저장되어 있어야 함)
df = pd.read_excel("landuse_colors.xlsx")

st.set_page_config(page_title="토지이용 색상 검색기", page_icon="🎨", layout="centered")

st.title("🎨 토지이용 색상 검색기")
st.write("토지이용 구분을 입력하면 CAD 코드와 색상 코드를 알려드립니다.")


# 컬럼명 앞뒤 공백 제거
df.columns = df.columns.str.strip()

# HEX 컬럼 추가
def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

df["HEX"] = df.apply(lambda row: rgb_to_hex(row["R"], row["G"], row["B"]), axis=1)

# 검색
query = st.text_input("토지이용 구분 입력 (예: 단독주택, 상업용지, 도로 등):")

if query:
    row = df[df["토지이용 구분"] == query]
    if not row.empty:
        code = row.iloc[0]["CAD 색상번호"]
        hex_code = row.iloc[0]["HEX"]
        st.success(f"✅ {query} → CAD 코드: {code} / HEX {hex_code}")


        # 색상 미리보기 박스
        st.markdown(
            f"""
            <div style='width:200px; height:100px; 
                        border-radius:10px; 
                        border:1px solid #000; 
                        background-color: {hex_code};'>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("❌ 해당 구분을 찾을 수 없습니다. (landuse_colors.xlsx를 확인하세요)")


# 📋 전체 표 (토지이용, CAD 색상번호, HEX만 보여주기)
st.subheader("📋 토지이용 전체 색상표")
st.dataframe(df[["토지이용 구분", "CAD 색상번호", "HEX"]], use_container_width=True)
