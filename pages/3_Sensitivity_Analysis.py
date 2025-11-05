"""
PlaylistPro Retention Optimizer - Sensitivity Analysis
Budget sensitivity analysis and diminishing returns visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from music_streaming_retention_75k import MusicStreamingRetentionOptimizer
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Sensitivity Analysis - PlaylistPro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📊 Budget Sensitivity Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Understanding Diminishing Returns & Optimal Budget Allocation</p>', unsafe_allow_html=True)

st.markdown("---")

# Introduction
st.markdown("""
### 🎯 What is Sensitivity Analysis?

Sensitivity analysis helps answer a critical business question: **"How much should we spend on retention?"**

By running the optimization model across different budget levels ($150 to $1,000), we can observe:
- 📈 **Net Value Growth**: How retained CLV increases with budget
- 📉 **Diminishing Returns**: Where additional spending yields smaller gains
- 💰 **Optimal Budget Range**: The sweet spot that balances ROI and coverage
- 🎯 **Constraint Binding**: Which operational limits restrict further growth

**Key Finding from Analysis:** The optimal weekly budget is **$250-$400**, where PlaylistPro achieves 
strong ROI (1,500-2,000%) before diminishing returns become significant.
""")

st.markdown("---")

# Pre-computed results from report
st.markdown("### 📋 Pre-Computed Results (From Technical Report)")

st.info("""
**💡 These results come from the full prescriptive analysis report**, where we ran 12 optimization 
scenarios from $150 to $1,000 budget. Use these insights to guide your budget decisions.
""")

# Create pre-computed results table
precomputed_results = pd.DataFrame({
    'Budget': [150, 175, 200, 225, 250, 300, 350, 400, 500, 600, 750, 1000],
    'Customers': [75, 87, 100, 112, 125, 143, 156, 168, 187, 200, 218, 237],
    'Spend': [150, 175, 200, 225, 250, 300, 350, 400, 500, 600, 750, 1000],
    'Net_Value': [3479, 4023, 4567, 5111, 5655, 6520, 7165, 7810, 8880, 9730, 10850, 12200],
    'ROI': [2319, 2299, 2284, 2272, 2262, 2173, 2047, 1953, 1776, 1622, 1447, 1220]
})

# Display table
display_df = precomputed_results.copy()
display_df['Budget'] = display_df['Budget'].apply(lambda x: f'${x:,}')
display_df['Spend'] = display_df['Spend'].apply(lambda x: f'${x:,}')
display_df['Net_Value'] = display_df['Net_Value'].apply(lambda x: f'${x:,}')
display_df['ROI'] = display_df['ROI'].apply(lambda x: f'{x:,}%')

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")

# Visualizations from report
st.markdown("### 📈 Key Visualizations")

st.markdown("""
These charts visualize the budget sensitivity results, showing how key metrics change as weekly 
budget increases. **All visualizations are from the technical analysis report.**
""")

# Check if visualizations exist
viz_path = "visualizations"
if os.path.exists(viz_path):
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Net Value vs Budget", 
        "ROI vs Budget", 
        "Customer Coverage", 
        "All Metrics"
    ])
    
    with tab1:
        st.markdown("#### Budget Sensitivity: Net Value vs Weekly Budget")
        st.markdown("""
        This chart shows how **expected net value** (retained CLV minus campaign cost) grows with budget.
        
        **Key Insights:**
        - Strong growth from $150-$400 (steep slope)
        - Curve begins to flatten around $400-$500
        - Diminishing returns evident beyond $500
        - **Optimal range: $250-$400** (marked in green)
        """)
        
        viz1_path = os.path.join(viz_path, "viz1_budget_netvalue.png")
        if os.path.exists(viz1_path):
            image = Image.open(viz1_path)
            st.image(image, use_container_width=True)
        else:
            st.warning("Visualization not found. Please ensure viz1_budget_netvalue.png exists in visualizations/ folder.")
    
    with tab2:
        st.markdown("#### Budget Sensitivity: ROI vs Weekly Budget")
        st.markdown("""
        This chart illustrates the **diminishing returns** pattern as budget increases.
        
        **Key Insights:**
        - ROI starts at 2,319% at $150 budget
        - Steady decline as budget increases
        - Still excellent (1,220%) even at $1,000
        - Lower budgets = higher efficiency, but less total value
        - **Trade-off:** Maximize ROI vs. maximize total net value
        """)
        
        viz2_path = os.path.join(viz_path, "viz2_budget_roi.png")
        if os.path.exists(viz2_path):
            image = Image.open(viz2_path)
            st.image(image, use_container_width=True)
        else:
            st.warning("Visualization not found. Please ensure viz2_budget_roi.png exists in visualizations/ folder.")
    
    with tab3:
        st.markdown("#### Budget Sensitivity: Customer Coverage")
        st.markdown("""
        This chart shows how many customers can be treated at different budget levels.
        
        **Key Insights:**
        - Rapid growth from $150-$400 (75 → 168 customers)
        - Growth slows after $400 due to operational constraints
        - Plateaus around $750-$1,000 (approaching max capacity)
        - **Constraint binding:** Email/push capacity limits further growth
        """)
        
        viz3_path = os.path.join(viz_path, "viz3_budget_coverage.png")
        if os.path.exists(viz3_path):
            image = Image.open(viz3_path)
            st.image(image, use_container_width=True)
        else:
            st.warning("Visualization not found. Please ensure viz3_budget_coverage.png exists in visualizations/ folder.")
    
    with tab4:
        st.markdown("#### All Metrics Dashboard")
        st.markdown("""
        Combined view of all key metrics across budget levels.
        """)
        
        # Create multi-metric chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Net Value ($)', 'ROI (%)', 'Customers Treated', 'Budget Utilization (%)'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Net Value
        fig.add_trace(
            go.Scatter(
                x=precomputed_results['Budget'], 
                y=precomputed_results['Net_Value'],
                mode='lines+markers', 
                name='Net Value',
                line=dict(color='#28a745', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # ROI
        fig.add_trace(
            go.Scatter(
                x=precomputed_results['Budget'], 
                y=precomputed_results['ROI'],
                mode='lines+markers', 
                name='ROI',
                line=dict(color='#ffc107', width=3),
                marker=dict(size=8)
            ),
            row=1, col=2
        )
        
        # Customers
        fig.add_trace(
            go.Scatter(
                x=precomputed_results['Budget'], 
                y=precomputed_results['Customers'],
                mode='lines+markers', 
                name='Customers',
                line=dict(color='#17a2b8', width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )
        
        # Budget Utilization (always 100% in these scenarios)
        budget_util = (precomputed_results['Spend'] / precomputed_results['Budget'] * 100)
        fig.add_trace(
            go.Scatter(
                x=precomputed_results['Budget'], 
                y=budget_util,
                mode='lines+markers', 
                name='Utilization',
                line=dict(color='#dc3545', width=3),
                marker=dict(size=8)
            ),
            row=2, col=2
        )
        
        # Update axes
        fig.update_xaxes(title_text="Weekly Budget ($)", row=1, col=1)
        fig.update_xaxes(title_text="Weekly Budget ($)", row=1, col=2)
        fig.update_xaxes(title_text="Weekly Budget ($)", row=2, col=1)
        fig.update_xaxes(title_text="Weekly Budget ($)", row=2, col=2)
        
        fig.update_yaxes(title_text="Net Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="ROI (%)", row=1, col=2)
        fig.update_yaxes(title_text="Customers", row=2, col=1)
        fig.update_yaxes(title_text="Utilization (%)", row=2, col=2)
        
        fig.update_layout(
            height=700, 
            showlegend=False, 
            title_text="Budget Sensitivity: All Key Metrics"
        )
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Visualizations folder not found. Please ensure the visualizations/ directory exists with PNG files.")

st.markdown("---")

# Key Recommendations
st.markdown("### 💡 Strategic Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🎯 Optimal Budget
    **$250-$400 per week**
    
    - Best ROI range (1,500-2,000%)
    - Strong net value growth
    - Before diminishing returns
    - Treats 125-168 customers
    """)

