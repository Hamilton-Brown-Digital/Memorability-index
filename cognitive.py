import re
import requests
from bs4 import BeautifulSoup
from textstat import textstat

# Analyze cognitive load of a webpage
# Usage: python cognitive.py

def analyze_cognitive_load(url):
    # 1. Fetch & extract visible text
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)

    # 2. Readability (Flesch Reading Ease → normalize 0–100 to 0–10)
    flesch = textstat.flesch_reading_ease(text)
    readability_score = max(0.0, min(10.0, flesch / 10.0))

    # 3. Information density (avg words per <p>)
    paras = soup.find_all("p")
    words = text.split()
    avg_wpp = (
        sum(len(p.get_text().split()) for p in paras) / len(paras)
        if paras else len(words)
    )
    density_score = max(0.0, min(10.0, 10 - (avg_wpp / 20.0)))

    # 4. Sentence complexity (jargon ratio: % words ≥3 syllables)
    all_words = re.findall(r"\w+", text)
    syllables = [textstat.syllable_count(w) for w in all_words]
    jargon_ratio = (
        sum(1 for s in syllables if s >= 3) / len(all_words)
        if all_words else 0
    )
    complexity_score = max(0.0, min(10.0, 10 - (jargon_ratio * 20)))

    # 5. Message hierarchy clarity (headings vs paragraphs)
    heading_count = sum(len(soup.find_all(f"h{i}")) for i in range(1, 7))
    hierarchy_ratio = (heading_count / len(paras)) if paras else 0
    hierarchy_score = max(0.0, min(10.0, hierarchy_ratio * 5))

    # 6. Combine into a final 0–10 score
    cognitive_load_score = round(
        (readability_score + density_score + complexity_score + hierarchy_score) / 4, 1
    )

    # 7. Feedback based on thresholds
    feedback = []
    if avg_wpp > 100:
        feedback.append("High information density detected.")
    if hierarchy_score < 5:
        feedback.append("Message hierarchy is unclear.")
    if jargon_ratio > 0.2:
        feedback.append("High jargon usage detected.")
    if readability_score < 5:
        feedback.append("Readability is low; consider simpler wording.")

    return {
        "cognitive_load_score": cognitive_load_score,
        "readability_score": round(readability_score, 1),
        "density_score": round(density_score, 1),
        "complexity_score": round(complexity_score, 1),
        "hierarchy_score": round(hierarchy_score, 1),
        "feedback": feedback
    }
