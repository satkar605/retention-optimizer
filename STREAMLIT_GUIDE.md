# PlaylistPro Retention Optimizer - Streamlit Dashboard

## Quick Start Guide

### Prerequisites

Ensure you have the following files in your project directory:
- `prediction.csv` - XGBoost churn predictions (75,001 customers)
- `test.csv` - Customer features and engagement data
- `music_streaming_retention_75k.py` - Optimization engine
- `streamlit_app.py` - Dashboard interface

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Verify Gurobi license:
```bash
python -c "import gurobipy; print('Gurobi ready!')"
```

### Launch Dashboard

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## Dashboard Features

### 1. Data Overview
- Automatic loading of XGBoost predictions and customer features
- Real-time KPIs: total customers, high-risk count, at-risk CLV
- Interactive visualizations of churn distribution and segmentation

### 2. Optimization Settings (Sidebar)
Configure operational constraints:
- **Weekly Budget**: $25K - $500K
- **Email Capacity**: 5K - 75K emails per week
- **Call Capacity**: 50 - 2,000 calls per week
- **Min High-Risk Coverage**: 40% - 90%
- **Min Premium Coverage**: 0% - 80%

### 3. Run Optimization
Click "RUN OPTIMIZATION" to:
- Build Gurobi MILP model for 75K+ customers
- Solve in 30-90 seconds
- Generate optimal treatment plan

### 4. Results Analysis
View comprehensive results across 4 tabs:

**By Action**
- Treatment mix pie chart
- Net value by action
- Detailed performance table

**By Segment**
- Risk × Value heatmap
- Segment-level ROI analysis

**By Channel**
- Email, call, in-app distribution
- Capacity utilization metrics

**Top Customers**
- Top 50 highest-impact customers
- Prioritized by net value

### 5. Constraint Analysis
- Identify binding constraints
- Shadow price recommendations
- What-if guidance

### 6. Export Treatment Plans
Download:
- **Complete treatment plan** with holdout assignments
- **Email list** for marketing automation
- **Call queue** prioritized by CLV

### 7. Sensitivity Analysis
Run what-if scenarios across budget levels:
- Compare 5-10 different budget scenarios
- Visualize ROI curves and diminishing returns
- Identify optimal budget allocation
- Export sensitivity results

## Weekly Workflow

### Monday: Planning
1. Data Science team exports fresh `prediction.csv` from XGBoost model
2. Open Streamlit dashboard
3. Adjust constraints based on current capacity
4. Run optimization
5. Review results and validate

### Tuesday: Execution Setup
1. Download complete treatment plan
2. Upload email list to marketing automation platform
3. Upload call queue to CRM system
4. Brief call center team on priorities

### Wednesday-Friday: Campaign Execution
1. Marketing automation sends retention emails
2. Call center works through retention calls
3. Monitor delivery rates and engagement

### Week 5+: Measurement & Learning
1. Calculate actual churn rates: treated vs holdout
2. Compute realized uplift per action
3. Update action catalog with calibrated values
4. Re-run optimization with improved estimates

## Troubleshooting

### Dashboard won't load
- Verify `prediction.csv` and `test.csv` are in project directory
- Check that both files have required columns

### Optimization fails
- Ensure Gurobi license is valid and active
- Check that constraints aren't infeasible (e.g., budget too low)
- Try relaxing min_high_risk_pct or min_premium_pct

### Slow performance
- Large datasets (>100K customers) may take 2-3 minutes to optimize
- Sensitivity analysis with 10+ scenarios can take 5-10 minutes
- Consider reducing the number of scenarios or running on a more powerful machine

### Data merge issues
- Ensure `customer_id` column exists in both files
- Verify no duplicate customer IDs
- Check for data type consistency

## Tips for Best Results

1. **Start Conservative**: Begin with estimated uplifts, then calibrate with actual data
2. **Use Holdout Groups**: Always exclude 10% for A/B testing
3. **Track Everything**: Measure churn rates weekly for treated vs holdout
4. **Update Regularly**: Re-run optimization weekly with fresh predictions
5. **Adjust Constraints**: Use sensitivity analysis to find optimal budget
6. **Validate Actions**: Ensure action costs and uplifts reflect reality

## Key Metrics to Track

### Optimization Health
- Budget utilization: 80-95% is ideal
- Email capacity binding: May need to expand
- ROI: Should be >150% after calibration

### Campaign Effectiveness
- Actual uplift vs estimated uplift per action
- Treatment execution rate (target: >90%)
- Holdout group size (target: ~10%)

### Business Impact
- Churn rate reduction (treated vs baseline)
- CLV retained per dollar spent
- Customer satisfaction scores

## Advanced Features

### Custom Actions
Create `retention_actions.csv` to define your own:
```csv
action_id,action_name,channel,cost,uplift,eligible_segment
1,Custom Email,email,3,0.10,all
2,Special Offer,email,25,0.18,Premium
```

### Custom Constraints
Modify `music_streaming_retention_75k.py` to add:
- Geographic fairness constraints
- Daily capacity limits
- Exclude no-contact customers
- Subscription-specific quotas

### Shadow Price Analysis
Export dual values from Gurobi model to understand:
- Value of relaxing each constraint by 1 unit
- Which capacity expansions have highest ROI
- Budget allocation priorities

## Support

For technical issues:
- Check Gurobi documentation: https://www.gurobi.com/documentation/
- Review model logs in console output
- Verify data quality and completeness

For business questions:
- Review action catalog and ensure uplifts are calibrated
- Validate constraints align with operational reality
- Ensure CLV estimates reflect actual customer economics

---

**Built with**: Python • Streamlit • Gurobi • Plotly • XGBoost Predictions

**Version**: 1.0

**Last Updated**: October 2025

