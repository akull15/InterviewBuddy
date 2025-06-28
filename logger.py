import csv
import os
from datetime import datetime

def log_interview(name, company, round_type, question, answer, feedback):
    os.makedirs("logs", exist_ok=True)
    file_path = f"logs/{name.lower().replace(' ', '_')}_interview_log.csv"

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "name", "company", "round_type", "question", "answer", "feedback"])
        writer.writerow([
            datetime.now().isoformat(),
            name,
            company,
            round_type,
            question,
            answer,
            feedback
        ])