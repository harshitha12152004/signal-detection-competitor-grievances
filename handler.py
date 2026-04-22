import json
from pathlib import Path
from typing import Any, Dict, List

from signals.competitor_grievances import detect_competitor_grievances

DATA_DIR = Path("data")

def detect_grievances_lambda(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless/Lambda-style handler.

    Supports two modes:
    1) If event['body'] has a "text" field -> analyze that text.
    2) Otherwise -> analyze all .txt files under data/ (same as app.py).
    """

    # Case 1: HTTP-style event with JSON body { "text": "..." }
    body_text = None
    if "body" in event and event["body"]:
        try:
            payload = event["body"]
            if isinstance(payload, str):
                payload = json.loads(payload)
            body_text = payload.get("text")
        except Exception:
            body_text = None

    signals: List[Dict[str, Any]] = []

    if body_text:
        # Analyze just the given text
        signals = detect_competitor_grievances(
            text=body_text,
            source_url="local:event-body",
            company="Ad-hoc Text",
        )
    else:
        # Fallback: process all .txt files from data/
        for file_path in DATA_DIR.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8")
            company = file_path.stem.replace("_", " ").title()
            file_signals = detect_competitor_grievances(
                text=text,
                source_url=f"file://{file_path.absolute()}",
                company=company,
            )
            signals.extend(file_signals)

    # Lambda-style HTTP response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(signals, indent=2),
    }
