from sentence_transformers import SentenceTransformer, util
import torch
import json

model = SentenceTransformer("all-mpnet-base-v2")

def load_mitre_techniques(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return [(item["techniqueID"], f"{item['name']}: {item.get('description', '')}", item["tactic"]) for item in data]

def map_description_to_technique(description, mitre_techniques, top_n=3):
    description_embedding = model.encode(description, convert_to_tensor=True)

    technique_ids = []
    texts = []
    tactics = []

    for tid, full_text, tactic in mitre_techniques:
        technique_ids.append(tid)
        texts.append(full_text)
        tactics.append(tactic)

    technique_embeddings = model.encode(texts, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(description_embedding, technique_embeddings)[0]

    top_results = torch.topk(cosine_scores, k=top_n)
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append((technique_ids[idx], texts[idx].split(":")[0], tactics[idx]))

    return results
