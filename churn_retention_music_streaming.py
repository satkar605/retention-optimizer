
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np

# Use very small sample for license limits
np.random.seed(42)
n_customers = 300  # Small for demo license

# Generate data matching your 75K structure
customers_df = pd.DataFrame({
    'customer_id': range(200000, 200000 + n_customers),
    'p': np.random.beta(2, 5, n_customers),
    'subscription_type': np.random.choice(['Free', 'Student', 'Premium', 'Family'], n_customers, p=[0.25, 0.25, 0.30, 0.20]),
    'payment_plan': np.random.choice(['Monthly', 'Yearly'], n_customers, p=[0.70, 0.30])
})

# Estimate CLV (2-year horizon)
sub_val = {'Free': 100, 'Student': 120, 'Premium': 240, 'Family': 360}
pay_mult = {'Monthly': 1.0, 'Yearly': 1.3}
customers_df['v'] = (
    customers_df['subscription_type'].map(sub_val) * 
    customers_df['payment_plan'].map(pay_mult) *
    (1 + np.random.uniform(0, 0.5, n_customers))
)

# Segments
customers_df['risk'] = pd.cut(customers_df['p'], bins=[0, 0.3, 0.7, 1.0], labels=['low', 'med', 'high'])
customers_df['value_tier'] = pd.cut(customers_df['v'], bins=[0, 150, 300, 1000], labels=['low', 'med', 'high'])
customers_df['is_high_value'] = customers_df['value_tier'] == 'high'

print("="*80)
print("MUSIC STREAMING RETENTION OPTIMIZATION")
print("Your 75,001 Customer Dataset")
print("="*80)
print(f"\nð DATASET CHARACTERISTICS")
print(f"Sample: {n_customers} customers (demo) | Full dataset: 75,001 customers")
print(f"Churn probability: {customers_df['p'].min():.3f} - {customers_df['p'].max():.3f}")
print(f"CLV (2-year): ${customers_df['v'].min():.0f} - ${customers_df['v'].max():.0f}")
print(f"Total at-risk value: ${(customers_df['p'] * customers_df['v']).sum():,.0f}")

print(f"\nð¯ SEGMENTATION")
print(customers_df.groupby(['risk', 'value_tier'], observed=True).size().unstack(fill_value=0))

# Action catalog for music streaming
actions_df = pd.DataFrame([
    {'id': 0, 'name': 'No Action', 'channel': 'none', 'cost': 0, 'uplift': 0.00, 'eligible': 'all'},
    {'id': 1, 'name': 'Personalized Email', 'channel': 'email', 'cost': 2, 'uplift': 0.08, 'eligible': 'all'},
    {'id': 2, 'name': '20% Discount', 'channel': 'email', 'cost': 20, 'uplift': 0.15, 'eligible': 'all'},
    {'id': 3, 'name': 'Premium Trial', 'channel': 'in_app', 'cost': 10, 'uplift': 0.25, 'eligible': 'Free'},
    {'id': 4, 'name': 'Retention Call', 'channel': 'call', 'cost': 50, 'uplift': 0.30, 'eligible': 'high_value'},
    {'id': 5, 'name': 'VIP Service', 'channel': 'call', 'cost': 100, 'uplift': 0.40, 'eligible': 'high_value'},
])

print(f"\nð¼ RETENTION ACTIONS (Music Streaming)")
print(actions_df[['id', 'name', 'channel', 'cost', 'uplift', 'eligible']].to_string(index=False))
print(f"\nâ ï¸ Uplift values are ESTIMATES - must calibrate via A/B tests!")

# Operational constraints
budget = 5000
email_cap = 200
call_cap = 30
min_high_risk_pct = 0.60

print(f"\nð¯ WEEKLY OPERATIONAL CONSTRAINTS")
print(f"Budget: ${budget:,}")
print(f"Email capacity: {email_cap:,}")
print(f"Call capacity: {call_cap}")
print(f"Min high-risk coverage: {min_high_risk_pct:.0%}")

# ============================================================================
# GUROBI OPTIMIZATION
# ============================================================================

print(f"\n" + "="*80)
print("GUROBI OPTIMIZATION")
print("="*80)

