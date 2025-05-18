def generate_justification(description, tactic, technique_id):
    if technique_id == "Unknown":
        return "The description could not be confidently mapped to a MITRE technique."
    return f"The rule aligns with MITRE tactic '{tactic}' and technique '{technique_id}'."
