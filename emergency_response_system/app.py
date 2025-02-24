import streamlit as st
import folium
from streamlit_folium import folium_static

# Import configuration
from config import EMERGENCY_CONTACTS, EMERGENCY_INSTRUCTIONS

# Import utility modules
from utils.nlp_utils import load_spacy_model, setup_entity_ruler, extract_entities
from utils.geo_utils import get_lat_lon
from utils.document_utils import process_pdf
from utils.image_utils import load_clip_model, process_image
from utils.ai_utils import get_first_aid_response
from utils.notification_utils import notify_emergency_services

def main():
    st.title("Emergency Response System")

    # Create sidebar for emergency contacts and instructions
    with st.sidebar:
        st.header("📞 Emergency Contacts")
        for service, number in EMERGENCY_CONTACTS.items():
            st.write(f"{service}: {number}")

        st.header("🚨 Important Instructions")
        instruction_list = "\n".join([f"{i+1}. {instruction}" for i, instruction in enumerate(EMERGENCY_INSTRUCTIONS)])
        st.info(instruction_list)

    # Load models with error handling
    try:
        with st.spinner("Initializing emergency response system..."):
            nlp = load_spacy_model()
            clip_model, clip_processor = load_clip_model()
            setup_entity_ruler(nlp)
    except Exception as e:
        st.error(f"Error loading required models: {e}")
        return

    # Create tabs for different input methods
    input_tab, doc_tab = st.tabs(["📝 Direct Input", "📄 Document Upload"])

    situation_text = ""
    location = ""

    with input_tab:
        situation_text = st.text_area(
            "Describe the emergency situation:",
            placeholder="Example: There's a fire in the apartment building at 123 Main St. Multiple people need evacuation."
        )
        location = st.text_input(
            "Enter location:",
            placeholder="Example: 123 Main Street, City Name"
        )

    with doc_tab:
        uploaded_file = st.file_uploader("Upload PDF document", type="pdf")
        if uploaded_file:
            with st.spinner("Processing document..."):
                situation_text = process_pdf(uploaded_file)
                if situation_text:
                    st.success("Document processed successfully")
                    st.expander("View extracted text").write(situation_text)
                    location = st.text_input("Confirm location:", key="doc_location")
                else:
                    st.error("Could not extract text from document")

    # Image upload section with preview
    st.subheader("📸 Situation Image (Optional)")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Process emergency button with validation
    process_button = st.button("🚨 Process Emergency", use_container_width=True)

    if process_button:
        if not situation_text or not location:
            st.error("Please provide both situation description and location")
            return

        with st.spinner("Processing emergency information..."):
            # Create containers for different sections
            analysis_container = st.container()
            location_container = st.container()
            response_container = st.container()

            with analysis_container:
                st.subheader("🔍 Situation Analysis")

                # Process image if uploaded
                image_label = None
                if uploaded_image and clip_model and clip_processor:
                    image_label, confidence = process_image(uploaded_image, clip_model, clip_processor)
                    if image_label:
                        st.info(f"📸 Image Analysis: {image_label.title()} (Confidence: {confidence:.2f})")

                # Extract entities and display
                entities = extract_entities(situation_text, nlp)
                emergency_type = entities["emergency_type"][0] if entities["emergency_type"] else "Unknown"
                severity = entities["severity"][0] if entities["severity"] else "High"

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Emergency Type", emergency_type.title())
                with col2:
                    st.metric("Severity Level", severity.upper())

            with location_container:
                st.subheader("📍 Location Information")
                lat, lon = get_lat_lon(location)

                if lat and lon:
                    m = folium.Map(location=[lat, lon], zoom_start=15)
                    folium.Marker(
                        [lat, lon],
                        popup=location,
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                    folium_static(m)
                else:
                    st.warning("Could not locate the exact position on map")

            with response_container:
                st.subheader("🏥 Emergency Response")

                # Generate and display first aid response
                final_emergency_type = image_label if image_label else emergency_type
                first_aid = get_first_aid_response(final_emergency_type, situation_text)

                with st.expander("First Aid Instructions", expanded=True):
                    st.markdown(first_aid)

                # Send notifications
                notify_emergency_services(location, severity, final_emergency_type, situation_text)

if __name__ == "__main__":
    main()
