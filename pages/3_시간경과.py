import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# [기본] 시계 그리기 함수 (앞선 코드와 동일, 12시간제 기준)
def draw_passed_clock(h, m):
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    clock_face = plt.Circle((0, 0), 1.0, color="#FAFAFA", fill=True, ec="#34495E", lw=5)
    ax.add_patch(clock_face)
    
    for i in range(1, 13):
        angle = np.pi / 2 - i * (np.pi / 6)
        ax.text(0.8 * np.cos(angle), 0.8 * np.sin(angle), str(i), 
                fontsize=16, fontweight='bold', ha='center', va='center')
        
    for i in range(60):
        angle = i * (np.pi / 30)
        is_five = (i % 5 == 0)
        ax.plot([(1 - (0.07 if is_five else 0.03)) * np.cos(angle), 1 * np.cos(angle)],
                [(1 - (0.07 if is_five else 0.03)) * np.sin(angle), 1 * np.sin(angle)], 
                color="#2C3E50" if is_five else "#BDC3C7", linewidth=2 if is_five else 1)

    # 바늘 각도 계산
    min_angle = np.pi / 2 - m * (np.pi / 30)
    hour_angle = np.pi / 2 - (h % 12 + m / 60.0) * (np.pi / 6)
    
    ax.plot([0, 0.45 * np.cos(hour_angle)], [0, 0.45 * np.sin(hour_angle)], color="#E74C3C", linewidth=8, solid_capstyle='round')
    ax.plot([0, 0.75 * np.cos(min_angle)], [0, 0.75 * np.sin(min_angle)], color="#3498DB", linewidth=4, solid_capstyle='round')
    ax.add_patch(plt.Circle((0, 0), 0.04, color="#2C3E50", fill=True, zorder=4))
    
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.axis('off'); ax.set_aspect('equal')
    return fig


# -----------------------------------------------------------------
# 시간 경과 시뮬레이터 UI 및 로직 (기존 페이지 내 삽입 영역)
# -----------------------------------------------------------------
st.title("⏳ 시간이 흘러가면 몇 시가 될까요?")
st.write("기준 시간과 경과 시간을 선택하면 변해버린 시계를 보여줍니다.")

# 1. 기준 시간 입력 (오전/오후 구분을 위해 24시간제 입력 혹은 기본 datetime 객체 활용)
st.subheader("1️⃣ 처음 시각을 정해봐요")
col_base_h, col_base_m = st.columns(2)
with col_base_h:
    base_h = st.number_input("시 (0~23시)", min_value=0, max_value=23, value=10, key="base_hour")
with col_base_m:
    base_m = st.number_input("분 (0~59분)", min_value=0, max_value=59, value=0, key="base_minute")

# datetime 객체 생성 (연도/날짜는 고정하고 시/분만 임의 세팅)
base_time = datetime(2026, 1, 1, base_h, base_m)


# 2. 경과 시간 설정 (더할지 뺄지 선택 및 수량 지정)
st.subheader("2️⃣ 얼마나 시간이 흘렀나요?")
col_dir, col_delta_h, col_delta_m = st.columns([1, 1, 1])

with col_dir:
    direction = st.selectbox("방향", ["후 (시간이 더해져요)", "전 (시간이 되돌아가요)"], key="time_direction")

with col_delta_h:
    delta_hours = st.number_input("몇 시간?", min_value=0, max_value=24, value=1, step=1, key="delta_h")

with col_delta_m:
    delta_minutes = st.number_input("몇 분?", min_value=0, max_value=120, value=30, step=5, key="delta_m")

# 3. 시간 계산 로직 수행 (timedelta 활용)
time_offset = timedelta(hours=delta_hours, minutes=delta_minutes)

if "후" in direction:
    final_time = base_time + time_offset
    text_action = f"**{delta_hours}시간 {delta_minutes}분 후**"
else:
    final_time = base_time - time_offset
    text_action = f"**{delta_hours}시간 {delta_minutes}분 전**"


# 4. 결과 출력 (두 시계 나란히 배치하기)
st.subheader("3️⃣ 변화된 시계 확인하기")
col_clock1, col_clock2 = st.columns(2)

with col_clock1:
    st.markdown(f"#### 🎬 처음 시각: {base_time.strftime('%H:%M')}")
    fig_base = draw_passed_clock(base_time.hour, base_time.minute)
    st.pyplot(fig_base)

with col_clock2:
    st.markdown(f"#### 🏁 {text_action}의 시각: {final_time.strftime('%H:%M')}")
    fig_final = draw_passed_clock(final_time.hour, final_time.minute)
    st.pyplot(fig_final)

# 초등학생용 친절한 텍스트 가이드 마무리
final_ampm = "오후" if final_time.hour >= 12 else "오전"
final_h_12 = final_time.hour % 12
final_h_12 = 12 if final_h_12 == 0 else final_h_12

st.success(f"📢 처음 시각에서 {text_action}이 지나면 시계는 **[{final_ampm} {final_h_12}시 {final_time.minute}분]** 을 가리키게 됩니다!")