env = gp.Env()
model = gp.Model("MusicRetention", env=env)

# Build eligibility matrix
eligible = []
for _, c in customers_df.iterrows():
    i = c['customer_id']
    p, v = c['p'], c['v']
    sub = c['subscription_type']
    hv = c['is_high_value']
    
    for _, a in actions_df.iterrows():
        k = a['id']
        cost = a['cost']
        uplift = a['uplift']
        elig = a['eligible']
        
        # Check eligibility
        if elig == 'all':
            pass
        elif elig == 'Free' and sub != 'Free':
            continue
        elif elig == 'high_value' and not hv:
            continue
        
        # Store: (customer_id, action_id, cost, expected_value)
        expected_value = p * uplift * v - cost
        eligible.append((i, k, cost, expected_value))

print(f"â Built eligibility matrix: {len(eligible):,} customer-action pairs")

# Decision variables
x = model.addVars([(e[0], e[1]) for e in eligible], vtype=GRB.BINARY, name="x")

# Objective: Maximize expected retained CLV - cost
print(f"âï¸ Setting objective: maximize p Ã u Ã v - c")
model.setObjective(
    gp.quicksum(e[3] * x[e[0], e[1]] for e in eligible),
    GRB.MAXIMIZE
)

# Constraint: One action per customer
print(f"âï¸ Adding constraints...")
for i in customers_df['customer_id']:
    eligible_for_i = [e for e in eligible if e[0] == i]
    model.addConstr(gp.quicksum(x[e[0], e[1]] for e in eligible_for_i) <= 1)

# Budget constraint
model.addConstr(
    gp.quicksum(e[2] * x[e[0], e[1]] for e in eligible) <= budget,
    name="budget"
)

# Email capacity
email_actions = set(actions_df[actions_df['channel'] == 'email']['id'])
email_pairs = [e for e in eligible if e[1] in email_actions]
model.addConstr(
    gp.quicksum(x[e[0], e[1]] for e in email_pairs) <= email_cap,
    name="email_cap"
)

# Call capacity
call_actions = set(actions_df[actions_df['channel'] == 'call']['id'])
call_pairs = [e for e in eligible if e[1] in call_actions]
model.addConstr(
    gp.quicksum(x[e[0], e[1]] for e in call_pairs) <= call_cap,
    name="call_cap"
)

# Minimum high-risk coverage
high_risk_ids = set(customers_df[customers_df['risk'] == 'high']['customer_id'])
min_treat = int(min_high_risk_pct * len(high_risk_ids))
high_risk_pairs = [e for e in eligible if e[0] in high_risk_ids and e[1] > 0]
model.addConstr(
    gp.quicksum(x[e[0], e[1]] for e in high_risk_pairs) >= min_treat,
    name="min_high_risk"
)

print(f"\nð Solving...\n")
model.optimize()

# ============================================================================
# RESULTS
# ============================================================================

