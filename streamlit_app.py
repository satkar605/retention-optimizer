"""
PlaylistPro Retention Optimizer - Single Page Dashboard
Business narrative + Interactive optimizer in one place
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from music_streaming_retention_75k import MusicStreamingRetentionOptimizer
import os

# Page configuration
st.set_page_config(
    page_title="PlaylistPro Retention Optimizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = None
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'merged_data' not in st.session_state:
    st.session_state.merged_data = None

# Helper function
def load_customer_data():
    """Load and merge prediction and customer feature data"""
    try:
        predictions = pd.read_csv('prediction_250.csv')
        features = pd.read_csv('test_250.csv')
        merged = predictions.merge(features, on='customer_id', how='left')
        return merged, len(predictions), len(features)
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return None, 0, 0

# Header
st.title("PlaylistPro Retention Optimizer")
st.markdown("**Data-Driven Customer Retention Strategy**")

st.markdown("---")

# Business Context Section
st.markdown("""
### 🎯 The Business Problem

PlaylistPro, a music streaming service with **75,000 subscribers**, was facing a critical retention crisis:

- **47% annual churn rate** — losing nearly half of all customers every year
- **Millions in lost recurring revenue** from customer attrition
- **No systematic retention strategy** to combat churn

#### Key Gaps
- ❌ No predictive analytics to identify high-risk customers before they churned
- ❌ No optimization framework for allocating limited marketing budgets
- ❌ No clear ROI measurement on retention campaigns
- ❌ Manual, reactive approach instead of data-driven, proactive strategy

---

### 💡 The Solution

This dashboard implements an **end-to-end prescriptive analytics system** that combines:

1. **Predictive Machine Learning** — XGBoost model (94% AUC) predicts individual customer churn probability
2. **Prescriptive Optimization** — Mixed-Integer Linear Programming assigns optimal retention actions to maximize value
3. **Smart Constraints** — Respects budget limits, operational capacity, and fairness policies

---

### 📊 Proven Results

**Baseline Scenario** (\\$150 weekly budget, 250 customer sample):

- **\\$3,479 net value** generated
- **2,319% ROI** — every dollar spent returns \\$23 in retained customer value
- **75 customers treated** with personalized retention actions
- **~5 churns prevented** per week

**Optimal Performance Zone**: \\$250-400 weekly budget delivers strongest returns before diminishing effects.

