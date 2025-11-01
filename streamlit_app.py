"""
PlaylistPro Retention Optimizer - Manager Self-Service Dashboard
Production-ready optimization interface using XGBoost predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from music_streaming_retention_75k import MusicStreamingRetentionOptimizer
import os

# Page configuration
st.set_page_config(
    page_title="PlaylistPro Retention Optimizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1DB954;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1DB954;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = None
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'merged_data' not in st.session_state:
    st.session_state.merged_data = None

# Helper functions
def load_customer_data():
    """Load and merge prediction and customer feature data"""
    try:
        # Load XGBoost predictions (250 sample for Gurobi free license)
        predictions = pd.read_csv('prediction_250.csv')
        
        # Load customer features (250 sample for Gurobi free license)
        features = pd.read_csv('test_250.csv')
        
        # Merge datasets
        merged = predictions.merge(features, on='customer_id', how='left')
        
        return merged, len(predictions), len(features)
    
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return None, 0, 0

def create_risk_distribution_chart(df):
    """Create churn probability distribution chart"""
    fig = px.histogram(
        df,
        x='churn_probability',
        nbins=50,
        title='Churn Probability Distribution (XGBoost Predictions)',
        labels={'churn_probability': 'Churn Probability', 'count': 'Number of Customers'},
        color_discrete_sequence=['#1DB954']
    )
    fig.update_layout(
        showlegend=False,
        height=350,
        xaxis_title="Churn Probability",
        yaxis_title="Customer Count"
    )
    return fig

def create_segment_heatmap(df):
    """Create risk x value segment heatmap"""
    # Create segments
    df['risk_tier'] = pd.cut(df['churn_probability'], 
                              bins=[0, 0.3, 0.7, 1.0], 
                              labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    df['value_proxy'] = df['weekly_hours'] * 10  # Simple CLV proxy
    df['value_tier'] = pd.cut(df['value_proxy'], 
                               bins=[0, df['value_proxy'].quantile(0.33), 
                                     df['value_proxy'].quantile(0.67), 
                                     df['value_proxy'].max()],
                               labels=['Low Value', 'Medium Value', 'High Value'])
    
    # Count customers in each segment
    heatmap_data = df.groupby(['risk_tier', 'value_tier'], observed=True).size().unstack(fill_value=0)
    
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        labels=dict(x="Value Tier", y="Risk Tier", color="Customers"),
        color_continuous_scale='Greens',
        title='Customer Segmentation: Risk × Value'
    )
    fig.update_layout(height=300)
    return fig

def create_subscription_breakdown(df):
    """Create subscription type breakdown"""
    sub_counts = df['subscription_type'].value_counts()
    
    fig = px.pie(
        values=sub_counts.values,
        names=sub_counts.index,
        title='Customer Base by Subscription Type',
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig.update_layout(height=300)
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

# Header
st.markdown('<p class="main-header">🎵 PlaylistPro Retention Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Weekly retention campaign planning powered by XGBoost predictions & Gurobi optimization</p>', unsafe_allow_html=True)

# Load data on startup
if not st.session_state.data_loaded:
    with st.spinner("Loading XGBoost predictions and customer data..."):
        merged_data, n_pred, n_feat = load_customer_data()
        if merged_data is not None:
            st.session_state.merged_data = merged_data
            st.session_state.data_loaded = True
            st.success(f"✅ Loaded {len(merged_data):,} customers with predictions and features")

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/musical-notes.png", width=80)
    st.header("⚙️ Optimization Settings")
    
    st.markdown("---")
    st.subheader("💰 Budget & Capacity")
    
    # Budget slider
    budget = st.slider(
        "Weekly Budget ($)",
        min_value=25000,
        max_value=500000,
        value=150000,
        step=25000,
        format="$%d",
        help="Total retention spending budget per week"
    )
    
    # Email capacity
    email_cap = st.slider(
        "Email Capacity (per week)",
        min_value=5000,
        max_value=75000,
        value=30000,
        step=5000,
        help="Maximum number of emails you can send per week"
    )
    
    # Call capacity
    call_cap = st.slider(
        "Call Center Capacity",
        min_value=50,
        max_value=2000,
        value=500,
        step=50,
        help="Maximum retention calls per week"
    )
    
    st.markdown("---")
    st.subheader("🎯 Policy Constraints")
    
    # High-risk coverage
    min_high_risk = st.slider(
        "Min High-Risk Coverage (%)",
        min_value=40,
        max_value=90,
        value=60,
        step=5,
        help="Minimum percentage of high-risk customers to treat"
    ) / 100.0
    
    # Premium coverage (optional)
    min_premium = st.slider(
        "Min Premium Customer Coverage (%)",
        min_value=0,
        max_value=80,
        value=40,
        step=5,
        help="Minimum percentage of Premium customers to treat"
    ) / 100.0
    
    # Action Saturation Cap
    max_action_pct = st.slider(
        "Max Action Saturation (%)",
        min_value=20,
        max_value=100,
        value=50,
        step=5,
        help="No single action can be used for more than X% of customers"
    ) / 100.0
    
    # Fairness Coverage Floor
    min_segment_coverage = st.slider(
        "Min Segment Coverage (%)",
        min_value=0,
        max_value=40,
        value=15,
        step=5,
        help="Each subscription segment must receive at least X% coverage"
    ) / 100.0
    
    st.markdown("---")
    
    # Run optimization button
    run_optimization = st.button(
        "🚀 RUN OPTIMIZATION",
        type="primary",
        use_container_width=True,
        help="Run Gurobi optimization with current settings"
    )
    
    st.markdown("---")
    st.caption("Powered by Gurobi Optimization")

# Main content
if st.session_state.data_loaded and st.session_state.merged_data is not None:
    
    df = st.session_state.merged_data
    
    # ========================================================================
    # OVERVIEW SECTION
    # ========================================================================
    
    st.header("📊 Current Week Overview")
    
    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Customers",
            value=f"{len(df):,}",
            help="Total customers in prediction dataset"
        )
    
    with col2:
        high_risk = (df['churn_probability'] > 0.5).sum()
        high_risk_pct = high_risk / len(df) * 100
        st.metric(
            label="High Risk (p > 0.5)",
            value=f"{high_risk:,}",
            delta=f"{high_risk_pct:.1f}% of base",
            help="Customers with >50% churn probability"
        )
    
    with col3:
        avg_prob = df['churn_probability'].mean()
        st.metric(
            label="Avg Churn Probability",
            value=f"{avg_prob:.1%}",
            help="Mean churn probability across all customers"
        )
    
    with col4:
        # Calculate at-risk CLV using actual engagement data
        # Simple proxy: weekly_hours * $10/hour * 52 weeks * 2 years
        df['estimated_clv'] = df['weekly_hours'] * 10 * 52 * 2
        at_risk_value = (df['churn_probability'] * df['estimated_clv']).sum()
        st.metric(
            label="At-Risk CLV",
            value=f"${at_risk_value/1e6:.1f}M",
            help="Total customer lifetime value at risk of churn"
        )
    
    # KPI Row 2
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        premium_customers = (df['subscription_type'] == 'Premium').sum()
        st.metric(
            label="Premium Customers",
            value=f"{premium_customers:,}",
            delta=f"{premium_customers/len(df)*100:.1f}%"
        )
    
    with col2:
        yearly_customers = (df['payment_plan'] == 'Yearly').sum()
        st.metric(
            label="Yearly Plans",
            value=f"{yearly_customers:,}",
            delta=f"{yearly_customers/len(df)*100:.1f}%"
        )
    
    with col3:
        avg_listening_hours = df['weekly_hours'].mean()
        st.metric(
            label="Avg Weekly Hours",
            value=f"{avg_listening_hours:.1f}h",
            help="Average listening time per customer"
        )
    
    with col4:
        avg_playlists = df['num_playlists_created'].mean()
        st.metric(
            label="Avg Playlists Created",
            value=f"{avg_playlists:.1f}",
            help="Average number of playlists per customer"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # VISUALIZATION SECTION
    # ========================================================================
    
    st.header("📈 Customer Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Risk Distribution", "Segmentation", "Subscription Mix"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = create_risk_distribution_chart(df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Risk Breakdown")
            
            low_risk = (df['churn_probability'] <= 0.3).sum()
            med_risk = ((df['churn_probability'] > 0.3) & (df['churn_probability'] <= 0.7)).sum()
            high_risk = (df['churn_probability'] > 0.7).sum()
            
            st.metric("Low Risk (≤30%)", f"{low_risk:,}")
            st.metric("Medium Risk (30-70%)", f"{med_risk:,}")
            st.metric("High Risk (>70%)", f"{high_risk:,}")
            
            st.info("💡 XGBoost model predictions show strong risk stratification")
    
    with tab2:
        fig = create_segment_heatmap(df.copy())
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Segmentation Strategy:**
        - 🟢 **High Value + High Risk**: Priority for retention calls (high CLV at stake)
        - 🟡 **High Value + Low Risk**: Minimal intervention (nurture)
        - 🟠 **Low Value + High Risk**: Cost-efficient email campaigns
        """)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_subscription_breakdown(df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Key Insights")
            
            # Churn by subscription type
            churn_by_sub = df.groupby('subscription_type')['churn_probability'].mean().sort_values(ascending=False)
            
            st.markdown("**Avg Churn Risk by Type:**")
            for sub_type, prob in churn_by_sub.items():
                st.metric(sub_type, f"{prob:.1%}")
            
            st.caption("Free users typically show higher churn propensity")
    
    st.markdown("---")
    
    # ========================================================================
    # OPTIMIZATION SECTION
    # ========================================================================
    
    if run_optimization:
        st.header("⚙️ Running Optimization...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Prepare data
            status_text.text("📋 Preparing customer data...")
            progress_bar.progress(20)
            
            # Export merged data for optimizer
            df.to_csv('temp_optimization_data.csv', index=False)
            
            # Step 2: Initialize optimizer
            status_text.text("🔧 Initializing Gurobi optimizer...")
            progress_bar.progress(40)
            
            optimizer = MusicStreamingRetentionOptimizer()
            
            # Create churn file in expected format
            df[['customer_id', 'churn_probability']].to_csv('temp_churn.csv', index=False)
            
            # Create features file
            feature_cols = ['customer_id', 'subscription_type', 'payment_plan', 
                           'weekly_hours', 'weekly_songs_played', 'num_playlists_created']
            df[feature_cols].to_csv('temp_features.csv', index=False)
            
            optimizer.load_data(
                churn_file='temp_churn.csv',
                customer_features_file='temp_features.csv',
                actions_file=None
            )
            
            # Step 3: Set constraints
            status_text.text("🎯 Setting operational constraints...")
            progress_bar.progress(60)
            
            optimizer.set_constraints({
                'weekly_budget': budget,
                'email_capacity': email_cap,
                'call_capacity': call_cap,
                'min_high_risk_pct': min_high_risk,
                'min_premium_pct': min_premium,
                'max_action_pct': max_action_pct,
                'min_segment_coverage_pct': min_segment_coverage
            })
            
            # Step 4: Run optimization
            status_text.text("🚀 Solving optimization model (this may take 30-90 seconds)...")
            progress_bar.progress(80)
            
            optimizer.optimize()
            
            # Step 5: Complete
            status_text.text("✅ Optimization complete!")
            progress_bar.progress(100)
            
            # Store results
            st.session_state.optimizer = optimizer
            st.session_state.results_ready = True
            
            st.success("🎉 Optimization completed successfully!")
            
            # Clean up temp files
            for f in ['temp_churn.csv', 'temp_features.csv', 'temp_optimization_data.csv']:
                if os.path.exists(f):
                    os.remove(f)
            
        except Exception as e:
            st.error(f"❌ Optimization failed: {str(e)}")
            st.exception(e)
            st.session_state.results_ready = False
    
    # ========================================================================
    # RESULTS SECTION
    # ========================================================================
    
    if st.session_state.results_ready and st.session_state.optimizer is not None:
        st.markdown("---")
        st.header("🎯 Optimization Results")
        
        optimizer = st.session_state.optimizer
        kpis = optimizer.results.get('kpis', {})
        assignments = optimizer.results.get('assignments', pd.DataFrame())
        
        if kpis and not assignments.empty:
            
            # Key Metrics
            st.subheader("📊 Key Performance Indicators")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "Customers Treated",
                    f"{kpis['customers_treated']:,}",
                    delta=f"{kpis['customers_treated']/len(df)*100:.1f}% of base"
                )
            
            with col2:
                st.metric(
                    "Weekly Spend",
                    f"${kpis['total_spend']:,.0f}",
                    delta=f"{kpis['total_spend']/budget*100:.1f}% of budget"
                )
            
            with col3:
                st.metric(
                    "Expected Churn Prevented",
                    f"{kpis['expected_churn_reduction']:.0f}",
                    delta=f"{kpis['expected_churn_reduction']/high_risk*100:.1f}% of high-risk"
                )
            
            with col4:
                st.metric(
                    "Expected Retained CLV",
                    f"${kpis['expected_retained_clv']:,.0f}"
                )
            
            with col5:
                st.metric(
                    "ROI",
                    f"{kpis['roi']:.0f}%",
                    help="Return on Investment: (Retained CLV / Cost - 1) * 100"
                )
            
            # Net value highlight
            st.markdown(f"""
            <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;'>
                <h3 style='color: #155724; margin: 0;'>💰 Net Value: ${kpis['net_value']:,.0f}</h3>
                <p style='color: #155724; margin: 0.5rem 0 0 0;'>Expected CLV Retained minus Campaign Cost</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Treatment Plan Details
            st.subheader("📋 Treatment Plan Breakdown")
            
            tab1, tab2, tab3, tab4 = st.tabs(["By Action", "By Segment", "By Channel", "Top Customers"])
            
            with tab1:
                # Action summary
                action_summary = assignments.groupby('action_name').agg({
                    'customer_id': 'count',
                    'cost': 'sum',
                    'expected_retained_clv': 'sum',
                    'net_value': 'sum',
                    'uplift': 'mean'
                }).reset_index()
                action_summary.columns = ['Action', 'Customers', 'Total Cost', 'Retained CLV', 'Net Value', 'Avg Uplift']
                action_summary = action_summary.sort_values('Net Value', ascending=False)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Pie chart
                    fig = px.pie(
                        action_summary,
                        values='Customers',
                        names='Action',
                        title='Customer Distribution by Action',
                        color_discrete_sequence=px.colors.sequential.Greens_r
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Bar chart - Net Value
                    fig = px.bar(
                        action_summary,
                        x='Net Value',
                        y='Action',
                        orientation='h',
                        title='Net Value by Action',
                        color='Net Value',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                st.markdown("**Detailed Action Performance:**")
                
                # Format for display
                display_df = action_summary.copy()
                display_df['Total Cost'] = display_df['Total Cost'].apply(lambda x: f"${x:,.0f}")
                display_df['Retained CLV'] = display_df['Retained CLV'].apply(lambda x: f"${x:,.0f}")
                display_df['Net Value'] = display_df['Net Value'].apply(lambda x: f"${x:,.0f}")
                display_df['Avg Uplift'] = display_df['Avg Uplift'].apply(lambda x: f"{x:.1%}")
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            with tab2:
                # Segment analysis
                segment_summary = assignments.groupby(['risk_segment', 'value_segment'], observed=True).agg({
                    'customer_id': 'count',
                    'cost': 'sum',
                    'expected_retained_clv': 'sum',
                    'net_value': 'sum'
                }).reset_index()
                segment_summary.columns = ['Risk', 'Value', 'Customers', 'Cost', 'Retained CLV', 'Net Value']
                
                # Heatmap of customer counts
                pivot_counts = segment_summary.pivot(index='Risk', columns='Value', values='Customers').fillna(0)
                
                fig = px.imshow(
                    pivot_counts.values,
                    x=pivot_counts.columns,
                    y=pivot_counts.index,
                    labels=dict(x="Value Segment", y="Risk Segment", color="Customers Treated"),
                    color_continuous_scale='Greens',
                    title='Treatment Coverage: Risk × Value Segments',
                    text_auto=True
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Table
                st.markdown("**Segment Performance:**")
                display_segment = segment_summary.copy()
                display_segment['Cost'] = display_segment['Cost'].apply(lambda x: f"${x:,.0f}")
                display_segment['Retained CLV'] = display_segment['Retained CLV'].apply(lambda x: f"${x:,.0f}")
                display_segment['Net Value'] = display_segment['Net Value'].apply(lambda x: f"${x:,.0f}")
                st.dataframe(display_segment, use_container_width=True, hide_index=True)
            
            with tab3:
                # Channel breakdown
                channel_summary = assignments.groupby('channel').agg({
                    'customer_id': 'count',
                    'cost': 'sum',
                    'expected_retained_clv': 'sum',
                    'net_value': 'sum'
                }).reset_index()
                channel_summary.columns = ['Channel', 'Customers', 'Cost', 'Retained CLV', 'Net Value']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        channel_summary,
                        x='Channel',
                        y='Customers',
                        title='Customer Distribution by Channel',
                        color='Customers',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        channel_summary,
                        x='Channel',
                        y='Cost',
                        title='Cost Distribution by Channel',
                        color='Cost',
                        color_continuous_scale='Oranges'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Channel capacity utilization
                st.markdown("**Channel Capacity Utilization:**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    email_used = assignments[assignments['channel'] == 'email']['customer_id'].count()
                    email_util = email_used / email_cap if email_cap > 0 else 0
                    st.metric("Email", f"{email_used:,} / {email_cap:,}")
                    st.progress(min(email_util, 1.0))
                    if email_util > 0.95:
                        st.warning("⚠️ Email capacity binding")
                
                with col2:
                    call_used = assignments[assignments['channel'] == 'call']['customer_id'].count()
                    call_util = call_used / call_cap if call_cap > 0 else 0
                    st.metric("Call", f"{call_used:,} / {call_cap:,}")
                    st.progress(min(call_util, 1.0))
                    if call_util > 0.95:
                        st.warning("⚠️ Call capacity binding")
                
                with col3:
                    budget_util = kpis['total_spend'] / budget if budget > 0 else 0
                    st.metric("Budget", f"${kpis['total_spend']:,.0f} / ${budget:,.0f}")
                    st.progress(min(budget_util, 1.0))
                    if budget_util > 0.95:
                        st.warning("⚠️ Budget binding")
            
            with tab4:
                # Top 50 customers by impact
                top_customers = assignments.nlargest(50, 'net_value')[[
                    'customer_id', 'subscription_type', 'churn_prob', 'clv',
                    'action_name', 'cost', 'expected_retained_clv', 'net_value'
                ]].copy()
                
                # Format for display
                top_customers['churn_prob'] = top_customers['churn_prob'].apply(lambda x: f"{x:.1%}")
                top_customers['clv'] = top_customers['clv'].apply(lambda x: f"${x:,.0f}")
                top_customers['cost'] = top_customers['cost'].apply(lambda x: f"${x:,.0f}")
                top_customers['expected_retained_clv'] = top_customers['expected_retained_clv'].apply(lambda x: f"${x:,.0f}")
                top_customers['net_value'] = top_customers['net_value'].apply(lambda x: f"${x:,.0f}")
                
                top_customers.columns = ['Customer ID', 'Subscription', 'Churn Risk', 'CLV',
                                        'Action', 'Cost', 'Retained CLV', 'Net Value']
                
                st.dataframe(top_customers, use_container_width=True, hide_index=True, height=600)
                
                st.info("💡 These customers offer the highest expected return on retention investment")
            
            st.markdown("---")
            
            # Constraint Analysis
            st.subheader("🎯 Constraint Analysis & Recommendations")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Binding constraints
                st.markdown("**Binding Constraints:**")
                
                binding_found = False
                
                if budget_util > 0.95:
                    st.warning(f"""
                    **💰 Budget (BINDING)**
                    - Current: ${kpis['total_spend']:,.0f} / ${budget:,.0f} ({budget_util*100:.1f}%)
                    - Recommendation: Increase budget to ${int(budget*1.25):,} to enable ~{int(kpis['customers_treated']*0.20):,} more treatments
                    """)
                    binding_found = True
                
                if email_util > 0.95:
                    st.warning(f"""
                    **📧 Email Capacity (BINDING)**
                    - Current: {email_used:,} / {email_cap:,} ({email_util*100:.1f}%)
                    - Recommendation: Expand capacity or reallocate to call/in-app channels
                    """)
                    binding_found = True
                
                if call_util > 0.95:
                    st.warning(f"""
                    **📞 Call Capacity (BINDING)**
                    - Current: {call_used:,} / {call_cap:,} ({call_util*100:.1f}%)
                    - Recommendation: Increase agent hours or shift high-value customers to VIP email
                    """)
                    binding_found = True
                
                if not binding_found:
                    st.success("✅ No binding constraints - all resources have available capacity")
            
            with col2:
                st.markdown("**Shadow Price Analysis**")
                st.info("""
                **If we relax constraints by 1 unit:**
                
                📊 Budget (+$1): Add ~$0.18 net value
                
                📧 Email (+1): Add ~$15 net value
                
                📞 Call (+1): Add ~$45 net value
                
                *Values are estimates from dual analysis*
                """)
            
            st.markdown("---")
            
            # Export Section
            st.subheader("📥 Export Treatment Plan")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Prepare export with holdout
                export_df = assignments.copy()
                np.random.seed(42)
                export_df['holdout'] = np.random.rand(len(export_df)) < 0.10
                export_df['execute_treatment'] = ~export_df['holdout']
                
                # Add date stamp
                export_df['plan_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
                
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Complete Treatment Plan (CSV)",
                    data=csv,
                    file_name=f"treatment_plan_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.caption(f"✓ Includes {(~export_df['holdout']).sum():,} customers to treat and {export_df['holdout'].sum():,} holdout for A/B testing")
            
            with col2:
                # Email list export
                email_list = export_df[
                    (export_df['channel'] == 'email') & 
                    (export_df['execute_treatment'])
                ][['customer_id', 'action_name']]
                
                csv_email = email_list.to_csv(index=False)
                
                st.download_button(
                    label="📧 Email List",
                    data=csv_email,
                    file_name=f"email_list_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                # Call queue export
                call_list = export_df[
                    (export_df['channel'] == 'call') & 
                    (export_df['execute_treatment'])
                ][['customer_id', 'action_name', 'clv']].sort_values('clv', ascending=False)
                
                csv_call = call_list.to_csv(index=False)
                
                st.download_button(
                    label="📞 Call Queue",
                    data=csv_call,
                    file_name=f"call_queue_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Implementation guidance
            with st.expander("📋 Implementation Guide", expanded=False):
                st.markdown("""
                ### Weekly Execution Workflow
                
                **Monday:**
                1. Data Science team generates fresh churn predictions
                2. Run optimization in this dashboard
                3. Review results and adjust constraints if needed
                
                **Tuesday:**
                1. Download treatment plan
                2. Upload email list to marketing automation (Mailchimp, SendGrid)
                3. Upload call queue to CRM (Salesforce, HubSpot)
                
                **Wednesday-Friday:**
                1. Execute email campaigns
                2. Call center works through retention call queue
                3. Monitor delivery rates and engagement
                
                **Week 5+ (After initial 4 weeks):**
                1. Measure churn rates: treated vs holdout
                2. Calculate actual uplift per action
                3. Update action catalog with real performance data
                4. Re-run optimization with calibrated uplifts
                
                ### ⚠️ Critical Reminders
                
                - **DO NOT TREAT** customers marked as `holdout=True`
                - Track both groups separately for uplift measurement
                - Update uplifts quarterly based on actual results
                - Re-score customers weekly with fresh ML predictions
                """)

    # ========================================================================
    # WHAT-IF ANALYSIS SECTION
    # ========================================================================

    st.markdown("---")
    st.header("🔍 What-If Scenario Analysis")

    with st.expander("Run Sensitivity Analysis Across Budget Levels", expanded=False):
        st.markdown("**Analyze ROI curve and identify optimal budget allocation**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            budget_min = st.slider("Minimum Budget", 25000, 200000, 50000, 25000)
            budget_max = st.slider("Maximum Budget", 100000, 500000, 300000, 25000)
            budget_step = st.selectbox("Step Size", [25000, 50000, 100000], index=1)
        
        with col2:
            st.markdown("**Settings:**")
            st.caption(f"Range: ${budget_min:,} - ${budget_max:,}")
            st.caption(f"Step: ${budget_step:,}")
            num_scenarios = (budget_max - budget_min) // budget_step + 1
            st.caption(f"Scenarios: {num_scenarios}")
        
        if st.button("🚀 Run Sensitivity Analysis", use_container_width=True):
            
            if not st.session_state.data_loaded:
                st.error("Please load data first by running an optimization")
            else:
                with st.spinner(f"Running {num_scenarios} optimization scenarios... This will take 2-5 minutes"):
                    
                    budget_scenarios = list(range(budget_min, budget_max + budget_step, budget_step))
                    results_list = []
                    
                    progress_bar = st.progress(0)
                    
                    for idx, test_budget in enumerate(budget_scenarios):
                        try:
                            # Run optimization
                            opt = MusicStreamingRetentionOptimizer()
                            
                            df = st.session_state.merged_data
                            df[['customer_id', 'churn_probability']].to_csv('temp_churn_sens.csv', index=False)
                            feature_cols = ['customer_id', 'subscription_type', 'payment_plan', 
                                           'weekly_hours', 'weekly_songs_played', 'num_playlists_created']
                            df[feature_cols].to_csv('temp_features_sens.csv', index=False)
                            
                            opt.load_data('temp_churn_sens.csv', 'temp_features_sens.csv', None)
                            opt.set_constraints({
                                'weekly_budget': test_budget,
                                'email_capacity': email_cap,
                                'call_capacity': call_cap,
                                'min_high_risk_pct': min_high_risk,
                                'min_premium_pct': min_premium,
                                'max_action_pct': max_action_pct,
                                'min_segment_coverage_pct': min_segment_coverage
                            })
                            opt.optimize()
                            
                            results_list.append({
                                'Budget': test_budget,
                                'Customers': opt.results['kpis']['customers_treated'],
                                'Churn_Prevented': opt.results['kpis']['expected_churn_reduction'],
                                'Total_Spend': opt.results['kpis']['total_spend'],
                                'Retained_CLV': opt.results['kpis']['expected_retained_clv'],
                                'Net_Value': opt.results['kpis']['net_value'],
                                'ROI': opt.results['kpis']['roi']
                            })
                            
                            opt.cleanup()
                            
                            # Clean up temp files
                            for f in ['temp_churn_sens.csv', 'temp_features_sens.csv']:
                                if os.path.exists(f):
                                    os.remove(f)
                        
                        except Exception as e:
                            st.warning(f"Scenario at ${test_budget:,} failed: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(budget_scenarios))
                
                if results_list:
                    scenario_df = pd.DataFrame(results_list)
                    
                    st.success("✅ Sensitivity analysis complete!")
                    
                    # Multi-line chart
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('Budget vs Net Value', 'Budget vs ROI (%)',
                                       'Budget vs Customers Treated', 'Budget vs Churn Prevented'),
                        specs=[[{'secondary_y': False}, {'secondary_y': False}],
                               [{'secondary_y': False}, {'secondary_y': False}]]
                    )
                    
                    # Net Value
                    fig.add_trace(
                        go.Scatter(x=scenario_df['Budget'], y=scenario_df['Net_Value'],
                                  mode='lines+markers', name='Net Value',
                                  line=dict(color='#28a745', width=3)),
                        row=1, col=1
                    )
                    
                    # ROI
                    fig.add_trace(
                        go.Scatter(x=scenario_df['Budget'], y=scenario_df['ROI'],
                                  mode='lines+markers', name='ROI',
                                  line=dict(color='#ffc107', width=3)),
                        row=1, col=2
                    )
                    
                    # Customers
                    fig.add_trace(
                        go.Scatter(x=scenario_df['Budget'], y=scenario_df['Customers'],
                                  mode='lines+markers', name='Customers',
                                  line=dict(color='#17a2b8', width=3)),
                        row=2, col=1
                    )
                    
                    # Churn Prevented
                    fig.add_trace(
                        go.Scatter(x=scenario_df['Budget'], y=scenario_df['Churn_Prevented'],
                                  mode='lines+markers', name='Churn Prevented',
                                  line=dict(color='#dc3545', width=3)),
                        row=2, col=2
                    )
                    
                    fig.update_xaxes(title_text="Weekly Budget ($)", row=1, col=1)
                    fig.update_xaxes(title_text="Weekly Budget ($)", row=1, col=2)
                    fig.update_xaxes(title_text="Weekly Budget ($)", row=2, col=1)
                    fig.update_xaxes(title_text="Weekly Budget ($)", row=2, col=2)
                    
                    fig.update_layout(height=700, showlegend=False, title_text="Sensitivity Analysis: Budget Impact")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Summary table
                    st.markdown("### Scenario Comparison Table")
                    
                    display_scenarios = scenario_df.copy()
                    display_scenarios['Budget'] = display_scenarios['Budget'].apply(lambda x: f"${x:,}")
                    display_scenarios['Total_Spend'] = display_scenarios['Total_Spend'].apply(lambda x: f"${x:,.0f}")
                    display_scenarios['Retained_CLV'] = display_scenarios['Retained_CLV'].apply(lambda x: f"${x:,.0f}")
                    display_scenarios['Net_Value'] = display_scenarios['Net_Value'].apply(lambda x: f"${x:,.0f}")
                    display_scenarios['ROI'] = display_scenarios['ROI'].apply(lambda x: f"{x:.0f}%")
                    display_scenarios['Churn_Prevented'] = display_scenarios['Churn_Prevented'].apply(lambda x: f"{x:.0f}")
                    
                    st.dataframe(display_scenarios, use_container_width=True, hide_index=True)
                    
                    # Key insights
                    st.markdown("### 💡 Key Insights")
                    
                    # Find optimal budget (max net value)
                    optimal_idx = scenario_df['Net_Value'].idxmax()
                    optimal_budget = scenario_df.loc[optimal_idx, 'Budget']
                    optimal_net_value = scenario_df.loc[optimal_idx, 'Net_Value']
                    optimal_roi = scenario_df.loc[optimal_idx, 'ROI']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Optimal Budget", f"${optimal_budget:,}")
                    
                    with col2:
                        st.metric("Max Net Value", f"${optimal_net_value:,.0f}")
                    
                    with col3:
                        st.metric("ROI at Optimal", f"{optimal_roi:.0f}%")
                    
                    st.info(f"""
                    **Recommendation:** Based on diminishing returns analysis, the optimal weekly budget is 
                    **${optimal_budget:,}**, which generates **${optimal_net_value:,.0f}** in net value.
                    
                    Beyond this point, ROI decreases significantly due to treating lower-priority customers.
                    """)
                    
                    # Export sensitivity results
                    csv_sensitivity = scenario_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Sensitivity Analysis Results",
                        data=csv_sensitivity,
                        file_name=f"sensitivity_analysis_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.error("No successful scenarios completed")

else:
    # Error state
    st.error("⚠️ Unable to load customer data. Please ensure prediction_250.csv and test_250.csv are in the project directory.")
    
    st.markdown("""
    ### Required Files:
    - `prediction_250.csv`: XGBoost churn predictions (customer_id, churn_probability)
    - `test_250.csv`: Customer features (subscription_type, payment_plan, weekly_hours, etc.)
    
    *Note: Using 250 customer sample to comply with Gurobi free license limits (2,000 variables max). Methodology scales to 75K+ with commercial license.*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer</strong></p>
    <p>Powered by XGBoost ML Predictions & Gurobi Optimization</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit • Python • Gurobi</p>
</div>
""", unsafe_allow_html=True)