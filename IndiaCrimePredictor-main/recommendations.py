def generate_policy_recommendations(stats):
    """
    Generates AI-style policy recommendations based on crime statistics.
    """
    recommendations = []
    
    # Analyze Category Distribution
    categories = stats.get('charts', {}).get('category_distribution', {})
    if not categories:
        return ["Monitor overall crime trends and ensure adequate police visibility."]

    # Sort categories by volume
    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    top_crime = sorted_cats[0][0]
    
    # 1. Actionable recommendations based on top crime type
    if top_crime in ["Theft", "Robbery", "Burglary"]:
        recommendations.append({
            "title": f"Increase Patrols for {top_crime}",
            "text": f"High volume of {top_crime} detected. Recommend enhancing CCTV surveillance in residential areas and increasing night-time patrolling."
        })
    elif top_crime in ["Murder", "Attempt to Murder"]:
        recommendations.append({
            "title": "Violent Crime Mitigation",
            "text": "Address underlying social tensions. Increase communal harmony programs and tighten firearm/weapon regulations in high-risk zones."
        })
    elif top_crime == "Cyber Crimes":
        recommendations.append({
            "title": "Digital Literacy & Cyber Defense",
            "text": "Cyber crimes are the primary threat. Launch state-wide digital awareness campaigns and strengthen Cyber-Cell response units."
        })
    elif top_crime == "Rape" or top_crime == "Assault on Women":
        recommendations.append({
            "title": "Women Safety Infrastructure",
            "text": "Implement 'Safe City' initiatives. Improve street lighting, increase female police presence, and ensure faster judicial processing for gender-based crimes."
        })
    else:
        recommendations.append({
            "title": "General Security Update",
            "text": f"Focus resources on mitigating {top_crime} trends through data-driven localized policing."
        })

    # 2. Recommendation based on growth rate
    growth = stats.get('kpis', {}).get('growth', 0)
    if growth > 5:
        recommendations.append({
            "title": "Critical Growth Alert",
            "text": f"A significant {growth}% year-on-year growth detected. Recommend immediate deployment of additional rapid-response units and task force mobilization."
        })
    elif growth < -5:
        recommendations.append({
            "title": "Success Pattern Analysis",
            "text": "Crime rate is significantly declining. Recommend analyzing and scaling current policing strategies across neighboring regions."
        })

    # 3. Preventive Strategy
    recommendations.append({
        "title": "Holistic Community Policing",
        "text": "Invest in bridge programs between law enforcement and local communities to build trust and gather actionable human intelligence."
    })

    return recommendations
