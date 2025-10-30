"""
Music Streaming Churn Retention Optimization
Production-ready model for 75,001 customers

Maximizes: Expected Retained CLV - Cost
Formula: Î£ (p_i Ã u_k Ã v_i - c_k) for selected customer-action pairs

Author: Gurobot - Gurobi Optimization
Date: 2025
"""

import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
from typing import Dict, Optional

class MusicStreamingRetentionOptimizer:
    """
    Prescriptive weekly retention planning for music streaming service.
    
    Optimizes customer treatment selection to maximize expected retained CLV
    while respecting budget, capacity, and policy constraints.
    """
    
    def __init__(self):
        self.customers_df = None
        self.actions_df = None
        self.constraints = None
        self.model = None
        self.env = None
        self.results = {}
        
    def load_data(
        self,
        churn_file: str,
        customer_features_file: Optional[str] = None,
        actions_file: Optional[str] = None
    ):
        """
        Load customer data and prepare for optimization.
        
        Args:
            churn_file: CSV with customer_id, churn_probability
            customer_features_file: Optional CSV with subscription_type, etc.
            actions_file: Optional CSV defining retention actions
        """
        print("="*80)
        print("DATA LOADING & PREPARATION")
        print("="*80)
        
        # Load churn probabilities
        self.customers_df = pd.read_csv(churn_file)
        required_cols = ['customer_id', 'churn_probability']
        if not all(col in self.customers_df.columns for col in required_cols):
            raise ValueError(f"Churn file must contain: {required_cols}")
        
        print(f"\nâ Loaded {len(self.customers_df):,} customers")
        
        # Rename for internal consistency
        self.customers_df.rename(columns={'churn_probability': 'p'}, inplace=True)
        
        # Load or estimate customer features
        if customer_features_file:
            features = pd.read_csv(customer_features_file)
            self.customers_df = self.customers_df.merge(features, on='customer_id', how='left')
        
        # Estimate CLV if not provided
        if 'v' not in self.customers_df.columns:
            self._estimate_clv()
        
        # Create segments
        self._create_segments()
        
        # Load or create action catalog
        if actions_file:
            self.actions_df = pd.read_csv(actions_file)
        else:
            self._create_default_actions()
        
        print(f"\nâ Ready: {len(self.customers_df):,} customers, {len(self.actions_df)} actions")
        print(f"  Total at-risk value: ${(self.customers_df['p'] * self.customers_df['v']).sum():,.0f}")
        
    def _estimate_clv(self):
        """Estimate CLV based on subscription type and engagement."""
        print(f"\nâï¸ Estimating CLV (no 'v' column provided)...")
        
        # Base annual revenue by subscription type
        subscription_value = {
            'Free': 100,      # Ad revenue estimate
            'Student': 120,   # ~$5/month discounted
            'Premium': 240,   # ~$10/month
            'Family': 360     # ~$15/month
        }
        
        payment_multiplier = {
            'Monthly': 1.0,
            'Yearly': 1.3     # 30% bonus for annual commitment
        }
        
        if 'subscription_type' in self.customers_df.columns:
            self.customers_df['base_value'] = self.customers_df['subscription_type'].map(
                subscription_value
            ).fillna(150)
        else:
            # If no subscription type, use average
            self.customers_df['base_value'] = 200
        
        if 'payment_plan' in self.customers_df.columns:
            self.customers_df['payment_mult'] = self.customers_df['payment_plan'].map(
                payment_multiplier
            ).fillna(1.0)
        else:
            self.customers_df['payment_mult'] = 1.0
        
        # Engagement multiplier (if features available)
        if 'weekly_hours' in self.customers_df.columns:
            self.customers_df['engagement_score'] = (
                (self.customers_df['weekly_hours'] / self.customers_df['weekly_hours'].max()) * 0.5 +
                (self.customers_df['weekly_songs_played'] / self.customers_df['weekly_songs_played'].max()) * 0.5
            )
        else:
            self.customers_df['engagement_score'] = 0.5  # Assume average
        
        # 2-year CLV estimate
        self.customers_df['v'] = (
            self.customers_df['base_value'] * 
            self.customers_df['payment_mult'] * 
            (1 + self.customers_df['engagement_score']) * 
            2  # 2-year horizon
        )
        
        print(f"  CLV range: ${self.customers_df['v'].min():.0f} - ${self.customers_df['v'].max():.0f}")
        print(f"  â ï¸ CLV estimates are proxies. Refine with actual customer economics!")
        
    def _create_segments(self):
        """Create risk and value segments."""
        self.customers_df['risk_segment'] = pd.cut(
            self.customers_df['p'],
            bins=[0, 0.3, 0.7, 1.0],
            labels=['low_risk', 'medium_risk', 'high_risk']
        )
        
        self.customers_df['value_segment'] = pd.cut(
            self.customers_df['v'],
            bins=[0, 150, 300, 1000],
            labels=['low_value', 'medium_value', 'high_value']
        )
        
        self.customers_df['is_high_value'] = self.customers_df['value_segment'] == 'high_value'
        
    def _create_default_actions(self):
        """Create default retention action catalog for music streaming."""
        print(f"\nâï¸ Creating default action catalog...")
        
        self.actions_df = pd.DataFrame([
            {
                'action_id': 0,
                'action_name': 'No Action',
                'channel': 'none',
                'cost': 0,
                'uplift': 0.00,
                'eligible_segment': 'all',
                'description': 'Do nothing'
            },
            {
                'action_id': 1,
                'action_name': 'Personalized Email',
                'channel': 'email',
                'cost': 2,
                'uplift': 0.08,
                'eligible_segment': 'all',
                'description': 'Automated email with playlist recommendations'
            },
            {
                'action_id': 2,
                'action_name': '20% Discount Offer',
                'channel': 'email',
                'cost': 20,
                'uplift': 0.15,
                'eligible_segment': 'all',
                'description': '1-month discount for paid tiers'
            },
            {
                'action_id': 3,
                'action_name': 'Premium Trial (Free users)',
                'channel': 'in_app',
                'cost': 10,
                'uplift': 0.25,
                'eligible_segment': 'Free',
                'description': '30-day free Premium trial'
            },
            {
                'action_id': 4,
                'action_name': 'Family Plan Upgrade',
                'channel': 'email',
                'cost': 15,
                'uplift': 0.18,
                'eligible_segment': 'Premium',
                'description': 'Discounted Family plan upgrade'
            },
            {
                'action_id': 5,
                'action_name': 'Retention Specialist Call',
                'channel': 'call',
                'cost': 50,
                'uplift': 0.30,
                'eligible_segment': 'high_value',
                'description': 'Personal outreach from retention team'
            },
            {
                'action_id': 6,
                'action_name': 'VIP Concierge Service',
                'channel': 'call',
                'cost': 100,
                'uplift': 0.40,
                'eligible_segment': 'high_value',
                'description': 'Dedicated account manager + exclusive perks'
            },
            {
                'action_id': 7,
                'action_name': 'Win-Back Email Series',
                'channel': 'email',
                'cost': 30,
                'uplift': 0.22,
                'eligible_segment': 'all',
                'description': 'Multi-touch campaign with special offers'
            }
        ])
        
        print(f"  â ï¸ CRITICAL: Uplift values are ESTIMATES!")
        print(f"     You MUST run A/B tests to measure actual treatment effects!")
        
    def set_constraints(self, constraints_dict: Dict):
        """
        Set operational constraints.
        
        Args:
            constraints_dict: Dictionary with keys:
                - weekly_budget: Total retention budget per week
                - email_capacity: Max emails per week
                - call_capacity: Max calls per week
                - min_high_risk_pct: Min % of high-risk to treat (0-1)
        """
        self.constraints = constraints_dict
        print(f"\nð¯ Operational Constraints Set:")
        for key, value in constraints_dict.items():
            print(f"  {key}: {value}")
        
    def optimize(self):
        """Build and solve the optimization model."""
        print(f"\n" + "="*80)
        print("GUROBI OPTIMIZATION MODEL")
        print("="*80)
        
        # Create environment
        self.env = gp.Env()
        self.model = gp.Model("MusicStreamingRetention", env=self.env)
        
        # Build eligibility matrix
        print(f"\nâï¸ Building eligibility matrix...")
        eligible = []
        
        for _, cust in self.customers_df.iterrows():
            i = cust['customer_id']
            p, v = cust['p'], cust['v']
            
            # Get customer attributes for eligibility checking
            sub_type = cust.get('subscription_type', 'Unknown')
            is_high_value = cust['is_high_value']
            
            for _, action in self.actions_df.iterrows():
                k = action['action_id']
                cost = action['cost']
                uplift = action['uplift']
                elig = action['eligible_segment']
                
                # Check eligibility
                if elig == 'all':
                    pass
                elif elig == 'Free' and sub_type != 'Free':
                    continue
                elif elig == 'Premium' and sub_type != 'Premium':
                    continue
                elif elig == 'high_value' and not is_high_value:
                    continue
                
                # Expected value = p Ã u Ã v - c
                expected_value = p * uplift * v - cost
                eligible.append((i, k, cost, expected_value))
        
        print(f"â {len(eligible):,} eligible customer-action pairs")
        
        # Decision variables: x[i,k] = 1 if customer i gets action k
        x = self.model.addVars(
            [(e[0], e[1]) for e in eligible],
            vtype=GRB.BINARY,
            name="assign"
        )
        
        # Objective: Maximize expected net value
        print(f"âï¸ Setting objective: max Î£ (p Ã u Ã v - c)")
        self.model.setObjective(
            gp.quicksum(e[3] * x[e[0], e[1]] for e in eligible),
            GRB.MAXIMIZE
        )
        
        # Constraints
        print(f"âï¸ Adding constraints...")
        
        # One action per customer
        for i in self.customers_df['customer_id']:
            eligible_for_i = [e for e in eligible if e[0] == i]
            self.model.addConstr(
                gp.quicksum(x[e[0], e[1]] for e in eligible_for_i) <= 1,
                name=f"one_action_{i}"
            )
        
        # Budget constraint
        self.model.addConstr(
            gp.quicksum(e[2] * x[e[0], e[1]] for e in eligible) <= self.constraints['weekly_budget'],
            name="budget"
        )
        
        # Email capacity
        if 'email_capacity' in self.constraints:
            email_actions = set(self.actions_df[self.actions_df['channel'] == 'email']['action_id'])
            email_pairs = [e for e in eligible if e[1] in email_actions]
            self.model.addConstr(
                gp.quicksum(x[e[0], e[1]] for e in email_pairs) <= self.constraints['email_capacity'],
                name="email_capacity"
            )
        
        # Call capacity
        if 'call_capacity' in self.constraints:
            call_actions = set(self.actions_df[self.actions_df['channel'] == 'call']['action_id'])
            call_pairs = [e for e in eligible if e[1] in call_actions]
            self.model.addConstr(
                gp.quicksum(x[e[0], e[1]] for e in call_pairs) <= self.constraints['call_capacity'],
                name="call_capacity"
            )
        
        # Minimum high-risk coverage
        if 'min_high_risk_pct' in self.constraints:
            high_risk_ids = set(
                self.customers_df[self.customers_df['risk_segment'] == 'high_risk']['customer_id']
            )
            if high_risk_ids:
                min_treat = int(self.constraints['min_high_risk_pct'] * len(high_risk_ids))
                high_risk_pairs = [e for e in eligible if e[0] in high_risk_ids and e[1] > 0]
                self.model.addConstr(
                    gp.quicksum(x[e[0], e[1]] for e in high_risk_pairs) >= min_treat,
                    name="min_high_risk"
                )
        
        # Minimum Premium customer coverage (policy constraint)
        if 'min_premium_pct' in self.constraints and self.constraints['min_premium_pct'] > 0:
            if 'subscription_type' in self.customers_df.columns:
                premium_ids = set(
                    self.customers_df[self.customers_df['subscription_type'] == 'Premium']['customer_id']
                )
                if premium_ids:
                    min_premium_treat = int(self.constraints['min_premium_pct'] * len(premium_ids))
                    premium_pairs = [e for e in eligible if e[0] in premium_ids and e[1] > 0]
                    if premium_pairs:
                        self.model.addConstr(
                            gp.quicksum(x[e[0], e[1]] for e in premium_pairs) >= min_premium_treat,
                            name="min_premium"
                        )
        
        print(f"\nð Solving...\n")
        self.model.optimize()
        
        if self.model.status == GRB.OPTIMAL:
            print(f"\nâ OPTIMAL SOLUTION FOUND")
            print(f"  Expected Net Value: ${self.model.objVal:,.2f}\n")
            self._extract_solution(eligible, x)
        else:
            print(f"\nâ Optimization failed with status: {self.model.status}")
            
    def _extract_solution(self, eligible, x):
        """Extract solution into results dataframe."""
        assignments = []
        
        for e in eligible:
            i, k, cost, exp_val = e
            if x[i, k].X > 0.5:
                cust = self.customers_df[self.customers_df['customer_id'] == i].iloc[0]
                action = self.actions_df[self.actions_df['action_id'] == k].iloc[0]
                
                retained = cust['p'] * action['uplift'] * cust['v']
                
                assignments.append({
                    'customer_id': i,
                    'subscription_type': cust.get('subscription_type', 'Unknown'),
                    'risk_segment': cust['risk_segment'],
                    'value_segment': cust['value_segment'],
                    'churn_prob': cust['p'],
                    'clv': cust['v'],
                    'action_id': k,
                    'action_name': action['action_name'],
                    'channel': action['channel'],
                    'cost': cost,
                    'uplift': action['uplift'],
                    'expected_retained_clv': retained,
                    'net_value': retained - cost
                })
        
        self.results['assignments'] = pd.DataFrame(assignments)
        
        # Calculate KPIs
        if len(assignments) > 0:
            total_spend = sum(a['cost'] for a in assignments)
            total_retained = sum(a['expected_retained_clv'] for a in assignments)
            churn_reduction = sum(a['churn_prob'] * a['uplift'] for a in assignments)
            
            self.results['kpis'] = {
                'customers_treated': len(assignments),
                'total_spend': total_spend,
                'expected_retained_clv': total_retained,
                'expected_churn_reduction': churn_reduction,
                'net_value': total_retained - total_spend,
                'roi': (total_retained / total_spend - 1) * 100 if total_spend > 0 else 0
            }
    
    def generate_report(self):
        """Generate comprehensive business report."""
        print("="*80)
        print("RETENTION PLAN RESULTS")
        print("="*80)
        
        if 'kpis' not in self.results:
            print("No solution available. Run optimize() first.")
            return
        
        kpis = self.results['kpis']
        
        print(f"\nð KEY PERFORMANCE INDICATORS")
        print("-"*80)
        print(f"Customers Treated:           {kpis['customers_treated']:,}")
        print(f"Total Weekly Spend:          ${kpis['total_spend']:,.2f}")
        print(f"Expected Churn Reduction:    {kpis['expected_churn_reduction']:.1f} customers")
        print(f"Expected Retained CLV:       ${kpis['expected_retained_clv']:,.2f}")
        print(f"Net Value (CLV - Cost):      ${kpis['net_value']:,.2f}")
        print(f"ROI:                         {kpis['roi']:.1f}%")
        
        if len(self.results['assignments']) > 0:
            print(f"\nð TREATMENT PLAN BY ACTION")
            print("-"*80)
            action_summary = self.results['assignments'].groupby('action_name').agg({
                'customer_id': 'count',
                'cost': 'sum',
                'expected_retained_clv': 'sum',
                'net_value': 'sum'
            }).reset_index()
            action_summary.columns = ['Action', 'Customers', 'Cost', 'Retained CLV', 'Net Value']
            action_summary = action_summary.sort_values('Net Value', ascending=False)
            print(action_summary.to_string(index=False))
            
            print(f"\nð¯ TREATMENT BY SEGMENT")
            print("-"*80)
            segment_summary = self.results['assignments'].groupby(['risk_segment', 'value_segment'], observed=True).agg({
                'customer_id': 'count',
                'expected_retained_clv': 'sum',
                'cost': 'sum',
                'net_value': 'sum'
            }).reset_index()
            segment_summary.columns = ['Risk', 'Value', 'Count', 'Retained CLV', 'Cost', 'Net Value']
            print(segment_summary.to_string(index=False))
            
            print(f"\nð TOP 20 HIGHEST IMPACT CUSTOMERS")
            print("-"*80)
            top20 = self.results['assignments'].nlargest(20, 'net_value')[
                ['customer_id', 'subscription_type', 'churn_prob', 'clv',
                 'action_name', 'cost', 'expected_retained_clv', 'net_value']
            ]
            print(top20.to_string(index=False))
        
        print(f"\nð CONSTRAINT STATUS")
        print("-"*80)
        binding = []
        for constr in self.model.getConstrs():
            if abs(constr.Slack) < 0.01 and 'one_action' not in constr.ConstrName:
                binding.append(constr.ConstrName)
                print(f"â¢ {constr.ConstrName}: BINDING")
                print(f"  â {self._explain_constraint(constr.ConstrName)}")
        
        if not binding:
            print("No binding constraints (budget/capacity not fully used)")
        
        print(f"\nð§ª EXPERIMENT RECOMMENDATION")
        print("-"*80)
        print("1. Implement 10% random holdout per action")
        print("2. Track treated vs. control churn rates weekly")
        print("3. Calculate actual uplift after 4 weeks")
        print("4. Update action catalog with calibrated uplifts")
        print("5. Re-run optimization weekly with fresh churn scores")
        
    def _explain_constraint(self, name: str) -> str:
        """Explain binding constraints in business terms."""
        if 'budget' in name.lower():
            return "Budget fully utilized. Increase budget to enable more treatments."
        elif 'call' in name.lower():
            return "Call center at capacity. Expand agent hours or shift to email/in-app."
        elif 'email' in name.lower():
            return "Email capacity maxed. Increase send limit or prioritize higher-uplift actions."
        elif 'high_risk' in name.lower():
            return "Minimum high-risk coverage requirement met. Policy ensures vulnerable customers are protected."
        return "Fully utilized."
    
    def export_treatment_list(self, filename: str = 'treatment_list.csv'):
        """Export treatment list with holdout assignments."""
        if 'assignments' not in self.results:
            print("No solution available. Run optimize() first.")
            return
        
        export_df = self.results['assignments'].copy()
        
        # Add 10% holdout per action
        np.random.seed(42)
        export_df['holdout'] = np.random.rand(len(export_df)) < 0.10
        export_df['execute_treatment'] = ~export_df['holdout']
        
        export_df.to_csv(filename, index=False)
        
        print(f"\nð¤ Treatment list exported to: {filename}")
        print(f"   Total customers: {len(export_df):,}")
        print(f"   Treated: {export_df['execute_treatment'].sum():,}")
        print(f"   Holdout: {export_df['holdout'].sum():,}")
        print(f"\nâ ï¸ DO NOT TREAT the holdout group - needed for uplift measurement!")
        
    def cleanup(self):
        """Dispose Gurobi resources."""
        if self.model:
            self.model.dispose()
        if self.env:
            self.env.dispose()


