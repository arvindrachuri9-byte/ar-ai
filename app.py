import streamlit as st

st.set_page_config(page_title="AR.AI – Marketing Intelligence", layout="wide")

st.title("🚀 AR.AI – Marketing Intelligence Engine")
st.subheader("Turn brand inputs into actionable marketing strategies")

# ---------- INPUTS ----------
with st.form("marketing_form"):
    brand = st.text_input("Brand Name", value="Saints Chocolate")
    category = st.text_input("Product Category", value="Luxury Artisanal Chocolate")
    market = st.text_input("Target Market (e.g. India Urban, US SMBs)", value="Affluent Urban Connoisseurs (India)")
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
if submitted:
    st.success("AR.AI Strategy Generated")

    st.markdown("## 🎯 Quarterly SMART Objective")
    if goal == "Sales Growth":
        st.write(f"Achieve a **25% increase in e-commerce revenue** by the end of the quarter by optimizing performance campaigns and increasing **AOV**.")
    elif goal == "Brand Awareness":
        st.write(f"Increase **Social Media Impressions by 40%** and **Organic Search Traffic by 20%** to establish **{brand}** as a premium category leader.")
    elif goal == "Lead Generation":
        st.write(f"Generate **500 new qualified email subscribers** through gated content and tasting event sign-ups, focusing on **CPL** below industry average.")
    else:
        st.write(f"Improve **Repeat Purchase Rate by 15%** and increase **Customer Lifetime Value (CLV)** through personalized loyalty programs and exclusive offers.")


    st.markdown("## 📢 Recommended Channels & Tactical Initiatives")
    if goal == "Brand Awareness":
        st.write("- **Instagram & YouTube Reels:** Focus on aspirational lifestyle videos and celebrity/influencer collaborations.\n- **PR & Media:** Target high-end food, travel, and lifestyle publications for features.\n- **SEO:** Target high-value, niche keywords (e.g., 'sustainable artisan chocolate India').")
    elif goal == "Sales Growth":
        st.write("- **Meta Performance Ads (Instagram/FB):** Use DCO (Dynamic Creative Optimization) for retargeting high-intent customers and lookalike audiences.\n- **Google Shopping:** Optimize product feeds for high-margin items.\n- **E-mail:** Launch flash sales and abandoned cart recovery sequences.")
    elif goal == "Lead Generation":
        st.write("- **LinkedIn/Business Partnerships:** Run targeted campaigns for B2B/Corporate gifting leads.\n- **Gated Content:** Offer a 'Luxury Chocolate Pairing Guide' (PDF) in exchange for email.\n- **Local Experiential Events:** Promote ticketed tasting events in target metro cities.")
    else:
        st.write("- **Loyalty Program:** Launch a tiered points-based system (Gold, Platinum) with early access to new products.\n- **WhatsApp CRM:** Use personalized broadcast messages for birthdays, anniversaries, and restocking alerts.\n- **Exclusive Content:** Send 'Behind the Bean' educational content only to existing customers.")

    st.markdown("---")

    st.markdown("## ✍️ Specific Content Strategy: The Luxury Narrative")
    st.write("**Core Strategy:** Move beyond simple product shots. Every piece of content must reinforce the brand's premium value through storytelling. We will focus on the three pillars of luxury content.")

    st.markdown("### 1. The Heritage & Sourcing (Authority)")
    st.write("Content that establishes *why* your product is worth the premium price.")
    st.write(
        """
        * **Video:** **"The Origin Story"** - Short Reel/TikTok of a hand-selection process of cocoa beans, focusing on the texture, soil, and the sound of the bean-to-bar process.
        * **Photo:** Macro shots of **raw ingredients** (cocoa pods, rare vanilla beans) with dark, moody lighting.
        * **Caption Theme:** "Crafted from beans so rare, they’re found only at [Region Name]."
        """
    )

    st.markdown("### 2. The Craftsmanship & Expertise (Quality)")
    st.write("Content that highlights the skill, time, and care that goes into the product.")
    st.write(
        """
        * **Video:** **"The Perfect Temper"** - Slow-motion ASMR video of the chocolatier tempering on marble, ending with the 'snap' test.
        * **Photo:** Elegant hands **decorating a Bon Bon** with gold leaf or painting with cocoa butter. Focus is on precision.
        * **Caption Theme:** "The 72-hour process behind the signature **{Category}** texture."
        """
    )

    st.markdown("### 3. The Exclusivity & Lifestyle (Aspiration)")
    st.write("Content that showcases the product in an aspirational, luxury setting.")
    st.write(
        """
        * **Video:** **"The Pairing Ritual"** - A sophisticated hand pairing a Bon Bon with fine whiskey or coffee in a minimalist, high-end environment.
        * **Photo:** Flat lays of **custom gift boxes** next to items like a luxury watch, cashmere, or high-end stationery.
        * **Caption Theme:** "An indulgence reserved for your most private moments."
        """
    )
    
    st.markdown("---")

    st.markdown("## 📊 Quarterly Measurables & KPIs")
    st.write("Primary KPIs to track: **" + ", ".join(kpis) + "**")

    st.markdown("## 🔁 Optimization Logic")
    st.write("""
    - **Revenue/ROAS Optimization:** Aggressively pause ad sets where **ROAS** is below 3x. Scale top-performing audiences by 20% weekly.
    - **Content Optimization:** Replace creative assets (videos/photos) with **Engagement Rate** below 2.5% every 10 days to combat creative fatigue.
    - **Funnel Optimization:** Run A/B tests on landing pages to reduce **CAC** and increase **Conversion Rate**.
    """)

    st.info("AR.AI Recommendation: Dedicate 60% of your budget to Performance (Sales) and 40% to Storytelling (Brand Awareness) to ensure sustainable growth.")
