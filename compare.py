# compare.py
# Competitive benchmarking for brand memorability

from analyzer import analyze_website
from cognitive import analyze_cognitive_load
from insights import generate_insights


def hex_set(palette):
    """
    Convert the visual analysis palette into a set of hex color codes.
    """
    return { sw["hex"] for sw in palette }


def palette_overlap(p1, p2):
    """
    Calculate the percentage overlap between two color sets.
    """
    if not p1 or not p2:
        return 0.0
    intersection = p1 & p2
    return round(len(intersection) / len(p1) * 100, 1)


def compare_brands(primary_url, competitor_urls):
    """
    Run visual and cognitive analysis on a primary site and its competitors,
    compute averages, overlaps, complexity deltas, and generate insights + recommendations.
    """
    urls = [primary_url] + competitor_urls
    visual_scores = []
    cognitive_scores = []
    palettes = {}
    results = {}

    # 1) Execute analyses for each URL
    for u in urls:
        vis = analyze_website(u)
        cog = analyze_cognitive_load(u)
        visual_scores.append(vis["score"])
        cognitive_scores.append(cog["cognitive_load_score"])
        palettes[u] = hex_set(vis["breakdown"]["Dominant Colours"])
        results[u] = {"visual": vis, "cognitive": cog}

    # 2) Compute industry averages (exclude primary)
    comp_visual = visual_scores[1:]
    comp_cog    = cognitive_scores[1:]
    avg_visual  = round(sum(comp_visual) / len(comp_visual), 1) if comp_visual else 0.0
    avg_cognitive = round(sum(comp_cog) / len(comp_cog), 1) if comp_cog else 0.0

    # 3) Calculate palette overlaps versus competitors
    palette_overlaps = {
        comp: palette_overlap(palettes[primary_url], palettes.get(comp, set()))
        for comp in competitor_urls
    }

    # 4) Complexity delta — primary vs. average competitor complexity
    comp_complex = [results[c]["cognitive"]["complexity_score"] for c in competitor_urls]
    avg_complex  = round(sum(comp_complex) / len(comp_complex), 1) if comp_complex else 0.0
    prim_complex = results[primary_url]["cognitive"]["complexity_score"]
    complexity_delta = round(prim_complex - avg_complex, 1)

    # 5) Build basic narrative insights
    insights = []
    insights.append(
        f"Your visual distinctiveness: {visual_scores[0]} vs industry average of {avg_visual}"
    )
    sign = "above" if cognitive_scores[0] >= avg_cognitive else "below"
    insights.append(
        f"Your cognitive load: {cognitive_scores[0]} ({sign} average of {avg_cognitive})"
    )
    for comp, overlap in palette_overlaps.items():
        insights.append(
            f"Your colour palette overlaps {overlap}% with {comp}"
        )
    if complexity_delta != 0:
        direction = "higher than" if complexity_delta > 0 else "lower than"
        insights.append(
            f"Your content complexity is {abs(complexity_delta)} points {direction} competitor average"
        )

    # 6) Generate detailed, actionable recommendations
    recommendations = generate_insights(
        primary_vis=visual_scores[0],
        primary_cog=cognitive_scores[0],
        avg_vis=avg_visual,
        avg_cog=avg_cognitive,
        palette_overlaps=palette_overlaps,
        complexity_delta=complexity_delta
    )

    return {
        "urls": urls,
        "visual_scores": visual_scores,
        "cognitive_scores": cognitive_scores,
        "avg_visual": avg_visual,
        "avg_cognitive": avg_cognitive,
        "palette_overlaps": palette_overlaps,
        "complexity_delta": complexity_delta,
        "insights": insights,
        "recommendations": recommendations
    }