# ============================================================================
# USAGE EXAMPLE FOR 75K CUSTOMERS
# ============================================================================

if __name__ == "__main__":
    
    print("""
    ============================================================================
    MUSIC STREAMING RETENTION OPTIMIZATION
    Production Model for 75,001 Customers
    ============================================================================
    
    This script optimizes weekly retention campaigns by selecting the best
    action for each customer to maximize:
    
        Expected Retained CLV - Cost = Î£ (p Ã u Ã v - c)
    
    where:
        p = churn probability (from your ML model)
        u = uplift (% reduction in churn from action)
        v = customer lifetime value (2-year proxy)
        c = cost of action
    
    ============================================================================
    """)
    
    # Initialize optimizer
    optimizer = MusicStreamingRetentionOptimizer()
    
    # Load your data
    # REPLACE with your actual file paths
    optimizer.load_data(
        churn_file='churn_probabilities_75k.csv',  # Must have: customer_id, churn_probability
        customer_features_file='customer_features.csv',  # Optional: subscription_type, payment_plan, etc.
        actions_file=None  # Optional: Or use default actions
    )
    
    # Set operational constraints
    optimizer.set_constraints({
        'weekly_budget': 150000,      # $150K weekly retention budget
        'email_capacity': 30000,      # Can send 30K emails per week
        'call_capacity': 500,         # 500 agent calls per week
        'min_high_risk_pct': 0.60     # Treat at least 60% of high-risk customers
    })
    
    # Run optimization
    optimizer.optimize()
    
    # Generate business report
    optimizer.generate_report()
    
    # Export treatment list for execution
    optimizer.export_treatment_list('weekly_treatment_plan.csv')
    
    # Cleanup
    optimizer.cleanup()
    
    print("""
    ============================================================================
    â OPTIMIZATION COMPLETE
    ============================================================================
    
    Next Steps:
    1. Upload 'weekly_treatment_plan.csv' to your CRM/marketing automation
    2. Execute treatments where execute_treatment=True
    3. Track holdout group separately (DO NOT TREAT)
    4. After 4 weeks, measure churn rates: treated vs. holdout
    5. Update action catalog with actual uplifts
    6. Re-run this script weekly with fresh churn probabilities
    
    Key Formula: Model maximizes p Ã u Ã v - c for each customer
    
    Questions? Contact your Gurobi representative or support@gurobi.com
    ============================================================================
    """)
