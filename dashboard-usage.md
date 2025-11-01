# PlaylistPro Retention Optimizer - Complete Dashboard Guide

**Interactive Prescriptive Analytics Dashboard for Weekly Retention Planning**

---

## 📋 Table of Contents

1. [What This Dashboard Does](#what-this-dashboard-does)
2. [Dashboard Layout Overview](#dashboard-layout-overview)
3. [Left Sidebar: Controls & Settings](#left-sidebar-controls--settings)
4. [Main Dashboard: Metrics & Visualizations](#main-dashboard-metrics--visualizations)
5. [Running an Optimization](#running-an-optimization)
6. [Understanding Results](#understanding-results)
7. [Exporting Treatment Plans](#exporting-treatment-plans)
8. [Sensitivity Analysis](#sensitivity-analysis)
9. [Weekly Workflow](#weekly-workflow)
10. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## What This Dashboard Does

This tool solves the weekly retention planning problem: **"Which at-risk customers should we contact, with what actions, to maximize retained customer lifetime value?"**

### The Problem
You have **250 at-risk customers** each week (sample for demo purposes), but limited budget, email capacity, and call center resources. You can't contact everyone, and ignoring customers leads to churn.

### The Solution
A mathematical optimization model (Gurobi MILP) that automatically generates the **optimal weekly treatment plan** in 5-10 seconds, maximizing expected ROI while respecting all operational and policy constraints.

### What You Get
- **Treatment plan CSV** with exact customer-action assignments
- **Expected ROI** of 300-500%
- **Balanced action mix** (emails, calls, discounts)
- **Fair coverage** across all customer segments

---

## Dashboard Layout Overview

```
┌─────────────────────────────────────────────────────────┐
│  🎵 PlaylistPro Retention Optimizer                    │
│  Weekly retention campaign planning                     │
├──────────────┬──────────────────────────────────────────┤
│              │  ✅ Loaded 250 customers                 │
│   SIDEBAR    │                                          │
│   (Controls) │  📊 Current Week Overview                │
│              │  ┌────┬────┬────┬────┬────┬────┬────┐   │
│              │  │KPI1│KPI2│KPI3│KPI4│KPI5│KPI6│KPI7│   │
│              │  └────┴────┴────┴────┴────┴────┴────┘   │
│   Sliders    │                                          │
│   for all    │  📈 Customer Analytics (3 tabs)          │
│   constraints│  [Risk Distribution] [Segmentation]      │
│              │                                          │
│   🚀 RUN     │  [After clicking RUN OPTIMIZATION:]      │
│   Button     │  ⚙️ Running Optimization... (5-10 sec)  │
│              │                                          │
│              │  🎯 Optimization Results                 │
│              │  - Key metrics                           │
│              │  - Treatment plan breakdown              │
│              │  - Export buttons                        │
│              │                                          │
│              │  🔍 What-If Scenario Analysis            │
└──────────────┴──────────────────────────────────────────┘
```

---

## Left Sidebar: Controls & Settings

### 🎵 App Logo & Header
- **PlaylistPro icon** at the top
- **"⚙️ Optimization Settings"** section header

---

### 💰 Budget & Capacity Section

These are your **operational resource limits** for the week.

#### **Weekly Budget ($)** 
- **Range:** $25,000 - $500,000
- **Default:** $150,000
- **What it controls:** Maximum dollars you can spend on all retention activities this week
- **How to set:**
  - Look at your approved retention marketing budget
  - Divide monthly budget by 4 for weekly allocation
  - Example: $600K/month = $150K/week
- **Tip:** If optimizer uses 95%+, consider increasing to capture more opportunities

#### **Email Capacity (per week)**
- **Range:** 5,000 - 75,000 emails
- **Default:** 30,000
- **What it controls:** Maximum retention emails your marketing team can send
- **How to set:**
  - Check with marketing ops on weekly throughput
  - Account for other scheduled campaigns
  - Consider deliverability limits (don't flood inboxes)
- **Tip:** Email is cheapest (~$2-5 each), so higher capacity = more reach

#### **Call Center Capacity**
- **Range:** 50 - 2,000 calls
- **Default:** 500
- **What it controls:** Maximum retention calls your agents can make
- **How to set:**
  - Calculate: (# agents) × (calls/agent/day) × 5 days
  - Example: 5 agents × 20 calls/day × 5 days = 500
  - Reserve capacity for inbound calls
- **Tip:** Calls are expensive (~$25-50 each) but most effective

---

### 🎯 Policy Constraints Section

These ensure you meet **strategic business goals** beyond pure profit.

#### **Min High-Risk Coverage (%)**
- **Range:** 40% - 90%
- **Default:** 60%
- **What it controls:** Minimum percentage of high-risk customers (p > 0.5) you MUST contact
- **Why it exists:** 
  - Brand reputation: Can't ignore customers about to churn
  - Strategic mandate: "We try to save every at-risk customer"
- **Example:** If 125 customers have >50% churn risk, you must contact ≥75 (60%)
- **Tip:** Lower this if budget is too tight; raise it for aggressive retention

#### **Min Premium Customer Coverage (%)**
- **Range:** 0% - 80%
- **Default:** 40%
- **What it controls:** Minimum percentage of Premium subscribers you MUST contact
- **Why it exists:**
  - VIP treatment for highest-value segment
  - Proactive loyalty building
  - Revenue protection (Premium = 70% of revenue)
- **Example:** If 63 Premium customers exist, you must contact ≥25 (40%)
- **Tip:** Increase if Premium churn is rising

#### **Max Action Saturation (%)**
- **Range:** 20% - 100%
- **Default:** 50%
- **What it controls:** No single action (e.g., email) can be used for >X% of customers
- **Why it exists:**
  - Prevents lazy "95% email only" campaigns
  - Forces diverse action mix
  - Better customer experience
- **Example:** With 250 customers and 50% cap, no action can be assigned to >125 customers
- **Tip:** Lower (e.g., 40%) for more diversity; raise (e.g., 70%) for flexibility

#### **Min Segment Coverage (%)**
- **Range:** 0% - 40%
- **Default:** 15%
- **What it controls:** Each subscription segment (Premium/Free/Family/Student) must get ≥X% coverage
- **Why it exists:**
  - Ensures fairness across demographics
  - Prevents algorithmic bias
  - Maintains relationships with entire customer base
- **Example:** Each of the 4 subscription types must have ≥15% contacted
- **Tip:** Set to 0% to maximize pure ROI; set to 20%+ for strong equity focus

---

### 🚀 Run Optimization Button

**Large green button:** "🚀 RUN OPTIMIZATION"
- **What it does:** Executes Gurobi MILP solver with current settings
- **How long:** 5-10 seconds for 250 customers
- **When to click:** After adjusting any sliders/settings
- **What happens:** Progress bar shows:
  1. Loading data... (20%)
  2. Initializing optimizer... (40%)
  3. Setting constraints... (60%)
  4. Solving model... (80%)
  5. Complete! (100%)

---

## Main Dashboard: Metrics & Visualizations

### ✅ Status Banner

**Green success banner at top:**
```
✅ Loaded 250 customers with predictions and features
```
- Confirms data loaded successfully
- Shows sample size (250 for Gurobi free license compliance)

---

### 📊 Current Week Overview (8 KPIs)

**Row 1 - Core Metrics:**

1. **Total Customers**
   - Number: 250
   - What it means: Total customers in this week's optimization cohort
   - Help text: "Total customers in prediction dataset"

2. **High Risk (p > 0.5)**
   - Number: ~125 (49.9% of base)
   - What it means: Customers with >50% churn probability
   - Delta: Shows percentage of customer base
   - Help text: "Customers with >50% churn probability"

3. **Avg Churn Probability**
   - Number: ~50.9%
   - What it means: Mean churn risk across all 250 customers
   - Help text: "Mean churn probability across all customers"

4. **At-Risk CLV**
   - Number: ~$55.0M
   - What it means: Total customer lifetime value at risk of churn
   - Formula: Σ (churn_probability × estimated_CLV)
   - Help text: "Total customer lifetime value at risk of churn"

**Row 2 - Segment Details:**

5. **Premium Customers**
   - Number: ~63 (25% of base)
   - What it means: Count of Premium subscription customers
   - Delta: Percentage of total customer base

6. **Yearly Plans**
   - Number: ~127 (50.8% of base)
   - What it means: Customers on annual payment plans
   - Delta: Percentage of total customer base

7. **Avg Weekly Hours**
   - Number: ~25.0h
   - What it means: Average listening time per customer per week
   - Help text: "Average listening time per customer"

8. **Avg Playlists Created**
   - Number: ~7.5
   - What it means: Average number of playlists per customer
   - Help text: "Average number of playlists per customer"

---

### 📈 Customer Analytics (3 Tabs)

#### **Tab 1: Risk Distribution**

**Left Side - Histogram Chart:**
- **Title:** "Churn Probability Distribution (XGBoost Predictions)"
- **X-axis:** Churn Probability (0.0 to 1.0)
- **Y-axis:** Number of Customers
- **Color:** Green (#1DB954 - Spotify green)
- **What it shows:** Distribution of churn risk across all customers
- **How to read:**
  - Peaks on the left (low risk) = many safe customers
  - Peaks on the right (high risk) = many at-risk customers
  - Flat distribution = mixed risk levels

**Right Side - Risk Breakdown:**
- **Low Risk (≤30%):** Count of customers
- **Medium Risk (30-70%):** Count of customers
- **High Risk (>70%):** Count of customers
- **Info box:** "💡 XGBoost model predictions show strong risk stratification"

#### **Tab 2: Segmentation**

**Heatmap Chart:**
- **Title:** "Customer Segmentation: Risk × Value"
- **Axes:** 
  - Y-axis: Risk Tier (Low/Medium/High)
  - X-axis: Value Tier (Low/Medium/High)
- **Color:** Green intensity shows customer count
- **What it shows:** Distribution of customers across 9 segments
- **How to read:**
  - **Top-right (High Risk + High Value):** Priority for retention calls
  - **Top-left (High Risk + Low Value):** Cost-efficient email campaigns
  - **Bottom-right (Low Risk + High Value):** Nurture with minimal intervention

**Strategy Guide:**
```
🟢 High Value + High Risk: Priority for retention calls (high CLV at stake)
🟡 High Value + Low Risk: Minimal intervention (nurture)
🟠 Low Value + High Risk: Cost-efficient email campaigns
```

#### **Tab 3: Subscription Mix**

**Left Side - Pie Chart:**
- **Title:** "Customer Base by Subscription Type"
- **Segments:** Premium, Free, Family, Student (roughly 25% each)
- **Colors:** Green gradient
- **What it shows:** Distribution of subscription types

**Right Side - Key Insights:**
- **Avg Churn Risk by Type:**
  - Shows mean churn probability for each subscription type
  - Typically: Free > Student > Family > Premium
- **Caption:** "Free users typically show higher churn propensity"

---

## Running an Optimization

### Step-by-Step Process

**1. Review Current Week Data**
- Check the 8 KPI metrics
- Look at risk distribution
- Identify high-risk segments

**2. Adjust Constraints (Sidebar)**
```
Example Settings:
  Budget: $150,000
  Email Capacity: 30,000
  Call Capacity: 500
  Min High-Risk: 60%
  Min Premium: 40%
  Max Action Saturation: 50%
  Min Segment Coverage: 15%
```

**3. Click "🚀 RUN OPTIMIZATION"**
- Progress bar appears
- Takes 5-10 seconds
- Don't refresh page during optimization

**4. Wait for Completion**
```
Progress stages:
📋 Preparing customer data... (20%)
🔧 Initializing Gurobi optimizer... (40%)
🎯 Setting operational constraints... (60%)
🚀 Solving optimization model... (80%)
✅ Optimization complete! (100%)
```

**5. Review Results**
- Success message: "🎉 Optimization completed successfully!"
- Results section appears below

---

## Understanding Results

### 📊 Key Performance Indicators (5 Metrics)

**1. Customers Treated**
- Example: 160 customers (64% of base)
- Meaning: How many customers receive an action
- Delta: Percentage of total customer base

**2. Weekly Spend**
- Example: $145,000 (97% of budget)
- Meaning: Total campaign cost
- Delta: Percentage of budget used
- Tip: If >95%, budget is binding—consider increasing

**3. Expected Churn Prevented**
- Example: 42 customers (33% of high-risk)
- Meaning: How many customers we expect to save
- Formula: Σ (churn_prob × uplift)
- Delta: Percentage of high-risk customers saved

**4. Expected Retained CLV**
- Example: $725,000
- Meaning: Total customer value we expect to keep
- Formula: Σ (churn_prob × uplift × CLV)

**5. ROI**
- Example: 400%
- Meaning: Return on investment
- Formula: (Retained CLV / Cost - 1) × 100%
- Help: "Return on Investment: (Retained CLV / Cost - 1) × 100"
- **What's good:**
  - 200%+ = Excellent
  - 100-200% = Good
  - 50-100% = Acceptable
  - <50% = Concerning

**Net Value Highlight Box:**
```
💰 Net Value: $580,000
Expected CLV Retained minus Campaign Cost
```

---

### 📋 Treatment Plan Breakdown (4 Tabs)

#### **Tab 1: By Action**

**Pie Chart:** Customer Distribution by Action
- Shows how customers are split across actions
- Example: 40% Email, 30% Discount Email, 20% Call, 10% In-App

**Bar Chart:** Net Value by Action
- Shows profit contribution of each action
- Sorted by net value (highest to lowest)

**Detailed Table:**
| Action | Customers | Total Cost | Retained CLV | Net Value | Avg Uplift |
|--------|-----------|------------|--------------|-----------|------------|
| Retention Call | 50 | $1,250 | $22,500 | $21,250 | 20% |
| Discount Email | 60 | $300 | $9,000 | $8,700 | 15% |
| Basic Email | 50 | $100 | $2,500 | $2,400 | 10% |

#### **Tab 2: By Segment**

**Heatmap:** Treatment Coverage: Risk × Value Segments
- Shows how many customers treated in each of 9 segments
- Color intensity = customer count
- Text overlay shows exact numbers

**Segment Performance Table:**
| Risk | Value | Customers | Cost | Retained CLV | Net Value |
|------|-------|-----------|------|--------------|-----------|
| High | High | 35 | $875 | $31,500 | $30,625 |
| High | Medium | 28 | $560 | $14,000 | $13,440 |

#### **Tab 3: By Channel**

**Bar Charts:**
- Customer Distribution by Channel
- Cost Distribution by Channel

**Channel Capacity Utilization:**

**Email:**
- Used: 2,400 / 30,000 (8%)
- Progress bar (green if <90%, yellow if 90-95%, red if >95%)
- Warning: "⚠️ Email capacity binding" (if >95%)

**Call:**
- Used: 500 / 500 (100%)
- Progress bar (red)
- Warning: "⚠️ Call capacity binding"

**Budget:**
- Used: $145K / $150K (97%)
- Progress bar (yellow)
- Warning: "⚠️ Budget binding"

#### **Tab 4: Top Customers**

**Table of Top 50 Customers by Impact:**
| Customer ID | Subscription | Churn Risk | CLV | Action | Cost | Retained CLV | Net Value |
|-------------|--------------|------------|-----|--------|------|--------------|-----------|
| 12345 | Premium | 72% | $1,200 | Retention Call | $25 | $450 | $425 |
| 67890 | Free | 55% | $300 | Discount Email | $5 | $82 | $77 |

**Info:** "💡 These customers offer the highest expected return on retention investment"

---

### 🎯 Constraint Analysis & Recommendations

**Left Side - Binding Constraints:**

Shows warnings for any constraint at >95% utilization:

```
⚠️ Budget (BINDING)
  - Current: $145,000 / $150,000 (97%)
  - Recommendation: Increase budget to $187,500 to enable ~40 more treatments
```

```
⚠️ Call Capacity (BINDING)
  - Current: 500 / 500 (100%)
  - Recommendation: Increase agent hours or shift high-value customers to VIP email
```

If no binding constraints:
```
✅ No binding constraints - all resources have available capacity
```

**Right Side - Shadow Price Analysis:**

Shows marginal value of relaxing each constraint:

```
If we relax constraints by 1 unit:

📊 Budget (+$1): Add ~$0.18 net value
📧 Email (+1): Add ~$15 net value
📞 Call (+1): Add ~$45 net value

*Values are estimates from dual analysis*
```

**How to use this:**
- Highest shadow price = biggest bottleneck
- Focus investments on constraints with high shadow prices
- Example: If call shadow price is $45, hiring more agents has high ROI

---

## Exporting Treatment Plans

### 📥 Export Section (3 Buttons)

**1. Download Complete Treatment Plan (CSV)**
- **File name:** `treatment_plan_YYYYMMDD.csv`
- **Contains:**
  - All customer IDs and actions
  - Costs, expected CLV retained, net value
  - Churn probabilities, CLV estimates
  - Subscription type, risk segment, value segment
  - **Holdout flag** (10% randomly marked as holdout for A/B testing)
  - **Execute treatment flag** (TRUE for 90%, FALSE for 10% holdout)
  - Plan date timestamp
- **Use for:** Master record, analysis, reporting

**2. Download Email List (CSV)**
- **File name:** `email_list_YYYYMMDD.csv`
- **Contains:** 
  - Customer IDs assigned to email actions
  - Action name (e.g., "discount_email", "basic_email")
  - Only customers with `execute_treatment = TRUE`
- **Use for:** Upload to Mailchimp, SendGrid, HubSpot

**3. Download Call Queue (CSV)**
- **File name:** `call_queue_YYYYMMDD.csv`
- **Contains:**
  - Customer IDs assigned to call actions
  - Action name
  - CLV (sorted highest to lowest - call most valuable first)
  - Only customers with `execute_treatment = TRUE`
- **Use for:** Upload to call center CRM (Salesforce, etc.)

**Important Notes:**
- ✅ Includes 10% holdout group for A/B testing
- ⚠️ DO NOT contact customers with `holdout = TRUE`
- Track holdout vs. treated groups separately
- Measure actual churn rates after 30 days

---

### 📋 Implementation Guide (Expandable)

**Click "📋 Implementation Guide" to reveal:**

**Weekly Execution Workflow:**

**Monday:**
1. Data Science team generates fresh churn predictions
2. Run optimization in this dashboard
3. Review results and adjust constraints if needed

**Tuesday:**
1. Download treatment plan
2. Upload email list to marketing automation
3. Upload call queue to CRM

**Wednesday-Friday:**
1. Execute email campaigns
2. Call center works through retention call queue
3. Monitor delivery rates and engagement

**Week 5+ (After initial 4 weeks):**
1. Measure churn rates: treated vs holdout
2. Calculate actual uplift per action
3. Update action catalog with real performance data
4. Re-run optimization with calibrated uplifts

**⚠️ Critical Reminders:**
- DO NOT TREAT customers marked as `holdout=True`
- Track both groups separately for uplift measurement
- Update uplifts quarterly based on actual results
- Re-score customers weekly with fresh ML predictions

---

## Sensitivity Analysis

### 🔍 What-If Scenario Analysis (Expandable Section)

**Purpose:** Test different budget levels to find optimal investment point

**How to Access:**
- Scroll to bottom of page
- Click "Run Sensitivity Analysis Across Budget Levels"

**Controls:**

1. **Minimum Budget**
   - Slider: $25K - $200K
   - Default: $50K
   - Starting point for scenario analysis

2. **Maximum Budget**
   - Slider: $100K - $500K
   - Default: $300K
   - Ending point for scenario analysis

3. **Step Size**
   - Options: $25K, $50K, $100K
   - Default: $50K
   - Increment between scenarios

**Example Setup:**
```
Min Budget: $50,000
Max Budget: $300,000
Step Size: $50,000

= 6 scenarios: $50K, $100K, $150K, $200K, $250K, $300K
```

**Run Time:** ~2-3 minutes (5-10 seconds per scenario)

**Click:** "🚀 Run Sensitivity Analysis"

---

### Sensitivity Results

**4 Charts (2×2 Grid):**

**1. Budget vs Net Value** (Top-left)
- Shows how net value changes with budget
- Curve typically increases then flattens (diminishing returns)
- Optimal budget = peak before flatten

**2. Budget vs ROI (%)** (Top-right)
- Shows return on investment at each budget level
- ROI typically decreases as budget increases
- Shows diminishing returns clearly

**3. Budget vs Customers Treated** (Bottom-left)
- Shows coverage increasing with budget
- Usually linear until hitting other constraints

**4. Budget vs Churn Prevented** (Bottom-right)
- Shows retention impact at each budget level
- Similar to customers treated but weighted by churn probability

**All charts:**
- Green lines with markers
- Interactive (hover for exact values)
- X-axis always shows budget level

---

### Scenario Comparison Table

**Columns:**
| Budget | Customers | Churn Prevented | Total Spend | Retained CLV | Net Value | ROI |
|--------|-----------|-----------------|-------------|--------------|-----------|-----|
| $50K | 80 | 20 | $48K | $240K | $192K | 400% |
| $100K | 140 | 35 | $96K | $432K | $336K | 350% |
| $150K | 160 | 42 | $145K | $725K | $580K | 400% |

- Sorted by budget (ascending)
- All dollar values formatted with $ and commas
- ROI formatted as percentage

---

### 💡 Key Insights Section

**Metrics Highlighted:**

1. **Optimal Budget**
   - Example: $180,000
   - Budget level with highest net value

2. **Max Net Value**
   - Example: $620,000
   - Highest net value achieved

3. **ROI at Optimal**
   - Example: 345%
   - ROI at the optimal budget point

**Recommendation Box:**
```
Based on diminishing returns analysis, the optimal weekly budget is 
$180,000, which generates $620,000 in net value.

Beyond this point, ROI decreases significantly due to treating 
lower-priority customers.
```

**Download Button:**
- "📥 Download Sensitivity Analysis Results"
- CSV with all scenario data
- Use for executive presentations, budget planning

---

## Weekly Workflow

### Monday Morning: Plan

1. **Open Dashboard** → Data loads automatically (250 customers)
2. **Review Overview Metrics**
   - Check high-risk count
   - Review at-risk CLV
   - Examine risk distribution chart
3. **Adjust Constraints** (if needed)
   - Set budget based on available funds
   - Confirm capacity matches this week's resources
   - Adjust policy constraints based on strategic priorities
4. **Run Optimization** → 5-10 seconds
5. **Review Results**
   - Check ROI (target: >200%)
   - Verify action mix is balanced
   - Check for binding constraints
   - Review top customers for VIP treatment
6. **Download Treatment Plan** → Save master CSV

---

### Tuesday Morning: Execute

1. **Download Channel-Specific Files:**
   - Email list → `email_list_YYYYMMDD.csv`
   - Call queue → `call_queue_YYYYMMDD.csv`

2. **Upload to Systems:**
   - **Email list** → Marketing automation (Mailchimp, SendGrid)
   - **Call queue** → CRM system (Salesforce, HubSpot)

3. **Quality Check:**
   - Verify row counts match expected
   - Spot-check a few customer IDs
   - Confirm holdout customers excluded

---

### Wednesday-Friday: Monitor

1. **Email Campaigns:**
   - Monitor send rates
   - Track open/click rates
   - Watch for bounces/unsubscribes

2. **Call Center:**
   - Agents work through queue (highest CLV first)
   - Track contact rates
   - Record outcomes in CRM

3. **Track Engagement:**
   - Which customers engaged?
   - Which actions performed best?
   - Any unexpected issues?

---

### Week 5+: Measure & Improve

**After 30 days (minimum):**

1. **Calculate Actual Churn Rates:**
   - **Treated group:** % who churned despite intervention
   - **Holdout group:** % who churned without intervention
   - **Actual uplift:** Difference between the two

2. **Compare to Predictions:**
   - Predicted uplift: 15%
   - Actual uplift: 12%
   - Adjustment: Lower uplift estimates by 3%

3. **Update Action Catalog:**
   - Replace estimated uplifts with measured uplifts
   - Update in `actions.csv` or optimizer config
   - Re-run optimizations with calibrated values

4. **Continuous Improvement:**
   - Repeat measurement every quarter
   - A/B test new actions (e.g., SMS, in-app messages)
   - Refine CLV estimation models

---

## Troubleshooting & FAQs

### Q: Dashboard shows "Unable to load customer data"
**A:** The 250-customer sample files are missing.
- Check that `prediction_250.csv` and `test_250.csv` exist in repository
- Verify files uploaded to Streamlit Cloud correctly
- Try redeploying the app

---

### Q: Optimization is stuck/taking too long
**A:** Should complete in 5-10 seconds for 250 customers.
- If >30 seconds, refresh the page
- Check Streamlit Cloud logs for errors
- Verify Gurobi license is valid (free academic license)

---

### Q: Getting "Model too large for Gurobi license" error
**A:** The free Gurobi license limits to 2,000 variables.
- Current setup: 250 customers × 8 actions = 2,000 variables ✅
- If you increased customer count, reduce back to 250
- For >250 customers, need commercial Gurobi license

---

### Q: ROI seems too high (>500%)
**A:** Uplift estimates may be optimistic.
- **Initial model:** Uses estimated uplifts (20% for calls, 15% for emails)
- **After A/B testing:** Replace with actual measured uplifts
- Typical actual uplifts: 5-12% (lower than estimates)
- ROI will normalize once you use real data

---

### Q: Budget is binding every week—should I increase it?
**A:** Yes, if you have funds available!
- Binding budget = you're leaving money on the table
- Run sensitivity analysis to see optimal budget level
- Check shadow price: each $1 added returns $X in net value
- **Rule of thumb:** Keep increasing until ROI drops below 150%

---

### Q: Only one action is used (e.g., 90% emails)
**A:** Adjust the "Max Action Saturation" constraint.
- **Current default:** 50% (no action >50% of customers)
- **If dominated:** Lower to 40% or 30%
- **If too restrictive:** Raise to 60% or 70%
- Ensures balanced campaign mix

---

### Q: Some customer segments are ignored
**A:** Increase "Min Segment Coverage" constraint.
- **Current default:** 15% (each segment gets ≥15%)
- **For stronger fairness:** Raise to 20-25%
- **For pure ROI focus:** Lower to 5-10%
- Ensures all demographics receive outreach

---

### Q: Call capacity is always binding
**A:** Calls are high-impact but limited.
- **Option 1:** Increase call center capacity (hire/train agents)
- **Option 2:** Reserve calls for highest-value customers only
- **Option 3:** Add "VIP Email" action (mid-cost, mid-uplift alternative)
- **Check shadow price:** Each additional call adds ~$45 in net value

---

### Q: How do I know if the solution is optimal?
**A:** Gurobi guarantees mathematical optimality.
- **"✅ OPTIMAL SOLUTION FOUND"** = proven best solution
- Not a heuristic or approximation
- Given your constraints, this is the maximum possible net value
- Different constraints = different optimal solution

---

### Q: Can I run this for 5,000 or 75,000 customers?
**A:** Yes, but you need a commercial Gurobi license.
- **Free license limit:** 2,000 variables (250 customers)
- **Academic license:** ~5,000 customers
- **Commercial license:** Unlimited (tested up to 75K+)
- **Solve times:** 
  - 250 customers: 5-10 seconds
  - 5,000 customers: 10-15 seconds
  - 75,000 customers: 60-90 seconds

---

### Q: What if I don't have churn predictions?
**A:** You need ML predictions first.
- This is a **prescriptive** tool (step 3 of analytics)
- Requires **predictive** model output (step 2)
- Build XGBoost/Random Forest churn model first
- Feed predictions into this optimizer
- See project README for full pipeline

---

### Q: How accurate are the "Expected" metrics?
**A:** Depends on your uplift estimates.
- **Initial run:** Uses generic uplift estimates (20%, 15%, 10%)
- **Accuracy:** ±30% (order of magnitude correct)
- **After A/B testing:** Uses measured uplifts
- **Accuracy:** ±10% (reliable)
- **Best practice:** Run for 4-6 weeks, measure, recalibrate

---

### Q: Why is there a 10% holdout group?
**A:** For rigorous A/B testing and uplift measurement.
- **Treated (90%):** Receive assigned actions
- **Holdout (10%):** Receive NO outreach
- **After 30 days:** Compare churn rates
- **Calculate uplift:** % reduction in churn due to treatment
- **Use uplift:** Update model with real performance data
- **⚠️ Critical:** DO NOT contact holdout customers!

---

### Q: Can I manually override the recommendations?
**A:** Yes, the CSV is editable.
- Download treatment plan
- Edit in Excel/Google Sheets
- Remove customers you don't want to contact
- Add custom actions if needed
- **Note:** Manual edits may reduce optimality

---

### Q: How do I explain this to executives?
**Use this script:**

> "This dashboard uses mathematical optimization to create our weekly retention plan. It analyzes 250 at-risk customers and determines the optimal allocation of our budget, email capacity, and call center resources to maximize retained revenue.
>
> The model respects all our operational constraints and policy requirements—like ensuring we contact at least 60% of high-risk customers and 40% of Premium subscribers—while finding the combination that delivers the highest ROI.
>
> It runs in 10 seconds and typically generates 300-400% ROI, meaning for every dollar we spend on retention, we keep $4 in customer lifetime value. We can export the treatment plan as a CSV and upload it directly to our marketing automation and CRM systems."

---

## Technical Notes

### System Requirements
- **Browser:** Chrome, Firefox, Safari, Edge (latest versions)
- **Internet:** Required (cloud-based app)
- **Data files:** `prediction_250.csv`, `test_250.csv` (automatically loaded)

### Data Privacy
- No customer PII displayed (only customer IDs)
- All data processed in-memory (not saved to Streamlit servers)
- Treatment plans exported to your local machine
- GDPR/CCPA compliant (no persistent storage)

### License Information
- **Streamlit:** Open-source (Apache 2.0)
- **Gurobi:** Free academic license (2,000 variable limit)
- **Python packages:** All open-source (pandas, numpy, plotly)

### Performance
- **Load time:** 2-3 seconds (initial data load)
- **Optimization time:** 5-10 seconds (250 customers)
- **Sensitivity analysis:** 2-3 minutes (6 scenarios)

---

## Support & Questions

**For technical issues:**
- Check Streamlit Cloud logs ("Manage app" button)
- Verify all CSV files present in repository
- Try redeploying the app

**For model questions:**
- See `PRESCRIPTIVE_MODEL_EXPLAINED.md` for full mathematical formulation
- See `README.md` for project overview
- See `music_streaming_retention_75k.py` for optimizer source code

**For business questions:**
- Review this guide (dashboard-usage.md)
- Check examples in each section
- Start with default settings and adjust incrementally

---

## Quick Reference Card

### Default Settings
```
Budget: $150,000
Email Capacity: 30,000
Call Capacity: 500
Min High-Risk: 60%
Min Premium: 40%
Max Action Saturation: 50%
Min Segment Coverage: 15%
```

### Typical Results (250 customers)
```
Customers Treated: 160 (64%)
Weekly Spend: $145K
Churn Prevented: 42 customers
Retained CLV: $725K
Net Value: $580K
ROI: 400%
```

### Key Buttons
- **🚀 RUN OPTIMIZATION** → Execute solver
- **📥 Download Complete Treatment Plan** → Master CSV
- **📧 Email List** → For marketing automation
- **📞 Call Queue** → For CRM system
- **🚀 Run Sensitivity Analysis** → Budget scenarios

### Key Metrics to Watch
- **ROI** → Target: >200%
- **Budget Utilization** → Sweet spot: 85-95%
- **Binding Constraints** → Focus investment here
- **Action Mix** → Should be balanced (no single action >60%)

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Dashboard:** PlaylistPro Retention Optimizer  
**Powered by:** Streamlit + Gurobi + XGBoost
