import spacy
import re

nlp = spacy.load("en_core_web_md")

def clean_value(val):
    return val.replace("\n", " ").strip()

def extract_fields(text):
    doc = nlp(text)
    results = {
        "dates": [],
        "people": [],
        "locations": [],
        "emails": [],
        "phones": [],
    }

    def clean_entity(text):
        # Remove newlines, labels like 'Address', 'Phone', etc.
        text = text.replace("\n", " ").strip()
        text = re.sub(r"\b(Address|Phone|Email)\b", "", text, flags=re.IGNORECASE)
        return text.strip()

    for ent in doc.ents:
        cleaned = clean_entity(ent.text)
        if ent.label_ == "DATE" and cleaned:
            results["dates"].append(cleaned)
        elif ent.label_ == "PERSON" and cleaned:
            results["people"].append(cleaned)
        elif ent.label_ in ["GPE", "LOC"] and cleaned:
            results["locations"].append(cleaned)


    results["emails"] = [clean_value(e) for e in re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)]
    results["phones"] = [clean_value(p) for p in re.findall(r"\(?\+?[0-9]{1,4}\)?[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{4,}", text)]

    return results
