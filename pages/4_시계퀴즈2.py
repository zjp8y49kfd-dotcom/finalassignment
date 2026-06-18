import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime, timedelta

# [고정] 시계를 그리는 함수
def draw_quiz_clock(h, m):
    fig, ax = plt.subplots(figsize=(4, 4))
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

    min_angle = np.pi / 2 - m * (np.pi / 30)
    hour_angle = np.pi / 2 - (h % 12 + m / 60.0) * (np.pi / 6)
    
    ax.plot([0, 0.45 * np.cos(hour_angle)], [0, 0.45 * np.sin(hour_angle)], color="#E74C3C", linewidth=8, solid_capstyle='round')
    ax.plot([0, 0.75 * np.cos(min_angle)], [0, 0.75 * np.sin(min_angle)], color="#3498DB", linewidth=4, solid_capstyle='round')
    ax.add_patch(plt.Circle((0, 0), 0.04, color="#2C3E50", fill=True, zorder=4))
    
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.axis('off'); ax.set_aspect('equal')
    return fig

# -----------------------------------------------------------------
# 퀴즈 메인 로직
# -----------------------------------------------------------------
st.title("⏰ 시간 계산 퀴즈")
st.write("제시된 문제와 시계를 보고, 알맞은 정답을 입력해 보세요.")

if "p_ans_h" not in st.session_state:
    st.session_state.p_ans_h = 1
if "p_ans_m" not in st.session_state:
    st.session_state.p_ans_m = 0

# 1. 문제 데이터 생성 및 고정
if "passed_quiz" not in st.session_state:
    st.session_state.passed_quiz = {
        "base_h": random.randint(1, 12),
        "base_m": random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]),
        "delta_h": random.randint(0, 2),
        "delta_m": random.choice([10, 15, 20, 30, 40, 45, 50]),
        "direction": random.choice(["후", "전"])
    }

q = st.session_state.passed_quiz

# 2. 총 분(Minutes) 단위를 이용한 경계면 오류 없는 정확한 연산
total_base_minutes = q["base_h"] * 60 + q["base_m"]
total_delta_minutes = q["delta_h"] * 60 + q["delta_m"]

if q["direction"] == "후":
    total_final_minutes = total_base_minutes + total_delta_minutes
else:
    total_final_minutes = total_base_minutes - total_delta_minutes

total_final_minutes = total_final_minutes % (12 * 60)
if total_final_minutes <= 0:
    total_final_minutes += (12 * 60)

correct_h = total_final_minutes // 60
correct_m = total_final_minutes % 60
if correct_h == 0:
    correct_h = 12

# 3. 텍스트 포맷 정리 (0시간 표현 생략)
h_text = f"{q['delta_h']}시간 " if q['delta_h'] > 0 else ""
m_text = f"{q['delta_m']}분"

# 4. 담백한 문장으로 문제 제시 인터페이스 구성
problem_text = f"❓ **{q['base_h']}시 {q['base_m']}분**에서 **{h_text}{m_text} {q['direction']}**은 몇 시 몇 분일까요?"
st.info(f"### 📝 문제 \n\n {problem_text}")

col_quiz, col_space = st.columns([1.2, 1])
with col_quiz:
    st.markdown("##### 📍 [참고] 처음 시각 시계 모양")
    base_fig = draw_quiz_clock(q["base_h"], q["base_m"])
    st.pyplot(base_fig)

# 5. 사용자 정답 입력 UI
st.markdown("### ✏️ 내가 생각한 정답을 입력해요")
col_ans1, col_ans2 = st.columns(2)
with col_ans1:
    user_ans_h = st.number_input("정답 '시' (1~12)", min_value=1, max_value=12, value=st.session_state.p_ans_h, key="input_h")
with col_ans2:
    user_ans_m = st.number_input("정답 '분' (0~59)", min_value=0, max_value=59, value=st.session_state.p_ans_m, key="input_m")

# 6. 정답 확인 및 결과에 따른 맞춤형 시계 명칭 피드백
if st.button("📢 정답 확인하기!", type="primary", key="p_ans_btn"):
    if user_ans_h == correct_h and user_ans_m == correct_m:
        st.balloons()
        st.success(f"🎉 정답입니다! 정말 잘했어요! 정답은 **{correct_h}시 {correct_m}분**이에요.")
        st.markdown("---")
        st.markdown(f"#### 🏁 [정답 해설] 우리가 맞춘 정답 시계 모양이에요!")
        ans_fig = draw_quiz_clock(correct_h, correct_m)
        st.pyplot(ans_fig)
    else:
        st.error("😢 조금 아쉬워요! 다시 한번 꼼꼼하게 바늘을 계산해볼까요?")
        st.markdown("---")
        st.markdown(f"#### 💡 [힌트] 정답 시계의 모습을 살짝 보여줄게요!")
        ans_fig = draw_quiz_clock(correct_h, correct_m)
        st.pyplot(ans_fig)

# 7. 새로운 문제 생성 버튼
st.markdown("---")
if st.button("🔄 새로운 문제 풀기", key="p_next_btn"):
    if "passed_quiz" in st.session_state:
        del st.session_state.passed_quiz
    st.session_state.p_ans_h = 1
    st.session_state.p_ans_m = 0
    st.rerun()