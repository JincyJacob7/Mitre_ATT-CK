import json

def generate_navigator_layer(mapped_data):
    techniques = []
    seen_ids = set()
    for row in mapped_data:
        technique_id = row["MITRE Technique"]
        if technique_id != "Unknown" and technique_id not in seen_ids:
            techniques.append({"techniqueID": technique_id, "score": 100})
            seen_ids.add(technique_id)
    return {
        "version": "4.3",
        "name": "Mapped Techniques",
        "domain": "enterprise-attack",
        "techniques": techniques,
        "gradient": {"colors": ["#ffffff", "#66b1ff"], "minValue": 0, "maxValue": 100},
        "metadata": [],
        "filters": {"stages": ["act"], "platforms": ["Windows", "Linux", "macOS"]},
        "sorting": 0,
        "layout": "side",
        "hideDisabled": False,
        "showID": False,
        "selectTechniquesAcrossTactics": True
    }
