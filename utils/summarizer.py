from transformers import pipeline

# Load once (IMPORTANT)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    result = summarizer(text, max_length=250, min_length=30, do_sample=False)
    return result[0]["summary_text"]
