
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
from utils.prompts import socratic_prompt, bias_prompt
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="ProcureThink AI", layout="wide")
st.title("🤖 ProcureThink AI: Critical Thinking for Procurement")

# Input box for procurement decision rationale
decision_text = st.text_area("📄 Paste your procurement decision rationale here:", height=200)

# Generate Socratic Questions
if st.button("🧠 Generate Socratic Questions") and decision_text:
    prompt = socratic_prompt(decision_text)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    questions = response.choices[0].message.content
    st.markdown("### Socratic Questions:")
    st.write(questions)

# Bias Detection
if st.button("🧩 Check for Cognitive Biases") and decision_text:
    bias_check = bias_prompt(decision_text)
    bias_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": bias_check}]
    )
    st.markdown("### Bias Assessment:")
    st.write(bias_response.choices[0].message.content)

# Tradeoff Visualizer
st.markdown("### ⚖️ Tradeoff Explorer")
cost = st.slider("Cost Priority", 0, 100, 50)
quality = st.slider("Quality Priority", 0, 100, 50)
delivery = st.slider("Delivery Speed Priority", 0, 100, 50)

labels = 'Cost', 'Quality', 'Delivery'
sizes = [cost, quality, delivery]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

# Save decision log
if st.button("💾 Save Decision to Log"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "decision_summary": decision_text,
        "cost_weight": cost,
        "quality_weight": quality,
        "delivery_weight": delivery
    }
    try:
        log_df = pd.read_csv("data/decision_logs.csv")
    except FileNotFoundError:
        log_df = pd.DataFrame()
    log_df = pd.concat([log_df, pd.DataFrame([log_entry])], ignore_index=True)
    log_df.to_csv("data/decision_logs.csv", index=False)
    st.success("✅ Decision saved to log.")
