import re


def summarize_text(text: str, max_sentences: int = 4) -> str:
    """
    Extracts the most relevant sentences from the LLM output
    to produce a concise summary without a secondary LLM call.
    """
    # Clean markdown artifacts
    cleaned = re.sub(r"#{1,6}\s*", "", text)
    cleaned = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", cleaned)
    cleaned = re.sub(r"\n{2,}", " ", cleaned)
    cleaned = cleaned.strip()

    # Split on sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

    # Score by legal relevance keywords
    priority_keywords = [
        "ipc", "section", "punished", "imprisonment", "offence",
        "guilty", "applicable", "charged", "conviction", "penalty",
        "relevant", "constitutes", "liable", "culpable",
    ]

    def score(sentence: str) -> int:
        lower = sentence.lower()
        return sum(1 for kw in priority_keywords if kw in lower)

    scored = sorted(sentences, key=score, reverse=True)
    top = scored[:max_sentences]

    # Re-order them by original position for coherence
    ordered = [s for s in sentences if s in top]

    return " ".join(ordered) if ordered else text[:400] + "..."
