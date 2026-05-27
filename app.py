import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 AI 상담 챗봇")

# -----------------------------
# API KEY 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini Client 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini Client 생성 실패: {e}")
    st.stop()

# -----------------------------
# 시스템 프롬프트
# -----------------------------
SYSTEM_PROMPT = """
너는 따뜻하고 공감 능력이 뛰어난 연애상담 AI야.

규칙:
- 상대를 비난하지 말 것
- 현실적이고 차분하게 조언할 것
- 사용자의 감정을 먼저 공감할 것
- 짧고 자연스럽게 대화할 것
- 위험하거나 공격적인 조언은 금지
"""

# -----------------------------
# 채팅 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 기존 메시지 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("연애 고민을 입력해보세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("생각 중..."):

            try:
                # 이전 대화 기록 문자열로 변환
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                full_prompt = f"""
{SYSTEM_PROMPT}

다음은 지금까지의 대화 기록이야:

{history_text}

AI 답변:
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=500
                    )
                )

                ai_answer = response.text

                # 응답 출력
                st.markdown(ai_answer)

                # 기록 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_answer
                    }
                )

            except Exception as e:
                error_message = f"오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 설정")

    if st.button("대화 기록 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
### ✨ 커스터마이징 팁
SYSTEM_PROMPT를 수정하면:
- 연애상담
- 고민상담
- 공부코치
- 영어회화
- MBTI 상담
등으로 바꿀 수 있어요.
"""
    )
