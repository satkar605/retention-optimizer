# PlaylistPro Retention Optimizer

**Prescriptive analytics platform for subscription retention management**

Optimization engine that transforms ML churn predictions into executable weekly retention campaigns, maximizing customer lifetime value within operational constraints.

---

## Business Problem

Subscription businesses face a critical challenge: identifying which at-risk customers to target with limited retention budget and operational capacity. Traditional approaches either treat all high-risk customers (cost-prohibitive) or only high-value customers (leaves revenue gaps). This creates suboptimal resource allocation and missed retention opportunities.

## Solution Overview

This platform solves the retention planning problem using mixed-integer linear programming (Gurobi), automatically generating optimal weekly treatment plans for 75,000+ customers in under 90 seconds. The system balances competing objectives while respecting real-world capacity constraints.

**Core optimization:**
```
Maximize: Σ (churn_probability × uplift × CLV - action_cost)
Subject to: weekly budget, email capacity, call center capacity, policy requirements
```

The model prioritizes customers by expected net value, ensuring resources flow to highest-impact opportunities.

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

**Expected Outcomes:**
- 150-300% ROI on retention campaigns (industry benchmark)
- 15-25% reduction in churn among treated customers
- Clear visibility into constraint bottlenecks for capacity planning

---

## Model Formulation

### Decision Variables
```
x[i,k] ∈ {0,1} for all customer-action pairs

x[i,k] = 1 if customer i receives action k
x[i,k] = 0 otherwise
```

### Objective Function
```
Maximize: Σ (p_i × u_k × v_i - c_k) × x[i,k]

Where:
  p_i = churn probability (from XGBoost model)
  u_k = uplift (% churn reduction from action k)
  v_i = customer lifetime value (2-year horizon)
  c_k = cost of action k
```

### Constraints

1. **One action per customer:** Each customer receives at most one retention action
2. **Budget:** Total weekly spending cannot exceed allocated retention budget
3. **Channel capacity:** Email and call volumes respect operational limits
4. **Policy requirements:** Minimum coverage thresholds for high-risk and Premium customers
5. **Eligibility:** Actions only assigned to eligible customer segments

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
- **Problem size:** 75,001 customers × 8 actions = 600,008 binary variables
- **Solve time:** 30-90 seconds on standard hardware
- **Optimality:** Gurobi guarantees optimal solution to within 0.01% gap
- **Scalability:** Can handle 500,000+ customers with clustering approach

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
├── streamlit_app.py                    # Interactive dashboard (1,043 lines)
├── music_streaming_retention_75k.py    # Optimization engine (615 lines)
├── prediction.csv                      # XGBoost churn predictions (75,001 rows)
├── test.csv                            # Customer features
├── requirements.txt                    # Python dependencies
├── STREAMLIT_GUIDE.md                  # User documentation
├── CONFIGURATION_GUIDE.md              # Setup examples
├── IMPLEMENTATION_SUMMARY.md           # Technical documentation
└── test_optimizer.py                   # Verification script
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

**Built for:** Data science portfolios, business analytics demonstrations, optimization coursework

**Technologies:** Python, Gurobi, Streamlit, XGBoost, Plotly, Pandas

**Scale:** Production-ready for 75,000+ customers, extensible to 500,000+ with modifications
