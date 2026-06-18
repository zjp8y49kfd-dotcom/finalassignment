import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="초등 시계 사진관", page_icon="📸", layout="centered")
st.title("📸 찰칵! 맞춤형 시계 사진관")
st.write("알고 싶은 시간을 선택하면, 그 시간에 딱 맞는 시계 그림을 보여줍니다.")


# 2. 시간 입력 받기 (24시간 및 60분 단위)
st.subheader("⚙️ 확인하고 싶은 시간을 골라보세요")
col_input1, col_input2 = st.columns(2)

with col_input1:
    # 초등학생이 24시간제를 함께 배울 수 있도록 0~23시 설정
    input_hour = st.number_input("시 (0시 ~ 23시)", min_value=0, max_value=23, value=14, step=1)

with col_input2:
    input_minute = st.number_input("분 (0분 ~ 59분)", min_value=0, max_value=59, value=15, step=1)


# 3. 입력된 시간에 따른 오전/오후 및 12시간제 변환 노출
display_hour = input_hour % 12
if display_hour == 0:
    display_hour = 12

ampm = "오후 ☀️" if input_hour >= 12 else "오전 🌅"

st.info(f"💡 선택한 시간은 **[{ampm} {display_hour}시 {input_minute}분]** 입니다. (24시간제 표현: {input_hour:02d}:{input_minute:02d})")


# 4. 지정된 시간에 맞는 고정 시계 그림을 생성하는 함수
def generate_static_clock(h_24, m):
    # 12시간제 바늘 위치 계산용 변환
    h_12 = h_24 % 12
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 시계 판 배경 (둥근 원)
    clock_face = plt.Circle((0, 0), 1.0, color="#FAFAFA", fill=True, ec="#34495E", lw=5)
    ax.add_patch(clock_face)
    
    # 시계 숫자 배치 (1~12)
    for i in range(1, 13):
        angle = np.pi / 2 - i * (np.pi / 6)
        x, y = 0.8 * np.cos(angle), 0.8 * np.sin(angle)
        ax.text(x, y, str(i), fontsize=20, fontweight='bold', 
                ha='center', va='center', color='#2C3E50')
        
    # 눈금 그리기 (5분 단위와 1분 단위 구별)
    for i in range(60):
        angle = i * (np.pi / 30)
        is_five = (i % 5 == 0)
        length = 0.07 if is_five else 0.03
        width = 3 if is_five else 1
        color = "#2C3E50" if is_five else "#BDC3C7"
        
        x_start, y_start = (1 - length) * np.cos(angle), (1 - length) * np.sin(angle)
        x_end, y_end = 1 * np.cos(angle), 1 * np.sin(angle)
        ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=width)

    # 바늘 각도 계산 (시침은 분의 진행도에 따라 미세하게 움직임)
    min_angle = np.pi / 2 - m * (np.pi / 30)
    hour_angle = np.pi / 2 - (h_12 + m / 60.0) * (np.pi / 6)

    # 빨간색 짧은 시침
    ax.plot([0, 0.45 * np.cos(hour_angle)], [0, 0.45 * np.sin(hour_angle)], 
            color="#E74C3C", linewidth=9, solid_capstyle='round', zorder=3)
    
    # 파란색 긴 분침
    ax.plot([0, 0.75 * np.cos(min_angle)], [0, 0.75 * np.sin(min_angle)], 
            color="#3498DB", linewidth=5, solid_capstyle='round', zorder=2)
    
    # 가운데 중심 점
    center_dot = plt.Circle((0, 0), 0.04, color="#2C3E50", fill=True, zorder=4)
    ax.add_patch(center_dot)

    # 불필요한 그래프 외곽 축 숨기기
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis('off')
    ax.set_aspect('equal')
    
    return fig

# 5. 생성된 시계 사진 보여주기
st.markdown("### 🖼️ 완성된 시계 사진")
clock_picture = generate_static_clock(input_hour, input_minute)
st.pyplot(clock_picture)