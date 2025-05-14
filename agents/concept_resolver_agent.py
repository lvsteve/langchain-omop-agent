from tools.omop_vocabulary import lookup_concepts

def resolve(parsed):
    concept_ids = []
    for condition in parsed.get("conditions", []):
        ids = lookup_concepts(condition)
        if ids:
            concept_ids += ids
        else:
            print(f"[WARN] No concept IDs found for condition: '{condition}'")
    if not concept_ids:
        print("[ERROR] No valid concept IDs found for any condition. Query will return no results.")
        return {"concept_ids": None, "age_filter": parsed.get("age_filter"), "visit_type": parsed.get("visit_type"), "year": parsed.get("year")}
    return {"concept_ids": concept_ids, "age_filter": parsed.get("age_filter"), "visit_type": parsed.get("visit_type"), "year": parsed.get("year")}
