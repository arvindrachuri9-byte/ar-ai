import streamlit as st
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ---------- USAGE LIMITS ----------
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

if "refine_count" not in st.session_state:
    st.session_state.refine_count = 0

MAX_GENERATIONS = 3
MAX_REFINES = 5


def card(title, content):
    
def generate_pdf(brand, explanation, kpis, channels, allocation, gtm):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"<b>{brand} – Marketing Strategy</b>", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    content.append(Paragraph(explanation.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>KPIs</b>", styles["Heading2"]))
    for kpi in kpis:
        content.append(Paragraph(f"- {kpi}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Channel Strategy</b>", styles["Heading2"]))
    for ch in channels:
        content.append(Paragraph(f"- {ch}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Budget Allocation (INR)</b>", styles["Heading2"]))
    for ch, amt in allocation.items():
        content.append(Paragraph(f"- {ch}: ₹{amt}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Go-To-Market Plan</b>", styles["Heading2"]))
    for phase in gtm:
        content.append(Paragraph(f"- {phase}", styles["BodyText"]))

    doc.build(content)
    return temp_file.name


    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"<b>{brand} – Marketing Strategy</b>", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    content.append(Paragraph(explanation.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>KPIs</b>", styles["Heading2"]))
    for kpi in kpis:
        content.append(Paragraph(f"- {kpi}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Channel Strategy</b>", styles["Heading2"]))
    for ch in channels:
        content.append(Paragraph(f"- {ch}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Budget Allocation (INR)</b>", styles["Heading2"]))
    for ch, amt in allocation.items():
        content.append(Paragraph(f"- {ch}: ₹{amt}", styles["BodyText"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Go-To-Market Plan</b>", styles["Heading2"]))
    for phase in gtm:
        content.append(Paragraph(f"- {phase}", styles["BodyText"]))

    doc.build(content)
    return temp_file.name

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
            background-color:#0f172a;
            padding:30px;
            border-radius:12px;
            text-align:center;
            border:1px solid #1e293b;
        ">
            <h2 style="color:#f8fafc;">⚠️ Something went wrong</h2>
            <p style="color:#cbd5f5; font-size:16px;">
                AR.AI couldn’t generate the strategy right now.<br>
                Please refresh or try again in a moment.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AR.AI – Marketing Intelligence",
    layout="wide"
)

# ---------- OPENAI ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- MEMORY ----------
if "strategy_context" not in st.session_state:
    st.session_state.strategy_context = ""

# ---------- DECISION LOGIC ----------

def select_kpis(goal):
    return {
        "Sales Growth": ["Revenue", "Conversion Rate", "AOV"],
        "Brand Awareness": ["Reach", "Engagement Rate", "Share of Voice"],
        "Lead Generation": ["Leads", "CAC", "Conversion Rate"],
        "Customer Retention": ["Repeat Rate", "LTV", "Churn"],
    }[goal]

def prioritize_channels(budget):
    if budget < 5000:
        return ["Paid Search", "Organic Social", "Email"]
    elif budget < 20000:
        return ["Meta Ads", "Google Ads", "Influencers"]
    else:
        return ["Meta Ads", "Google Ads", "Influencers", "YouTube"]

def allocate_budget(budget, channels):
    split = round(budget / len(channels), 2)
    return {ch: split for ch in channels}

def go_to_market(goal):
    if goal == "Brand Awareness":
        return [
            "Phase 1: Awareness launch",
            "Phase 2: Influencer amplification",
            "Phase 3: Retargeting"
        ]
    return [
        "Phase 1: Performance testing",
        "Phase 2: Scale winning channels",
        "Phase 3: Retention & optimization"
    ]

# ---------- AI EXPLAINER ----------

def explain_strategy(data):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are a senior marketing strategist.
Create a clear, client-ready executive summary.

{data}
"""
    )
    return response.output_text

# ---------- HEADER ----------
st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.caption("AI-powered marketing strategy, budgeted and explainable")

st.markdown("---")

# # ---------- SIDEBAR INPUTS ----------
with st.sidebar:
    st.markdown("## ⚙️ Strategy Inputs")

    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market")

    goal = st.selectbox(
        "Primary Goal",
        [
            "Sales Growth",
            "Brand Awareness",
            "Lead Generation",
            "Customer Retention"
        ]
    )

    budget = st.number_input(
        "Total Marketing Budget (INR)",
        min_value=500,
        step=500
    )

    generate = st.button("🚀 Generate Strategy")


# ---------- STRATEGY GENERATION ----------
if generate and brand:

    # ----- Usage limit check -----
    if st.session_state.generation_count >= MAX_GENERATIONS:
        st.error("❌ Free limit reached. Please upgrade to generate more strategies.")
        st.stop()

    st.session_state.generation_count += 1
    try:
        # decision logic
        kpis = select_kpis(goal)
        channels = prioritize_channels(budget)
        allocation = allocate_budget(budget, channels)
        gtm = go_to_market(goal)

        with st.spinner("AR.AI building your strategy..."):
            explanation = explain_strategy(...)

        st.session_state.strategy_context = explanation

        # ✅ PASTE CARD CODE HERE
        card("📌 Executive Summary", explanation)
        card("🎯 Objectives & KPIs", "<br>".join([f"• {kpi}" for kpi in kpis]))
        card("📢 Channel Strategy", "<br>".join([f"• {ch}" for ch in channels]))
        card("💰 Budget Allocation (INR)", "<br>".join([f"• {ch}: ₹{amt}" for ch, amt in allocation.items()]))
        card("🚀 Go-To-Market Plan", "<br>".join([f"• {phase}" for phase in gtm]))

st.markdown("---")
st.markdown("## 📄 Export Strategy")

pdf_path = generate_pdf(
    brand,
    explanation,
    kpis,
    channels,
    allocation,
    gtm
)

with open(pdf_path, "rb") as f:
    st.download_button(
        label="⬇️ Download Strategy PDF",
        data=f,
        file_name=f"{brand}_Marketing_Strategy.pdf",
        mime="application/pdf"
    )


        # buttons etc can continue here

    except Exception:
        show_404_error()



        # ---------- CLIENT APPROVAL ----------
        st.markdown("---")
        st.markdown("## ✅ Client Approval")
        st.button("Approve Strategy", key="approve_strategy")


    except Exception:
        show_404_error()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Approve Strategy"):
            st.success("✅ Strategy approved and ready for execution.")

    with col2:
        st.info("✏️ Use the chat below to request changes")

# ---------- CHAT / CONVERSATION ----------
if st.session_state.strategy_context:

    st.markdown("---")
    st.markdown("## 💬 Talk to AR.AI")
    st.caption("Ask for changes, reallocation, more detail, or focus areas")

    user_message = st.text_area(
        "Your message to AR.AI",
        placeholder="Example: Shift more budget to Instagram and explain why",
        height=100
    )
    
if st.button("Send to AR.AI", key="send_to_arai") and user_message:
    try:
        with st.spinner("AR.AI refining strategy..."):
            refinement = client.responses.create(
                model="gpt-4o-mini",
                input=f"""
You are AR.AI, a marketing intelligence engine.

Existing strategy:
{st.session_state.strategy_context}

User request:
{user_message}

Rules:
- You MAY change channels, tactics, and budget allocation
- You MUST keep total budget the same
- You MUST explain why changes were made
"""
            )

        st.markdown("### 🔄 Updated Recommendation")
        st.markdown(refinement.output_text)

        st.session_state.strategy_context += "\n\nUPDATE:\n" + refinement.output_text

    except Exception:
        show_404_error()

elif generate:
    st.warning("Please enter a Brand Name.")
