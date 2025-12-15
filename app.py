import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="AR.AI – Marketing Intelligence", layout="wide")

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.subheader("Turn brand inputs into actionable marketing strategies")

# ---------- INPUTS ----------
with st.form("marketing_form"):
    # REMOVED VALUE PARAMETERS TO ENSURE DYNAMIC INPUT IS USED
    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market (e.g. India Urban, US SMBs)")
    goal = st.selectbox(
        "Primary Marketing Goal",
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"]
    )
    kpis = st.multiselect(
        "Key Measurable Metrics",
        ["Revenue", "ROAS (Return on Ad Spend)", "CAC (Customer Acquisition Cost)", "Engagement Rate", "Conversion Rate", "AOV (Average Order Value)", "Repeat Rate"]
    )

    submitted = st.form_submit_button("Generate Strategy")

# ---------- OUTPUT ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if submitted and brand:

    st.success(f"AR.AI Strategy Generated for {brand}")

    prompt = f"""
You are AR.AI, a senior marketing intelligence engine.

Create a CUSTOM marketing strategy.
Do not reuse templates.
Do not assume food or luxury unless relevant.

Brand: {brand}
Category: {category}
Market: {market}
Goal: {goal}
KPIs: {", ".join(kpis)}

Give output in this format:
1. Quarterly Objective
2. Target Audience & Positioning
3. Channel Strategy
4. Content Strategy
5. Budget Split (percentage)
6. KPIs
7. 90-Day Plan
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    st.markdown(response.choices[0].message.content)

else:
    if submitted:
        st.warning("Please enter a Brand Name.")
