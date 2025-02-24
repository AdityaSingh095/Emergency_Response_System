```markdown
# Emergency Response System 🚨

![Emergency System Demo](https://via.placeholder.com/800x400.png?text=Emergency+Response+Demo) *Example screenshot placeholder*

A comprehensive emergency management system combining AI, geolocation, and real-time notifications to provide immediate crisis assistance.

## Features ✨

- 📝 **Multi-modal Input** - Text description or PDF document upload
- 🖼️ **Visual Analysis** - CLIP model for emergency type detection from images
- 📍 **Smart Geolocation** - Interactive Folium map with OpenCage integration
- 🚑 **AI-Powered First Aid** - Gemini-generated emergency instructions
- 📱 **SMS Alerts** - Twilio integration for government/user notifications
- 📄 **Document Processing** - PDF text extraction capabilities
- 🔍 **Entity Recognition** - Custom spaCy NLP pipeline for situation analysis

## Installation ⚙️

1. **Clone Repository**
```bash
git clone https://github.com/AdityaSingh095/emergency_response_system.git
cd emergency_response_system
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **API Configuration**  
Update `config.py` with your credentials:
```python
# Get keys from respective services
OPENCAGE_API_KEY = 'your_geocoding_key'
TWILIO_ACCOUNT_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_token' 
GEMINI_API_KEY = 'your_gemini_key'
```

## Usage 🚀

1. **Launch Application**
```bash
streamlit run app.py
```

2. **Input Methods**  
   - *Direct Input*: Describe emergency & location in text fields  
   - *Document Upload*: Submit PDF with emergency details  
   - *Image Upload*: Optional situation photo for visual analysis

3. **Emergency Processing**  
Click 🚨 `Process Emergency` to:
- Get real-time situation analysis
- View location on interactive map
- Receive AI-generated first aid instructions
- Trigger SMS alerts to authorities

## Project Structure 📂
```
emergency_response_system/
├── app.py                   # Main Streamlit interface
├── config.py                # API keys & configurations
├── utils/
│   ├── __init__.py          # Package initialization
│   ├── nlp_utils.py         # NLP entity extraction
│   ├── geo_utils.py         # Geolocation services
│   ├── document_utils.py    # PDF processing
│   ├── image_utils.py       # CLIP image analysis
│   ├── ai_utils.py          # Gemini AI integration
│   └── notification_utils.py # Twilio SMS alerts
```

## Dependencies 📦
```python
streamlit==1.31.0
spacy==3.7.2
PyPDF2==3.0.1
transformers==4.37.2
torch==2.1.0
google-generativeai==0.3.0
twilio==8.3.0
folium==0.14.0
opencage==1.4.2
requests==2.31.0
python-dotenv==0.19.0
```

## Configuration Guide 🔐
1. **API Services**  
   - [OpenCage Geocoding](https://opencagedata.com/) - For location coordinates  
   - [Twilio](https://www.twilio.com/) - SMS notifications  
   - [Google Gemini](https://ai.google.dev/) - AI first aid generation  

2. **Emergency Contacts**  
Modify `EMERGENCY_CONTACTS` in config.py:
```python
EMERGENCY_CONTACTS = {
    "Police": "100",
    "Fire": "101", 
    "Ambulance": "102"
}
```

## Troubleshooting ⚠️
| Issue | Solution |
|-------|----------|
| API Errors | Verify keys in config.py |
| Model Load Failures | Check internet connection |
| PDF Extraction Issues | Ensure document is text-based (not scanned) |
| Low Image Recognition | Use clear, well-lit photos |
| SMS Not Failed | Verify Twilio credentials | 

## Roadmap 🗺️
- [ ] Multi-language support
- [ ] Real-time emergency tracking
- [ ] Integration with official emergency APIs
- [ ] Offline mode for limited connectivity
- [ ] Voice command interface

## License 📄
MIT License - See [LICENSE](LICENSE) for full text

---

**Important Security Note** 🔒  
Never commit actual API keys to version control. Use environment variables or .gitignore for production deployments.
```
