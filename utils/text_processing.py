import re
from typing import List, Optional

def extract_sentences(text: str) -> List[str]:
    return re.split(r"[.!?]+", text)

def contains_competitor(text: str, competitors: List[str]) -> List[str]:
    text_lower = text.lower()
    found = []
    for comp in competitors:
        if comp.lower() in text_lower:
            found.append(comp)
    return found

def contains_negative_phrases(text: str, negative_phrases: List[str]) -> List[str]:
    text_lower = text.lower()
    matches = []
    for phrase in negative_phrases:
        phrase_lower = phrase.lower()
        if phrase_lower in text_lower:
            matches.append(phrase)
    return matches

def normalize_sentence(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())