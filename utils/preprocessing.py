import re

def clean_text(text):
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M", "", text)
    text = text.encode("ascii", "ignore").decode()
    return text.strip()