**Production Ready**: Framework scales to full 75,000 customer base with commercial Gurobi license.
""")

st.markdown("---")

# Load data on startup
if not st.session_state.data_loaded:
    with st.spinner("Loading customer data..."):
        merged_data, n_pred, n_feat = load_customer_data()
        if merged_data is not None:
            st.session_state.merged_data = merged_data
            st.session_state.data_loaded = True

# Sidebar Configuration
with st.sidebar:
    st.header("Optimization Settings")
    
    st.markdown("### Budget & Capacity")
    
    budget = st.slider(
        "Weekly Budget ($)",
        min_value=150,
        max_value=1000,
        value=150,
        step=25,
        help="Optimal range: $250-400"
    )
    
    email_cap = st.slider(
        "Email Capacity (per week)",
        min_value=60,
        max_value=250,
        value=120,
        step=10
    )
    
    push_cap = st.slider(
        "Push/In-App Capacity",
        min_value=50,
        max_value=250,
        value=100,
        step=10
    )
    
    st.markdown("### Policy Constraints")
    
    min_high_risk = st.slider(
        "Min High-Risk Coverage (%)",
        min_value=40,
        max_value=90,
        value=60,
        step=5
    ) / 100.0
    
    min_premium = st.slider(
        "Min Premium Coverage (%)",
        min_value=10,
        max_value=80,
        value=40,
        step=5
    ) / 100.0
    
    max_action_pct = st.slider(
        "Max Action Saturation (%)",
        min_value=30,
        max_value=80,
        value=50,
        step=5
    ) / 100.0
    
    min_segment_coverage = st.slider(
        "Min Segment Coverage (%)",
        min_value=10,
        max_value=40,
        value=15,
        step=5
    ) / 100.0
    
    st.markdown("---")
    
    run_optimization = st.button(
        "RUN OPTIMIZATION",
        type="primary",
        use_container_width=True
    )

# Main content
if st.session_state.data_loaded and st.session_state.merged_data is not None:
    
    df = st.session_state.merged_data
    
    # Overview
    st.header("Current Week Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{len(df):,}")
    
    with col2:
        high_risk = (df['churn_probability'] > 0.5).sum()
        st.metric("High Risk (p > 0.5)", f"{high_risk:,}")
    
    with col3:
        avg_prob = df['churn_probability'].mean()
        st.metric("Avg Churn Probability", f"{avg_prob:.1%}")
    
    with col4:
        premium_customers = (df['subscription_type'] == 'Premium').sum()
        st.metric("Premium Customers", f"{premium_customers:,}")
    
    st.markdown("---")
    
    # Run optimization
    if run_optimization:
        st.header("Running Optimization...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Preparing data...")
            progress_bar.progress(20)
            
            df.to_csv('temp_optimization_data.csv', index=False)
            
            status_text.text("Initializing optimizer...")
            progress_bar.progress(40)
            
            optimizer = MusicStreamingRetentionOptimizer()
            
            df[['customer_id', 'churn_probability']].to_csv('temp_churn.csv', index=False)
            feature_cols = ['customer_id', 'subscription_type', 'payment_plan', 
                           'weekly_hours', 'weekly_songs_played', 'num_playlists_created']
            df[feature_cols].to_csv('temp_features.csv', index=False)
            
            optimizer.load_data(
                churn_file='temp_churn.csv',
                customer_features_file='temp_features.csv',
                actions_file=None
            )
            
            status_text.text("Setting constraints...")
            progress_bar.progress(60)
            
            optimizer.set_constraints({
                'weekly_budget': budget,
                'email_capacity': email_cap,
                'call_capacity': push_cap,
                'min_high_risk_pct': min_high_risk,
                'min_premium_pct': min_premium,
                'max_action_pct': max_action_pct,
                'min_segment_coverage_pct': min_segment_coverage
            })
            
            status_text.text("Solving optimization (30-90 seconds)...")
            progress_bar.progress(80)
            
            optimizer.optimize()
            
            status_text.text("Complete!")
            progress_bar.progress(100)
            
            st.session_state.optimizer = optimizer
            st.session_state.results_ready = True
            
            st.success("Optimization completed successfully!")
            
            for f in ['temp_churn.csv', 'temp_features.csv', 'temp_optimization_data.csv']:
                if os.path.exists(f):
                    os.remove(f)
            
        except Exception as e:
            st.error(f"Optimization failed: {str(e)}")
            st.session_state.results_ready = False
    
    # Results
    if st.session_state.results_ready and st.session_state.optimizer is not None:
        st.markdown("---")
        st.header("Optimization Results")
        
        optimizer = st.session_state.optimizer
        kpis = optimizer.results.get('kpis', {})
        assignments = optimizer.results.get('assignments', pd.DataFrame())
        
        if kpis and not assignments.empty:
            
            # Key Metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Customers Treated", f"{kpis['customers_treated']:,}")
            
            with col2:
                st.metric("Weekly Spend", f"${kpis['total_spend']:,.0f}")
            
            with col3:
                st.metric("Churn Prevented", f"{kpis['expected_churn_reduction']:.0f}")
            
            with col4:
                st.metric("Retained CLV", f"${kpis['expected_retained_clv']:,.0f}")
            
            with col5:
                st.metric("ROI", f"{kpis['roi']:.0f}%")
            
            st.success(f"**Net Value: ${kpis['net_value']:,.0f}**")
            
            st.markdown("---")
            
            # Results tabs
            tab1, tab2 = st.tabs(["Treatment Plan", "Top Customers"])
            
            with tab1:
                action_summary = assignments.groupby('action_name').agg({
                    'customer_id': 'count',
                    'cost': 'sum',
                    'net_value': 'sum'
                }).reset_index()
                action_summary.columns = ['Action', 'Customers', 'Total Cost', 'Net Value']
                
                st.dataframe(action_summary, use_container_width=True, hide_index=True)
            
            with tab2:
                top_customers = assignments.nlargest(50, 'net_value')[[
                    'customer_id', 'subscription_type', 'churn_prob',
                    'action_name', 'net_value'
                ]].copy()
                
                st.dataframe(top_customers, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Export
            st.subheader("Export Treatment Plan")
            
            export_df = assignments.copy()
            csv = export_df.to_csv(index=False)
            
            st.download_button(
                label="Download Complete Treatment Plan (CSV)",
                data=csv,
                file_name=f"treatment_plan_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

else:
    st.error("Unable to load customer data. Please ensure prediction_250.csv and test_250.csv are in the project directory.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Predictive Analytics + Prescriptive Optimization</p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        © 2025 PlaylistPro Analytics Team | Satkar Karki
    </p>
</div>
""", unsafe_allow_html=True)
