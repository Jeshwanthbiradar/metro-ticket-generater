# ============================================================
# METRO TICKET BOOKING APPLICATION (FIXED)
# ============================================================

import streamlit as st
import qrcode
from gtts import gTTS
from io import BytesIO
import uuid

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Metro Ticket Booking",
    page_icon="🚇",
    layout="centered"
)

# ---------------- SESSION STATE INITIALIZATION ----------------
# This ensures data persists when buttons (like Download) are clicked
if 'ticket_data' not in st.session_state:
    st.session_state.ticket_data = None

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def generate_qr_code(ticket_text):
    """Generates a QR code image from ticket text."""
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_voice_audio(message):
    """Converts text to speech using gTTS."""
    try:
        tts = gTTS(text=message, lang="en", slow=False)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# ============================================================
# MAIN UI
# ============================================================
st.title("🚇 METRO TICKET BOOKING SYSTEM")

st.markdown("### Passenger Details")

# List of metro stations
stations = ["Ameerpet", "KPHB", "Kukatpally", "Madhapur", "Nizampet"]

with st.form("booking_form"):
    passenger_name = st.text_input("Passenger Name")
    
    col1, col2 = st.columns(2)
    with col1:
        source_station = st.selectbox("Source Station", stations)
    with col2:
        destination_station = st.selectbox("Destination Station", stations)
    
    ticket_count = st.number_input("Number of Tickets", min_value=1, max_value=5, step=1)
    
    # Fare Calculation
    PRICE_PER_TICKET = 30
    total_fare = ticket_count * PRICE_PER_TICKET
    
    # Submit Button
    submitted = st.form_submit_button("🎫 Book Ticket")

# ============================================================
# BOOKING LOGIC
# ============================================================
if submitted:
    # Validation
    if not passenger_name.strip():
        st.error("⚠️ Passenger name is required.")
    elif source_station == destination_station:
        st.error("⚠️ Source and Destination cannot be the same.")
    else:
        # Generate Data
        ticket_id = str(uuid.uuid4())[:8]
        
        ticket_text = f"""
METRO TICKET
-------------------------
Ticket ID : {ticket_id}
Passenger : {passenger_name}
From      : {source_station}
To        : {destination_station}
Tickets   : {ticket_count}
Amount    : ₹{total_fare}
-------------------------
        """
        
        voice_msg = (
            f"Hello {passenger_name}. Ticket booked from {source_station} to "
            f"{destination_station}. Total fare is {total_fare} rupees."
        )

        # Save to Session State (Persist Data)
        st.session_state.ticket_data = {
            "text": ticket_text,
            "qr_buffer": generate_qr_code(ticket_text),
            "audio_buffer": generate_voice_audio(voice_msg),
            "ticket_id": ticket_id
        }
        st.success("✅ Ticket Booked Successfully!")

# ============================================================
# DISPLAY RESULTS (From Session State)
# ============================================================
if st.session_state.ticket_data:
    data = st.session_state.ticket_data
    
    st.markdown("---")
    col_ticket, col_qr = st.columns([1.5, 1])
    
    with col_ticket:
        st.markdown("### 🧾 Ticket Details")
        st.code(data["text"], language="text")
        
        # Audio Player
        if data["audio_buffer"]:
            st.markdown("### 🔊 Announcement")
            st.audio(data["audio_buffer"], format="audio/mp3")

    with col_qr:
        st.markdown("### 📱 QR Code")
        st.image(data["qr_buffer"], width=200)

    # Download Section
    st.markdown("### ⬇ Download Options")
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        st.download_button(
            label="Download QR (PNG)",
            data=data["qr_buffer"],
            file_name=f"Metro_{data['ticket_id']}.png",
            mime="image/png"
        )
        
    with d_col2:
        st.download_button(
            label="Download Ticket (TXT)",
            data=data["text"],
            file_name=f"Ticket_{data['ticket_id']}.txt",
            mime="text/plain"
        )
