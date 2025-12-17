import streamlit as st
from openai import OpenAI

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import tempfile

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


def show_404_error(message="Something went wrong. Please try again."):
    st.markdown(
        f"""
        <div style="
            background-color:#1e293b;
            padding:30px;
            border-radius:16px;
            border:1px solid #334155;
        ">
            <h2 style="color:#f8fafc;">⚠️ Something went wrong</h2>
            <p style="color:#cbd5f5;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# DECISION LOGIC
# --------------------------------------------------

def select_kpis(goal):
    if goal == "Sales Growth":
        return ["Revenue", "Conversion Rate", "AOV"]
    if goal == "Brand Awareness":
        return ["Reach", "Engagement Rate", "Share of Voice"]
    if goal == "Lead Generation":
        return ["Leads", "CAC", "Conversion Rate"]
    if goal == "Customer Retention":
        return ["Repeat Rate", "LTV", "Churn"]


def prioritize_channels(budget):
    if budget < 5000:
        return ["Paid Search", "Organic Social", "Email"]
    elif budget < 20000:
        return ["Paid Search", "Meta Ads", "Influencers"]
    else:
        return ["Meta Ads", "Google Ads", "Influencers", "YouTube"]


def allocate_budget(budget, channels):
    split = budget / len(channels)
    return {ch: round(split, 2) for ch in channels}


def go_to_market_sequence(goal):
    if goal == "Brand Awareness":
        return [
            "Phase 1: Awareness launch",
            "Phase 2: Influencer amplification",
            "Phase 3: Retargeting",
        ]
    return [
        "Phase 1: Performance testing",
        "Phase 2: Scale winning channels",
        "Phase 3: Retention & optimization",
    ]

# --------------------------------------------------
# AI AGENTS
# --------------------------------------------------

def ai_call(prompt, client):
    def generate_campaign_ideas(context, client, tone, platforms, campaign_type):
    prompt = f"""
You are AR.AI, a senior creative strategist.

Brand strategy context:
{context}

Generate campaign ideas based on:
Campaign Types: {campaign_type}
Platforms: {platforms}
Tone: {tone}

Deliver:
1. FIVE Paid Ad angles
2. THREE Influencer campaign concepts
3. ONE Flagship brand campaign

For EACH idea include:
- Campaign name
- Platform
- Core hook
- Execution idea
- Primary KPI

Make ideas realistic, modern, and scroll-stopping.
"""
    return ai_call(prompt, client)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text


# --------------------------------------------------
# PDF EXPORT
# --------------------------------------------------

def generate_pdf(brand, explanation, kpis, channels, allocation, gtm):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"<b>{brand} – Marketing Strategy</b>", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(explanation.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(Spacer(1, 12))

    sections = [
        ("KPIs", kpis),
        ("Channels", channels),
        ("Budget Allocation (INR)", [f"{k}: ₹{v}" for k, v in allocation.items()]),
        ("Go-To-Market Plan", gtm),
    ]

    for title, items in sections:
        content.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
        for item in items:
            content.append(Paragraph(f"- {item}", styles["BodyText"]))
        content.append(Spacer(1, 12))

    doc.build(content)
    return temp_file.name

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Strategy Inputs")
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


    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market")

    goal = st.selectbox(
        "Primary Goal",
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"],
    )

    budget = st.number_input(
        "Total Marketing Budget (INR)",
        min_value=500,
        step=500
    )

    generate = st.button("🚀 Generate Strategy")

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.markdown("Configure inputs on the left. Strategy appears here.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# initialize memory
if "strategy_context" not in st.session_state:
    st.session_state.strategy_context = ""

# --------------------------------------------------
# STRATEGY GENERATION
# --------------------------------------------------

if generate:
    if not brand:
        st.warning("Please enter a Brand Name.")
    else:
        try:
            kpis = select_kpis(goal)
            channels = prioritize_channels(budget)
            allocation = allocate_budget(budget, channels)
            gtm = go_to_market_sequence(goal)

            prompt = f"""
You are AR.AI, a senior marketing intelligence system.

Brand: {brand}
Category: {category}
Market: {market}
Goal: {goal}
Budget: INR {budget}

KPIs: {kpis}
Channels: {channels}
Allocation: {allocation}
Go-To-Market: {gtm}

Generate a clear, client-ready marketing strategy.
"""

            with st.spinner("AR.AI building your strategy..."):
                explanation = ai_call(prompt, client)

            st.session_state.strategy_context = explanation

            card("📌 Executive Summary", explanation)
            card("🎯 KPIs", "<br>".join(kpis))
            card("📢 Channels", "<br>".join(channels))
            card("💰 Budget Allocation", "<br>".join([f"{k}: ₹{v}" for k, v in allocation.items()]))
            card("🚀 Go-To-Market Plan", "<br>".join(gtm))
            st.markdown("---")
st.markdown("## 🎯 Campaign Ideas")

with st.spinner("AR.AI generating campaign ideas..."):
    campaign_ideas = generate_campaign_ideas(
        st.session_state.strategy_context,
        client,
        tone,
        platforms,
        campaign_type
    )

card("🎨 Campaign Concepts", campaign_ideas)


            st.markdown("---")

            pdf_path = generate_pdf(brand, explanation, kpis, channels, allocation, gtm)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Strategy PDF",
                    f,
                    file_name=f"{brand}_Marketing_Strategy.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            show_404_error(str(e))

# --------------------------------------------------
# REFINEMENT SECTION (ALWAYS AVAILABLE)
# --------------------------------------------------

if st.session_state.strategy_context:
    st.markdown("---")
    st.markdown("## 💬 Refine or Redesign Strategy")

    user_input = st.text_input(
        "Ask AR.AI to refine, redesign, or make it more specific",
        key="refine_input"
    )

    if st.button("Send to AR.AI", key="send_refine"):
        if user_input.strip() == "":
            st.warning("Please enter a refinement request.")
        else:
            with st.spinner("AR.AI refining strategy..."):
                refinement = ai_call(
                    f"""
Current strategy:
{st.session_state.strategy_context}

User request:
{user_input}

Rules:
- Keep total budget unchanged
- Explain changes clearly
""",
                    client
                )

            st.markdown("### 🔄 Refined Strategy")
            st.markdown(refinement)

            st.session_state.strategy_context += "\n\nREFINEMENT:\n" + refinement
            st.session_state.refine_input = ""
