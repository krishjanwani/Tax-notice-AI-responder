import streamlit as st
import os
from google import genai
from dotenv import load_dotenv
import fitz 

# 1. SETUP
load_dotenv()
st.set_page_config(page_title="CA AI Final", layout="centered")
st.title("⚖️ Tax Notice AI-Responder")

# 2. API KEY (Automation)
# The code first looks for a secret .env file, then the sidebar
api_key = os.getenv("GEMINI_API_KEY")
user_key = st.sidebar.text_input("Enter API Key (Optional)", type="password")
final_key = user_key if user_key else api_key
# 1. Look for the key in Streamlit Secrets (Cloud)
# 2. Look for the key in the .env file (Local testing)
# 3. Look for the key in the sidebar (Manual entry)

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

user_key = st.sidebar.text_input("Override API Key (Optional)", type="password")
final_key = user_key if user_key else api_key

# 3. INTERFACE
file = st.file_uploader("Upload Tax Notice (PDF)", type="pdf")

if file and final_key:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    st.info("Notice Content Loaded.")
    
    if st.button("Generate Draft"):
        try:
            # Universal client format to bypass 404 errors
            client = genai.Client(api_key=final_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=f"Act as a CA. Draft a formal reply for: {text}"
            )
            st.success("Draft Generated!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"System Error: {e}")
elif not final_key:
    st.warning("Please provide an API Key to continue.")