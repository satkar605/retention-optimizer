# Sample Configuration Files

## constraints_config.json

```json
{
  "weekly_budget": 150000,
  "email_capacity": 30000,
  "call_capacity": 500,
  "min_high_risk_pct": 0.60,
  "min_premium_pct": 0.40
}
```

## retention_actions.csv

```csv
action_id,action_name,channel,cost,uplift,eligible_segment,description
0,No Action,none,0,0.00,all,Do nothing - baseline
1,Personalized Email,email,2,0.08,all,Automated email with curated playlist recommendations
2,20% Discount Offer,email,20,0.15,all,One-month subscription discount for paid tiers
3,Premium Trial,in_app,10,0.25,Free,30-day free Premium trial for Free users
4,Family Plan Upgrade,email,15,0.18,Premium,Discounted upgrade to Family plan
5,Retention Specialist Call,call,50,0.30,high_value,Personal outreach from retention team
6,VIP Concierge Service,call,100,0.40,high_value,Dedicated account manager + exclusive artist events
7,Win-Back Email Series,email,30,0.22,all,Multi-touch campaign with special offers over 2 weeks
8,Student Discount,email,12,0.14,Student,Extended student discount period
9,Playlist Curator Access,in_app,5,0.12,all,Early access to new playlists and features
10,Concert Ticket Giveaway,email,40,0.20,high_value,Entry into exclusive concert ticket lottery
```

## customer_features_sample.csv

```csv
customer_id,subscription_type,payment_plan,weekly_hours,weekly_songs_played,num_playlists_created,tenure_days
200000,Free,Monthly,22.2,299,42,1644
200001,Premium,Monthly,41.5,437,4,2718
200002,Free,Monthly,16.6,57,38,2783
200003,Student,Monthly,21.8,181,80,757
200004,Family,Monthly,33.6,348,67,80
```

## CLV Estimation Guidelines

### Base Annual Revenue by Subscription Type

| Subscription | Monthly Price | Annual Revenue | Gross Margin (70%) |
|--------------|---------------|----------------|--------------------|
| Free | $0 (ads) | $100 | $70 |
| Student | $4.99 | $60 | $42 |
| Premium | $9.99 | $120 | $84 |
| Family | $14.99 | $180 | $126 |

### Payment Plan Multiplier

- **Monthly**: 1.0x (baseline)
- **Yearly**: 1.3x (30% bonus for annual commitment, reflects higher retention)

### Engagement Multiplier

Calculate engagement score (0 to 1) based on:

```python
engagement_score = (
    (weekly_hours / max_weekly_hours) * 0.3 +
    (weekly_songs / max_weekly_songs) * 0.3 +
    ((1 - skip_rate) / max_skip_rate) * 0.2 +
    (num_playlists / max_playlists) * 0.2
)
```

Highly engaged users have 50-100% higher lifetime value.

### Final CLV Formula (2-year horizon)

```python
CLV = base_revenue * payment_multiplier * (1 + engagement_score) * 2 * gross_margin_pct
```

**Example**:
- Premium user, Yearly plan
- 30 weekly hours (high engagement â score = 0.7)
- CLV = $120 Ã 1.3 Ã (1 + 0.7) Ã 2 Ã 0.70 = **$372**

### Segment-Based CLV Proxies (if no engagement data)

Use these as defaults:

| Risk Segment | Low Value | Medium Value | High Value |
|--------------|-----------|--------------|------------|
| Low Risk | $150 | $280 | $450 |
| Medium Risk | $180 | $320 | $500 |
| High Risk | $200 | $350 | $550 |

*High-risk customers who stay tend to have higher LTV due to sunk cost and habit formation.*

## Uplift Estimation Guidelines

### Industry Benchmarks (Music Streaming)

| Action Type | Estimated Uplift | Confidence | Notes |
|-------------|------------------|------------|-------|
| Generic Email | 5-10% | Medium | Automated, low-touch |
| Personalized Email | 8-15% | Medium | Requires ML-driven personalization |
| Discount Offer | 12-20% | High | Proven tactic, short-term boost |
| Premium Trial | 20-30% | High | Strong for Free-to-Premium conversion |
| Retention Call | 25-35% | Medium | High-touch, expensive |
| VIP Service | 35-45% | Low | Limited data, high-value only |
| Win-Back Series | 18-25% | Medium | Multi-touch over 2-4 weeks |

### Initial Estimates (Conservative Approach)

Start with **lower bounds** of the ranges above. Why?
- Overestimating uplift â over-spending on ineffective actions
- Underestimating â opportunity cost, but safer

After 4 weeks of measurement, adjust to actual values.

### Segmented Uplifts (Advanced)

Uplift varies by customer segment:

| Action | Free Users | Student | Premium | Family |
|--------|-----------|---------|---------|--------|
| Email | 10% | 8% | 7% | 6% |
| Discount | 18% | 15% | 14% | 12% |
| Trial | 25% | N/A | N/A | N/A |
| Call | 35% | 30% | 28% | 25% |

*Free users have higher uplift because they have less to lose by churning.*

## Operational Constraints Guidelines

### Weekly Budget

