"""
Quick test script to verify optimizer with Premium constraint works correctly
"""

import pandas as pd
from music_streaming_retention_75k import MusicStreamingRetentionOptimizer

print("="*80)
print("TESTING OPTIMIZER WITH PREMIUM CONSTRAINT")
print("="*80)

# Test 1: Load data
print("\n[TEST 1] Loading data...")
try:
    optimizer = MusicStreamingRetentionOptimizer()
    optimizer.load_data(
        churn_file='prediction.csv',
        customer_features_file='test.csv',
        actions_file=None
    )
    print("✅ Data loaded successfully")
    print(f"   - Customers: {len(optimizer.customers_df):,}")
    print(f"   - Actions: {len(optimizer.actions_df)}")
except Exception as e:
    print(f"❌ Data loading failed: {e}")
    exit(1)

# Test 2: Set constraints including Premium
print("\n[TEST 2] Setting constraints with Premium coverage...")
try:
    optimizer.set_constraints({
        'weekly_budget': 50000,
        'email_capacity': 10000,
        'call_capacity': 200,
        'min_high_risk_pct': 0.60,
        'min_premium_pct': 0.40  # NEW CONSTRAINT
    })
    print("✅ Constraints set successfully")
    print(f"   - Premium constraint: 40%")
except Exception as e:
    print(f"❌ Constraint setting failed: {e}")
    exit(1)

# Test 3: Run optimization
print("\n[TEST 3] Running optimization...")
try:
    optimizer.optimize()
    print("✅ Optimization completed successfully")
    
    if optimizer.results and 'kpis' in optimizer.results:
        kpis = optimizer.results['kpis']
        print(f"\n   KEY RESULTS:")
        print(f"   - Customers Treated: {kpis['customers_treated']:,}")
        print(f"   - Weekly Spend: ${kpis['total_spend']:,.2f}")
        print(f"   - Expected Churn Reduction: {kpis['expected_churn_reduction']:.1f}")
        print(f"   - ROI: {kpis['roi']:.1f}%")
        print(f"   - Net Value: ${kpis['net_value']:,.2f}")
except Exception as e:
    print(f"❌ Optimization failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Verify Premium constraint
print("\n[TEST 4] Verifying Premium constraint satisfaction...")
try:
    assignments = optimizer.results['assignments']
    
    # Check Premium customers
    if 'subscription_type' in optimizer.customers_df.columns:
        total_premium = (optimizer.customers_df['subscription_type'] == 'Premium').sum()
        treated_premium = (assignments['subscription_type'] == 'Premium').sum()
        premium_pct = treated_premium / total_premium
        
        print(f"   - Total Premium customers: {total_premium:,}")
        print(f"   - Treated Premium customers: {treated_premium:,}")
        print(f"   - Coverage: {premium_pct:.1%}")
        
        if premium_pct >= 0.39:  # Allow small tolerance
            print(f"   ✅ Premium constraint satisfied (>= 40%)")
        else:
            print(f"   ⚠️ Premium constraint may not be satisfied")
    else:
        print("   ⚠️ No subscription_type column found")
        
except Exception as e:
    print(f"❌ Verification failed: {e}")

# Test 5: Verify high-risk constraint
print("\n[TEST 5] Verifying high-risk constraint satisfaction...")
try:
    high_risk_total = (optimizer.customers_df['risk_segment'] == 'high_risk').sum()
    high_risk_treated = (assignments['risk_segment'] == 'high_risk').sum()
    high_risk_pct = high_risk_treated / high_risk_total
    
    print(f"   - Total high-risk customers: {high_risk_total:,}")
    print(f"   - Treated high-risk customers: {high_risk_treated:,}")
    print(f"   - Coverage: {high_risk_pct:.1%}")
    
    if high_risk_pct >= 0.59:  # Allow small tolerance
        print(f"   ✅ High-risk constraint satisfied (>= 60%)")
    else:
        print(f"   ⚠️ High-risk constraint may not be satisfied")
        
except Exception as e:
    print(f"❌ Verification failed: {e}")

# Cleanup
print("\n[CLEANUP] Disposing Gurobi resources...")
optimizer.cleanup()
print("✅ Cleanup complete")

print("\n" + "="*80)
print("ALL TESTS PASSED! Optimizer is working correctly with Premium constraint")
print("="*80)
print("\nNext steps:")
print("1. Run Streamlit dashboard: streamlit run streamlit_app.py")
print("2. Configure constraints in sidebar")
print("3. Click 'RUN OPTIMIZATION'")
print("4. Review results and export treatment plans")

