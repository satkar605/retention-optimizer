"""
PlaylistPro Retention Optimizer - Main Entry Point
Redirects to the landing page by default
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="PlaylistPro Retention Optimizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="auto"
)

# Sidebar navigation help
st.sidebar.success("👆 Select a page above to navigate")
st.sidebar.info("""
**Quick Navigation:**
- 🏠 **Home**: Understanding the problem & solution
- ⚙️ **Optimizer**: Run optimization scenarios  
- 📊 **Sensitivity Analysis**: Budget analysis & ROI insights
""")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Start with the Home page to understand the business context")

# Main content - Welcome message
st.markdown("""
<style>
    .welcome-box {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .welcome-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .welcome-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #1DB954;
        margin: 1rem 0;
    }
    .nav-button {
        background-color: white;
        color: #1DB954;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        border: 2px solid white;
        margin: 0.5rem;
        cursor: pointer;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome-box">
    <div class="welcome-title">🎵 Welcome to PlaylistPro Retention Optimizer</div>
    <div class="welcome-subtitle">Data-Driven Customer Retention Strategy Powered by ML & Optimization</div>
</div>
""", unsafe_allow_html=True)

# Navigation cards
st.markdown("## 🗺️ Choose Your Destination")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🏠 Home</h3>
        <p><strong>Start Here!</strong></p>
        <p>Learn about the 47% churn crisis, our ML+Optimization solution, and proven ROI results.</p>
        <ul style='text-align: left; margin-top: 1rem;'>
            <li>Business problem overview</li>
            <li>Solution architecture</li>
            <li>Key findings & ROI</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Go to Home Page", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🏠_Home.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>⚙️ Optimizer Dashboard</h3>
        <p><strong>Run Optimizations</strong></p>
        <p>Configure constraints, run optimization scenarios, and export treatment plans.</p>
        <ul style='text-align: left; margin-top: 1rem;'>
            <li>Set budget & capacity</li>
            <li>Run Gurobi optimization</li>
            <li>View & export results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚙️ Launch Optimizer", use_container_width=True):
        st.switch_page("pages/2_⚙️_Optimizer.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Sensitivity Analysis</h3>
        <p><strong>Budget Insights</strong></p>
        <p>Understand diminishing returns and find the optimal budget allocation range.</p>
        <ul style='text-align: left; margin-top: 1rem;'>
            <li>Budget sensitivity charts</li>
            <li>Optimal range: $250-400</li>
            <li>Custom scenarios</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 View Analysis", use_container_width=True):
        st.switch_page("pages/3_📊_Sensitivity_Analysis.py")

st.markdown("---")

# Quick stats
st.markdown("## 📈 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="ML Model Accuracy",
        value="94% AUC",
        help="XGBoost churn prediction model performance"
    )

with col2:
    st.metric(
        label="Baseline ROI",
        value="2,319%",
        delta="At $150 budget",
        help="Return on investment for retention campaigns"
    )

with col3:
    st.metric(
        label="Optimal Budget",
        value="$250-400",
        delta="Per week",
        help="Sweet spot before diminishing returns"
    )

with col4:
    st.metric(
        label="Customer Base",
        value="75,000",
        help="Total customers analyzed (demo: 250 sample)"
    )

st.markdown("---")

# Technology stack
st.markdown("## 🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Machine Learning & Analytics:**
    - 🤖 **XGBoost**: Gradient boosting for churn prediction
    - 🐼 **Pandas & NumPy**: Data manipulation and analysis
    - 📊 **Plotly**: Interactive visualizations
    - 📈 **Scikit-learn**: Model evaluation metrics
    """)

with col2:
    st.markdown("""
    **Optimization & Deployment:**
    - 🎯 **Gurobi**: Mixed-integer linear programming solver
    - 🚀 **Streamlit**: Interactive dashboard framework
    - 🐍 **Python 3.9+**: Core programming language
    - 📝 **Quarto**: Technical report generation
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Combining Predictive Analytics with Prescriptive Optimization</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Built with ❤️ using Streamlit • Python • XGBoost • Gurobi
    </p>
    <p style='font-size: 0.8rem; color: #999; margin-top: 1rem;'>
        © 2025 PlaylistPro Analytics Team
    </p>
</div>
""", unsafe_allow_html=True)

# Auto-redirect to Home page after 3 seconds (optional - commented out by default)
# import time
# time.sleep(3)
# st.switch_page("pages/1_🏠_Home.py")
