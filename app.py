import streamlit as st
from openai import OpenAI
# ---------- MEMORY FOR CONVERSATION ----------

if "strategy_context" not in st.session_state:
    st.session_state.strategy_context = ""

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
# ---------- AI EXPLAINER (GPT AS NARRATOR) ----------

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


st.set_page_config(page_title="AR.AI – Marketing Intelligence", layout="wide")

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.subheader("Turn brand inputs into actionable marketing strategies")

# ---------- INPUTS ----------
with st.form("marketing_form"):
    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market")
    goal = st.selectbox(
        "Primary Marketing Goal",
        ["Sales Growth", "Brand Awareness", "Lead Generation", "Customer Retention"]
    )
    currency = "INR"

    budget = st.number_input(
        "Total Marketing Budget (INR)",
        min_value=500,
        value=500,
        step=500
    )

    submitted = st.form_submit_button("Generate Strategy")

# ---------- OUTPUT ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if submitted and brand:

    st.success(f"AR.AI Strategy Generated for {brand}")

    # KPI SELECTION
    kpis = select_kpis(goal)
    st.markdown("## 🎯 Selected KPIs")
    st.write(", ".join(kpis))

    # CHANNEL PRIORITIZATION
    channels = prioritize_channels(budget)
    st.markdown("## 📢 Channel Prioritization")
    st.write(", ".join(channels))

    # BUDGET ALLOCATION
    allocation = allocate_budget(budget, channels)
    st.markdown("## 💰 Budget Allocation")
    for ch, amt in allocation.items():
        st.write(f"{ch}: {currency} {amt}")

    # GO-TO-MARKET SEQUENCE
    gtm = go_to_market_sequence(goal)
    st.markdown("## 🚀 Go-To-Market Sequence")
    for phase in gtm:
        st.write(phase)

    # AI SYNTHESIS
    with st.spinner("AR.AI explaining decisions..."):
        explanation = explain_with_ai(
            "Marketing Intelligence Summary",
            f"""
            Brand: {brand}
            Category: {category}
            Market: {market}
            Goal: {goal}
            Budget: {currency} {budget}
            KPIs: {kpis}
            Channels: {channels}
            Allocation: {allocation}
            Go-To-Market: {gtm}
            """,
            client
        )

    st.markdown("## 🧠 AR.AI Strategic Rationale")
    st.markdown(explanation)
    st.session_state.strategy_context = explanation
    st.markdown("---")
st.markdown("## 💬 Talk to AR.AI")

user_followup = st.text_input(
    "Ask AR.AI to be more specific, adjust channels, or refine the strategy"
)

refine_button = st.button("Refine Strategy")
if refine_button and user_followup:

    with st.spinner("AR.AI is refining the strategy..."):
        refinement = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
            You are AR.AI, a marketing intelligence system.

            This is the existing strategy:
            {st.session_state.strategy_context}

            User request:
            {user_followup}

            Rules:
            - Do NOT create a new strategy
            - Only refine or explain what already exists
            - Be specific and actionable
            - Keep budget, goal, and channels consistent
            """
        )

    st.markdown("### 🔄 AR.AI Response")
    st.markdown(refinement.output_text)

    # Update memory with refinement
    st.session_state.strategy_context += "\n\nREFINEMENT:\n" + refinement.output_text



elif submitted:
    st.warning("Please enter a Brand Name.")

