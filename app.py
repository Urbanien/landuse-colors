import streamlit as st
import pandas as pd

# 엑셀 파일 불러오기 (같은 폴더에 landuse_colors.xlsx 저장되어 있어야 함)
df = pd.read_excel("landuse_colors.xlsx")

st.set_page_config(page_title="토지이용 색상 검색기", page_icon="🎨", layout="centered")

st.title("🎨 토지이용 색상 검색기")
st.write("토지이용 구분을 입력하면 RGB 값, 색상 코드를 알려드립니다.")


# 검색 입력창
query = st.text_input("토지이용 구분 입력 (예: 단독주택, 상업용지, 도로 등):")

if query:
    row = df[df["토지이용 구분"] == query]
    if not row.empty:
     code = row.iloc[0]["CAD 색상번호"]     # CAD 코드 가져오기
        r, g, b = row.iloc[0][["R", "G", "B"]]

# RGB → HEX 변환
        hex_code = "#{:02X}{:02X}{:02X}".format(r, g, b)

# 결과 표시 (CAD 코드 + HEX)
        st.success(f"✅ {query} → CAD 코드: {code} / HEX {hex_code}")

# 색상 미리보기 박스 (HEX 코드 사용)
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
