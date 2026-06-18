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
    
    # 숫자 배치
    for i in range(1, 13):
        angle = np.pi / 2 - i * (np.pi / 6)
        ax.text(0.8 * np.cos(angle), 0.8 * np.sin(angle), str(i), 
                fontsize=16, fontweight='bold', ha='center', va='center')
        
    # 눈금 배치
    for i in range(60):
        angle = i * (np.pi / 30)
        is_five = (i % 5 == 0)
        ax.plot([(1 - (0.07 if is_five else 0.03)) * np.cos(angle), 1 * np.cos(angle)],
                [(1 - (0.07 if is_five else 0.03)) * np.sin(angle), 1 * np.sin(angle)], 
                color="#2C3E50" if is_five else "#BDC3C7", linewidth=2 if is_five else 1)

    # 바늘 각도 계산 및 그리기
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
st.title("🧙‍♂️ 시간 탐험대! 흐른 시간 맞추기")
st.write("랜덤으로 제시되는 시계와 문제를 보고, 바뀐 뒤의 시간을 맞추는 놀이예요.")

# 1. 세션 상태를 활용해 문제 데이터 독립 고정 (오류 방지 및 깔끔한 문장 처리)
if "passed_quiz" not in st.session_state:
    st.session_state.passed_quiz = {
        "base_h": random.randint(1, 12),
        "base_m": random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]), # 초등용 5분 단위
        "delta_h": random.randint(0, 2), # 0~2시간 변동
        "delta_m": random.choice([10, 15, 20, 30, 40, 45, 50]), # 분 변동
        "direction": random.choice(["후", "전"]),
        "story_idx": random.randint(0, 2)
    }

q = st.session_state.passed_quiz

# 2. 파이썬 datetime 모듈을 이용한 완벽한 정답 연산
base_dt = datetime(2026, 1, 1, q["base_h"], q["base_m"])
offset = timedelta(hours=q["delta_h"], minutes=q["delta_m"])

if q["direction"] == "후":
    correct_dt = base_dt + offset
    dir_text = "후"
else:
    correct_dt = base_dt - offset
    dir_text = "전"

# 초등학생용 12시간제 변환 (예: 0시는 12시로 표현)
correct_h = correct_dt.hour % 12
if correct_h == 0: 
    correct_h = 12
correct_m = correct_dt.minute

# 3. Pylance 오류를 완전히 방지하기 위해 삼중 따옴표 기반으로 스토리 문장 생성
h_text = f"{q['delta_h']}시간 " if q['delta_h'] > 0 else ""
m_text = f"{q['delta_m']}분"

story_0 = f"⏱️ 지금 시계는 **{q['base_h']}시 {q['base_m']}분**을 가리키고 있어요. 지금부터 **{h_text}{m_text} {dir_text}**은 몇 시 몇 분일까요?"
story_1 = f"🍪 민지가 **{q['base_h']}시 {q['base_m']}분**에 쿠키를 굽기 시작했어요. 맛있게 구워지기까지 **{h_text}{m_text}**이 더 걸린다면, 쿠키가 다 구워진 시각은 언제일까요?"
story_2 = f"⚽ 정우가 축구를 마치고 시계를 보니 **{q['base_h']}시 {q['base_m']}분**이었어요. 친구들과 정확히 **{h_text}{m_text} 동안** 신나게 뛰었다면, 축구를 **시작했던 시각**은 언제일까요?"

stories = [story_0, story_1, story_2]
current_story = stories[q["story_idx"]]

# 4. 문제 및 '처음 시각 시계' 레이아웃 제시
st.info(f"### 📝 문제 \n\n {current_story}")

col_quiz, col_space = st.columns([1.2, 1])
with col_quiz:
    st.markdown("##### 📍 [힌트] 처음 시각 시계 모양")
    base_fig = draw_quiz_clock(q["base_h"], q["base_m"])
    st.pyplot(base_fig)


# 5. 사용자 정답 입력 UI
st.markdown("### ✏️ 내가 생각한 정답을 입력해요")
col_ans1, col_ans2 = st.columns(2)
with col_ans1:
    user_ans_h = st.number_input("정답 '시' (1~12)", min_value=1, max_value=12, value=1, key="p_ans_h")
with col_ans2:
    user_ans_m = st.number_input("정답 '분' (0~59)", min_value=0, max_value=59, value=0, key="p_ans_m")

# 6. 정답 확인 및 결과에 따른 맞춤형 시계 명칭 피드백
if st.button("📢 정답 확인하기!", type="primary", key="p_ans_btn"):
    if user_ans_h == correct_h and user_ans_m == correct_m:
        st.balloons()
        st.success(f"🎉 정답입니다! 정말 잘했어요! 정답은 **{correct_h}시 {correct_m}분**이에요.")
        
        # 🟢 정답인 경우: '정답 해설 시계'로 명명
        st.markdown("---")
        st.markdown(f"#### 🏁 [정답 해설] 우리가 맞춘 정답 시계 모양이에요!")
        ans_fig = draw_quiz_clock(correct_h, correct_m)
        st.pyplot(ans_fig)
        st.caption(f"내가 입력한 {user_ans_h}시 {user_ans_m}분과 정답 시계의 모양이 똑같아요!")
    else:
        st.error("😢 조금 아쉬워요! 다시 한번 꼼꼼하게 바늘을 계산해볼까요?")
        
        # 🔴 오답인 경우: '힌트 시계'로 명명하여 스스로 고치도록 유도
        st.markdown("---")
        st.markdown(f"#### 💡 [힌트] 정답 시계의 모습을 살짝 보여줄게요!")
        ans_fig = draw_quiz_clock(correct_h, correct_m)
        st.pyplot(ans_fig)
        st.caption(f"힌트 시계를 잘 보고 짧은 바늘(시)과 긴 바늘(분)이 어디에 가 있는지 다시 입력해 보세요.")