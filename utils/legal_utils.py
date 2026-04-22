import re

def extract_ipc_sections(text):
    matches = re.findall(r"\bSection\s+\d+\b", text, re.IGNORECASE)
    return sorted(list(set(matches))) if matches else ["IPC section not found"]


def categorize_case(text):
    categories = {
        "Criminal": ["murder", "assault", "robbery", "theft", "fraud", "kidnapping"],
        "Civil": ["property", "contract", "divorce", "inheritance"],
        "Cyber": ["hacking", "phishing", "cyber fraud", "data breach"],
        "Corporate": ["business", "tax fraud", "shareholder"],
        "Labor": ["employment", "wages", "harassment"]
    }

    text = text.lower()

    for category, keywords in categories.items():
        if any(k in text for k in keywords):
            return category

    return "General Legal Issue"


def recommend_lawyer(category):
    mapping = {
        "Criminal": "Criminal Lawyer",
        "Civil": "Civil Lawyer",
        "Cyber": "Cyber Crime Specialist",
        "Corporate": "Corporate Lawyer",
        "Labor": "Labor Law Attorney",
        "General Legal Issue": "Legal Consultant"
    }

    return mapping.get(category, "Legal Expert")
