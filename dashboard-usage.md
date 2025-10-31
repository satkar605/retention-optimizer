# PlaylistPro Retention Optimizer - Manager's Guide

## What This Dashboard Does

This tool helps you **decide which at-risk customers to contact each week** to prevent churn, while staying within your budget and operational limits. Think of it as an intelligent assistant that automatically creates your weekly retention campaign plan.

**The Problem It Solves:**  
You have 75,000 customers, but only limited budget and staff capacity. You can't contact everyone, so the optimizer figures out which customers are worth targeting based on their churn risk and lifetime value.

**The Output:**  
A weekly action plan telling you exactly which customers to email, which to call, and which to offer discounts to—maximizing revenue retained per dollar spent.

---

## Understanding the Controls (Left Sidebar)

### 💰 Budget & Capacity Constraints

These are your **operational limits**—the resources you have available each week.

#### **Weekly Budget ($)**
- **What it is:** Total dollars you can spend on retention activities this week (emails, calls, discounts, etc.)
- **Why it matters:** Prevents overspending on retention campaigns
- **Typical range:** $50,000 - $300,000/week
- **How to set it:**
  - Start with your approved retention marketing budget
  - Consider it as a weekly cap, not a target to hit
  - Example: If you have $600K/month, set weekly budget to ~$150K

**Manager Tip:** If the optimizer uses 95%+ of the budget, you're probably leaving money on the table—consider increasing it.

---

