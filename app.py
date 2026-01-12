import streamlit as st
import pandas as pd
import google.generativeai as genai
from gradio_client import Client
from st_supabase_connection import SupabaseConnection

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Vastra by NV",
    page_icon="🧵",
    layout="wide"
)

# --------------------------------------------------
# 2. LOAD SECRETS SAFELY
# --------------------------------------------------
GOOGLE_KEY = st.secrets.get("AIzaSyDjyEStNmeRqveZsP7WdAEIbk3nZntrLdc")
HF_TOKEN = st.secrets.get("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")
SUPABASE_URL = st.secrets.get("https://pzozsuvtdtdnooqutrgp.supabase.co")
SUPABASE_KEY = st.secrets.get("sb_publishable_Sbm1g1dCi3qGNs_uzxAroQ_-_od4t9C")

if not GOOGLE_KEY:
    st.error("❌ Google API Key missing in Streamlit Secrets")
    st.stop()

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase credentials missing in Streamlit Secrets")
    st.stop()

# --------------------------------------------------
# 3. INITIALIZE SERVICES
# --------------------------------------------------
# Gemini
genai.configure(api_key=GOOGLE_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# Supabase
conn = st.connection(
    "supabase",
    type=SupabaseConnection,
    url=SUPABASE_URL,
    key=SUPABASE_KEY
)

# --------------------------------------------------
# 4. SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("🧵 VASTRA")
    st.caption("by Nikhilesh Vastralaya")

    menu = st.radio(
        "Select Hub",
        ["📊 Dashboard", "🧾 Finance & AI", "📦 Inventory", "🎨 AI Stylist"]
    )

# --------------------------------------------------
# 5. DASHBOARD
# --------------------------------------------------
if menu == "📊 Dashboard":
    st.title("📊 Vastra Business Pulse")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", "₹12,450", "+₹520")
    col2.metric("Orders Today", "18", "+3")
    col3.metric("Low Stock Items", "4")

    st.subheader("Weekly Sales Trend")
    st.line_chart(pd.DataFrame({"Sales": [10, 25, 15, 45, 30, 60, 40]}))

# --------------------------------------------------
# 6. FINANCE & AI
# --------------------------------------------------
elif menu == "🧾 Finance & AI":
    st.title("🧠 AI Business Advisor")

    prompt = st.text_area(
        "Ask AI about your business",
        "Give me 3 marketing ideas to increase boutique sales"
    )

    if st.button("Generate AI Insight"):
        with st.spinner("Gemini is analyzing your business..."):
            try:
                response = ai_model.generate_content(prompt)
                st.success(response.text)
            except Exception as e:
                st.error("AI generation failed")
                st.exception(e)

# --------------------------------------------------
# 7. INVENTORY
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
        st.error("Could not fetch inventory data")
        st.exception(e)

# --------------------------------------------------
# 8. AI STYLIST (OPTIONAL / ADVANCED)
# --------------------------------------------------
elif menu == "🎨 AI Stylist":
    st.title("🎨 AI Virtual Try-On (Experimental)")

    if not HF_TOKEN:
        st.warning("Hugging Face token not configured")
        st.stop()

    cloth = st.file_uploader("Upload Cloth Image", type=["png", "jpg"])
    person = st.file_uploader("Upload Person Image", type=["png", "jpg"])

    if cloth and person and st.button("Generate AI Try-On"):
        with st.spinner("Generating AI try-on..."):
            try:
                client = Client(
                    "yisol/IDM-VTON",
                    hf_token=HF_TOKEN
                )
                result = client.predict(
                    person,
                    cloth,
                    "Virtual try on",
                    api_name="/predict"
                )
                st.image(result[0], caption="AI Generated Look")

            except Exception as e:
                st.error("AI Try-On failed")
                st.exception(e)

