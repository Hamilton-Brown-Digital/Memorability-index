def generate_insights(primary_vis, primary_cog,
                      avg_vis, avg_cog,
                      palette_overlaps,   # dict: { competitor_url: overlap_pct }
                      complexity_delta):  # primary_complex - avg_comp_complex

    recs = []

    # 1) Visual differentiation
    obs = f"Your visual distinctiveness scores {primary_vis} vs industry average of {avg_vis}"
    impact = ("This suggests your site is "
              + ("underperforming" if primary_vis < avg_vis else "leading")
              + " on visual memorability.")
    if primary_vis < avg_vis:
        action = ("experiment with a bolder, unique accent colour—"
                  "e.g. introduce a high-contrast brand hue in key CTAs.")
        predicted = round((avg_vis - primary_vis) * 0.5, 1)
    else:
        action = ("double down on your minimalist layout and whitespace "
                  "to maintain top-tier visual clarity.")
        predicted = round((primary_vis - avg_vis) * 0.3, 1)

    recs.append({
        "Observation": obs,
        "Impact": impact,
        "Recommendation": f"Consider {action}",
        "Expected outcome": f"Could improve overall visual score by ~{predicted}"
    })

    # 2) Content simplification
    obs = f"Your cognitive load scores {primary_cog} vs industry average of {avg_cog}"
    impact = ("This indicates your messaging is "
              + ("more complex than" if primary_cog < avg_cog else "easier than")
              + " competitors to process.")
    if primary_cog < avg_cog:
        action = ("simplify headline copy and reduce paragraphs by 20%—"
                  "focus on single-sentence value props above the fold.")
        predicted = round((avg_cog - primary_cog) * 0.6, 1)
    else:
        action = ("maintain your clear, concise tone but audit pages "
                  "for any jargon spikes.")
        predicted = round((primary_cog - avg_cog) * 0.2, 1)

    recs.append({
        "Observation": obs,
        "Impact": impact,
        "Recommendation": f"Consider {action}",
        "Expected outcome": f"Could improve overall cognitive score by ~{predicted}"
    })

    # 3) Palette overlap insights (pick top overlap)
    if palette_overlaps:
        # find largest overlap competitor
        comp, overlap = max(palette_overlaps.items(), key=lambda x: x[1])
        obs = (f"Your colour palette overlaps {overlap}% with {comp}")
        impact = ("High overlap risks brand confusion in a crowded market.")
        action = ("diversify your accent palette—introduce at least 2 unique brand colours "
                  "not used by competitors.")
        predicted = 1.0  # assume +1 point for differentiation
        recs.append({
            "Observation": obs,
            "Impact": impact,
            "Recommendation": f"Consider {action}",
            "Expected outcome": f"Could improve visual distinctiveness by ~{predicted}"
        })

    # 4) Complexity gap
    obs = (f"Your content complexity is {abs(complexity_delta)} "
           + ("points higher" if complexity_delta > 0 else "points lower")
           + " than competitor average")
    impact = ("Too high a complexity gap can overwhelm first-time visitors." 
              if complexity_delta > 0 
              else "Your simpler structure gives you a readability edge.")
    if complexity_delta > 0:
        action = ("reduce multi-syllable terms by 30%—use plain-language synonyms "
                  "for common jargon.")
        predicted = round(min(complexity_delta * 0.4, 1.5), 1)
    else:
        action = ("leverage your clear language in marketing materials to reinforce recall.")
        predicted = 0.5
    recs.append({
        "Observation": obs,
        "Impact": impact,
        "Recommendation": f"Consider {action}",
        "Expected outcome": f"Could improve cognitive clarity by ~{predicted}"
    })

    # Trim to max 5 recommendations
    return recs[:5]
