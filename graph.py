import os
import sys
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

# Add root path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.env import GEMINI_API_KEY
import google.generativeai as genai
from langgraph.graph import StateGraph
from typing import TypedDict

# ✅ Check for valid key
if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY is missing in your .env file!")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Gemini Wrapper using correct model
class GeminiLLM:
    def __init__(self, model="gemini-1.5-pro"):  # <-- FIXED MODEL
        self.model = genai.GenerativeModel(model)

    def predict(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error from Gemini: {str(e)}"

# ✅ Initialize the LLM
llm = GeminiLLM()

# --- 🔹 Generate Interview Question ---
def ask_question(state):
    company = state.get("company", "a tech company")
    round_type = state.get("round_type", "DSA")
    experience_level = state.get("experience_level", "beginner")  # Default level

    # Company-specific styles
    company_styles = {
        "Google": "emphasizing algorithmic depth and problem-solving",
        "Amazon": "focusing on leadership principles and scalable systems",
        "Flipkart": "blending coding challenges with product understanding",
        "Microsoft": "focusing on practical software design and code clarity",
        "Zomato": "highlighting real-time system design and data efficiency",
        "PayPal": "emphasizing security, APIs, and financial transaction logic"
    }
    company_style = company_styles.get(company, "for a top tech company")

    # Tailor prompt based on round type and experience level
    if round_type == "DSA":
        prompt = (
            f"Generate a {experience_level}-level DSA interview question {company_style}. "
            f"Ensure input/output clarity and moderate difficulty appropriate for 0–3 years experience."
        )

    elif round_type == "System Design":
        prompt = (
            f"Generate a {experience_level}-level system design interview question {company_style}. "
            f"Focus on understanding architecture fundamentals, trade-offs, and basic scalability concepts."
        )

    elif round_type == "HR":
        prompt = (
            f"Generate a behavioral HR interview question {company_style}. "
            f"Target soft skills, work scenarios, and values alignment suitable for a {experience_level}-level candidate."
        )

    elif round_type == "Machine Learning":
        prompt = (
            f"Generate a {experience_level}-level machine learning interview question {company_style}. "
            f"Include basic concepts such as algorithms, evaluation metrics, or deployment scenarios."
        )

    elif round_type == "Cloud Architecture":
        prompt = (
            f"Generate a {experience_level}-level cloud architecture interview question {company_style}. "
            f"Focus on beginner-to-intermediate cloud design concepts using platforms like AWS, GCP, or Azure."
        )

    else:
        prompt = (
            f"Generate a {experience_level}-level general technical interview question {company_style} "
            f"for a {round_type} round suitable for 0–3 years of experience."
        )

    question = llm.predict(prompt)
    return {"question": question}

# --- 🔹 Evaluate User's Answer ---
def evaluate_answer(state):
    question = state.get("question", "")
    answer = state.get("answer", "")
    round_type = state.get("round_type", "")

    if round_type == "Machine Learning":
        prompt = f"""
        You are a senior ML engineer.

        Question: {question}
        Answer: {answer}

        Evaluate this ML answer based on clarity, correctness, use of algorithms, and explanation depth.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """
    
    elif round_type == "Cloud Architecture":
        prompt = f"""
        You are a cloud systems architect.

        Question: {question}
        Answer: {answer}

        Evaluate this cloud architecture response based on scalability, design reasoning, cost awareness, and cloud-native principles.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """

    elif round_type == "DSA":
        prompt = f"""
        You are a DSA interview evaluator.

        Question: {question}
        Answer: {answer}

        Evaluate the response based on algorithmic correctness, time/space complexity, and edge case handling.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """

    elif round_type == "System Design":
        prompt = f"""
        You are a senior software architect.

        Question: {question}
        Answer: {answer}

        Evaluate the system design based on scalability, availability, modularity, and real-world feasibility.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """

    elif round_type == "HR":
        prompt = f"""
        You are an HR professional.

        Question: {question}
        Answer: {answer}

        Evaluate this answer based on communication clarity, self-awareness, relevance, and culture fit.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """
    
    else:
        prompt = f"""
        Question: {question}
        Answer: {answer}

        Evaluate this answer on a scale of 1 to 10 based on appropriateness and depth.

        Format:
        Score: <1-10>
        Feedback: <Detailed feedback>
        """

    evaluation = llm.predict(prompt)
    return {"evaluation": evaluation}

# --- 🔹 State Schema ---
class InterviewState(TypedDict, total=False):
    name: str
    company: str
    round_type: str
    experience_level: str  
    question: str
    answer: str
    evaluation: str

# --- 🔹 Build LangGraph ---
def build_graph():
    sg = StateGraph(InterviewState)
    sg.add_node("generate_question", ask_question)
    sg.add_node("evaluate_answer", evaluate_answer)
    sg.set_entry_point("generate_question")
    sg.add_edge("generate_question", "evaluate_answer")
    sg.set_finish_point("evaluate_answer")
    return sg.compile()
