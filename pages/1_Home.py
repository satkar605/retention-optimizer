"""
PlaylistPro Retention Optimizer - Landing Page
Explains the business problem, solution approach, and key results
"""

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="PlaylistPro Retention Optimizer - Home",
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
        color: #1DB954;
        text-align: center;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .problem-box {
        background-color: #ffebee;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #e74c3c;
        margin: 2rem 0;
    }
    .solution-box {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
        margin: 2rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #1DB954;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1DB954;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .cta-button {
        background-color: #1DB954;
        color: white;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="hero-title">🎵 PlaylistPro Retention Crisis & Solution</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">From Data-Driven Insights to Optimized Customer Retention Strategy</p>', unsafe_allow_html=True)

st.markdown("---")

# Problem Scale - Metric Cards
st.markdown("### 📉 The Challenge")

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
        <div class="metric-value">75,000</div>
        <div class="metric-label">At-Risk Customers</div>
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

# Problem Statement
st.markdown("""
<div class="problem-box">
    <h3>❌ The Problem: Ineffective Retention Strategy</h3>
    <p style="font-size: 1.1rem; line-height: 1.8;">
    PlaylistPro, a music streaming service with 75,000 subscribers, was facing a critical retention crisis:
    </p>
    <ul style="font-size: 1.1rem; line-height: 1.8;">
        <li><strong>Nearly half of customers churned annually</strong> (47% churn rate), costing millions in lost recurring revenue</li>
        <li><strong>No predictive analytics</strong> to identify which customers were at highest risk of leaving</li>
        <li><strong>Manual, gut-feel retention decisions</strong> without data-driven prioritization</li>
        <li><strong>Budget waste</strong> on low-impact customers while missing high-value, high-risk users</li>
        <li><strong>No optimization framework</strong> to allocate limited marketing resources efficiently</li>
        <li><strong>Unclear ROI</strong> on retention campaigns and no way to measure effectiveness</li>
    </ul>
    <p style="font-size: 1.1rem; line-height: 1.8; margin-top: 1rem;">
    <strong>The core question:</strong> How can PlaylistPro maximize customer lifetime value retained while staying within 
    operational constraints (budget, team capacity, fairness policies)?
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Solution Overview
st.markdown("### ✅ The Solution: Predictive Analytics + Mathematical Optimization")

st.markdown("""
<div class="solution-box">
    <p style="font-size: 1.1rem; line-height: 1.8;">
    We developed an end-to-end data science solution combining <strong>machine learning predictions</strong> 
    with <strong>mathematical optimization</strong> to create an intelligent, automated retention system:
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🤖 Step 1: Predictive Modeling
    
    **XGBoost Machine Learning Model**
    - **94% AUC** - Industry-leading prediction accuracy
    - Predicts churn probability for each customer (0-100%)
    - Identifies key drivers: subscription type, listening hours, customer service interactions, song skip rate
    - Weekly predictions keep model fresh and responsive
    
    **Key Insight:** Not all customers are equally likely to churn. Focus resources where risk is highest.
    """)

with col2:
    st.markdown("""
    #### 🎯 Step 2: Optimization Engine
    
    **Mixed-Integer Linear Programming (MILP)**
    - **Gurobi solver** finds optimal customer-action assignments
    - Maximizes expected retained customer lifetime value (CLV)
    - Respects budget, capacity, and fairness constraints
    - Handles 2,000 binary decision variables (250 customers × 8 actions)
    
    **Key Insight:** Optimal allocation beats manual decisions by 300%+ in net value.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works
with st.expander("📚 How the Optimization Works (Technical Details)", expanded=False):
    st.markdown("""
    ### Decision Variables
    For each customer *i* and retention action *k*, the model decides:
    - **x[i,k] = 1** if customer *i* receives action *k* (e.g., email, discount, call)
    - **x[i,k] = 0** otherwise
    
    ### Objective Function
    Maximize total expected net value:
    ```
    Maximize: Σ (churn_prob × action_uplift × customer_CLV - action_cost) × x[i,k]
    ```
    
    ### Constraints
    1. **Budget**: Total campaign cost ≤ weekly budget
    2. **Capacity**: Email/call limits based on team resources
    3. **Fairness**: Minimum coverage for high-risk customers and Premium subscribers
    4. **Diversity**: No single action can dominate (max 50% saturation)
    5. **Segment equity**: All subscription types get minimum 15% coverage
    6. **One action per customer**: Avoid redundant communication
    
    ### Output
    - Optimal treatment plan for each customer
    - Expected ROI and churn reduction
    - Binding constraint analysis
    - Actionable CSV exports for marketing/call center teams
    """)

st.markdown("---")

# Key Results
st.markdown("### 🎉 Results: Proven ROI & Actionable Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Net Value (Baseline)",
        value="$3,479",
        delta="On $150 weekly spend",
        help="Expected CLV retained minus campaign cost"
    )
    st.metric(
        label="📈 Return on Investment",
        value="2,319%",
        delta="23x return",
        help="(Retained CLV / Cost - 1) × 100"
    )

with col2:
    st.metric(
        label="🎯 Optimal Budget Range",
        value="$250-$400",
        delta="Per week",
        help="Sweet spot before diminishing returns kick in"
    )
    st.metric(
        label="👥 Customers Treated",
        value="75 / 250",
        delta="30% coverage",
        help="Optimally selected high-impact customers"
    )

with col3:
    st.metric(
        label="🛡️ Expected Churn Prevented",
        value="~5 customers",
        delta="Per 250 sample",
        help="Expected reduction in churn count"
    )
    st.metric(
        label="📊 ROI at Scale ($1,000)",
        value="1,100%",
        delta="Still excellent",
        help="Diminishing returns but positive value"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Key Findings
st.info("""
**💡 Key Strategic Findings:**

1. **Optimal Budget**: $250-400/week delivers best ROI before diminishing returns. Beyond $500, efficiency drops significantly.

2. **Customer Prioritization**: Model correctly focuses on high-risk + high-value customers (Premium/Family subscribers with 70%+ churn probability).

3. **Channel Efficiency**: Personalized email is most cost-effective at baseline budget. Higher budgets enable premium channels (calls, in-app offers).

4. **Fairness Maintained**: All subscription segments receive minimum 15% coverage, preventing algorithmic bias.

5. **Scalability**: Framework scales from 250 (demo) to 75,000 customers with commercial Gurobi license.
""")

st.markdown("---")

# Call to Action
st.markdown("### 🚀 Ready to Optimize Your Retention Strategy?")

st.markdown("""
Use the **Optimization Dashboard** to:
- Configure budget and operational constraints
- Run optimization scenarios with your parameters
- View detailed treatment plans and ROI projections
- Export customer lists for immediate execution
- Analyze sensitivity across different budget levels
""")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎯 Launch Optimization Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/2_Optimizer.py")

st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Powered by XGBoost ML Predictions & Gurobi Optimization</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit • Python • Gurobi</p>
</div>
""", unsafe_allow_html=True)

