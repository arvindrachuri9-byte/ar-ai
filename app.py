import streamlit as st
from openai import OpenAI

# ---------- DECISION LOGIC (AR.AI BRAIN) ----------

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
    split = 1 / len(channels)
    for channel in channels:
        allocation[channel] = round(budget * split, 2)
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

# ---------- AI EXPLAINER ----------

def explain_with_ai(title, data, client):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are a senior marketing strategist.
Explain the following decisions clearly and practically.

{title}:
{data}
"""
    )
    return response.output_text


# ---------- STREAMLIT UI ----------

st.set_page_config(page_title="AR.AI – Marketing Intelligence", layout="wide")

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.subheader("Turn brand inputs into actionable marketing strategies")

# ---------- INPUT FORM ----------

with st.form("marketing_form"):
    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market")
    goal = st.selectbox(
        "Primary Marketing Goal",
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"]
    )

    budget = st.number_input(
        "Total Marketing Budget (INR)",
        min_value=500,
        value=500,
        step=500
    )

    submitted = st.form_submit_button("Generate Strategy")

# ---------- OPENAI CLIENT ----------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- STRATEGY EXECUTION ----------

if submitted and brand:

    st.success(f"AR.AI Strategy Generated for {brand}")

    # DECISION ENGINE
    kpis = select_kpis(goal)
    channels = prioritize_channels(budget)
    allocation = allocate_budget(budget, channels)
    gtm = go_to_market_sequence(goal)

    # AI EXPLANATION
    with st.spinner("AR.AI explaining decisions..."):
        explanation = explain_with_ai(
            "Marketing Intelligence Summary",
            f"""
Brand: {brand}
Category: {category}
Market: {market}
Goal: {goal}
Budget: INR {budget}
KPIs: {kpis}
Channels: {channels}
Allocation: {allocation}
Go-To-Market: {gtm}
""",
            client
        )

    # ---------- CLIENT-READY OUTPUT ----------

    st.markdown("## 📌 Executive Summary")
    st.markdown(explanation)

    st.markdown("---")
    st.markdown("## 🎯 Objectives & KPIs")
    for kpi in kpis:
        st.write(f"- {kpi}")

    st.markdown("---")
    st.markdown("## 📢 Channel Strategy")
    for channel in channels:
        st.write(f"- {channel}")

    st.markdown("---")
    st.markdown("## 💰 Budget Allocation")
    for ch, amt in allocation.items():
        st.write(f"- {ch}: INR {amt}")

    st.markdown("---")
    st.markdown("## 🚀 Go-To-Market Plan")
    for phase in gtm:
        st.write(f"- {phase}")

    # ---------- CLIENT ACTIONS ----------

    st.markdown("---")
    st.markdown("## ✅ Client Actions")

    approve = st.button("Approve Strategy")
    request_changes = st.button("Request Changes")

    if approve:
        st.success("✅ Strategy approved. Ready for execution.")

    # ---------- MEMORY ----------

    if "strategy_context" not in st.session_state:
        st.session_state.strategy_context = explanation

    # ---------- CONVERSATION ----------

    if request_changes:
        st.markdown("---")
        st.markdown("## 💬 Talk to AR.AI")

        user_followup = st.text_input(
            "Ask AR.AI to refine, reallocate budget, or adjust channels"
        )

        refine_button = st.button("Refine Strategy")

        if refine_button and user_followup:
            with st.spinner("AR.AI is refining the strategy..."):
                refinement = client.responses.create(
                    model="gpt-4o-mini",
                    input=f"""
You are AR.AI, a marketing intelligence system.

Existing strategy:
{st.session_state.strategy_context}

User request:
{user_followup}

Rules:
- You MAY adjust budget allocation, channels, and tactics
- You MUST keep the total budget the same
- You MUST explain WHY any number or channel was changed
- Changes must be practical and realistic
"""
                )

            st.markdown("### 🔄 AR.AI Updated Strategy")
            st.markdown(refinement.output_text)

            st.session_state.strategy_context += "\n\nREFINEMENT:\n" + refinement.output_text

elif submitted:
    st.warning("Please enter a Brand Name.")
