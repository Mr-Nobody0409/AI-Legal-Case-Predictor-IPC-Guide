import re

# ─── IPC Section Extractor ────────────────────────────────────────────────────

# Common IPC sections with descriptions
IPC_DESCRIPTIONS = {
    "302": "Murder",
    "304": "Culpable homicide not amounting to murder",
    "304A": "Causing death by negligence",
    "307": "Attempt to murder",
    "308": "Attempt to commit culpable homicide",
    "320": "Grievous hurt",
    "323": "Voluntarily causing hurt",
    "324": "Voluntarily causing hurt by dangerous weapons",
    "325": "Voluntarily causing grievous hurt",
    "326": "Grievous hurt by dangerous weapons",
    "354": "Assault on woman with intent to outrage modesty",
    "375": "Rape",
    "376": "Punishment for rape",
    "377": "Unnatural offences",
    "378": "Theft",
    "379": "Punishment for theft",
    "380": "Theft in dwelling house",
    "382": "Theft after preparation for hurt",
    "383": "Extortion",
    "384": "Punishment for extortion",
    "390": "Robbery",
    "392": "Punishment for robbery",
    "395": "Dacoity",
    "397": "Robbery with attempt to cause death",
    "406": "Criminal breach of trust",
    "415": "Cheating",
    "420": "Cheating and dishonestly inducing delivery of property",
    "426": "Mischief",
    "441": "Criminal trespass",
    "447": "Punishment for criminal trespass",
    "463": "Forgery",
    "465": "Punishment for forgery",
    "468": "Forgery for purpose of cheating",
    "471": "Using as genuine a forged document",
    "499": "Defamation",
    "500": "Punishment for defamation",
    "503": "Criminal intimidation",
    "504": "Intentional insult with intent to provoke breach of peace",
    "506": "Punishment for criminal intimidation",
    "509": "Word, gesture or act intended to insult modesty of a woman",
    "34": "Acts done by several persons in furtherance of common intention",
    "120B": "Criminal conspiracy",
    "149": "Every member of unlawful assembly guilty of offence committed",
    "363": "Kidnapping",
    "364": "Kidnapping for ransom",
    "365": "Kidnapping with intent to secretly confine person",
    "498A": "Husband or relative of husband subjecting woman to cruelty",
}


def extract_ipc_sections(text: str) -> list[str]:
    """
    Extracts IPC section numbers from LLM output text.
    Handles patterns like: IPC 302, Section 302, u/s 302, IPC-302
    """
    patterns = [
        r"IPC[\s\-]?(\d{1,3}[A-Z]?)",
        r"[Ss]ection[\s](\d{1,3}[A-Z]?)",
        r"[Ss]ec[\.\s](\d{1,3}[A-Z]?)",
        r"u/s[\s](\d{1,3}[A-Z]?)",
        r"under[\s](\d{1,3}[A-Z]?)\s+IPC",
    ]

    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            found.add(m.strip())

    # Filter to known IPC sections or plausible range (1–511)
    validated = []
    for s in sorted(found):
        num = re.sub(r"[A-Z]", "", s)
        if num.isdigit() and 1 <= int(num) <= 511:
            validated.append(f"IPC {s}")

    return validated if validated else ["IPC section not identified — consult a lawyer"]


# ─── Case Categorization ──────────────────────────────────────────────────────

CATEGORY_KEYWORDS = {
    "Murder & Culpable Homicide": [
        "murder", "killed", "death", "homicide", "shoot", "stabbed",
        "poisoned", "strangulation", "beaten to death",
    ],
    "Theft & Property Crimes": [
        "theft", "stolen", "robbery", "burglary", "dacoity", "pickpocket",
        "shoplifting", "looted", "snatched", "trespas",
    ],
    "Fraud & Cheating": [
        "fraud", "cheating", "forgery", "embezzlement", "scam", "ponzi",
        "fake", "misrepresentation", "counterfeit", "breach of trust",
    ],
    "Assault & Violence": [
        "assault", "attack", "beaten", "hurt", "injury", "fight", "brawl",
        "hit", "punched", "kicked", "grievous", "wounded",
    ],
    "Sexual Offences": [
        "rape", "molestation", "sexual assault", "outrage modesty",
        "harassment", "eve teasing", "stalking", "voyeurism",
    ],
    "Cybercrime": [
        "hacking", "phishing", "cyber", "online fraud", "identity theft",
        "data breach", "ransomware", "malware", "social media",
    ],
    "Defamation": [
        "defamation", "slander", "libel", "false statement", "reputation",
        "insult", "character assassination",
    ],
    "Kidnapping & Abduction": [
        "kidnap", "abduct", "held hostage", "ransom", "missing person",
        "confined", "illegal detention",
    ],
    "Domestic Violence": [
        "domestic", "spouse", "wife", "husband", "dowry", "cruelty",
        "marital", "in-laws",
    ],
}


def categorize_case(description: str) -> str:
    """Categorizes the legal case based on keyword matching."""
    desc_lower = description.lower()
    scores: dict[str, int] = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            scores[category] = score

    if not scores:
        return "General Criminal Law"

    return max(scores, key=scores.get)


# ─── Lawyer Recommendation ────────────────────────────────────────────────────

LAWYER_MAP = {
    "Murder & Culpable Homicide": "Criminal Defense Lawyer (Specialization: Homicide & Capital Offences)",
    "Theft & Property Crimes": "Criminal Lawyer (Specialization: Property & Theft Law)",
    "Fraud & Cheating": "Corporate Criminal Lawyer (Specialization: Economic Offences & White-Collar Crime)",
    "Assault & Violence": "Criminal Defense Lawyer (Specialization: Violent Crimes & Bodily Harm)",
    "Sexual Offences": "Criminal Lawyer (Specialization: POCSO & Sexual Offences)",
    "Cybercrime": "Cyber Law Attorney (Specialization: IT Act & Digital Crimes)",
    "Defamation": "Civil & Criminal Lawyer (Specialization: Defamation & Media Law)",
    "Kidnapping & Abduction": "Criminal Defense Lawyer (Specialization: Kidnapping & Trafficking)",
    "Domestic Violence": "Family Law Attorney (Specialization: DV Act & Section 498A)",
    "General Criminal Law": "General Practice Criminal Lawyer",
}


def recommend_lawyer(category: str) -> str:
    """Returns the recommended lawyer type for the given category."""
    return LAWYER_MAP.get(category, "General Practice Criminal Lawyer")
