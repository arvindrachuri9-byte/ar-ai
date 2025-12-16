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
            background-color:#0f172a;
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


def show_404_error():
    st.markdown(
        """
        <div style="
            background-color:#1e293b;
            padding:30px;
            border-radius:16px;
            border:1px solid #334155;
        ">
            <h2 style="color:#f8fafc;">⚠️ Something went wrong</h2>
            <p style="color:#cbd5f5;">
            AR.AI encountered an internal issue while building this strategy.
            Please try again or refine your inputs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# DECISION LOGIC (AR.AI BRAIN)
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
    allocation = {}
    split = budget / len(channels)
    for ch in channels:
        allocation[ch] = round(split, 2)
    return allocation


def go_to_market_sequence(goal):
    if goal == "Brand Awareness":
        return [
            "Phase 1: Awareness launch",
            "Phase 2: Influencer amplification",
            "Phase 3: Retargeting"
        ]
    else:
        return [
            "Phase 1: Performance testing",
            "Phase 2: Scale winning channels",
            "Phase 3: Retention & optimization"
        ]

# --------------------------------------------------
# MULTI-AGENT AI
# --------------------------------------------------

def strategy_agent(context, client):
    return client.responses.create(
        model="gpt-4o-mini",
        input=f"You are a brand strategist.\n\n{context}"
    ).output_text


def media_agent(context, client):
    return client.responses.create(
        model="gpt-4o-mini",
        input=f"You are a media planning expert.\n\n{context}"
    ).output_text


def growth_agent(context, client):
    return client.responses.create(
        model="gpt-4o-mini",
        input=f"You are a growth analyst.\n\n{context}"
    ).output_text


def synthesis_agent(strategy, media, growth, client):
    return client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are AR.AI, a CMO-level marketing intelligence system.

Synthesize the following inputs into ONE clear, client-ready strategy.

STRATEGY:
{strategy}

MEDIA:
{media}

GROWTH:
{growth}
"""
    ).output_text

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

    for section, items in [
        ("KPIs", kpis),
        ("Channels", channels),
        ("Budget Allocation (INR)", [f"{k}: ₹{v}" for k, v in allocation.items()]),
        ("Go-To-Market Plan", gtm),
    ]:
        content.append(Paragraph(f"<b>{section}</b>", styles["Heading2"]))
        for i in items:
            content.append(Paragraph(f"- {i}", styles["BodyText"]))
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
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"]
    )

    budget = st.number_input("Total Marketing Budget (INR)", min_value=500, step=500)

    generate = st.button("🚀 Generate Strategy")

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.markdown("Configure inputs on the left. Strategy appears here.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if generate and brand:
    try:
        kpis = select_kpis(goal)
        channels = prioritize_channels(budget)
        allocation = allocate_budget(budget, channels)
        gtm = go_to_market_sequence(goal)

        context = f"""
Brand: {brand}
Category: {category}
Market: {market}
Goal: {goal}
Budget: INR {budget}
KPIs: {kpis}
Channels: {channels}
Allocation: {allocation}
Go-To-Market: {gtm}
"""

        with st.spinner("AR.AI agents collaborating..."):
            s = strategy_agent(context, client)
            m = media_agent(context, client)
            g = growth_agent(context, client)
            explanation = synthesis_agent(s, m, g, client)

        st.session_state.strategy_context = explanation

        card("📌 Executive Summary", explanation)
        card("🎯 KPIs", "<br>".join(kpis))
        card("📢 Channels", "<br>".join(channels))
        card("💰 Budget Allocation", "<br>".join([f"{k}: ₹{v}" for k, v in allocation.items()]))
        card("🚀 Go-To-Market Plan", "<br>".join(gtm))
        st.markdown("---")
st.markdown("## 💬 Refine Strategy")

# initialize memory if missing
if "strategy_context" not in st.session_state:
    st.session_state.strategy_context = ""

user_input = st.text_input(
    "Ask AR.AI to refine or redesign the strategy",
    key="refine_input"
)

if st.button("Send to AR.AI", key="send_refine"):
    if user_input.strip() == "":
        st.warning("Please enter a request to refine the strategy.")
    else:
        with st.spinner("AR.AI refining strategy..."):
            refinement = client.responses.create(
                model="gpt-4o-mini",
                input=f"""
You are AR.AI, a senior marketing intelligence system.

Current strategy:
{st.session_state.strategy_context}

User request:
{user_input}

Rules:
- You may adjust channels, sequencing, and allocation
- Keep total budget unchanged
- Explain every change clearly
"""
            )

        st.markdown("### 🔄 AR.AI Refined Strategy")
        st.markdown(refinement.output_text)

        # append to memory
        st.session_state.strategy_context += (
            "\n\nREFINEMENT:\n" + refinement.output_text
        )

        # clear input after response
        st.session_state.refine_input = ""


        st.markdown("---")
        pdf_path = generate_pdf(brand, explanation, kpis, channels, allocation, gtm)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download Strategy PDF",
                f,
                file_name=f"{brand}_Marketing_Strategy.pdf",
                mime="application/pdf"
            )

        st.markdown("---")
        st.markdown("## 💬 Refine Strategy")

        user_message = st.text_input("Ask AR.AI to refine or adjust")

        if st.button("Send to AR.AI") and user_message:

            if st.session_state.refine_count >= MAX_REFINES:
                st.error("❌ Refinement limit reached.")
                st.stop()

            st.session_state.refine_count += 1

            refinement = client.responses.create(
                model="gpt-4o-mini",
                input=f"""
Existing strategy:
{st.session_state.strategy_context}

User request:
{user_message}
"""
            )

            st.markdown(refinement.output_text)
            st.session_state.strategy_context += "\n\n" + refinement.output_text

    except Exception:
        show_404_error()
