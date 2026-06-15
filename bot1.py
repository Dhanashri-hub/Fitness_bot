import ollama
import streamlit as st

st.set_page_config(
    page_title="FitMentor",
    page_icon="🏋️",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}

h1{
    text-align:center;
}

.stButton button{
    width:100%;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("🏋️ FitMentor")
st.caption("Your personal fitness coach for workouts, nutrition, and healthy habits.")

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:

    st.header("👤 Your Profile")

    goal = st.selectbox(
        "Fitness Goal",
        [
            "Weight Loss",
            "Muscle Gain",
            "Strength Building",
            "General Fitness"
        ]
    )

    experience = st.selectbox(
        "Experience",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=20
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- Welcome Message ----------
if len(st.session_state.messages) == 0:
    st.info(
        "👋 Welcome! Ask me about workouts, diet plans, fat loss, muscle gain, recovery, or fitness routines."
    )

# ---------- Display Previous Messages ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- AI Function ----------
def fitness_coach(messages):

    system_prompt = f"""
    You are FitMentor, a friendly and experienced fitness coach.

    User Profile:
    - Goal: {goal}
    - Experience Level: {experience}
    - Age: {age}

    Rules:
    - Be friendly and motivating.
    - Keep responses practical.
    - Give realistic workout and nutrition advice.
    - Use bullet points when useful.
    - Avoid overly technical explanations.
    - Personalize advice using the user's profile.
    """

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + messages
    )

    return response["message"]["content"]

# ---------- Quick Actions ----------
st.subheader("Quick Start")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔥 Weight Loss Plan"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Create a beginner weight loss plan."
            }
        )
        st.rerun()

with col2:
    if st.button("💪 Muscle Gain Plan"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Create a beginner muscle gain plan."
            }
        )
        st.rerun()

# ---------- Chat Input ----------
prompt = st.chat_input(
    "Ask about workouts, diet, calories, muscle gain..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = fitness_coach(st.session_state.messages)

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )