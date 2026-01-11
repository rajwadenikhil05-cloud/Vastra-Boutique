import streamlit as st
import pandas as pd
import google.generativeai as genai
from gradio_client import Client
from st_supabase_connection import SupabaseConnection

# --- 1. SECURE CONFIG ---
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
# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("VASTRA")
    menu = st.radio("SELECT HUB", ["📊 Dashboard", "🧾 Finance & AI", "📦 Inventory", "🎨 AI Stylist"])

# --- 3. LOGIC ---
if menu == "📊 Dashboard":
    st.title("Vastra Live Pulse")
    st.metric("Total Sales", "₹12,450")
    st.line_chart(pd.DataFrame([10, 20, 15, 45]))

elif menu == "🧾 Finance & AI":
    st.title("Financial Intelligence")
    if st.button("Generate Strategy"):
        response = ai_model.generate_content("Give me 3 tips for my boutique.")
        st.info(response.text)

elif menu == "📦 Inventory":
    st.title("Digital Warehouse")
    try:
        data = conn.query("*", table="inventory").execute()
        st.dataframe(pd.DataFrame(data.data))
    except Exception as e:
        st.error("Check if your Supabase table is named 'inventory'")

elif menu == "🎨 AI Stylist":
    st.title("AI Stylist Studio")
    cloth = st.file_uploader("Upload Cloth")
    person = st.file_uploader("Upload Person")
    if st.button("Generate AI Shoot"):
        if cloth and person:
            client = Client("yisol/IDM-VTON", hf_token=HF_TOKEN)
            result = client.predict(person, cloth, "Try this", api_name="/predict")

            st.image(result[0])


