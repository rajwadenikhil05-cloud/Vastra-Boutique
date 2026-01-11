import streamlit as st
import pandas as pd
import google.generativeai as genai
from gradio_client import Client
from st_supabase_connection import SupabaseConnection

# --- 1. SECURE CONFIG ---
# Use the NAMES from your Secrets tab, not the actual values!
GOOGLE_KEY = st.secrets["AIzaSyD-H7Q_tUo5EXaQsNB5286iSH1rKuiy6fs"]
HF_TOKEN = st.secrets["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"]
SUPABASE_URL = st.secrets["https://pzozsuvtdtdnooqutrgp.supabase.co"]
SUPABASE_KEY = st.secrets["sb_publishable_Sbm1g1dCi3qGNs_uzxAroQ_-_od4t9C"]

# Initialize AI & DB
genai.configure(api_key=GOOGLE_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash-latest')
conn = st.connection("supabase", 
                     type=SupabaseConnection, 
                     url=SUPABASE_URL, 
                     key=SUPABASE_KEY)

# --- 2. THE PREMIUM INTERFACE (CRED Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #030303; overflow: hidden; }
    @keyframes roam {
        0% { transform: translate(0,0); }
        50% { transform: translate(50px, 100px); }
        100% { transform: translate(0,0); }
    }
    .bg-asset { position: fixed; z-index: -1; opacity: 0.1; font-size: 150px; animation: roam 20s infinite; }
    div[data-testid="stMetric"], .stDataFrame {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
    }
    </style>
    <div class="bg-asset" style="top:10%; left:10%;">👕</div>
    <div class="bg-asset" style="top:60%; left:75%;">👗</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (The Navigation) ---
with st.sidebar:
    st.title("VASTRA")
    st.caption("by Nikhilesh Vastralaya")
    st.divider()
    menu = st.radio("SELECT HUB", ["📊 Dashboard", "🧾 Finance & AI", "📦 Inventory", "🎨 AI Stylist"])

# --- 4. HUB LOGIC (Replacing all previous errors) ---

if menu == "📊 Dashboard":
    st.title("Vastra Live Pulse")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", "₹12,450", "+520")
    c2.metric("New Arrivals", "12", "This Week")
    c3.metric("Customer Flow", "145", "+20%")
    st.line_chart(pd.DataFrame({'Sales': [10, 25, 15, 45, 30]}))

elif menu == "🧾 Finance & AI":
    st.title("Financial Intelligence")
    st.subheader("Google AI Business Strategy")
    if st.button("Generate Strategy"):
        with st.spinner("Analyzing..."):
            response = ai_model.generate_content("Give me 3 tips for my boutique.")
            st.info(response.text)

elif menu == "📦 Inventory":
    st.title("Digital Warehouse")
    try:
        data = conn.query("*", table="inventory").execute()
        st.dataframe(pd.DataFrame(data.data), use_container_width=True)
    except:
        st.warning("Database connecting...")

elif menu == "🎨 AI Stylist":
    st.title("AI Stylist Studio")
    cloth = st.file_uploader("Upload Cloth")
    person = st.file_uploader("Upload Person")
    if st.button("Generate AI Shoot"):
        client = Client("yisol/IDM-VTON", hf_token=HF_TOKEN)
        result = client.predict(person, cloth, "Try this", api_name="/predict")

        st.image(result)
