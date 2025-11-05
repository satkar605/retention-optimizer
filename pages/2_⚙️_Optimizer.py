"""
PlaylistPro Retention Optimizer - Main Dashboard
Simplified optimization interface with smart constraint validation
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
    
    # Calculate feasible ranges based on dataset
    if st.session_state.data_loaded and st.session_state.merged_data is not None:
        df_temp = st.session_state.merged_data
        N = len(df_temp)
        high_risk_count = int((df_temp['churn_probability'] > 0.5).sum())
        premium_count = int((df_temp['subscription_type'] == 'Premium').sum())
        
        # Calculate minimum required capacity
        min_high_risk_needed = int(high_risk_count * 0.6)  # 60% of high-risk
        min_premium_needed = int(premium_count * 0.4)  # 40% of premium
        
        # Segment coverage (15% of each segment)
        segment_sizes = []
        for seg in ['Premium', 'Free', 'Family', 'Student']:
            seg_size = int((df_temp['subscription_type'] == seg).sum())
            segment_sizes.append(int(seg_size * 0.15))
        min_segment_needed = sum(segment_sizes)
        
        # Overall minimum capacity needed
        min_capacity_needed = max(min_high_risk_needed, min_premium_needed, min_segment_needed)
        
        # Budget slider with smart minimum
        min_budget = max(150, min_capacity_needed * 2)  # $2 = cheapest action
        budget = st.slider(
            "Weekly Budget ($)",
            min_value=min_budget,
            max_value=1000,
            value=max(150, min_budget),
            step=25,
            format="$%d",
            help=f"Minimum ${min_budget} required to meet policy constraints. Optimal range: $250-$400."
        )
        
        # Email capacity with smart minimum
        email_cap = st.slider(
            "Email Capacity (per week)",
            min_value=min_capacity_needed,
            max_value=int(N),
            value=min(120, max(min_capacity_needed, 120)),
            step=10,
            help=f"Minimum {min_capacity_needed} needed for policy floors. Max {N} (total customers)."
        )
        
        # Push capacity with smart minimum
        push_cap = st.slider(
            "In-App/Push Notification Capacity",
            min_value=50,
            max_value=int(N),
            value=min(100, int(N)),
            step=10,
            help="In-app messages and push notifications capacity."
        )
    else:
        # Fallback if data not loaded
        budget = st.slider("Weekly Budget ($)", min_value=150, max_value=1000, value=150, step=25)
        email_cap = st.slider("Email Capacity (per week)", min_value=60, max_value=250, value=120, step=10)
        push_cap = st.slider("In-App/Push Notification Capacity", min_value=50, max_value=250, value=100, step=10)
    
    st.markdown("---")
    st.subheader("🎯 Policy Constraints")
    
    st.info("💡 These constraints ensure fairness and strategic alignment. Adjust carefully.")
    
    # High-risk coverage
    min_high_risk = st.slider(
        "Min High-Risk Coverage (%)",
        min_value=40,
        max_value=90,
        value=60,
        step=5,
        help="Minimum % of high-risk customers (p>0.5) to treat. Ensures we don't ignore at-risk users."
    ) / 100.0
    
    # Premium coverage
    min_premium = st.slider(
        "Min Premium Customer Coverage (%)",
        min_value=10,
        max_value=80,
        value=40,
        step=5,
        help="Minimum % of Premium customers to treat. VIP treatment for high-value subscribers."
    ) / 100.0
    
    # Action Saturation Cap
    max_action_pct = st.slider(
        "Max Action Saturation (%)",
        min_value=30,
        max_value=80,
        value=50,
        step=5,
        help="No single action can be used for more than X% of customers. Forces campaign diversity."
    ) / 100.0
    
    # Fairness Coverage Floor
    min_segment_coverage = st.slider(
        "Min Segment Coverage (%)",
        min_value=10,
        max_value=40,
        value=15,
        step=5,
        help="Each subscription segment (Premium/Free/Family/Student) must receive at least X% coverage."
    ) / 100.0
    
    st.markdown("---")
    
    # Feasibility validation
    run_disabled = False
    error_messages = []
    
    if st.session_state.data_loaded and st.session_state.merged_data is not None:
        total_capacity = email_cap + push_cap
        
        # Check if capacity meets minimum requirements
        if total_capacity < min_capacity_needed:
            error_messages.append(f"⚠️ Total capacity ({total_capacity}) below minimum required ({min_capacity_needed})")
            run_disabled = True
        
        # Check if budget is sufficient
        if budget < min_capacity_needed * 2:
            error_messages.append(f"⚠️ Budget (${budget}) too low to cover minimum treatments (need ~${min_capacity_needed * 2})")
            run_disabled = True
        
        # Check action saturation vs segment floor conflict
        if max_action_pct < min_segment_coverage:
            error_messages.append("⚠️ Max action saturation is below segment floor - relax one of them")
            run_disabled = True
        
        # Display errors if any
        if error_messages:
            for msg in error_messages:
                st.error(msg)
    
    # Run optimization button
    run_optimization = st.button(
        "🚀 RUN OPTIMIZATION",
        type="primary",
        use_container_width=True,
        help="Run Gurobi optimization with current settings",
        disabled=run_disabled
    )
    
    st.markdown("---")
    st.caption("Powered by Gurobi Optimization")

# Main content
if st.session_state.data_loaded and st.session_state.merged_data is not None:
    
    df = st.session_state.merged_data
    
    # ========================================================================
    # OVERVIEW SECTION (Simplified - 5 key metrics)
    # ========================================================================
    
    st.header("📊 Current Week Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
        # Calculate at-risk CLV
        def calculate_clv(row):
            sub_type = row['subscription_type']
            payment_plan = row.get('payment_plan', 'Monthly')
            
            monthly_revenue = {
                'Premium': 15,
                'Family': 20,
                'Student': 10,
                'Free': 3
            }
            
            lifetime_months = {
                'Yearly': 24,
                'Monthly': 12
            }
            
            revenue = monthly_revenue.get(sub_type, 10)
            lifetime = lifetime_months.get(payment_plan, 12)
            
            return revenue * lifetime
        
        df['estimated_clv'] = df.apply(calculate_clv, axis=1)
        at_risk_value = (df['churn_probability'] * df['estimated_clv']).sum()
        st.metric(
            label="At-Risk CLV",
            value=f"${at_risk_value/1e3:.1f}K",
            help="Total customer lifetime value at risk of churn"
        )
    
    with col5:
        premium_customers = (df['subscription_type'] == 'Premium').sum()
        st.metric(
            label="Premium Customers",
            value=f"{premium_customers:,}",
            delta=f"{premium_customers/len(df)*100:.1f}%"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # VISUALIZATION SECTION
    # ========================================================================
    
    st.header("📈 Customer Analytics")
    
    tab1, tab2 = st.tabs(["Risk Distribution", "Segmentation"])
    
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
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_segment_heatmap(df.copy())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_subscription_breakdown(df)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Segmentation Strategy:**
        - 🟢 **High Value + High Risk**: Priority for retention (high CLV at stake)
        - 🟡 **High Value + Low Risk**: Minimal intervention (nurture)
        - 🟠 **Low Value + High Risk**: Cost-efficient email campaigns
        """)
    
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
                'call_capacity': push_cap,
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
            
            # Treatment Plan Details (Simplified - 3 tabs instead of 4)
            st.subheader("📋 Treatment Plan Breakdown")
            
            tab1, tab2, tab3 = st.tabs(["By Action & Channel", "By Segment", "Top Customers"])
            
            with tab1:
                # Combined action and channel analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Action Distribution**")
                    action_summary = assignments.groupby('action_name').agg({
                        'customer_id': 'count',
                        'cost': 'sum',
                        'expected_retained_clv': 'sum',
                        'net_value': 'sum'
                    }).reset_index()
                    action_summary.columns = ['Action', 'Customers', 'Total Cost', 'Retained CLV', 'Net Value']
                    action_summary = action_summary.sort_values('Net Value', ascending=False)
                    
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
                    st.markdown("**Channel Distribution**")
                    channel_summary = assignments.groupby('channel').agg({
                        'customer_id': 'count',
                        'cost': 'sum',
                        'net_value': 'sum'
                    }).reset_index()
                    channel_summary.columns = ['Channel', 'Customers', 'Cost', 'Net Value']
                    
                    fig = px.bar(
                        channel_summary,
                        x='Channel',
                        y='Customers',
                        title='Customer Distribution by Channel',
                        color='Customers',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed action table
                st.markdown("**Detailed Action Performance:**")
                display_df = action_summary.copy()
                display_df['Total Cost'] = display_df['Total Cost'].apply(lambda x: f"${x:,.0f}")
                display_df['Retained CLV'] = display_df['Retained CLV'].apply(lambda x: f"${x:,.0f}")
                display_df['Net Value'] = display_df['Net Value'].apply(lambda x: f"${x:,.0f}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
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
                    push_used = assignments[assignments['channel'].isin(['in_app', 'push'])]['customer_id'].count()
                    push_util = push_used / push_cap if push_cap > 0 else 0
                    st.metric("Push/In-App", f"{push_used:,} / {push_cap:,}")
                    st.progress(min(push_util, 1.0))
                    if push_util > 0.95:
                        st.warning("⚠️ Push/In-App capacity binding")
                
                with col3:
                    budget_util = kpis['total_spend'] / budget if budget > 0 else 0
                    st.metric("Budget", f"${kpis['total_spend']:,.0f} / ${budget:,.0f}")
                    st.progress(min(budget_util, 1.0))
                    if budget_util > 0.95:
                        st.warning("⚠️ Budget binding")
            
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

