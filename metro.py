# ============================================================
# METRO TICKET BOOKING - FIXED & RESPONSIVE
# ============================================================

import streamlit as st
import qrcode
from gtts import gTTS
from io import BytesIO
import uuid
import time

# ---------------- 1. PAGE CONFIG ----------------
st.set_page_config(
    page_title="Metro Smart Travel",
    page_icon="🚄",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default to save space
)

# ---------------- 2. CUSTOM CSS (FIXED FOR SCREEN FIT) ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3, h4, p, label, .stMarkdown { color: #ffffff !important; }

    /* Fix Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }

    /* TICKET CARD STYLING (FIXED) */
    .ticket-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        color: #333 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border-left: 8px solid #3a7bd5;
        margin-bottom: 20px;
        max-width: 400px; /* Prevents it from being too wide */
    }
    
    /* Text inside ticket must be dark */
    .ticket-card h3, .ticket-card h4, .ticket-card p, .ticket-card div, .ticket-card span {
        color: #333 !important;
    }

    /* Adjust padding for top of page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- 3. SESSION STATE ----------------
if 'current_ticket' not in st.session_state:
    st.session_state.current_ticket = None

# ---------------- 4. FUNCTIONS ----------------
def calculate_fare(start, end, count, journey_type, travel_class):
    # Simple logic for demo
    if start == end: return 0
    fare = 30 * count # Base fare
    if journey_type == "Return": fare *= 1.8
    if travel_class == "Premium": fare *= 1.5
    return int(fare)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2c3e50", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_audio(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer
    except: return None

# ---------------- 5. MAIN LAYOUT ----------------
st.markdown("<h3>🚄 Metro <span style='color:#00d2ff'>SmartBooking</span></h3>", unsafe_allow_html=True)

# Use columns with equal width to prevent squeezing
col1, col2 = st.columns([1, 1], gap="medium")

# === LEFT SIDE: FORM ===
with col1:
    with st.container(border=True):
        st.markdown("#### 📝 Journey Details")
        with st.form("booking_form"):
            passenger_name = st.text_input("Passenger Name")
            c1, c2 = st.columns(2)
            with c1: source = st.selectbox("From", ["Ameerpet", "KPHB", "Kukatpally", "Madhapur", "Nizampet"])
            with c2: dest = st.selectbox("To", ["Ameerpet", "KPHB", "Kukatpally", "Madhapur", "Nizampet"], index=1)
            
            c3, c4 = st.columns(2)
            with c3: j_type = st.radio("Type", ["Single", "Return"])
            with c4: t_class = st.radio("Class", ["Standard", "Premium"])
            
            count = st.slider("Passengers", 1, 5, 1)
            submitted = st.form_submit_button("💳 Pay & Book")

if submitted:
    if not passenger_name:
        st.error("Enter Name!")
    elif source == dest:
        st.error("Invalid Route!")
    else:
        fare = calculate_fare(source, dest, count, j_type, t_class)
        t_id = str(uuid.uuid4())[:8].upper()
        timestamp = time.strftime("%H:%M | %d-%b")
        
        ticket_data = {
            "id": t_id, "name": passenger_name, "route": f"{source} -> {dest}",
            "fare": fare, "class": t_class, "pax": count, "time": timestamp,
            "qr": generate_qr(f"{t_id}-{passenger_name}"),
            "audio": generate_audio(f"Booking confirmed for {passenger_name}")
        }
        st.session_state.current_ticket = ticket_data

# === RIGHT SIDE: TICKET ===
with col2:
    if st.session_state.current_ticket:
        t = st.session_state.current_ticket
        
        st.markdown("#### 🎟️ Your Ticket")
        
        # --- HTML FIX: NO INDENTATION INSIDE THE STRING ---
        # We assign the HTML to a variable first to keep it clean
        html_code = f"""
<div class="ticket-card">
    <div style="border-bottom: 2px dashed #ccc; padding-bottom:10px; margin-bottom:10px;">
        <h3 style="margin:0; color:#3a7bd5;">METRO RAIL</h3>
    </div>
    <div style="margin-bottom: 10px;">
        <p style="font-size:12px; color:#666; margin:0;">PASSENGER</p>
        <h4 style="margin:0; color:#333;">{t['name']}</h4>
    </div>
    <div style="display:flex; justify-content:space-between;">
        <div>
            <p style="font-size:12px; color:#666; margin:0;">ROUTE</p>
            <p style="font-weight:bold; margin:0; color:#333;">{t['route']}</p>
        </div>
        <div>
            <p style="font-size:12px; color:#666; margin:0;">AMOUNT</p>
            <p style="font-weight:bold; margin:0; color:#333;">₹{t['fare']}</p>
        </div>
    </div>
    <div style="margin-top:15px; font-size:12px; color:#888;">
        ID: {t['id']} | {t['time']}
    </div>
</div>
"""
        st.markdown(html_code, unsafe_allow_html=True)
        
        # QR and Audio
        c_qr, c_dl = st.columns([1, 2])
        with c_qr:
            st.image(t['qr'], width=120)
        with c_dl:
            if t['audio']: st.audio(t['audio'], format="audio/mp3")
            st.download_button("⬇ Download QR", t['qr'], file_name=f"QR_{t['id']}.png", mime="image/png")

    else:
        st.info("👈 Book a ticket to see it here.")
ss
