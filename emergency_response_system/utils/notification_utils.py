import streamlit as st
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, NOTIFICATION_NUMBERS

def send_emergency_sms(to_number, message):
    """Send emergency SMS using Twilio API"""
    if not to_number or not message:
        return False, "Missing phone number or message"

    try:
        # Initialize the Twilio client with your credentials
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send the SMS using the Twilio API
        sent_message = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,  # Use your verified Twilio number
            to=to_number
        )
        return True, sent_message.sid
    except Exception as e:
        return False, str(e)

def notify_emergency_services(location, severity, emergency_type, situation_text):
    """Handles emergency notifications with multiple fallback options"""
    if not location or not severity or not emergency_type:
        st.warning("Missing information for emergency notification")
        return {}

    # Format messages
    gov_message = (
        f"🚨 URGENT EMERGENCY ALERT!\n"
        f"Location: {location}\n"
        f"Emergency: {emergency_type}\n"
        f"Severity: {severity}\n"
        f"Details: {situation_text[:100]}..."  # Truncate long messages
    )

    user_message = (
        f"🔹 Emergency services have been notified.\n"
        f"Location: {location}\n"
        f"Emergency: {emergency_type}\n"
        f"Help is being coordinated.\n"
        f"Stay safe and follow emergency instructions."
    )

    # Log notifications for verification
    st.subheader("Emergency Notifications")
    with st.expander("View Emergency Alert Details"):
        st.markdown("### 🚨 Government Alert")
        st.code(gov_message)
        st.markdown("### 👤 User Alert")
        st.code(user_message)

    # Send SMS notifications
    results = {}
    for recipient, number in NOTIFICATION_NUMBERS.items():
        message = gov_message if recipient == "government" else user_message
        success, result = send_emergency_sms(number, message)
        results[recipient] = {"success": success, "result": result}

        if success:
            st.success(f"✅ Alert sent to {recipient}")
        else:
            st.warning(f"⚠️ Could not send SMS to {recipient}. Alert logged in system.")

    return results
