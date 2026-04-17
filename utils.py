import re
from transformers import pipeline

# ------------------------------
# IPC Extraction
# ------------------------------
def extract_ipc_sections(text):
    matches = re.findall(r"\bSection\s+\d+\b", text, re.IGNORECASE)
    return sorted(set(matches)) if matches else ["Not found"]

# ------------------------------
# Categorization
# ------------------------------
def categorize_case(text):
    categories = {
        "Criminal": ["murder", "assault", "robbery", "theft"],
        "Civil": ["property", "contract", "divorce"],
        "Cyber": ["hacking", "phishing", "data breach"]
    }

    text = text.lower()
    for cat, keys in categories.items():
        if any(k in text for k in keys):
            return cat

    return "General"

def recommend_lawyer(category):
    return {
        "Criminal": "Criminal Lawyer",
        "Civil": "Civil Lawyer",
        "Cyber": "Cyber Crime Expert",
        "General": "Legal Consultant"
    }.get(category, "Legal Expert")

# ------------------------------
# Summarization
# ------------------------------
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    return summarizer(text, max_length=200, min_length=30)[0]["summary_text"]
