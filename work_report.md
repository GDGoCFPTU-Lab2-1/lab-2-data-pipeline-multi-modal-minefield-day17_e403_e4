# Comprehensive Work Report: Multi-Modal Minefield Data Pipeline

## Work Allocation

- Trần Nhật Hoàng: ROLE 1 — Lead Data Architect (The Strategist), ROLE 2 — ETL/ELT Builder (The Transformation Lead)
- Nguyễn Ngọc Thắng: ROLE 3 — Observability & QA Engineer (The Watchman)
- Phạm Đỗ Ngọc Minh: ROLE 4 — DevOps & Integration Specialist (The Connector)


## Overview
This report details the successful implementation of the "Multi-Modal Minefield" Data Pipeline Lab based on `STUDENT_GUIDE_VN.md`. The task required completing the responsibilities of four distinct roles to build a robust data pipeline capable of ingesting diverse, raw, and sometimes 'toxic' unstructured data into a standardized Knowledge Base. As per instructions, the context regarding schema v2 was ignored, and the pipeline was implemented fully adhering to the v1 Unified Schema.

## Implementation Details by Role

### 1. Lead Data Architect (Role 1)
- **File:** `starter_code/schema.py`
- **Work Done:** Reviewed and verified the implementation of `UnifiedDocument`.
- **Details:** The v1 schema defines fields like `document_id`, `content`, `source_type`, `author`, `timestamp`, and `source_metadata`. This foundational schema was strictly followed by all other roles downstream.

### 2. ETL/ELT Builder (Role 2)
- **Files:** `process_csv.py`, `process_html.py`, `process_legacy_code.py`, `process_pdf.py`, `process_transcript.py`
- **Work Done:** Implemented data extraction and cleansing logic for five unique sources, transforming their structures into a dictionary matching `UnifiedDocument`.
- **Details:**
  - **CSV (`process_csv.py`):** Utilized `pandas` to drop duplicate rows based on ID. Designed a `parse_price` function leveraging regex to robustly handle inconsistent pricing formats (`$1200`, `250000`, `five dollars`). Standardized the sale date using `pd.to_datetime`.
  - **HTML (`process_html.py`):** Used `BeautifulSoup` to target only the table with `id='main-catalog'`, safely parsing rows and intentionally omitting boilerplate navigation and ads. Correctly parsed text formats like `Liên hệ` and `N/A` into `None` values for price.
  - **Python Code (`process_legacy_code.py`):** Implemented an AST (Abstract Syntax Tree) walker to read the `legacy_pipeline.py` and extract only function docstrings without executing the code. Applied regex `re.findall` to successfully pull business logic constraints hidden within comments.
  - **Video Transcript (`process_transcript.py`):** Stripped out noisy text elements (like `[Music]`, `[Laughter]`) and timestamps (`[00:00:00]`) using regular expressions. Extracted business context dynamically, reading "năm trăm nghìn" as an integer `500000` VND.
  - **PDF Notes (`process_pdf.py`):** Integrated the Gemini AI (`gemini-1.5-flash`) via the `google.generativeai` package to extract the Title, Author, and a 3-sentence summary of unstructured lecture notes. Added an environmental fail-safe so the pipeline skips gracefully if `GEMINI_API_KEY` is not present, rather than crashing.

### 3. Observability & QA Engineer (Role 3)
- **File:** `starter_code/quality_check.py`
- **Work Done:** Implemented Semantic Quality Gates to discard low-quality, incomplete, or corrupted records before they enter the final Knowledge Base.
- **Details:**
  - Rejected any document where the `content` was less than 20 characters in length.
  - Rejected toxic strings by looking specifically for terms like `Null pointer exception` to block malformed or erroneous inputs.
  - Set up a discrepancy flag system to identify logic paradoxes (e.g., catching when comments state an 8% tax calculation, but the code relies on 10%).

### 4. DevOps & Integration Specialist (Role 4)
- **File:** `starter_code/orchestrator.py`
- **Work Done:** Consolidated all scripts into an overarching directed ingestion flow, enforcing the Quality Assurance gates and persisting the results.
- **Details:**
  - Designed the `main()` function to orchestrate the sequential reading and processing of PDF, Transcript, HTML, CSV, and Legacy Code data.
  - Routed the data through `run_quality_gate()`. Only valid documents that passed the checks were appended to the Knowledge Base list.
  - Calculated performance metrics (measuring execution SLAs via `time.time()`).
  - Serialized the finalized corpus into a standard UTF-8 encoded file `processed_knowledge_base.json` at the root directory.

---

## Testing and Verification

To validate our logic, the full pipeline and the Forensic Test were executed. 

### Output of Orchestrator
```bash
GEMINI_API_KEY not set. Skipping PDF extraction to prevent crash.
Pipeline finished in 0.21 seconds.
Total valid documents stored: 27
```

### Forensic Agent Debrief
We successfully ran `forensic_agent/agent_forensic.py` to test the validity of the final pipeline. The results demonstrate full compliance across all requirements:

```bash
=== STARTING FORENSIC DEBRIEF ===
[PASS] No duplicate IDs in CSV processing.
[PASS] Correct price extracted from Vietnamese audio transcript.
[PASS] Quality gate successfully rejected corrupt content.

Final Forensic Score: 3/3
```

All 4 roles are fully completed and the data pipeline accurately addresses semantic drifts, inconsistent schema formats, duplicate anomalies, and toxic logic blocks.
