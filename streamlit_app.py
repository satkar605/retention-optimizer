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
        font-size: 3.5rem;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.8rem;
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
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="hero-title">🎵 PlaylistPro Retention Crisis</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">From Predictive Analytics to Prescriptive Optimization</p>', unsafe_allow_html=True)

st.markdown("---")

# THE STORY BEGINS - Business Context from Report
st.markdown("## 📖 The Story: A Music Streaming Company in Crisis")

st.markdown("""
PlaylistPro is a music streaming service with **75,000 subscribers** across four subscription tiers: 
Premium, Free, Family, and Student. Like many subscription-based businesses, PlaylistPro faces a critical challenge: **customer churn**.

Every month, customers cancel their subscriptions for various reasons—better offers from competitors, 
dissatisfaction with the service, or simply losing interest. The financial impact is devastating.
""")

# Problem Scale - Metric Cards
st.markdown("### 📉 The Scale of the Problem")

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
    <h3>❌ The Problem: No Strategy, Just Guesswork</h3>
    <p style="font-size: 1.1rem; line-height: 1.8;">
    Before this project, PlaylistPro had <strong>no systematic approach</strong> to customer retention:
    </p>
    <ul style="font-size: 1.1rem; line-height: 1.8;">
        <li><strong>No predictive analytics:</strong> The company couldn't identify which customers were at highest risk of churning</li>
        <li><strong>Manual, gut-feel decisions:</strong> Marketing managers guessed which customers to target based on intuition</li>
        <li><strong>Budget waste:</strong> Money spent on low-value customers while high-value, high-risk customers were ignored</li>
        <li><strong>No optimization:</strong> No framework to allocate limited marketing resources efficiently across 75,000 customers</li>
        <li><strong>Unclear ROI:</strong> No way to measure whether retention campaigns were actually working</li>
        <li><strong>Operational chaos:</strong> Email capacity, call center resources, and discount budgets were not coordinated</li>
    </ul>
    <p style="font-size: 1.2rem; font-weight: bold; margin-top: 1.5rem; color: #c0392b;">
    💸 Result: Millions in lost recurring revenue every year, with no clear path to improvement.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# The Solution - Two-Phase Approach from Report
st.markdown("## ✅ The Solution: Predictive + Prescriptive Analytics")

st.markdown("""
This project developed an **end-to-end data science solution** that combines machine learning predictions 
with mathematical optimization to create an intelligent, automated retention system.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔮 Phase 1: Predictive Analytics
    
    **Goal:** Identify who will churn
    
    **Approach:**
    - Trained multiple ML models (Logistic Regression, Random Forest, XGBoost)
    - **XGBoost emerged as winner** with 94% AUC
    - Analyzed 75,000 customers with 20+ features
    
    **Key Predictors Discovered:**
    1. **Subscription type** (Premium vs. Free)
    2. **Customer service interactions** (complaints signal risk)
    3. **Listening hours** (low engagement = high risk)
    4. **Song skip rate** (dissatisfaction indicator)
    5. **Payment plan** (monthly vs. yearly)
    
    **Output:** Churn probability (0-100%) for each customer
    
    **Example:**
    - Customer #12345 (Premium): **72% churn risk**
    - Customer #67890 (Family): **15% churn risk**
    """)

with col2:
    st.markdown("""
    ### 🎯 Phase 2: Prescriptive Optimization
    
    **Goal:** Decide who gets what action
    
    **Approach:**
    - **Mixed-Integer Linear Programming (MILP)**
    - **Gurobi solver** (industry-leading optimizer)
    - 2,000 binary decision variables (250 customers × 8 actions)
    
    **Optimization Objective:**
    ```
    Maximize: Expected Retained CLV - Campaign Cost
    ```
    
    **Constraints Enforced:**
    1. **Budget limit** ($150/week baseline)
    2. **Email capacity** (120/week max)
    3. **Push notification capacity** (100/week max)
    4. **Fairness:** 60% of high-risk customers must be treated
    5. **VIP treatment:** 40% of Premium customers covered
    6. **Diversity:** No single action > 50% of customers
    7. **Equity:** All segments get ≥15% coverage
    
    **Output:** Optimal customer-action assignments
    """)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works - From Report Section 3
with st.expander("📚 How the Optimization Works (Technical Details)", expanded=False):
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
st.markdown("## 🎉 The Results: Proven ROI & Actionable Insights")

