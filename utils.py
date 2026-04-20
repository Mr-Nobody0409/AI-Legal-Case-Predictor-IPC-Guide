import re
from transformers import pipeline

# ------------------------------
# Load summarizer ONCE (IMPORTANT)
# ------------------------------
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ------------------------------
# IPC Section Extraction
# ------------------------------
def extract_ipc_sections(text):
    matches = re.findall(r"\bSection\s+\d+\b", text, re.IGNORECASE)
    return sorted(set(matches)) if matches else ["Not found"]

# ------------------------------
# Case Categorization
# ------------------------------
def categorize_case(text):
    categories = {
        "Criminal": ["murder", "assault", "robbery", "theft", "fraud"],
        "Civil": ["property", "contract", "divorce"],
        "Cyber": ["hacking", "phishing", "data breach"]
    }

    text = text.lower()
    for category, keywords in categories.items():
        if any(k in text for k in keywords):
            return category

    return "General"

# ------------------------------
# Lawyer Recommendation
# ------------------------------
def recommend_lawyer(category):
    mapping = {
        "Criminal": "Criminal Lawyer",
        "Civil": "Civil Lawyer",
        "Cyber": "Cyber Crime Expert",
        "General": "Legal Consultant"
    }
    return mapping.get(category, "Legal Expert")

# ------------------------------
# Summarization
# ------------------------------
def summarize_text(text):
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
