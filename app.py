import streamlit as st

st.set_page_config(page_title="AR.AI – Marketing Intelligence", layout="wide")

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.subheader("Turn brand inputs into actionable marketing strategies")

# ---------- INPUTS ----------
with st.form("marketing_form"):
    brand = st.text_input("Brand Name")
    category = st.text_input("Product Category")
    market = st.text_input("Target Market (e.g. India Urban, US SMBs)")
    goal = st.selectbox(
        "Primary Marketing Goal",
        ["Brand Awareness", "Lead Generation", "Sales Growth", "Customer Retention"]
    )
    kpis = st.multiselect(
        "Key Measurable Metrics",
        ["Reach", "CTR", "CPL", "CAC", "ROAS", "Revenue", "Repeat Rate"]
    )

    submitted = st.form_submit_button("Generate Strategy")

# ---------- OUTPUT ----------
if submitted:
    st.success("AR.AI Strategy Generated")

    st.markdown("## 🎯 Strategy Overview")
    st.write(
        f"**{brand}** in the **{category}** category should focus on **{goal.lower()}** "
        f"in the **{market}** market using a performance-driven, insight-led approach."
    )

    st.markdown("## 👥 Target Audience Personas")
    st.write("""
    - Urban, digital-first consumers
    - Value-driven but brand-aware
    - Influenced by social proof, reviews, and short-form content
    """)

    st.markdown("## 📢 Recommended Channels")
    if goal == "Brand Awareness":
        st.write("- Instagram & Facebook Reels\n- YouTube\n- Influencer Marketing")
    elif goal == "Lead Generation":
        st.write("- Google Search Ads\n- LinkedIn Ads\n- Landing Pages")
    elif goal == "Sales Growth":
        st.write("- Meta Performance Ads\n- Google Shopping\n- Retargeting")
    else:
        st.write("- Email Marketing\n- WhatsApp CRM\n- Loyalty Campaigns")

    st.markdown("## ✍️ Content Ideas")
    st.write("""
    - Short-form videos explaining product benefits  
    - Customer testimonials & reviews  
    - Problem–solution creatives  
    - Limited-time offers & CTAs
    """)

    st.markdown("## 📆 30-Day Execution Plan")
    st.write("""
    **Week 1:** Research, creatives, audience setup  
    **Week 2:** Launch ads & content  
    **Week 3:** Optimize based on KPIs  
    **Week 4:** Scale top-performing campaigns
    """)

    st.markdown("## 📊 KPI Tracking")
    st.write(f"Primary KPIs to track: **{', '.join(kpis)}**")

    st.markdown("## 🔁 Optimization Logic")
    st.write("""
    - Pause low CTR creatives  
    - Scale high ROAS audiences  
    - Refresh creatives every 10–14 days  
    - Reallocate budget weekly
    """)

    st.info("AR.AI Recommendation: Review performance weekly and iterate aggressively.")
