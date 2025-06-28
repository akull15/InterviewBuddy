🤖 InterviewBuddy – GenAI Interview Preparation
InterviewBuddy is an AI-powered mock interview assistant built using Google Gemini, Streamlit, and LangGraph. It helps candidates practice and improve their interview skills by simulating realistic technical and behavioral rounds, evaluating answers with AI, and offering feedback — all in a clean, intuitive interface.

🚀 Features
Feature	Description
🎯 Role & Company-specific Questions	Select your target company and interview round type (e.g., DSA, System Design, ML, Cloud Architecture, HR) to generate relevant and realistic interview questions.
🧠 Experience-Aware	Questions are tailored based on your experience level (beginner, intermediate, or advanced).
✍️ AI-Generated Questions & Feedback	Google Gemini Pro generates questions and evaluates user responses using natural language understanding.
📊 Scoring System	Get rated on a scale of 1–10 with detailed feedback to help you understand your strengths and improvement areas.
📚 Session History	Track all questions, answers, and feedback in a structured session history.
📥 CSV Export	Export your full interview session data to CSV — ideal for self-review or mentoring.
🗂 Persistent Logging	Logs each interview session locally for long-term tracking.

🖼️ UI Preview
Home Page	Interview Prompt	Evaluation Feedback
		

🧠 How It Works
User Input: Enter your name, select a company (e.g., Google, Amazon, etc.), round type (e.g., DSA, ML, HR), and experience level (e.g., beginner).

Question Generation: A Gemini-powered prompt node generates a personalized interview question.

Answer Submission: You submit an answer in free text format.

Evaluation: The system sends both question and answer to Gemini, which returns a score (1–10) and qualitative feedback.

Session Management: Each Q&A is added to a session log. You can review, scroll back, or download the entire session in CSV format.

🛠 Tech Stack
Layer	Technology
🧠 LLM	Google Gemini Pro (Generative AI)
🌐 App Framework	Streamlit
🔄 Workflow Engine	LangGraph
📦 Environment Config	python-dotenv
📊 Logging & Export	pandas, csv
🔐 API Handling	.env for key management

🧪 Supported Interview Rounds
DSA – Data Structures and Algorithms

System Design

Machine Learning

Cloud Architecture

HR / Behavioral

Each round type prompts the model differently based on:

Target company (e.g., Google, Amazon, etc.)

Experience level (Beginner to Intermediate)

Interview style cues (e.g., "scalable solutions", "leadership principles")
