from tools.omop_vocabulary import lookup_concepts

def resolve(parsed):
    concept_ids = []
    for condition in parsed["conditions"]:
        concept_ids += lookup_concepts(condition)
    return {"concept_ids": concept_ids, "age_filter": parsed["age_filter"]}
