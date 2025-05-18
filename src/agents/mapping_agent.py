from embedding_model import map_description_to_technique, load_mitre_techniques

def map_to_mitre_technique(description, mitre_techniques, top_n=3):
    import numpy as np
    from sentence_transformers import util
    from embedding_model import model

    description_embedding = model.encode(description, convert_to_tensor=True)
    scored = []

    for tid, full_text, tactic in mitre_techniques:
        technique_embedding = model.encode(full_text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(description_embedding, technique_embedding).item()
        scored.append((score, tid, full_text.split(":")[0], tactic))

    top_matches = sorted(scored, reverse=True)[:top_n]
    return [(tid, name, tactic) for _, tid, name, tactic in top_matches]
