"""
PlaylistPro Retention Optimizer - Landing Page
Tells the story of the business problem and the optimization solution
"""

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="PlaylistPro Retention Optimizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 3rem;
    }
    .problem-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #e74c3c;
        margin: 2rem 0;
    }
    .solution-box {
        background-color: #f0f9ff;
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #2980b9;
        margin: 2rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="hero-title">PlaylistPro Retention Optimization</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Data-Driven Customer Retention Strategy</p>', unsafe_allow_html=True)

st.markdown("---")

# THE STORY BEGINS - Business Context from Report
st.markdown("## Business Context")

st.markdown("""
PlaylistPro, a music streaming service with **75,000 subscribers**, faces a critical challenge: 
**47% annual churn rate** resulting in millions in lost recurring revenue.
""")

# Problem Scale - Metric Cards
st.markdown("### The Challenge")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">47%</div>
        <div class="metric-label">Annual Churn Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">~35,000</div>
        <div class="metric-label">Customers Lost/Year</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">$0</div>
        <div class="metric-label">Data-Driven Strategy</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">???</div>
        <div class="metric-label">Optimal Budget</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# The Problem - Directly from Report Introduction
st.markdown("""
<div class="problem-box">
    <h3>The Problem</h3>
    <p style="font-size: 1.05rem; line-height: 1.7;">
    PlaylistPro had <strong>no systematic retention strategy</strong>:
    </p>
    <ul style="font-size: 1.05rem; line-height: 1.7;">
        <li>No predictive analytics to identify high-risk customers</li>
        <li>Manual, intuition-based targeting decisions</li>
        <li>Inefficient budget allocation</li>
        <li>Unclear ROI on retention campaigns</li>
    </ul>
    <p style="font-size: 1.05rem; font-weight: 600; margin-top: 1rem; color: #e74c3c;">
    Result: Millions in lost recurring revenue annually.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# The Solution - Two-Phase Approach from Report
st.markdown("## The Solution")

st.markdown("""
An end-to-end analytics solution combining machine learning predictions with mathematical optimization 
to maximize customer lifetime value retention.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Predictive Analytics
    
    **XGBoost model (94% AUC)** predicts individual churn probability based on:
    - Subscription type and payment plan
    - Customer service interactions
    - Listening hours and engagement metrics
    - Song skip rate and content preferences
    
    **Output:** Churn risk score (0-100%) for each customer
    """)

with col2:
    st.markdown("""
    ### Prescriptive Optimization
    
    **Mixed-Integer Linear Programming** determines optimal action assignments:
    
    **Objective:** Maximize (Expected Retained CLV - Campaign Cost)
    
    **Constraints:**
    - Budget and operational capacity limits
    - Minimum coverage for high-risk customers (60%)
    - Minimum coverage for Premium subscribers (40%)
    - Campaign diversity requirements (no action >50%)
    - Fairness across all segments (≥15% each)
    
    **Output:** Customer-action assignments maximizing net value
    """)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works - From Report Section 3
with st.expander("Technical Details", expanded=False):
    st.markdown("""
    ### Decision Variables
    For each customer *i* and retention action *k*, the model decides:
    - **x[i,k] = 1** if customer *i* receives action *k* (e.g., email, discount, call)
    - **x[i,k] = 0** otherwise
    
    ### Objective Function (What We're Maximizing)
    ```
    Maximize: Σ (churn_prob × action_uplift × customer_CLV - action_cost) × x[i,k]
    ```
    
    **Translation:** For each customer-action pair, calculate:
    - How likely they are to churn (XGBoost prediction)
    - How effective the action is (% churn reduction)
    - How valuable the customer is (lifetime value)
    - Subtract the cost of the action
    - Pick the combinations that maximize total value
    
    ### Example Calculation
    **Customer 12345: Premium subscriber**
    - Churn probability: 72%
    - Customer lifetime value: $240
    - Action: 20% discount offer
    - Action effectiveness: 15% churn reduction
    - Action cost: $20
    
    **Expected Net Value:**
    ```
    = 0.72 × 0.15 × $240 - $20
    = $25.92 - $20
    = $5.92 profit
    ```
    
    The optimizer finds the best combination of these assignments across all 250 customers!
    """)

st.markdown("---")

# Results - From Report Section 4 & 5
st.markdown("## Results")

st.markdown("""
The optimization model was run with a **baseline budget of $150/week** on a sample of 250 customers 
(scaled down from 75,000 due to Gurobi academic license limits). Here's what happened:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Net Value Generated",
        value="$3,479",
        delta="On $150 spend",
        help="Expected CLV retained minus campaign cost"
    )
    st.metric(
        label="Return on Investment",
        value="2,319%",
        delta="23x return",
        help="(Retained CLV / Cost - 1) × 100"
    )

with col2:
    st.metric(
        label="Customers Treated",
        value="75 / 250",
        delta="30% coverage",
        help="Optimally selected high-impact customers"
    )
    st.metric(
        label="Churn Prevented",
        value="~5 customers",
        delta="Per 250 sample",
        help="Expected reduction in churn count"
    )

with col3:
    st.metric(
        label="Optimal Budget Range",
        value="$250-400",
        delta="Per week",
        help="Sweet spot before diminishing returns"
    )
    st.metric(
        label="ROI at Scale ($1,000)",
        value="1,100%",
        delta="Still excellent",
        help="Diminishing returns but positive value"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Key Findings - From Report Summary
st.info("""
**Key Strategic Findings:**

1. **Optimal Budget:** $250-400/week delivers best ROI before diminishing returns. Beyond $500, efficiency drops significantly.

2. **Customer Prioritization:** Model focuses on high-risk + high-value customers (Premium/Family subscribers with 70%+ churn probability).

3. **Channel Efficiency:** Personalized email is most cost-effective at baseline budget. Higher budgets enable premium channels.

4. **Fairness:** All subscription segments receive minimum 15% coverage, preventing algorithmic bias.

5. **Scalability:** Framework scales from 250 (demo) to 75,000 customers with commercial Gurobi license.

6. **Resource Utilization:** Budget fully utilized while email/push capacity had slack, guiding future resource allocation.
""")

st.markdown("---")

# Call to Action
st.markdown("## Next Steps")

st.markdown("""
Use the interactive dashboard to:
- Configure budget and operational constraints
- Run optimization scenarios
- View detailed treatment plans and ROI projections
- Export customer lists for execution
- Analyze budget sensitivity and diminishing returns
""")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Launch Optimization Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/2_Optimizer.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("View Budget Sensitivity Analysis", use_container_width=True):
        st.switch_page("pages/3_Sensitivity_Analysis.py")

with col2:
    if st.button("Read Full Technical Report", use_container_width=True):
        st.markdown("[Download PDF Report](prescriptive_analysis_report.pdf)")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Predictive Analytics + Prescriptive Optimization</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Streamlit | Python | XGBoost | Gurobi
    </p>
    <p style='font-size: 0.85rem; color: #95a5a6; margin-top: 1rem;'>
        © 2025 PlaylistPro Analytics Team | Satkar Karki
    </p>
</div>
""", unsafe_allow_html=True)