**Formula**:
```
Recommended Budget = 2-5% of At-Risk Revenue
```

**Example**:
- 75,000 customers
- Average CLV: $250
- Average churn probability: 30%
- At-risk revenue = 75,000 Ã $250 Ã 0.30 = $5.625M
- Recommended budget = $5.625M Ã 2-5% = **$112K - $281K per week**

Start conservative, scale up based on measured ROI.

### Email Capacity

**Factors**:
- Email service provider limits (e.g., SendGrid, Mailchimp)
- Deliverability reputation management
- Content creation bandwidth

**Typical**:
- Small org (1-2 marketers): 5,000-10,000/week
- Medium org (marketing team): 20,000-50,000/week
- Large org (automation platform): 100,000+/week

### Call Capacity

**Formula**:
```
Calls per Week = (Agents Ã Hours/Day Ã Days/Week Ã Calls/Hour) Ã Utilization
```

**Example**:
- 5 agents
- 8 hours/day
- 5 days/week
- 3 calls/hour (20 min/call)
- 80% utilization
- Capacity = 5 Ã 8 Ã 5 Ã 3 Ã 0.80 = **480 calls/week**

### Minimum High-Risk Coverage

**Policy decision** based on:
- Brand reputation (can't ignore at-risk customers)
- Regulatory requirements (consumer protection)
- Internal equity/fairness standards

**Typical**: 50-70%
- 50%: Efficiency-focused (ROI maximization)
- 70%: Customer-centric (protect all high-risk)

## Cost Guidelines

### Email Costs

- **Automated email**: $0.50 - $2 per send (service fees + content creation)
- **Personalized email**: $2 - $5 (includes ML recommendation engine)
- **Email series** (multi-touch): $10 - $30 total

### Discount Costs

Calculate **opportunity cost**, not just discount amount:

```
Cost = Discount Amount Ã (1 - Incremental Probability Customer Would Have Stayed Anyway)
```

**Example**:
- Offer: 20% off $9.99/month = $2/month Ã 3 months = $6 discount
- Baseline retention (no action): 40%
- With discount: 55%
- Incremental: 15%
- True cost = $6 (we don't count the 40% who would've stayed)

**Simplified**: Use full discount value for conservative budgeting.

### Call Center Costs

- **Agent hourly rate**: $20-30/hour (fully loaded)
- **Calls per hour**: 3 (20 min/call)
- **Cost per call**: $7-10 base + $20-30 labor = **$27-40 per call**

*Use $50 as a conservative estimate for retention specialist calls.*

### Premium Trial Costs

- **Revenue foregone**: $9.99 Ã 1 month = $10
- **Server/streaming costs**: Negligible (marginal)
- **Conversion rate**: ~30% of trialists convert to paid
- **Effective cost**: $10 per trial

## Sensitivity Analysis

Run optimization multiple times with different budget levels to understand ROI curve:

| Weekly Budget | Customers Treated | Churn Reduction | Retained CLV | Net Value | ROI |
|---------------|-------------------|-----------------|--------------|-----------|-----|
| $50,000 | 18,000 | 720 | $950,000 | $900,000 | 1,800% |
| $100,000 | 32,000 | 1,280 | $1,650,000 | $1,550,000 | 1,550% |
| $150,000 | 45,000 | 1,800 | $2,280,000 | $2,130,000 | 1,420% |
| $200,000 | 55,000 | 2,200 | $2,750,000 | $2,550,000 | 1,275% |
| $250,000 | 62,000 | 2,480 | $3,050,000 | $2,800,000 | 1,120% |

**Insight**: Diminishing returns kick in around $150-200K/week. Optimal budget depends on your ROI threshold.

## Example: End-to-End Workflow

### Day 1: Monday (Scoring)

1. ML team generates churn probabilities for all 75K customers
2. Export to `churn_probabilities_75k.csv`

### Day 2: Tuesday (Optimization)

1. Run optimization script:
   ```bash
   python music_streaming_retention_75k.py
   ```
2. Review results, adjust constraints if needed
3. Export treatment list: `weekly_treatment_plan.csv`

### Day 3: Wednesday (Execution Setup)

1. Upload treatment list to CRM (Salesforce, HubSpot, etc.)
2. Create audience segments:
   - Email campaigns (actions 1, 2, 7)
   - Call queues (actions 5, 6)
   - In-app prompts (actions 3, 9)
3. **Exclude holdout customers** from all campaigns

### Day 4-7: Thursday-Sunday (Execution)

1. Marketing automation sends emails
2. Call center agents work through retention call queue
3. In-app prompts triggered for eligible users

### Week 2-4: Monitoring

1. Track metrics:
   - Campaign delivery rates
   - Open/click rates (emails)
   - Call completion rates
   - In-app engagement
2. Re-score customers weekly, re-run optimization

### Week 5: Measurement

1. Calculate churn rates (4 weeks post-treatment):
   - Treated group
   - Holdout group
2. Compute actual uplift per action
3. Update action catalog with calibrated uplifts
4. Re-run optimization â model learns!

### Ongoing

Repeat weekly, continuously improving as uplifts get calibrated.

---

**Questions or issues? Open a support ticket or contact your Gurobi representative.**
```
