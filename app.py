
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="제너 다이오드 양자터널링 시뮬레이터", layout="wide")

# 네 측정 데이터 (각도-전류)
current_data = {
    10:0,20:0.16,30:0.39,40:0.64,50:0.73,60:0.84,70:0.90,
    80:0.98,90:1.05,100:1.12,110:1.21,120:1.26,130:1.37,
    140:1.48,150:1.58,160:1.68,170:1.81,180:1.97,190:2.20,
    200:2.40,210:2.63,220:2.93,230:3.37,240:4.21,250:4.76,
    260:6.14,270:8.90,280:13.8,290:32.9,300:42.6
}

angles = list(current_data.keys())
currents = list(current_data.values())

st.title("🧪 제너 다이오드 양자터널링 간접 관측 시뮬레이터")

col1, col2 = st.columns([1,2])

with col1:
    angle = st.slider("🎚️ 가변저항 각도 (°)", 10, 300, 150, 10)
    current = current_data[angle]

    st.metric("⚡ 전류", f"{current:.2f} mA")

    if angle >= 280:
        st.error("🔴 Breakdown 영역! 전류가 급격히 증가합니다.")
    elif angle >= 250:
        st.warning("🟠 항복 영역에 접근 중")
    else:
        st.success("🟢 정상 영역")

    st.markdown(
        '''
        ### 🔌 실제 회로 연결
        - 9V 건전지 → 브레드보드 전원 레일
        - 가변저항(포텐셔미터) → 브레드보드 우측 연결
        - 제너 다이오드 + 저항 → 브레드보드 중앙
        - 멀티미터 → 직렬 연결하여 전류 측정
        '''
    )

with col2:
    df = pd.DataFrame({
        "각도(°)": angles,
        "전류(mA)": currents
    })

    fig = px.line(
        df,
        x="각도(°)",
        y="전류(mA)",
        markers=True,
        title="전류 변화 그래프"
    )

    fig.add_vrect(
        x0=280, x1=300,
        fillcolor="red", opacity=0.15,
        annotation_text="Breakdown"
    )

    fig.add_scatter(
        x=[angle],
        y=[current],
        mode="markers+text",
        text=[f"{angle}°\n{current:.2f} mA"],
        textposition="top center",
        marker=dict(size=15, color="red"),
        name="현재 위치"
    )

    st.plotly_chart(fig, use_container_width=True)

st.info(
    "💡 슬라이더를 움직이면 가변저항 각도에 따라 실제 측정한 전류 데이터가 실시간으로 변합니다."
)
