# ============================================================
# METRO TICKET BOOKING APPLICATION - ADVANCED
# ============================================================

import streamlit as st
import qrcode
from gtts import gTTS
from io import BytesIO
import uuid
import time # Imported for simulation delays

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Metro Smart Booking",
    page_icon="🚇",
    layout="wide" # Changed to wide for better dashboard feel
)

# ---------------- SESSION STATE SETUP ----------------
if 'current_ticket' not in st.session_state:
    st.session_state.current_ticket = None

if 'booking_history' not in st.session_state:
    st.session_state.booking_history = []

# ============================================================
# LOGIC FUNCTIONS
# ============================================================
def calculate_fare(start, end, count, journey_type, travel_class):
    """
    Calculates fare based on:
    1. Distance (number of stations between start and end)
    2. Journey Type (Single/Return)
    3. Class (Standard/Premium)
    """
    # Define Station Indices
    station_map = {
        "Ameerpet": 1, "KPHB": 2, "Kukatpally": 3, 
        "Madhapur": 4, "Nizampet": 5, "Hitech City": 6, "Raidurg": 7
    }
    
    dist = abs(station_map[start] - station_map[end])
    base_rate = 10 # Cost per station distance
    
    # Minimum fare is 20
    fare_per_person = max(20, dist * base_rate)
    
    # Multipliers
    if journey_type == "Return":
        fare_per_person *= 1.8  # 10% discount on return
    
    if travel_class == "Premium":
        fare_per_person *= 1.5  # 50% extra for premium
        
    return int(fare_per_person * count)

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
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
    except:
        return None

# ============================================================
# SIDEBAR - HISTORY & CONTROLS
# ============================================================
with st.sidebar:
    st.title("⚙️ Menu")
    
    # Reset Button
    if st.button("🔄 Reset System", type="primary"):
        st.session_state.current_ticket = None
        st.session_state.booking_history = []
        st.rerun()

    st.markdown("---")
    st.header("📜 Booking History")
    
    if not st.session_state.booking_history:
        st.info("No tickets booked yet.")
    else:
        for idx, ticket in enumerate(reversed(st.session_state.booking_history)):
            with st.expander(f"Ticket #{ticket['id']}"):
                st.write(f"**Route:** {ticket['route']}")
                st.write(f"**Amount:** ₹{ticket['amount']}")
                st.write(f"**Date:** {ticket['time']}")

# ============================================================
# MAIN INTERFACE
# ============================================================
st.title("🚇 Metro Smart Booking System")

# Define Stations
station_list = ["Ameerpet", "KPHB", "Kukatpally", "Madhapur", "Nizampet", "Hitech City", "Raidurg"]

# Layout: 2 Columns for Form and Preview
col_form, col_preview = st.columns([1, 1])

with col_form:
    st.subheader("📝 Plan Your Journey")
    with st.form("booking_form"):
        passenger_name = st.text_input("Passenger Name", placeholder="John Doe")
        
        c1, c2 = st.columns(2)
        with c1:
            source = st.selectbox("From", station_list)
        with c2:
            dest = st.selectbox("To", station_list, index=1)
            
        c3, c4 = st.columns(2)
        with c3:
            j_type = st.radio("Journey Type", ["Single", "Return"])
        with c4:
            t_class = st.radio("Class", ["Standard", "Premium"])
            
        count = st.slider("Passengers", 1, 10, 1)
        
        # Live Price Estimation (Requires button press in Forms, so we calculate after)
        submit = st.form_submit_button("💳 Proceed to Pay")

# ============================================================
# PROCESSING LOGIC
# ============================================================
if submit:
    if not passenger_name:
        st.error("⚠️ Please enter passenger name.")
    elif source == dest:
        st.error("⚠️ Source and Destination cannot be the same.")
    else:
        # 1. Calculate Fare
        total_price = calculate_fare(source, dest, count, j_type, t_class)
        
        # 2. Simulate Payment Process
        with st.spinner("Connecting to Payment Gateway..."):
            time.sleep(1.5) # Fake delay
        
        with st.spinner("Generating Secure Ticket..."):
            time.sleep(1)
            
        # 3. Generate Ticket Data
        t_id = str(uuid.uuid4())[:8].upper()
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        
        ticket_details = f"""
METRO PASS - {t_class.upper()}
------------------------------
ID      : {t_id}
Name    : {passenger_name}
Route   : {source} >> {dest}
Type    : {j_type} Journey
Pax     : {count}
Paid    : ₹{total_price}
Date    : {timestamp}
------------------------------
        """
        
        voice_text = f"Booking confirmed for {passenger_name}. {j_type} ticket from {source} to {dest}. Have a safe journey."
        
        # 4. Save to Session State
        new_ticket = {
            "id": t_id,
            "text": ticket_details,
            "qr": generate_qr_code(ticket_details),
            "audio": generate_audio(voice_text),
            "route": f"{source} to {dest}",
            "amount": total_price,
            "time": timestamp,
            "success_msg": True # Flag to show success toast
        }
        
        st.session_state.current_ticket = new_ticket
        st.session_state.booking_history.append(new_ticket)

# ============================================================
# TICKET DISPLAY SECTION
# ============================================================
if st.session_state.current_ticket:
    t = st.session_state.current_ticket
    
    # Show success toast only once immediately after booking
    if t.get("success_msg"):
        st.toast(f"✅ Payment of ₹{t['amount']} Successful!")
        t["success_msg"] = False # Turn off flag
    
    with col_preview:
        st.subheader("🎟️ Your Digital Ticket")
        
        # Container with border effect
        with st.container(border=True):
            # Header
            st.markdown(f"### 🚄 Metro {t_class if 't_class' in locals() else 'Travel'} Pass")
            st.divider()
            
            # Ticket Content Layout
            tc1, tc2 = st.columns([2, 1])
            
            with tc1:
                st.code(t["text"], language="text")
                if t["audio"]:
                    st.audio(t["audio"], format="audio/mp3")
            
            with tc2:
                st.image(t["qr"], caption="Scan at Gate", use_container_width=True)
                
            st.divider()
            
            # Download Buttons
            db1, db2 = st.columns(2)
            with db1:
                st.download_button("⬇ QR Code", t["qr"], file_name=f"QR_{t['id']}.png", mime="image/png", use_container_width=True)
            with db2:
                st.download_button("⬇ Receipt", t["text"], file_name=f"Ticket_{t['id']}.txt", mime="text/plain", use_container_width=True)