st.markdown("""
The optimization model was run with a **baseline budget of $150/week** on a sample of 250 customers 
(scaled down from 75,000 due to Gurobi academic license limits). Here's what happened:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Net Value Generated",
        value="$3,479",
        delta="On $150 spend",
        help="Expected CLV retained minus campaign cost"
    )
    st.metric(
        label="📈 Return on Investment",
        value="2,319%",
        delta="23x return!",
        help="(Retained CLV / Cost - 1) × 100"
    )

with col2:
    st.metric(
        label="👥 Customers Treated",
        value="75 / 250",
        delta="30% coverage",
        help="Optimally selected high-impact customers"
    )
    st.metric(
        label="🛡️ Churn Prevented",
        value="~5 customers",
        delta="Per 250 sample",
        help="Expected reduction in churn count"
    )

with col3:
    st.metric(
        label="🎯 Optimal Budget Range",
        value="$250-400",
        delta="Per week",
        help="Sweet spot before diminishing returns"
    )
    st.metric(
        label="📊 ROI at Scale ($1,000)",
        value="1,100%",
        delta="Still excellent",
        help="Diminishing returns but positive value"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Key Findings - From Report Summary
st.info("""
**💡 Key Strategic Findings from the Analysis:**

1. **Optimal Budget Discovery:** $250-400/week delivers best ROI before diminishing returns. Beyond $500, efficiency drops significantly.

2. **Smart Customer Prioritization:** Model correctly focuses on high-risk + high-value customers (Premium/Family subscribers with 70%+ churn probability).

3. **Channel Efficiency:** Personalized email is most cost-effective at baseline budget. Higher budgets enable premium channels (calls, in-app offers).

4. **Fairness Maintained:** All subscription segments receive minimum 15% coverage, preventing algorithmic bias against lower-value customers.

5. **Scalability Proven:** Framework scales from 250 (demo) to 75,000 customers with commercial Gurobi license. Methodology is production-ready.

6. **Constraint Binding Analysis:** Budget was fully utilized (binding), while email/push capacity had slack. This guides future resource allocation.
""")

st.markdown("---")

# What Makes This Different
st.markdown("## 🌟 What Makes This Approach Different?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### ❌ Traditional Approach (Before)
    - **Segment-based:** "Send discount to all Premium users"
    - **Rule-based:** "Target customers who haven't logged in for 30 days"
    - **One-size-fits-all:** Same action for everyone in a segment
    - **No optimization:** Budget allocated arbitrarily
    - **No measurement:** Can't prove ROI
    - **Reactive:** Wait until churn happens
    
    **Result:** Wasted budget, missed opportunities, unclear impact
    """)

with col2:
    st.markdown("""
    ### ✅ Optimization Approach (After)
    - **Individual-level:** Personalized decision for each customer
    - **Data-driven:** ML predictions guide targeting
    - **Optimized:** Mathematical guarantee of best allocation
    - **Constrained:** Respects budget, capacity, fairness
    - **Measurable:** Clear ROI metrics (2,319% baseline)
    - **Proactive:** Prevent churn before it happens
    
    **Result:** Maximum value, efficient spending, proven impact
    """)

st.markdown("---")

# The Technical Foundation - From Report
st.markdown("## 🔬 The Technical Foundation")

st.markdown("""
This solution combines cutting-edge techniques from multiple fields:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🤖 Machine Learning**
    - XGBoost gradient boosting
    - 94% AUC performance
    - Feature importance analysis
    - Cross-validation
    - Hyperparameter tuning
    """)

with col2:
    st.markdown("""
    **📊 Operations Research**
    - Mixed-Integer Linear Programming
    - Gurobi optimization solver
    - Constraint satisfaction
    - Sensitivity analysis
    - Dual variable interpretation
    """)

with col3:
    st.markdown("""
    **💼 Business Analytics**
    - Customer lifetime value (CLV)
    - Return on investment (ROI)
    - Budget allocation
    - Fairness metrics
    - A/B testing framework
    """)

st.markdown("---")

# Call to Action
st.markdown("## 🚀 Ready to Explore the Solution?")

st.markdown("""
Now that you understand the business problem and the approach, you can:

1. **Run the Optimizer** - Configure constraints and see optimal customer-action assignments
2. **Explore Sensitivity Analysis** - Understand how budget affects ROI and coverage
3. **Export Treatment Plans** - Download customer lists for immediate execution
""")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎯 Launch Optimization Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/2_Optimizer.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 View Budget Sensitivity Analysis", use_container_width=True):
        st.switch_page("pages/3_Sensitivity_Analysis.py")

with col2:
    if st.button("📄 Read Full Technical Report", use_container_width=True):
        st.markdown("[Download PDF Report](prescriptive_analysis_report.pdf)")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Combining Predictive Analytics with Prescriptive Optimization</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Built with Streamlit • Python • XGBoost • Gurobi
    </p>
    <p style='font-size: 0.8rem; color: #999; margin-top: 1rem;'>
        © 2025 PlaylistPro Analytics Team • Satkar Karki
    </p>
</div>
""", unsafe_allow_html=True)
