# Signal Detection – Competitor Grievance Detector

A simple Python‑based signal‑detection system that detects negative feedback about tools such as HackerRank, HireVue, Codility, etc., from public‑style review text.

## Features

- Rule‑based detection of competitor names and negative phrases.  
- Categorization of complaints into pain points (e.g., cost, bias, UX, etc.).  
- JSON output for downstream use by Vikaas.ai / InterviewGod.  

---

## Setup (CLI – main flow)

1. **Clone the repo** and move into the project directory:

   ```bash
   cd signal-detection-competitor-grievances
   ```

2. **Create and activate a virtual environment**:

   - Linux / macOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Place input text files** under `data/` (e.g., `sample_reviews_1.txt`, `sample_reviews_2.txt`, `sample_reviews_3.txt`).  
   Each file mimics public reviews, blog comments, or forum posts mentioning competitor tools and complaints.

5. **Run the detector (CLI mode)**:

   ```bash
   python app.py
   ```

6. **Output**:  
   All detected signals are written to:

   ```text
   outputs/grievances.json
   ```

This JSON file is the main sample output for the assignment.

---

## Serverless Wrapper (Local Execution Only)

This project also exposes the detector as a **Serverless Framework** function, compatible with AWS Lambda but used **only locally** (no cloud deployment).

### Prerequisites

- Node.js and npm installed (for the Serverless CLI).
- Serverless Framework v4 installed globally:

  ```bash
  npm install -g serverless
  ```

- A free Serverless Dashboard account (for v4 licensing).  
  After logging in, set `org` and `app` in `serverless.yml` to match your account.

### Local invocation with an ad‑hoc text (single input)

1. Create or edit `event.json` in the project root:

   ```json
   {
     "body": "{\"text\": \"HireVue felt biased and slow.\"}"
   }
   ```

2. Invoke the function locally:

   ```bash
   serverless invoke local -f detectGrievances --path event.json
   ```

3. The response will be a Lambda‑style JSON object:

   - `statusCode`: 200  
   - `headers`: `{"Content-Type": "application/json"}`  
   - `body`: a JSON array of detected signals (for that single text), including:
     - `company`
     - `signal_type`
     - `source_url`
     - `matched_competitors`
     - `matched_keywords`
     - `pain_points`
     - `signal_score`
     - `detected_at`
     - `reason`
     - `raw_text`

### Local invocation over all data files

If the event has no `text` field, the handler processes **all `.txt` files in `data/`**, similar to `python app.py`:

1. Create `event_all.json`:

   ```json
   {}
   ```

2. Invoke:

   ```bash
   serverless invoke local -f detectGrievances --path event_all.json
   ```

The response `body` will contain an array of signals from all input files.

### Optional: HTTP endpoint with serverless‑offline

If you installed the `serverless-offline` plugin and added it to `serverless.yml`:

```bash
npm install --save-dev serverless-offline
```

and `serverless.yml` includes:

```yaml
plugins:
  - serverless-offline
```

then you can run:

```bash
serverless offline
```

This starts a local HTTP server (e.g., `http://localhost:3000/detect`) where you can `POST` JSON:

```bash
curl -X POST http://localhost:3000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Codility felt outdated and not intuitive."}'
```

The response will be the same structured JSON signals.

---

## Data Ingestion Approach

- Inputs are plain text files under `data/` mimicking public reviews, blog comments, or forum posts.  
- No external APIs or web scraping is used; all text is local and static.  
- The same detection logic can be extended to accept URLs or RSS feeds by pre‑fetching their content and saving it into `data/`.  

The serverless handler supports two modes:

- **Ad‑hoc text** via `event.body.text` (single input).  
- **Batch processing** of all `.txt` files in `data/` when no text is provided.

---

## Scoring Logic

- The text is split into sentences and normalized (extra whitespace removed).  
- For each sentence that contains **at least one competitor** and **at least one negative phrase**:
  - A base score is computed, incremented for each negative phrase.
  - Extra points are added for intensifiers such as `really`, `very`, `extremely`, `worst`, `terrible`, `nightmare`.
  - The score is capped per sentence to avoid over‑inflating extreme rants.
- The final `signal_score` indicates the **severity** of the grievance (typically in the 30–50 range for strong complaints).

Each negative phrase is also mapped to one or more **pain point categories**, such as:

- `cost_pricing`  
- `process_bottleneck`  
- `process_speed`  
- `bias_fairness`  
- `usability`  
- `technical_stability`  
- `product_quality`  
- `lack_feedback`  

---

## Assumptions and Limitations

- Reviews are in **English**; there is no language detection or translation.  
- Competitor names and negative phrases are **hard‑coded lists**; they can be extended via code or configuration.  
- No NLP or LLM‑based scoring is used; only simple keyword matching and heuristics.  
- No user‑level or source‑reputation weighting; all signals are treated equally.  
- Text is assumed to be safe and non‑malicious; no content sanitization or PII removal is performed.  
- Serverless Framework is used **only for local development** and demonstration of a Lambda‑style handler; no cloud deployment is required for this assignment.
