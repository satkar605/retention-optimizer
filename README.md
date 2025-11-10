# PlaylistPro Retention Optimizer

**Prescriptive Analytics Platform for Customer Retention Management**

MILP optimization engine that transforms XGBoost churn predictions into executable weekly retention campaigns, maximizing customer lifetime value within operational constraints.

**Demonstrated Performance:** $3,479 net value | 2,319% ROI | 75 customers treated | $150 baseline budget

---

## Business Problem

PlaylistPro, a music streaming service with **75,000 subscribers**, faces a **47% annual churn rate**, costing millions in recurring revenue. The company lacks a systematic retention strategy—no predictive analytics to identify high-risk customers, no optimization framework for budget allocation, and unclear ROI on marketing campaigns.

Traditional approaches either treat all high-risk customers (cost-prohibitive) or only high-value customers (leaves revenue gaps). This creates suboptimal resource allocation and missed retention opportunities worth hundreds of thousands in potential retained revenue.

## Solution Overview

This platform solves the retention planning problem using mixed-integer linear programming (MILP with Gurobi), automatically generating optimal weekly treatment plans for 75,000+ customers in under 90 seconds. The system balances competing objectives while respecting real-world capacity constraints.

**Core optimization:**
```
Maximize: Σ (churn_probability × uplift × CLV - action_cost)
Subject to: weekly budget, email capacity, call center capacity, policy requirements
```

The model prioritizes customers by expected net value, ensuring resources flow to highest-impact opportunities.

**Baseline Results (250 customer sample, $150 weekly budget):**
- **Net Value Generated:** $3,479
- **ROI:** 2,319%
- **Customers Treated:** 75 customers
- **Expected Churn Prevention:** ~5 customers saved
- **Optimal Budget Range:** $250-400 per week (identified via sensitivity analysis)

---

## Key Features

### Self-Service Dashboard
Interactive Streamlit interface enables retention managers to configure constraints, run optimization scenarios, and export treatment plans without technical expertise.

### Production Scale
Handles 75,001 customers with real XGBoost predictions, merging churn scores with customer features for intelligent CLV estimation and segmentation.

### Experimental Design
Built-in 10% holdout groups enable A/B testing to measure actual treatment uplift, creating a learning loop that continuously improves model accuracy.

### Sensitivity Analysis
Compare multiple budget scenarios to identify optimal investment levels and visualize diminishing returns across different constraint configurations.

---

## Technical Architecture

**Data Pipeline:**
- Input: XGBoost churn predictions + customer features
- Processing: CLV estimation, risk/value segmentation
- Output: Optimized treatment assignments with holdout groups

**Optimization Model:**
- Decision Variables: Binary assignments (customer × action)
- Objective: Maximize expected retained CLV net of costs
- Constraints: Budget, channel capacities, minimum coverage policies
- Solver: Gurobi 11.0 (mixed-integer linear programming)

**Deployment:**
- Backend: Python, Pandas, NumPy
- Optimization: Gurobi (academic/commercial license)
- Frontend: Streamlit dashboard with Plotly visualizations
- Integration: CSV exports for CRM systems (Salesforce, HubSpot, etc.)

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run streamlit_app.py
```

Dashboard opens at `http://localhost:8501`

### Configure & Optimize

1. Adjust constraints in sidebar (budget, email/call capacity, policy requirements)
2. Click "RUN OPTIMIZATION"
3. Review results across tabs (Actions, Segments, Channels, Top Customers)
4. Download treatment plans for CRM execution

---

## Business Impact

**For Retention Managers:**
- Reduce planning time from 2 days to 5 minutes
- Test budget scenarios before committing resources
- Identify binding constraints limiting retention effectiveness
- Export CRM-ready treatment lists with built-in A/B testing

**For the Business:**
- Maximize ROI on retention spending through optimal resource allocation
- Ensure policy compliance (minimum high-risk and Premium customer coverage)
- Create data-driven learning loop: measure actual uplift, recalibrate model, re-optimize
- Scale weekly re-optimization with fresh ML predictions

**Demonstrated Results:**
- **2,319% ROI** on baseline scenario ($150 budget)
- **$3,479 net value** from optimized treatment allocation
- **75 customers treated** with expected **5 churn preventions**
- **Optimal budget range identified:** $250-400 per week via sensitivity analysis
- Clear visibility into constraint bottlenecks for capacity planning

---

## Model Formulation (MILP)

### Decision Variables
```
x[i,k] ∈ {0,1} for all customer-action pairs

x[i,k] = 1 if customer i receives action k
x[i,k] = 0 otherwise

Total: 250 customers × 8 actions = 2,000 binary decision variables
```

### Objective Function
```
Maximize: Σ (p_i × u_k × v_i - c_k) × x[i,k]

Where:
  p_i = churn probability (from XGBoost model, AUC 0.94)
  u_k = uplift (% churn reduction from action k)
  v_i = customer lifetime value (2-year horizon)
  c_k = cost of action k
```

**Objective:** Maximize expected retained CLV net of action costs

### Constraints

1. **One action per customer:** Each customer receives at most one retention action
   ```
   Σ x[i,k] ≤ 1  ∀ customers i
   ```

