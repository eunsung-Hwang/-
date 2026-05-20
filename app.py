import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="골키퍼 앱",
    page_icon="🧤",
    layout="centered"
)

st.title("🧤 골키퍼 반사신경 테스트")

st.write("축구 골키퍼처럼 반사신경을 테스트해보세요!")

# 사용자 이름 입력
name = st.text_input("골키퍼 이름을 입력하세요:")

# 난이도 선택
difficulty = st.selectbox(
    "난이도를 선택하세요:",
    ["쉬움", "보통", "어려움"]
)

# 버튼 클릭 시 결과 출력
if st.button("슛 막기!"):
    try:
        if not name.strip():
            st.warning("이름을 입력해주세요!")
        else:
            import random
            # 난이도별 성공 확률
            probs = {"쉬움": 0.9, "보통": 0.6, "어려움": 0.3}
            success = random.random() < probs[difficulty]
            if success:
                st.success(f"{name}님이 슛을 막았습니다! 🧤")
            else:
                st.error(f"{name}님이 슛을 막지 못했습니다. 😢")
    except Exception as e:
        st.error("오류가 발생했습니다.")
        st.exception(e)
