Brand Memorability Analyzer

A Flask-based web application that analyzes brand websites for:

Visual Distinctiveness: Captures a homepage screenshot, extracts the dominant colour palette, computes whitespace ratio, counts visual elements and typography variety, then generates a 0–10 Visual Distinctiveness Score with actionable feedback.

Cognitive Load: Scrapes visible text to calculate readability (Flesch–Kincaid), information density, sentence complexity, and hierarchy clarity, yielding a 0–10 Cognitive Load Score and targeted insights.

Competitive Benchmarking: Compare your site against 2–3 competitors, compute industry averages, visualize relative scores (bar charts), and highlight palette overlaps or complexity gaps.

Summary & Feedback: Human-readable summaries for both visual and content analyses to guide improvements.

History Tracking: Persists results in SQLite and displays recent analyses with timestamps.

Features

Single‑site analysis (Visual + Cognitive) via /

Competitive benchmarking via /compare (primary + up to three competitors)

Chart.js bar charts for comparative scores

TailwindCSS‑powered responsive UI

Selenium+OpenCV screenshot capture & colour extraction

TextStat for readability and NLP‑based metrics

SQLite database for persisting and viewing recent results

Getting Started

Prerequisites

Python 3.8+

Google Chrome & matching ChromeDriver on your PATH

Virtual environment (recommended)

Installation

# Clone repository
git clone https://github.com/YOUR_USERNAME/Brand-Memorability-Analyser.git
cd Brand-Memorability-Analyser

# Create & activate venv
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Install requirements
pip install -r requirements.txt

Configuration

Ensure chromedriver binary is accessible via PATH or placed in the project root.

Verify the static/ and templates/ folders exist.

Usage

Run the Flask server:

python app.py

Open http://127.0.0.1:5000 in your browser.

Analyze a single URL on the homepage, or click Competitive Benchmark to compare multiple sites.

Project Structure

brand-analyzer/
├── app.py               # Main Flask application
├── analyzer.py          # Visual distinctiveness logic
├── cognitive.py         # Cognitive load analysis logic
├── compare.py           # Competitive benchmarking logic
├── database.py          # SQLite persistence helpers
├── static/              # Generated screenshots & assets
│   └── screenshot.png
├── templates/           # Jinja2 templates
│   ├── index.html       # Single‑site analysis UI
│   └── compare.html     # Competitive benchmarking UI
├── requirements.txt     # Python dependencies
└── README.md            # Project overview & instructions

Extending & Deployment

Add Metrics: Tune thresholds or introduce new scoring factors in the respective modules.

Deploy: Containerize with Docker, or deploy on Heroku, Render, Fly.io, etc.

Reporting: Integrate PDF/CSV export for shareable client reports.



