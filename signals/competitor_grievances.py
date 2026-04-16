import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from utils.text_processing import (
    extract_sentences,
    contains_competitor,
    contains_negative_phrases,
    normalize_sentence,
)

COMPETITORS = [
    "HackerRank",
    "HireVue",
    "Codility",
    "TestGorilla",
    "CodeSignal",
    "DevSkills",
    "Spark Hire",
    "Interviewing.io",
]

NEGATIVE_PHRASES = [
    "expensive",
    "too expensive",
    "costs a lot",
    "pricing is high",
    "recruiter bottleneck",
    "slow process",
    "too slow",
    "takes too long",
    "bias",
    "biased",
    "black box",
    "no feedback",
    "lack of feedback",
    "unfair",
    "broken",
    "glitchy",
    "bugs",
    "bugged",
    "outdated",
    "poor user experience",
    "confusing interface",
    "hard to use",
    "not intuitive",
]

PAIN_POINT_MAP = {
    "expensive": "cost_pricing",
    "too expensive": "cost_pricing",
    "costs a lot": "cost_pricing",
    "pricing is high": "cost_pricing",
    "recruiter bottleneck": "process_bottleneck",
    "slow process": "process_speed",
    "too slow": "process_speed",
    "takes too long": "process_speed",
    "bias": "bias_fairness",
    "biased": "bias_fairness",
    "black box": "lack_transparency",
    "no feedback": "lack_feedback",
    "lack of feedback": "lack_feedback",
    "unfair": "bias_fairness",
    "broken": "technical_stability",
    "glitchy": "technical_stability",
    "bugs": "technical_stability",
    "bugged": "technical_stability",
    "outdated": "product_quality",
    "poor user experience": "usability",
    "confusing interface": "usability",
    "hard to use": "usability",
    "not intuitive": "usability",
}

def classify_pain_points(phrase: str) -> List[str]:
    key = phrase.lower()
    if key in PAIN_POINT_MAP:
        return [PAIN_POINT_MAP[key]]
    return []

def score_sentence(sentence: str) -> int:
    score = 0
    sentence_lower = sentence.lower()
    if "really" in sentence_lower or "very" in sentence_lower or "extremely" in sentence_lower:
        score += 5
    if "worst" in sentence_lower or "terrible" in sentence_lower or "awful" in sentence_lower:
        score += 10
    return score

def detect_competitor_grievances(
    text: str,
    source_url: str,
    company: Optional[str] = None,
    max_score_per_sentence: int = 50,
) -> List[Dict]:
    competitors_found = contains_competitor(text, COMPETITORS)
    if not competitors_found:
        return []

    sentences = extract_sentences(text)
    signals = []

    for sent in sentences:
        sent = normalize_sentence(sent)
        if not sent:
            continue

        comp_match = contains_competitor(sent, COMPETITORS)
        neg_phrases = contains_negative_phrases(sent, NEGATIVE_PHRASES)

        
        if not neg_phrases or not comp_match:
            continue

        pain_points = set()
        for phrase in neg_phrases:
            pain_points.update(classify_pain_points(phrase))

        base_score = sum(score_sentence(sent) for _ in range(len(neg_phrases)))
        signal_score = min(base_score, max_score_per_sentence)

        if not signal_score:
            signal_score = 30  # default if only generic negative words

        signal = {
            "company": company or "Unknown",
            "signal_type": "competitor_grievance",
            "source_url": source_url,
            "matched_keywords": list(neg_phrases),
            "matched_competitors": list(comp_match),
            "pain_points": list(pain_points),
            "signal_score": signal_score,
            "detected_at": datetime.utcnow().isoformat() + "Z",
            "reason": f"Negative feedback about {', '.join(comp_match)} with phrases: {', '.join(neg_phrases)}",
            "raw_text": sent,
        }
        signals.append(signal)

    return signals