2. **Weekly budget constraint:** Total spending cannot exceed allocated budget
   ```
   Σ (cost_k × x[i,k]) ≤ weekly_budget
   ```

3. **Channel capacity constraints:**
   - Email capacity: limited marketing automation throughput
   - Call/Push capacity: limited call center agent hours
   ```
   Σ x[i,k] ≤ capacity_channel  ∀ channels
   ```

4. **Policy requirements (fairness constraints):**
   - Minimum high-risk coverage: ≥60% of customers with churn probability >0.5
   - Minimum Premium customer coverage: ≥40% of Premium subscribers
   - Maximum action saturation: ≤50% of treatments per action type
   - Minimum segment coverage: ≥15% coverage across risk/value segments

5. **Eligibility constraints:** Actions only assigned to eligible customer segments
   ```
   x[i,k] = 0  if customer i ineligible for action k
   ```

---

## Sensitivity Analysis Findings

### Budget Optimization
Comprehensive sensitivity analysis across budget levels ($150-$1,000) revealed:

**Key Findings:**
- **Optimal Range:** $250-400 per week delivers best risk-adjusted returns
- **Baseline ($150):** $3,479 net value, 2,319% ROI, 75 customers treated
- **Diminishing Returns:** ROI decreases at budgets >$400 as lower-value customers treated
- **Marginal Value:** Each additional dollar of budget yields $0.15-0.25 in expected net value

**Budget Recommendations:**
1. **Conservative:** $150-250 (highest ROI, limited scale)
2. **Optimal:** $250-400 (balance of ROI and impact)
3. **Aggressive:** $400+ (maximize coverage, lower ROI acceptable)

**Constraint Analysis:**
- **Budget:** Often the binding constraint at lower investment levels
- **Email Capacity:** Becomes binding at higher budgets (120+ emails needed)
- **Call Capacity:** Limits high-value retention actions
- **Policy Requirements:** Ensures fairness but may limit pure ROI optimization

### Action Mix Insights
Optimization automatically balances retention action portfolio:
- **Personalized emails:** High volume, low cost, broad reach
- **Discount offers:** Moderate cost, strong uplift for price-sensitive segments
- **Premium trials:** Targeted at Free/Student tiers with high upgrade potential
- **Retention calls:** Reserved for highest-value, highest-risk customers

### Visualization Suite
Complete analysis includes 8 key visualizations:
1. **Budget vs Net Value:** Demonstrates linear growth to optimal range, then diminishing returns
2. **Budget vs ROI:** Shows ROI decline as budget increases (higher-value customers treated first)
3. **Budget vs Coverage:** Customer treatment volume scales with budget investment
4. **Action Mix Distribution:** Reveals optimal blend of email, discount, trial, and call actions
5. **Segment-Action Heatmap:** Shows which customer segments receive which treatments
6. **Risk-Value Matrix:** Visualizes customer distribution across churn risk and CLV dimensions
7. **Net Value Breakdown:** Decomposes total value by customer segment
8. **Churn vs CLV Scatter:** Identifies high-risk, high-value priority targets

All visualizations available in `/visualizations/` directory.

---

## Weekly Operational Workflow

### Monday: Optimization Planning
1. Data Science team exports fresh XGBoost churn predictions
2. Retention manager runs optimization in dashboard
3. Review constraint utilization and adjust if needed

### Tuesday: Campaign Setup
1. Download treatment plans from dashboard
2. Upload email list to marketing automation platform
3. Upload call queue to CRM, prioritized by expected CLV

### Wednesday-Friday: Execution
1. Marketing automation sends retention emails
2. Call center works through prioritized retention calls
3. Monitor delivery rates and engagement metrics

### Monthly: Learning & Calibration
1. Measure actual churn rates (treated vs. holdout groups)
2. Calculate realized uplift per action type
3. Update action catalog with calibrated uplift estimates
4. Document learnings for continuous improvement

---

## Data Requirements

### Required Input
**File:** `prediction.csv`
- `customer_id`: Unique identifier
- `churn_probability`: XGBoost prediction (0 to 1)

### Optional (Enhances CLV Estimation)
**File:** `test.csv`
- `subscription_type`: Free, Student, Premium, Family
- `payment_plan`: Monthly, Yearly
- `weekly_hours`: Listening time
- `weekly_songs_played`: Engagement metric
- `num_playlists_created`: Platform investment

### System Output
**File:** `treatment_plan_YYYYMMDD.csv`
- Customer assignments with action details
- Holdout flags for A/B testing
- Expected CLV and cost per customer
- Execution status (treat vs. control)

---

## Configuration

### Operational Constraints
Edit constraints in dashboard sidebar or modify optimizer directly:

```python
optimizer.set_constraints({
    'weekly_budget': 150000,        # Retention budget allocation
    'email_capacity': 30000,        # Marketing automation limit
    'call_capacity': 500,           # Call center agent hours
    'min_high_risk_pct': 0.60,     # Policy: cover 60% of high-risk
    'min_premium_pct': 0.40         # Policy: cover 40% of Premium users
})
```

