import streamlit as st
import pandas as pd
import google.generativeai as genai
from gradio_client import Client
from st_supabase_connection import SupabaseConnection

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Vastra by NV",
    page_icon="🧵",
    layout="wide"
)

# --------------------------------------------------
# 🔑 HARD-CODED KEYS (TEMPORARY, FOR DEMO)
# --------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDjyEStNmeRqveZsP7WdAEIbk3nZntrLdc"
HF_TOKEN = "hf_IoCpl0BrQHYyTQueHnJypYmZDPQInmNhHs"

SUPABASE_URL = "https://pzozsuvtdtdnooqutrgp.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_Sbm1g1dCi3qGNs_uzxAroQ_-_od4t9C"

# --------------------------------------------------
# INITIALIZE SERVICES
# --------------------------------------------------
genai.configure(api_key=GOOGLE_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

conn = st.connection(
    "supabase",
    type=SupabaseConnection,
    url=SUPABASE_URL,
    key=SUPABASE_ANON_KEY
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("🧵 VASTRA")
    st.caption("by Nikhilesh Vastralaya")

    menu = st.radio(
        "Select Hub",
        ["📊 Dashboard", "🧾 Finance & AI", "📦 Inventory", "🎨 AI Stylist"]
    )

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if menu == "📊 Dashboard":
    st.title("📊 Vastra Business Pulse")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", "₹12,450", "+₹520")
    col2.metric("Orders Today", "18", "+3")
    col3.metric("Low Stock Items", "4")

    st.line_chart(pd.DataFrame({"Sales": [10, 25, 15, 45, 30, 60, 40]}))

# --------------------------------------------------
# FINANCE & AI
# --------------------------------------------------
elif menu == "🧾 Finance & AI":
    st.title("🧠 AI Business Advisor")

    prompt = st.text_area(
        "Ask AI about your boutique",
        "Give me 3 ideas to increase sales for a local clothing store"
    )

    if st.button("Generate AI Insight"):
        with st.spinner("Gemini is thinking..."):
            response = ai_model.generate_content(prompt)
            st.success(response.text)

# --------------------------------------------------
# INVENTORY
# --------------------------------------------------
elif menu == "📦 Inventory":
    st.title("📦 Digital Inventory")

    try:
        result = conn.query("*", table="inventory").execute()
        df = pd.DataFrame(result.data)

        if df.empty:
            st.warning("Inventory table is empty")
        else:
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.warning("Inventory table not found (this is OK for demo)")

# --------------------------------------------------
# AI STYLIST
# --------------------------------------------------
elif menu == "🎨 AI Stylist":
    st.title("🎨 AI Virtual Try-On")

    cloth = st.file_uploader("Upload Cloth Image", type=["jpg", "png"])
    person = st.file_uploader("Upload Person Image", type=["jpg", "png"])

    if cloth and person and st.button("Generate Try-On"):
        with st.spinner("Generating AI try-on..."):
            client = Client("yisol/IDM-VTON", hf_token=HF_TOKEN)
            result = client.predict(
                person,
                cloth,
                "Virtual try on",
                api_name="/predict"
            )
            st.image(result[0])
