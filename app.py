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
# AI CORE
# --------------------------------------------------

def ai_call(prompt, client):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text


def generate_campaign_ideas(context, client, tone, platforms, campaign_type):
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

Make ideas modern, realistic, and scroll-stopping.
"""
    return ai_call(prompt, client)

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

    st.markdown("---")
    st.markdown("## 🎨 Campaign Preferences")

    campaign_type = st.multiselect(
        "Campaign Focus",
        ["Paid Ads", "Infl]()