### Action Catalog
Default actions for music streaming industry included. Customize by creating `retention_actions.csv`:

```csv
action_id,action_name,channel,cost,uplift,eligible_segment
1,Personalized Email,email,2,0.08,all
2,20% Discount,email,20,0.15,all
3,Premium Trial,in_app,10,0.25,Free
4,Retention Call,call,50,0.30,high_value
5,VIP Service,call,100,0.40,high_value
```

Note: Uplift estimates require calibration via A/B testing for production accuracy.

---

## Technical Details

### CLV Estimation
When customer-level CLV unavailable, model estimates using:
- Base revenue by subscription tier
- Payment plan commitment multiplier
- Engagement score from listening behavior
- 2-year retention horizon assumption

Formula: `CLV = base_revenue × payment_multiplier × (1 + engagement_score) × 2`

### Optimization Performance
- **Baseline problem size:** 250 customers × 8 actions = 2,000 binary decision variables
- **Full-scale capacity:** 75,001 customers × 8 actions = 600,008 binary variables
- **Solve time:** 30-90 seconds on standard hardware (academic Gurobi license)
- **Optimality:** Gurobi guarantees optimal solution to within 0.01% MIP gap
- **Scalability:** Production-ready for 75K customers, can scale to 500K+ with clustering
- **Baseline results:** $3,479 net value, 2,319% ROI from $150 budget scenario

### Shadow Prices
Model provides dual values (shadow prices) indicating marginal value of relaxing constraints:
- Budget +$1 → Additional $0.15-0.25 net value
- Email capacity +1 → Additional $10-20 net value
- Call capacity +1 → Additional $40-60 net value

Used for informed capacity planning and budget allocation decisions.

---

## Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

### Streamlit Community Cloud (Free)
1. Push repository to GitHub
2. Deploy at share.streamlit.io
3. Configure secrets for production data
4. Share dashboard link with stakeholders

### Enterprise Deployment
1. Containerize with Docker
2. Deploy on internal infrastructure
3. Integrate SSO authentication
4. Schedule automated weekly runs

---

## Project Structure

```
retention-optimizer/
├── streamlit_app.py                                  # Interactive dashboard (324 lines)
├── music_streaming_retention_75k.py                  # Optimization engine (615 lines)
├── prediction_250.csv                                # Churn predictions (250 customer sample)
├── test_250.csv                                      # Customer features
├── requirements.txt                                  # Python dependencies
├── README.md                                         # Project documentation
├── Satkar_Karki_Prescriptive_Analysis_Report.pdf    # Full analysis report
└── visualizations/                                   # Result visualizations
    ├── viz1_budget_netvalue.png                      # Budget vs Net Value
    ├── viz2_budget_roi.png                           # Budget vs ROI
    ├── viz3_budget_coverage.png                      # Budget vs Customer Coverage
    ├── viz4_action_mix.png                           # Treatment Action Distribution
    ├── viz5_segment_action.png                       # Segment-Action Heatmap
    ├── viz6_heatmap.png                              # Risk-Value Matrix
    ├── viz7_netvalue_breakdown.png                   # Net Value by Segment
    └── viz8_scatter_churn_clv.png                    # Churn Probability vs CLV
```

---

## Key Learnings from INFORMS Annual Meeting

This implementation incorporates optimization best practices from Gurobi technical sessions:

1. **Constraint Sensitivity Analysis:** Shadow prices inform capacity planning
2. **Explainability:** Binding constraint reporting makes model decisions transparent
3. **Warm Starts:** Week-over-week optimization benefits from previous solutions
4. **Practical Constraints:** Policy requirements ensure business alignment beyond pure ROI

---

## Dependencies

- Python 3.11+
- Gurobi 11.0 (requires academic or commercial license)
- Streamlit 1.29.0
- Pandas 2.1.4
- NumPy 1.24.3
- Plotly 5.18.0

See `requirements.txt` for complete list.

---

## License & Support

### Gurobi License
Academic license: Free for research and education
Commercial license: Contact Gurobi sales

### Documentation
- Gurobi: https://www.gurobi.com/documentation/
- Streamlit: https://docs.streamlit.io/

### Contact
For questions about implementation or customization, please open an issue on GitHub.

---

## Future Enhancements

### Short-term (1-2 weeks)
- Multi-week campaign sequencing
- Geographic fairness constraints
- Historical results dashboard

### Medium-term (1 month)
- Propensity scoring for action receptiveness
- Network effects modeling
- Real-time API for CRM integration

### Long-term (2-3 months)
- Reinforcement learning for uplift estimation
- Multi-channel attribution modeling
- Automated retraining pipeline

---

## Summary

**Built for:** Data science portfolios, business analytics case studies, prescriptive optimization demonstrations

**Technologies:** Python | Gurobi MILP | Streamlit | XGBoost | Plotly | Pandas | NumPy

**Performance:** $3,479 net value | 2,319% ROI | 30-90 second solve time | 2,000 binary variables

**Scale:** Production-ready for 75,000+ customers, extensible to 500,000+ with decomposition

**Documentation:** Complete prescriptive analysis report with 8 visualizations included
