import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AR.AI – Marketing Intelligence",
    layout="wide"
)

# --------------------------------------------------
# UI HELPERS
# --------------------------------------------------

def card(title, content):
    st.markdown(
        f"""
        <div style="
            background-color:transparent;
            padding:20px;
            border-radius:14px;
            margin-bottom:20px;
            border:1px solid #1e293b;
        ">
            <h3 style="color:#f8fafc;">{title}</h3>
            <div style="color:#cbd5f5; font-size:16px;">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# AI CORE
# --------------------------------------------------

def ai_call(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

def generate_campaign_ideas(context, tone, platforms, campaign_type):
    prompt = f"""
You are AR.AI, a senior creative strategist.

Brand strategy context:
{context}

Campaign Types: {campaign_type}
Platforms: {platforms}
Tone: {tone}

Generate:
1. FIVE Paid Ad angles
2. THREE Influencer campaign concepts
3. ONE Flagship brand campaign

For EACH idea include:
- Campaign name
- Platform
- Core hook
- Execution idea
- Primary KPI
"""
    return ai_call(prompt)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Strategy Inputs")

    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market")

    goal = st.selectbox(
        "Primary Goal",
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"]
    )

    budget = st.number_input(
        "Total Marketing Budget (INR)",
        min_value=500,
        step=500
    )
    budget_period = st.radio(
    "Budget Type",
    ["Monthly", "Annual"],
    horizontal=True
)

    st.markdown("---")
    st.markdown("## 🎨 Campaign Preferences")

    campaign_type = st.multiselect(
        "Campaign Focus",
        ["Paid Ads", "Influencer Marketing", "Brand Campaign"],
        default=["Paid Ads", "Influencer Marketing"]
    )

    tone = st.selectbox(
        "Creative Tone",
        ["Bold", "Premium", "Emotional", "Fun", "Minimal"]
    )

    platforms = st.multiselect(
        "Primary Platforms",
        ["Instagram", "YouTube", "Google", "Meta", "LinkedIn"],
        default=["Instagram", "Meta"]
    )

    st.markdown("---")
    generate = st.button("🚀 Generate Strategy", use_container_width=True)

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.markdown("Configure inputs on the left. Strategy appears here.")

# --------------------------------------------------
# STRATEGY GENERATION
# --------------------------------------------------

if generate:
    if not brand:
        st.warning("Please enter a Brand Name.")
    else:
    monthly_budget = budget if budget_period == "Monthly" else budget / 12

    # 1️⃣ Generate Strategy
    with st.spinner("AR.AI building your strategy..."):
        strategy_prompt = f"""
You are AR.AI, a senior marketing intelligence system.

Brand: {brand}
Category: {category}
Market: {market}
Goal: {goal}

Budget:
- Total Budget: INR {budget}
- Budget Type: {budget_period}
- Monthly Equivalent: INR {round(monthly_budget)}

Deliver a structured strategy with the following sections:

1. Budget Logic
2. Channel Mix & Allocation
3. Online Strategy
4. Offline Strategy
5. Key Measurables (CPC, CPL, CTR, CPA, ROAS)
"""
        strategy = ai_call(strategy_prompt)

    card("📌 Marketing Strategy", strategy)

    # 2️⃣ Generate Campaign Ideas
    st.markdown("---")
    st.markdown("## 🎯 Campaign Ideas")

    with st.spinner("AR.AI generating campaign ideas..."):
        campaigns = generate_campaign_ideas(
            strategy,
            tone,
            platforms,
            campaign_type
        )

    card("🎨 Campaign Concepts", campaigns)

    # 3️⃣ Create Download Content (AFTER BOTH EXIST)
    download_content = f"""
==============================
MARKETING STRATEGY
==============================

{strategy}

==============================
CAMPAIGN IDEAS
==============================

{campaigns}
"""

    # 4️⃣ Download Button (NOW SAFE)
    st.download_button(
        label="⬇️ Download Strategy + Campaign Ideas",
        data=download_content,
        file_name=f"{brand}_strategy_and_campaigns.txt",
        mime="text/plain"
    )
   
"""

        st.markdown("---")
st.markdown("## 💬 Refine or Talk to AR.AI")

user_refine_input = st.text_area(
    "Ask AR.AI to refine, improve, or modify the strategy",
    placeholder="Example: Make this more aggressive for Instagram, reduce offline spend, or improve CPL"
)

if st.button("Send to AR.AI"):
    if user_refine_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        with st.spinner("AR.AI refining strategy..."):
            refine_prompt = f"""
You are AR.AI, a senior marketing intelligence system.

Here is the current strategy:
{strategy}

User request:
{user_refine_input}

Rules:
- Keep budget constraints realistic
- Clearly explain changes

            refined_response = ai_call(refine_prompt)

        st.markdown("### 🔄 Refined Response")
        st.markdown(refined_response)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "<center style='color:#64748b;'>AR.AI © Marketing Intelligence Engine</center>",
    unsafe_allow_html=True
)
