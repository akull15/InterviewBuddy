import streamlit as st
from interview.graph import build_graph
from utils.logger import log_interview
import pandas as pd
import io

st.set_page_config(page_title="InterviewBuddy")
st.write("🚀 App started successfully")
# Streamlit config
st.set_page_config(page_title="InterviewBuddy", layout="centered")
st.title("🚀 InterviewBuddy – GenAI Interview preparation")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Form for user inputs
with st.form("user_input"):
    name = st.text_input("Enter your name")
    company = st.selectbox(
    "Target company",
    ["Google", "Amazon", "Flipkart", "Microsoft", "Zomato", "PayPal"]
    )
    round_type = st.selectbox("Select interview round", ["DSA", "HR", "System Design","Machine Learning","Cloud Architecture"])
    experience_level = st.selectbox(
        "Your experience level",
        ["beginner", "intermediate", "advanced"]
    )
    submitted = st.form_submit_button("Generate Question")

# Generate interview question
if submitted and name and company and round_type and experience_level:
    st.session_state.graph = build_graph()
    result = st.session_state.graph.invoke({
        "name": name,
        "company": company,
        "round_type": round_type,
        "experience_level": experience_level  # ✅ Added
    })
    st.session_state.question = result["question"]
    st.session_state.evaluation = None

# Display question and answer input
if "question" in st.session_state:
    st.subheader("📌 Interview Question:")
    st.markdown(st.session_state.question)

    user_answer = st.text_area("Your Answer")

    if st.button("Submit Answer") and user_answer:
        result = st.session_state.graph.invoke({
            "question": st.session_state.question,
            "answer": user_answer
        })

        feedback = result["evaluation"]
        st.session_state.evaluation = feedback

        # Save in session history
        st.session_state.history.append({
            "question": st.session_state.question,
            "answer": user_answer,
            "evaluation": feedback
        })

        # Save persistently in CSV file
        log_interview(name, company, round_type, st.session_state.question, user_answer, feedback)

# Show feedback
if st.session_state.get("evaluation"):
    st.subheader("📝 Evaluation & Feedback:")
    st.markdown(st.session_state.evaluation)

# Display session history
if st.session_state.history:
    st.subheader("📚 Session Interview History")
    for i, entry in enumerate(st.session_state.history, 1):
        st.markdown(f"**Q{i}:** {entry['question']}")
        st.markdown(f"**Your A{i}:** {entry['answer']}")
        st.markdown(f"**Feedback:** {entry['evaluation']}")
        st.markdown("---")

    # Offer CSV download for the session log
    df = pd.DataFrame(st.session_state.history)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="📥 Download Session Log (CSV)",
        data=csv_buffer.getvalue(),
        file_name=f"{name.lower().replace(' ', '_')}_session_log.csv",
        mime="text/csv"
    )