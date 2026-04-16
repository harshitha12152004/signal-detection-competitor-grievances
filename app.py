import json
import sys
from pathlib import Path
from typing import List,Dict

from signals.competitor_grievances import detect_competitor_grievances

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main(data_dir: Path, output_path: Path):
    all_signals: List[Dict] = []

    for file_path in data_dir.glob("*.txt"):
        print(f"Processing {file_path}...")
        text = read_file(file_path)
        # You can infer company name from filename or hardcode it here
        company = file_path.stem.replace("_", " ").title()
        signals = detect_competitor_grievances(
            text=text,
            source_url=f"file://{file_path.absolute()}",
            company=company,
        )
        all_signals.extend(signals)

    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_signals, f, indent=2)

    print(f"✅ Written signals to {output_path}")
    for sig in all_signals:
        print(
            f"  [{sig['company']}] {sig['reason'][:80]}... "
            f"(score: {sig['signal_score']})"
        )

if __name__ == "__main__":
    main(DATA_DIR, OUTPUT_DIR / "grievances.json")