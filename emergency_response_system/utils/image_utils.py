import torch
import streamlit as st
from PIL import Image

@st.cache_resource
def load_clip_model():
    """Load the CLIP model with caching"""
    try:
        from transformers import CLIPProcessor, CLIPModel
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        return model, processor
    except Exception as e:
        st.error(f"Error loading CLIP model: {e}")
        return None, None

def process_image(image_file, model, processor):
    """Process image to detect emergency type using CLIP model"""
    if not image_file or not model or not processor:
        return None, None

    try:
        image = Image.open(image_file).convert("RGB")
        text_inputs = ["fire", "earthquake", "flood", "car accident", "building collapse",
                      "cyclone", "landslide", "medical emergency"]

        inputs = processor(text=text_inputs, images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits_per_image, dim=1).cpu().numpy()
        predicted_label = text_inputs[probs.argmax()]
        return predicted_label, float(probs.max())
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None, None
