# PlaylistPro Retention Optimizer - Quick Start Guide

## 🚀 Launch the Dashboard

```bash
cd /Users/satkarkarki/Desktop/portfolio/playlist-pro-retention-optimization
streamlit run streamlit_app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📱 Navigation Overview

### Page 1: 🏠 Home (Landing Page)
**Start here to understand the business problem**

- Learn about the 47% churn crisis
- Understand the XGBoost + MILP solution
- See key results and ROI (2,319% baseline)
- Click "Launch Optimization Dashboard" to proceed

---

### Page 2: ⚙️ Optimizer Dashboard
**Run optimization scenarios**

#### Step 1: Configure Constraints (Left Sidebar)

**Budget & Capacity:**
- Weekly Budget: $150-$1,000 (optimal: $250-400)
- Email Capacity: Automatically sets minimum based on policy floors
- Push/In-App Capacity: 50-250 notifications

**Policy Constraints:**
- Min High-Risk Coverage: 60% (ensures we treat risky customers)
- Min Premium Coverage: 40% (VIP treatment for valuable customers)
- Max Action Saturation: 50% (forces campaign diversity)
- Min Segment Coverage: 15% (fairness across subscription types)

#### Step 2: Validate Settings
- Green checkmarks = feasible
- Red error messages = infeasible (adjust sliders)
- Run button disabled if settings are invalid

#### Step 3: Run Optimization
- Click "🚀 RUN OPTIMIZATION"
- Wait 30-90 seconds for Gurobi to solve
- View results below

#### Step 4: Analyze Results

**Key Metrics:**
- Customers Treated
- Weekly Spend
- Expected Churn Prevented
- Expected Retained CLV
- ROI %
- **Net Value** (the big one!)

**Tabs:**
- **By Action & Channel**: See how customers are distributed across emails, calls, discounts, etc.
- **By Segment**: Risk × Value heatmap showing strategic focus
- **Top Customers**: Top 50 highest-impact assignments

#### Step 5: Export Treatment Plans
- Download complete CSV with all assignments
- Export email list for marketing team
- Export call queue for customer service (sorted by CLV)

---

### Page 3: 📊 Sensitivity Analysis
**Understand optimal budget allocation**

#### Pre-Computed Results
- View 12 scenarios from $150 to $1,000
- See how Net Value and ROI change with budget

#### Visualizations
- **Net Value vs Budget**: Growth curve with optimal range
- **ROI vs Budget**: Diminishing returns pattern
- **Customer Coverage**: How many customers treated at each level
- **All Metrics**: Combined dashboard view

#### Key Insights
- **Optimal Budget**: $250-400/week
- **ROI at $150**: 2,319% (highest efficiency)
- **ROI at $1,000**: 1,220% (still excellent, but diminishing)

#### Custom Scenarios (Optional)
- Run your own budget range
- Takes 2-5 minutes for multiple scenarios
- Exports custom results to CSV

---

## 🎯 Recommended Workflow

### First-Time User:
1. **Read Landing Page** (2 minutes)
   - Understand the business problem
   - Learn about the solution
   
2. **Run Baseline Optimization** (3 minutes)
   - Use default settings ($150 budget)
   - Click "Run Optimization"
   - Review results
   
3. **Explore Sensitivity Analysis** (5 minutes)
   - See why $250-400 is optimal
   - Understand diminishing returns
   
4. **Run Optimal Scenario** (3 minutes)
   - Return to Optimizer
   - Set budget to $300
   - Run and compare to baseline
   
5. **Export Treatment Plan** (1 minute)
   - Download CSV
   - Share with marketing team

**Total Time: ~15 minutes**

---

### Weekly Operations:
1. **Run Weekly Optimization** (Mondays)
   - Load latest churn predictions
   - Use optimal budget ($250-400)
   - Export treatment plan
   
2. **Distribute Tasks**
   - Email list → Marketing automation
   - Call queue → Customer service team
   - Discount codes → CRM system
   
3. **Track Results** (Next Monday)
   - Compare predicted vs. actual churn
   - Adjust budget if needed
   - Iterate and improve

---

## 💡 Tips & Best Practices

### Constraint Configuration:
- **Start Conservative**: Use default constraints first
- **High-Risk Coverage**: Keep at 60%+ to prevent churn in critical segment
- **Premium Coverage**: 40% ensures VIP treatment for valuable customers
- **Action Saturation**: 50% forces diversity (avoid email-only campaigns)
- **Segment Fairness**: 15% prevents algorithmic bias

### Budget Selection:
- **Tight Budget**: $150-250 → High ROI, limited coverage
- **Optimal Budget**: $250-400 → Best balance
- **Scale Budget**: $400-750 → Maximum coverage, lower ROI
- **Avoid**: Below $150 (infeasible) or above $1,000 (poor ROI)

### Interpreting Results:
- **ROI > 1,500%**: Excellent efficiency
- **ROI 1,000-1,500%**: Good efficiency
- **ROI < 1,000%**: Consider reducing budget
- **Net Value**: The ultimate metric (CLV retained - cost)

### Constraint Binding:
- **Budget Binding**: Increasing budget will improve results
- **Email Capacity Binding**: Add more email resources
- **Push Capacity Binding**: Expand in-app messaging team
- **If Nothing Binding**: You have excess capacity (reduce budget)

---

## ⚠️ Troubleshooting

### "Run Optimization" Button is Disabled
**Cause:** Infeasible constraint combination

**Solution:**
- Read error messages in sidebar
- Common issues:
  - Budget too low for required treatments
  - Email capacity below minimum floors
  - Conflicting policy constraints
- Adjust sliders until errors clear

### Optimization Takes Forever (>2 minutes)
**Cause:** Complex constraint combination or large dataset

**Solution:**
- Wait up to 90 seconds for Gurobi
- If still running, check Gurobi license
- Reduce dataset size (use 250 sample, not 75K)

### "Data file not found" Error
**Cause:** Missing prediction_250.csv or test_250.csv

**Solution:**
```bash
# Ensure these files exist:
ls prediction_250.csv
ls test_250.csv
```

### Visualizations Not Showing (Sensitivity Page)
**Cause:** Missing visualizations folder

**Solution:**
```bash
# Ensure visualizations exist:
ls visualizations/
```

Should see: viz1_budget_netvalue.png through viz8_scatter_churn_clv.png

---

## 📊 Understanding the Metrics

### Customers Treated
Number of customers receiving retention action (out of 250 sample)

### Weekly Spend
Actual campaign cost (should be ≤ budget)

### Expected Churn Prevented
Predicted reduction in churn count (based on action uplift)

### Expected Retained CLV
Customer lifetime value saved from churn

### Net Value
**Most Important Metric**
```
Net Value = Expected Retained CLV - Weekly Spend
```
This is what you're maximizing!

### ROI (Return on Investment)
```
ROI = (Expected Retained CLV / Weekly Spend - 1) × 100%
```
Efficiency metric. 2,000% ROI means $21 retained per $1 spent.

---

## 🎓 Advanced Features

### Holdout Group (A/B Testing)
Exports include 10% holdout flag for validation
- `holdout = True`: Don't treat (control group)
- `execute_treatment = False`: Skip this customer

Compare churn rates:
- Treatment group vs. Holdout group
- Validate model predictions

### Custom Scenarios (Sensitivity Page)
- Test different budget ranges
- Compare constraint combinations
- Export scenario results for presentations

### Top Customer Analysis
- Focus on high-net-value assignments
- Prioritize calls for top customers
- Personalize offers for Premium/Family

---

## 📞 Need Help?

1. **Inline Help**: Hover over ⓘ icons in dashboard
2. **Technical Report**: Read `prescriptive_analysis_report.pdf`
3. **Implementation Details**: See `DASHBOARD_UPGRADE_SUMMARY.md`
4. **Configuration Guide**: Check `CONFIGURATION_GUIDE.md`

---

## ✅ Quick Checklist

Before running optimization:
- [ ] Data files loaded (prediction_250.csv, test_250.csv)
- [ ] Budget set within feasible range
- [ ] Email capacity ≥ minimum required
- [ ] Push capacity ≥ 50
- [ ] No red error messages in sidebar
- [ ] "Run Optimization" button enabled

After optimization:
- [ ] Net Value is positive
- [ ] ROI > 1,000%
- [ ] Customers treated makes sense (30-90% coverage)
- [ ] Treatment plan exported
- [ ] Results shared with team

---

**Happy Optimizing!** 🎵

For more details, see `DASHBOARD_UPGRADE_SUMMARY.md`

