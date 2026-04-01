```python
import streamlit as st
import time
from openai import OpenAI, RateLimitError

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AR.AI Strategy Generator",
    page_icon="🚀",
    layout="wide"
)

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- AI FUNCTION ----------------
def ai_call(prompt):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            return response.output_text

        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return "Rate limit reached. Please try again in a few seconds."

        except Exception as e:
            return f"Error: {str(e)}"

# ---------------- HEADER ----------------
st.title("AR.AI Marketing Strategy Generator")
st.markdown("Generate a full marketing strategy, media plan, growth ideas, and final recommendations.")

# ---------------- INPUTS ----------------
company_name = st.text_input("Brand / Company Name")
industry = st.text_input("Industry")
target_audience = st.text_area("Target Audience")
goals = st.text_area("Business Goals")
budget = st.text_input("Monthly Marketing Budget")
competitors = st.text_area("Competitors")
extra_notes = st.text_area("Additional Notes")

# ---------------- GENERATE BUTTON ----------------
if st.button("Generate Strategy"):

    if not company_name or not industry:
        st.warning("Please fill in at least Brand Name and Industry.")

    else:
        context = f"""
        Company Name: {company_name}
        Industry: {industry}
        Target Audience: {target_audience}
        Goals: {goals}
        Budget: {budget}
        Competitors: {competitors}
        Additional Notes: {extra_notes}
        """

        strategy_prompt = f"""
        You are a senior brand strategist.

        Create a detailed marketing strategy for the following brand.

        {context}

        Include:
        - Brand positioning
        - USP
        - Audience segments
        - Content pillars
        - Social media strategy
        - Campaign ideas
        - Influencer strategy
        - Paid ads recommendation
        - Offline marketing recommendation
        """

        media_prompt = f"""
        You are a media planner.

        Create a media plan for this business:

        {context}

        Include:
        - Meta ads
        - Google ads
        - Influencer spends
        - Outdoor media
        - Budget split
        - Best channels
        - Suggested ad frequency
        """

        growth_prompt = f"""
        You are a growth marketing expert.

        Suggest growth strategies for this brand:

        {context}

        Include:
        - Growth hacks
        - Referral strategy
        - Retention strategy
        - CRM ideas
        - Loyalty ideas
        - Community building
        - WhatsApp strategy
        - Email marketing ideas
        """

        with st.spinner("Generating strategy..."):
            strategy = ai_call(strategy_prompt)

        with st.spinner("Generating media plan..."):
            media = ai_call(media_prompt)

        with st.spinner("Generating growth plan..."):
            growth = ai_call(growth_prompt)

        final_prompt = f"""
        Combine the following into one polished report:

        STRATEGY:
        {strategy}

        MEDIA:
        {media}

        GROWTH:
        {growth}

        Format it professionally with headings and bullet points.
        """

        with st.spinner("Combining everything into final report..."):
            final_report = ai_call(final_prompt)

        st.success("Report Generated Successfully")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Strategy",
            "Media Plan",
            "Growth Plan",
            "Final Report"
        ])

        with tab1:
            st.subheader("Marketing Strategy")
            st.write(strategy)

        with tab2:
            st.subheader("Media Plan")
            st.write(media)

        with tab3:
            st.subheader("Growth Plan")
            st.write(growth)

        with tab4:
            st.subheader("Final Combined Report")
            st.write(final_report)

# ---------------- SIDEBAR ----------------
st.sidebar.title("AR.AI")
st.sidebar.info(
    "This tool helps generate marketing strategy, media plans, and growth ideas for brands."
)

st.sidebar.markdown("### Required Streamlit Secret")
st.sidebar.code('OPENAI_API_KEY = "your-key-here"')
```

Also add this inside your Streamlit secrets:

```toml
OPENAI_API_KEY = "your-openai-api-key
```
