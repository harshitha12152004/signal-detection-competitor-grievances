# Signal Detection – Competitor Grievance Detector

A simple Python‑based signal‑detection system that detects negative feedback about tools such as HackerRank, HireVue, Codility, etc., from public‑style review text.

## Features

- Rule‑based detection of competitor names and negative phrases.
- Categorization of complaints into pain points (e.g., cost, bias, UX, etc.).
- JSON output for downstream use by Vikaas.ai / InterviewGod.

## Setup

1. Clone the repo.
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Place input text files under `data/` (e.g., `sample_reviews_1.txt`).

4. Run the detector:

   ```bash
   python app.py
   ```

5. Output signals are written to `outputs/grievances.json`.

## Data ingestion approach

- Inputs are plain text files mimicking public reviews, blog comments, or forum posts.
- No external APIs or web scraping is used; all text is local and static.
- This can be extended to accept URLs or RSS feeds by pre‑fetching and saving them into `data/`.

## Scoring logic

- Each sentence is broken out and normalized.
- For each sentence containing at least one competitor and one negative phrase:
  - Base score is incremented for each negative phrase.
  - Extra points are added for intensifiers (`really`, `very`, `terrible`, `worst`, etc.).
  - Score is capped per sentence to avoid over‑inflating extreme rants.
- Signal score indicates severity of grievance (30–50 typical range).

## Assumptions and limitations

- Reviews are in English; no language detection or translation.
- Competitor names and negative phrases are hard‑coded; they can be extended via config.
- No NLP or LLM scoring; only simple keyword matching and heuristics.
- No user‑level or source‑reputation weighting; all signals are treated equally.
- Text is assumed to be safe and non‑malicious; no content sanitization is performed.