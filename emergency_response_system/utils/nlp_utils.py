import spacy
import streamlit as st
from config import EMERGENCY_TYPES, SEVERITY_LEVELS

@st.cache_resource
def load_spacy_model():
    """Load the spaCy NLP model with caching"""
    try:
        return spacy.load("en_core_web_sm")  # Using smaller model
    except Exception as e:
        st.error(f"Error loading spaCy model: {e}")
        return None

def setup_entity_ruler(nlp):
    """Set up custom entity patterns for emergency response"""
    if not nlp or "entity_ruler" in nlp.pipe_names:
        return

    try:
        ruler = nlp.add_pipe("entity_ruler", before="ner")

        # Add emergency type patterns
        emergency_patterns = [
            {"label": "EMERGENCY_TYPE", "pattern": [{"lower": word}]}
            for word in EMERGENCY_TYPES
        ]

        # Add severity patterns
        severity_patterns = [
            {"label": "SEVERITY", "pattern": [{"lower": word}]}
            for word in SEVERITY_LEVELS
        ]

        # Add all patterns to the ruler
        ruler.add_patterns(emergency_patterns + severity_patterns)
    except Exception as e:
        st.error(f"Error setting up entity ruler: {e}")

def extract_entities(text, nlp):
    """Extract location, emergency type, and severity from text"""
    if not nlp:
        return {
            "location": [],
            "emergency_type": ["Unknown"],
            "severity": ["High"]  # Default severity
        }

    try:
        doc = nlp(text)
        entities = {
            "location": [],
            "emergency_type": [],
            "severity": []
        }

        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC']:
                entities["location"].append(ent.text)
            elif ent.label_ == "EMERGENCY_TYPE":
                entities["emergency_type"].append(ent.text)
            elif ent.label_ == "SEVERITY":
                entities["severity"].append(ent.text)

        # Set defaults if no entities found
        if not entities["emergency_type"]:
            entities["emergency_type"] = ["Unknown"]
        if not entities["severity"]:
            entities["severity"] = ["High"]

        return entities
    except Exception as e:
        st.error(f"Error extracting entities: {e}")
        return {
            "location": [],
            "emergency_type": ["Unknown"],
            "severity": ["High"]
        }
