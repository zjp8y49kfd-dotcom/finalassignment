import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# [필수 고정] 1. 시계를 그리는 고정 함수 (없으시다면 추가, 이미 있다면 기존 함수 사용)
def draw_quiz_clock(h, m):
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

    # 바늘 각도 계산 및 그리기 (시침은 분 연동)
    min_angle = np.pi / 2 - m * (np.pi / 30)
    hour_angle = np.pi / 2 - (h % 12 + m / 60.0) * (np.pi / 6)
    
    ax.plot([0, 0.45 * np.cos(hour_angle)], [0, 0.45 * np.sin(hour_angle)], color="#E74C3C", linewidth=8, solid_capstyle='round')
    ax.plot([0, 0.75 * np.cos(min_angle)], [0, 0.75 * np.sin(min_angle)], color="#3498DB", linewidth=4, solid_capstyle='round')
    ax.add_patch(plt.Circle((0, 0), 0.04, color="#2C3E50", fill=True, zorder=4))
    
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.axis('off'); ax.set_aspect('equal')
    return fig


# -----------------------------------------------------------------
# 여기서부터 퀴즈 페이지 내부(함수 또는 if문 내부)에 붙여넣으세요
# -----------------------------------------------------------------

# 2. 세션 상태를 이용해 랜덤 문제 고정 (새로고침 방지)
if "quiz_h" not in st.session_state:
    st.session_state.quiz_h = random.randint(1, 12)
    st.session_state.quiz_m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]) # 5분 단위

# 문제 출제용 함수
def reset_quiz():
    st.session_state.quiz_h = random.randint(1, 12)
    st.session_state.quiz_m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

# 3. 화면에 시계 모양 제시
st.subheader("🎯 이 시계는 몇 시 몇 분을 가리키고 있을까요?")
q_fig = draw_quiz_clock(st.session_state.quiz_h, st.session_state.quiz_m)
st.pyplot(q_fig)

# 4. 사용자 답안 입력 레이아웃
col_h, col_m = st.columns(2)
with col_h:
    user_h = st.number_input("시", min_value=1, max_value=12, value=1, step=1, key="ans_h")
with col_m:
    user_m = st.number_input("분", min_value=0, max_value=59, value=0, step=1, key="ans_m")

# 5. 정답 확인 및 오답 처리
if st.button("📢 정답 확인하기", type="primary"):
    if user_h == st.session_state.quiz_h and user_m == st.session_state.quiz_m:
        st.balloons()
        st.success(f"🎉 정답입니다! 참 잘했어요! ({st.session_state.quiz_h}시 {st.session_state.quiz_m}분)")
    else:
        st.error("😢 아쉬워요! 바늘의 위치를 다시 확인하고 도전해 보세요.")

# 6. 다음 문제로 넘어가기 버튼
st.markdown("---")
if st.button("🔄 다음 문제 풀기"):
    reset_quiz()
    st.rerun()
    