# 🚇 Metro Ticket Booking System

A Python-based web application built with **Streamlit** that simulates a metro rail ticket booking interface. This application allows users to book tickets, generates unique QR codes, provides downloadable receipts, and plays voice announcements.

## 🌟 Features

* **User-Friendly Interface:** Simple form to input passenger details and select stations.
* **Fare Calculation:** Automatic fare calculation based on the number of tickets.
* **QR Code Generation:** Generates a scannable QR code containing ticket details.
* **Digital Downloads:**
    * Download QR Code (PNG format).
    * Download Ticket Receipt (Text format).
* **Voice Announcement:** Uses Google Text-to-Speech (gTTS) to play a confirmation announcement.
* **State Management:** Uses Streamlit Session State to persist ticket data across interactions.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit:** For the web interface.
* **QRcode:** For generating Quick Response codes.
* **gTTS (Google Text-to-Speech):** For generating audio announcements.
* **IO & UUID:** Standard libraries for file handling and unique ID generation.

## 📋 Prerequisites

Ensure you have Python installed on your system. You will need an active internet connection for the voice generation (gTTS) to work.

## 🚀 Installation & Setup

1.  **Clone the repository (or create a folder):**
    ```bash
    mkdir metro-booking
    cd metro-booking
    ```

2.  **Create a virtual environment (Optional but Recommended):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    Create a file named `requirements.txt` or run the command directly:
    ```bash
    pip install streamlit qrcode[pil] gTTS
    ```

4.  **Save the Application Code:**
    Save your Python code (the corrected version) into a file named `app.py`.

## ▶️ How to Run

Run the Streamlit application using the following terminal command:

```bash
streamlit run app.py