#### **Email Capacity (per week)**
- **What it is:** Maximum number of retention emails your marketing team can send per week
- **Why it matters:** Email systems and marketing ops have throughput limits
- **Typical range:** 10,000 - 50,000 emails/week
- **How to set it:**
  - Check with your email marketing team on their weekly capacity
  - Account for other campaigns already scheduled
  - Consider deliverability best practices (don't flood inboxes)

**Manager Tip:** Email is your cheapest channel (~$2-5 per customer), so you generally want high email capacity.

---

#### **Call Center Capacity**
- **What it is:** Maximum number of retention calls your team can make per week
- **Why it matters:** Agents are expensive and limited in availability
- **Typical range:** 200 - 1,000 calls/week
- **How to set it:**
  - Calculate: (Number of agents) × (calls per agent per day) × (5 days)
  - Example: 5 agents × 8 calls/day × 5 days = 200 calls/week
  - Reserve capacity for inbound calls and other campaigns

**Manager Tip:** Calls are expensive (~$25-50 per customer) but have the highest success rate. The optimizer reserves calls for your most valuable at-risk customers.

---

### 🎯 Policy Constraints

These are **business rules** that ensure you're hitting strategic targets, even if they're not the most profitable in the short term.

#### **Minimum High-Risk Coverage (%)**
- **What it is:** Minimum percentage of high-risk customers (churn probability > 50%) you MUST contact
- **Why it matters:** Ensures you don't ignore customers about to churn, even if they're lower value
- **Typical range:** 40% - 80%
- **Recommended:** 60% (contact at least 60% of high-risk customers)

**Business Reason:**  
You might have a strategic goal to "reach out to all customers at risk of leaving" for brand reputation, even if some aren't the most valuable. This constraint prevents the optimizer from only chasing high-value customers.

**Example:**  
- You have 15,000 high-risk customers this week
- Set constraint to 60%
- Optimizer MUST include at least 9,000 of them in the treatment plan

**Manager Tip:** If you're struggling to hit this constraint due to budget, you'll see a warning. Consider increasing budget or lowering the percentage.

---

#### **Minimum Premium Customer Coverage (%)**
- **What it is:** Minimum percentage of Premium subscription customers you MUST contact (regardless of churn risk)
- **Why it matters:** Premium customers are your highest-value segment—you want to show extra care
- **Typical range:** 20% - 60%
- **Recommended:** 40% (contact at least 40% of Premium customers)

**Business Reason:**  
Premium customers pay 3-5x more than Free users. Even if some Premium customers have low churn risk right now, you want to proactively engage them to maintain loyalty and reduce future churn.

**Example:**  
- You have 20,000 Premium customers
- Set constraint to 40%
- Optimizer MUST include at least 8,000 Premium customers in the plan (through emails, calls, or discounts)

**Manager Tip:** Adjust this based on your Premium churn trends. If Premium churn is rising, increase this percentage.

---

## How to Use the Dashboard (Weekly Workflow)

### Monday Morning: Run Your Weekly Optimization

1. **Review the Overview Section**
   - Check total high-risk customers this week
   - Look at at-risk CLV (customer lifetime value)
   - Review Premium customer count

2. **Adjust Your Constraints** (Left Sidebar)
   ```
   Example Settings:
   - Weekly Budget: $150,000
   - Email Capacity: 30,000
   - Call Capacity: 500
   - Min High-Risk Coverage: 60%
   - Min Premium Coverage: 40%
   ```

3. **Click "RUN OPTIMIZATION"**
   - Takes 30-90 seconds to solve
   - Gurobi optimizer finds the best treatment plan

4. **Review Results**
   - **Key Metrics:** Customers treated, spend, expected churn prevented, ROI
   - **Action Breakdown:** See exactly how many emails, calls, discounts to send
   - **Top Customers:** View the 50 highest-impact customers

5. **Check for Binding Constraints**
   - If you see "⚠️ Budget (BINDING)", you've maxed out your budget
   - If you see "⚠️ Email Capacity (BINDING)", you need more email throughput
   - Binding constraints mean you could do better if you increased that resource

6. **Download Treatment Plan**
   - Click "Download Complete Treatment Plan (CSV)"
   - Includes customer IDs, actions, and 10% holdout group for A/B testing

---

### Tuesday: Execute the Plan

1. **Email Campaign**
   - Download "Email List" button
   - Upload to your email platform (Mailchimp, SendGrid, etc.)
   - Schedule send for Tuesday afternoon

2. **Call Queue**
   - Download "Call Queue" button
   - Upload to your CRM (Salesforce, HubSpot, etc.)
   - Agents work through the queue Wednesday-Friday

3. **Discount Offers**
   - Check treatment plan for discount actions
   - Set up in-app or email discount codes

---

### Week 5+: Measure Results

After 4 weeks of execution:

1. **Compare Churn Rates:**
   - Treated customers vs. holdout group
   - Calculate actual uplift percentage

2. **Update the Optimizer:**
   - If actual uplift is different from estimates, update the action catalog
   - Re-run optimization with real-world data

---

## Understanding the Results

### What is "Expected Churn Prevented"?
The number of customers we expect to **save from churning** through these actions.

**Example:**  
- 10,000 customers with 60% churn probability
- We contact them with 20% uplift action
- Expected saves = 10,000 × 0.60 × 0.20 = 1,200 customers retained

---

### What is "Expected Retained CLV"?
The total customer lifetime value we expect to **keep** through these interventions.

**Example:**  
- 1,200 customers retained
- Average CLV = $500
- Retained CLV = 1,200 × $500 = $600,000

---

### What is "ROI"?
Return on investment: how much value you keep for every dollar spent.

**Formula:** ROI = (Retained CLV / Campaign Cost - 1) × 100%

**Example:**  
- Retained CLV: $600,000
- Campaign Cost: $100,000
- ROI = ($600,000 / $100,000 - 1) × 100% = **500%**

**What this means:** For every $1 you spend, you keep $6 in customer value.

**Good ROI targets:**
- 200%+ = Excellent (keep spending)
- 100-200% = Good (maintain)
- 50-100% = Acceptable (monitor)
- <50% = Concerning (reduce budget or improve actions)

---

## Common Questions

### Q: What if my budget is binding every week?
**A:** This is actually a good sign—it means you have more profitable opportunities than budget. Request budget increase and use the Sensitivity Analysis to show leadership the ROI of additional spend.

### Q: Should I always try to hit 100% utilization?
**A:** No. Aim for 85-95% utilization. If you're consistently at 100%, you're probably missing opportunities. Build in some slack.

### Q: What if I can't meet the high-risk coverage constraint?
**A:** Either increase budget/capacity, or lower the percentage. Talk to leadership about strategic priorities: maximize profit vs. contact all at-risk customers.

### Q: How do I know if the uplift estimates are accurate?
**A:** You don't at first—they're educated guesses. After 4-6 weeks, compare treated vs. holdout groups. Update the action catalog with real measured uplifts.

### Q: Can I run multiple scenarios before deciding?
**A:** Yes! Use the "What-If Scenario Analysis" section to test different budget levels and find the optimal investment point.

---

## Quick Reference: Constraint Cheat Sheet

| Constraint | What It Controls | Typical Value | When to Increase | When to Decrease |
|------------|------------------|---------------|------------------|------------------|
| **Weekly Budget** | Max dollars to spend | $150K | ROI > 200%, binding constraint | ROI < 100%, excess capacity |
| **Email Capacity** | Max emails per week | 30,000 | Email binding, high ROI on email | Email deliverability issues |
| **Call Capacity** | Max calls per week | 500 | Call binding, high CLV customers | Call costs exceeding value |
| **Min High-Risk %** | Coverage of at-risk | 60% | Strategic priority to contact churners | Budget too tight, lower value customers |
| **Min Premium %** | Coverage of Premium | 40% | Premium churn rising | Premium segment already loyal |

---

## Pro Tips for Maximum Impact

1. **Start Conservative**
   - Week 1: Set modest constraints, learn the system
   - Week 2-4: Adjust based on results
   - Week 5+: Optimize based on measured uplift

2. **Monitor Binding Constraints Weekly**
   - If the same constraint binds every week, that's your bottleneck
   - Request resources to expand that constraint

3. **Use Sensitivity Analysis**
   - Test budget levels from $50K to $300K
   - Find the point where ROI starts declining (diminishing returns)
   - That's your optimal budget

4. **Don't Ignore Holdout Groups**
   - 10% of customers are automatically held out
   - **DO NOT contact them** (they're your control group)
   - Measure their churn vs. treated customers after 30 days

5. **Review Top 50 Customers Weekly**
   - These are your highest-value opportunities
   - Consider VIP treatment beyond the optimizer's recommendation

---

## Support & Questions

If you have questions about interpreting results or adjusting constraints:
1. Review this guide
2. Check the sensitivity analysis for "what-if" scenarios
3. Run test scenarios with different settings (it's safe to experiment!)

**Remember:** The optimizer is a decision support tool, not autopilot. Use your business judgment alongside the recommendations.