with col2:
    st.markdown("""
    #### 📊 Budget < $250
    **High efficiency, low scale**
    
    - Excellent ROI (>2,000%)
    - Limited customer coverage
    - Misses high-value opportunities
    - Good for tight budgets
    """)

with col3:
    st.markdown("""
    #### 📈 Budget > $500
    **High scale, lower efficiency**
    
    - Lower ROI (<1,800%)
    - Maximum customer coverage
    - Diminishing returns evident
    - Consider if budget allows
    """)

st.info("""
**🎯 Bottom Line Recommendation:**

Start with **$250-$300/week** to achieve strong ROI while treating a meaningful portion of at-risk customers. 
Monitor results for 4-6 weeks, then consider scaling to $400-$500 if:
- ROI remains above 1,500%
- Operational capacity allows
- High-value customers still being missed
- Budget is available

**Avoid** going below $150 (infeasible) or above $750 (poor ROI) unless strategic reasons justify it.
""")

st.markdown("---")

# Custom Scenario Runner
st.markdown("### 🔬 Run Custom Sensitivity Analysis")

with st.expander("Run Your Own Budget Scenarios", expanded=False):
    st.markdown("""
    **⚠️ Note:** This will run multiple optimization scenarios and may take 2-5 minutes.
    Use the pre-computed results above for quick insights.
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        budget_min = st.slider("Minimum Budget", 100, 300, 150, 25)
        budget_max = st.slider("Maximum Budget", 200, 1000, 500, 50)
        budget_step = st.selectbox("Step Size", [25, 50, 100], index=1)
    
    with col2:
        st.markdown("**Settings:**")
        st.caption(f"Range: ${budget_min:,} - ${budget_max:,}")
        st.caption(f"Step: ${budget_step:,}")
        num_scenarios = (budget_max - budget_min) // budget_step + 1
        st.caption(f"Scenarios: {num_scenarios}")
    
    # Check if data is loaded
    if 'merged_data' not in st.session_state or st.session_state.merged_data is None:
        st.warning("⚠️ Please run an optimization in the main dashboard first to load customer data.")
        run_custom = False
    else:
        run_custom = st.button("🚀 Run Custom Sensitivity Analysis", use_container_width=True)
    
    if run_custom:
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
                        'email_capacity': 120,
                        'call_capacity': 100,
                        'min_high_risk_pct': 0.60,
                        'min_premium_pct': 0.40,
                        'max_action_pct': 0.50,
                        'min_segment_coverage_pct': 0.15
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
            
            st.success("✅ Custom sensitivity analysis complete!")
            
            # Display results
            st.markdown("### Custom Scenario Results")
            
            display_scenarios = scenario_df.copy()
            display_scenarios['Budget'] = display_scenarios['Budget'].apply(lambda x: f"${x:,}")
            display_scenarios['Total_Spend'] = display_scenarios['Total_Spend'].apply(lambda x: f"${x:,.0f}")
            display_scenarios['Retained_CLV'] = display_scenarios['Retained_CLV'].apply(lambda x: f"${x:,.0f}")
            display_scenarios['Net_Value'] = display_scenarios['Net_Value'].apply(lambda x: f"${x:,.0f}")
            display_scenarios['ROI'] = display_scenarios['ROI'].apply(lambda x: f"{x:.0f}%")
            display_scenarios['Churn_Prevented'] = display_scenarios['Churn_Prevented'].apply(lambda x: f"{x:.1f}")
            
            st.dataframe(display_scenarios, use_container_width=True, hide_index=True)
            
            # Find optimal
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
            
            # Export
            csv_sensitivity = scenario_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Custom Sensitivity Results",
                data=csv_sensitivity,
                file_name=f"custom_sensitivity_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        else:
            st.error("No successful scenarios completed")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>PlaylistPro Retention Optimizer - Sensitivity Analysis</strong></p>
    <p>Powered by XGBoost ML Predictions & Gurobi Optimization</p>
</div>
""", unsafe_allow_html=True)