if model.status == GRB.OPTIMAL:
    print("="*80)
    print("â OPTIMAL SOLUTION")
    print("="*80)
    print(f"Expected Net Value: ${model.objVal:,.2f}\n")
    
    # Extract assignments
    treated_list = []
    for e in eligible:
        i, k, cost, exp_val = e
        if x[i, k].X > 0.5:
            c = customers_df[customers_df['customer_id'] == i].iloc[0]
            a = actions_df[actions_df['id'] == k].iloc[0]
            retained = c['p'] * a['uplift'] * c['v']
            treated_list.append({
                'customer_id': i,
                'subscription': c['subscription_type'],
                'risk': c['risk'],
                'p': c['p'],
                'clv': c['v'],
                'action': a['name'],
                'channel': a['channel'],
                'cost': cost,
                'uplift': a['uplift'],
                'retained_clv': retained,
                'net_value': retained - cost
            })
    
    results_df = pd.DataFrame(treated_list)
    
    # KPIs
    total_spend = results_df['cost'].sum()
    total_retained = results_df['retained_clv'].sum()
    churn_reduction = (results_df['p'] * results_df['uplift']).sum()
    roi = (total_retained / total_spend - 1) * 100 if total_spend > 0 else 0
    
    print(f"ð KEY PERFORMANCE INDICATORS")
    print("-"*80)
    print(f"Customers Treated:           {len(results_df):,}")
    print(f"Total Spend:                 ${total_spend:,.2f}")
    print(f"Expected Churn Reduction:    {churn_reduction:.1f} customers")
    print(f"Expected Retained CLV:       ${total_retained:,.2f}")
    print(f"Net Value (CLV - Cost):      ${total_retained - total_spend:,.2f}")
    print(f"ROI:                         {roi:.1f}%")
    
    print(f"\nð TREATMENT PLAN BY ACTION")
    print("-"*80)
    action_summary = results_df.groupby('action').agg({
        'customer_id': 'count',
        'cost': 'sum',
        'retained_clv': 'sum',
        'net_value': 'sum'
    }).reset_index()
    action_summary.columns = ['Action', 'Count', 'Cost', 'Retained CLV', 'Net Value']
    print(action_summary.sort_values('Net Value', ascending=False).to_string(index=False))
    
    print(f"\nð¯ TREATMENT BY RISK SEGMENT")
    print("-"*80)
    risk_summary = results_df.groupby('risk', observed=True).agg({
        'customer_id': 'count',
        'cost': 'sum',
        'retained_clv': 'sum',
        'net_value': 'sum'
    }).reset_index()
    risk_summary.columns = ['Risk', 'Count', 'Cost', 'Retained CLV', 'Net Value']
    print(risk_summary.to_string(index=False))
    
    print(f"\nð TOP 10 HIGHEST IMPACT CUSTOMERS")
    print("-"*80)
    top10 = results_df.nlargest(10, 'net_value')[
        ['customer_id', 'subscription', 'p', 'clv', 'action', 'net_value']
    ]
    print(top10.to_string(index=False))
    
    print(f"\nð CONSTRAINT STATUS")
    print("-"*80)
    for constr in model.getConstrs():
        if abs(constr.Slack) < 0.01 and constr.ConstrName in ['budget', 'email_cap', 'call_cap', 'min_high_risk']:
            print(f"â¢ {constr.ConstrName}: BINDING")
            if 'budget' in constr.ConstrName:
                print(f"  â Budget fully used. More budget = more treatments.")
            elif 'email' in constr.ConstrName:
                print(f"  â Email capacity maxed. Expand or shift to other channels.")
            elif 'call' in constr.ConstrName:
                print(f"  â Call center at capacity. Hire more agents or use email.")
            elif 'high_risk' in constr.ConstrName:
                print(f"  â Min high-risk coverage met. Policy protects at-risk customers.")
    
    print(f"\nð§ª EXPERIMENT RECOMMENDATION")
    print("-"*80)
    np.random.seed(42)
    results_df['holdout'] = np.random.rand(len(results_df)) < 0.10
    print(f"Treated group: {(~results_df['holdout']).sum()} customers")
    print(f"Holdout group: {results_df['holdout'].sum()} customers (DO NOT TREAT)")
    print(f"\nWeekly measurement:")
    print(f"  1. Track churn rates: treated vs holdout")
    print(f"  2. Calculate actual uplift per action")
    print(f"  3. Update action catalog with real uplifts")
    print(f"  4. Re-run optimization weekly")
    
    model.dispose()
    env.dispose()

else:
    print(f"Optimization failed with status {model.status}")
    model.dispose()
    env.dispose()

print(f"\n" + "="*80)
print("NEXT STEPS FOR YOUR 75K DATASET")
print("="*80)
print(f"\nâ This demo shows the complete workflow with 300 customers")
print(f"â The model structure is production-ready for 75,001 customers")
print(f"\nð To scale to your full dataset:")
print(f"  1. Replace the simulated data with your actual churn probabilities")
print(f"  2. Use your real subscription types and CLV estimates")
print(f"  3. Define your actual action catalog with cost estimates")
print(f"  4. Set your operational constraints (budget, capacity)")
print(f"  5. Run optimization (Gurobi handles 75K+ efficiently)")
print(f"\nð¡ Formula: Model maximizes Î£ (p Ã u Ã v - c) for selected actions")
print(f"   where p=churn risk, u=uplift, v=CLV, c=cost")
