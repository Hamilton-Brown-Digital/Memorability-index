from flask import Flask, render_template, request
from flask_cors import CORS
from analyzer import analyze_website
from cognitive import analyze_cognitive_load
from compare import compare_brands
from database import init_db, save_result, get_recent_results

app = Flask(__name__)
CORS(app)  

@app.route("/", methods=["GET", "POST"])
def index():
    visual = None
    cognitive = None
    error = None
    history = get_recent_results()

    if request.method == "POST":
        # Handle both JSON (from React) and form data (from templates)
        if request.is_json:
            url = request.json.get("url", "").strip()
        else:
            url = request.form.get("url", "").strip()

        # Validate URL
        if not (url.startswith("http://") or url.startswith("https://")):
            error = "Please enter a valid URL starting with http:// or https://"
        else:
            try:
                # Run both analyses once
                visual = analyze_website(url)
                cognitive = analyze_cognitive_load(url)

                # Save to database if both produced scores
                if visual and "score" in visual and cognitive and "cognitive_load_score" in cognitive:
                    save_result(
                        url,
                        visual["score"],
                        visual.get("summary", ""),
                        cognitive["cognitive_load_score"]
                    )

                # Refresh history
                history = get_recent_results()
            except Exception as e:
                error = f"Analysis failed: {e}"

        # Return JSON for API requests
        if request.is_json:
            if error:
                return {"error": error}, 400
            return {
                "score": visual.get("score"),
                "screenshot": visual.get("screenshot"),
                "summary": visual.get("summary"),
                "breakdown": visual.get("breakdown"),
                "cognitive": cognitive
            }

    return render_template(
        "index.html",
        visual=visual,
        cognitive=cognitive,
        history=history,
        error=error
    )

@app.route("/compare", methods=["GET", "POST"])
def compare():
    data = None
    error = None

    if request.method == "POST":
        primary = request.form.get("primary", "").strip()
        comp1   = request.form.get("comp1", "").strip()
        comp2   = request.form.get("comp2", "").strip()
        comp3   = request.form.get("comp3", "").strip()
        competitors = [u for u in (comp1, comp2, comp3) if u]

        # Validate at least two URLs
        if not (primary and primary.startswith(("http://", "https://"))):
            error = "Please enter a valid primary URL."
        elif len(competitors) < 1:
            error = "Please enter at least one competitor URL."
        else:
            try:
                data = compare_brands(primary, competitors)
            except Exception as e:
                error = f"Comparison failed: {e}"

    return render_template(
        "compare.html",
        data=data,
        error=error
    )

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)