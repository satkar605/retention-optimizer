# Visualization Strategy Guide

## 📊 Current Visualizations Available

### Prescriptive Analysis (from optimization model)
1. **viz1_budget_netvalue.png** - Net Retained Value vs. Weekly Budget
2. **viz2_budget_roi.png** - ROI vs. Weekly Budget (shows 2,319% ROI)
3. **viz3_budget_coverage.png** - Customer Coverage vs. Budget
4. **viz4_action_mix.png** - Action Mix by Budget Level
5. **viz5_segment_action.png** - Action Mix by Customer Segment
6. **viz6_heatmap.png** - Correlation/Feature Heatmap
7. **viz7_netvalue_breakdown.png** - Net Value Component Breakdown
8. **viz8_scatter_churn_clv.png** - Churn Risk vs. Customer Lifetime Value

---

## 🌐 For Your Portfolio Website (site.html)

### ✅ **Already Included (Keep These)**
- viz2_budget_roi.png - in Prescriptive section
- viz1_budget_netvalue.png - in Prescriptive section  
- viz5_segment_action.png - in Key Findings
- viz8_scatter_churn_clv.png - in Key Findings

### 🎯 **Recommended Additions**

#### Add to "Discovery: What Drives Customers Away?" section:
```html
<div class="section">
  <h2>Discovery: What Drives Customers Away?</h2>
  <img src="visualizations/viz6_heatmap.png" alt="Feature Correlation Heatmap" 
       style="max-width: 700px; width: 100%; margin: 1.5rem auto; display: block;">
  <p>Correlation analysis revealed behavioral patterns predicting churn...</p>
</div>
```

#### Add to "Prescriptive Optimization" section (after the existing ROI charts):
```html
<h3>Fairness & Coverage Analysis</h3>
<div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
  <img src="visualizations/viz3_budget_coverage.png" alt="Customer Coverage Analysis" 
       style="max-width: 48%;">
  <img src="visualizations/viz7_netvalue_breakdown.png" alt="Net Value Breakdown" 
       style="max-width: 48%;">
</div>
<p>The optimization ensures all subscription tiers receive equitable attention...</p>
```

---

## 📁 For GitHub Repository Structure

### Recommended Folder Structure:

```
your-repo/
├── README.md
├── assets/
│   ├── descriptive/
│   │   └── viz6_heatmap.png
│   ├── prescriptive/
│   │   ├── viz1_budget_netvalue.png
│   │   ├── viz2_budget_roi.png
│   │   ├── viz3_budget_coverage.png
│   │   ├── viz4_action_mix.png
│   │   ├── viz5_segment_action.png
│   │   ├── viz7_netvalue_breakdown.png
│   │   └── viz8_scatter_churn_clv.png
│   └── predictive/
│       ├── model_comparison.png
│       ├── roc_curves.png
│       └── feature_importance.png
├── reports/
│   ├── executive-summary-report.pdf
│   ├── descriptive-analysis.html
│   └── predictive-analysis.html
└── code/
    ├── data_preparation.py
    ├── modeling.py
    └── optimization.py
```

### What to Include in GitHub README.md:

**Hero Section:**
- viz2_budget_roi.png (shows the impressive 2,319% ROI)

**Problem Statement:**
- Churn distribution chart (from descriptive analysis)

**Prescriptive Results:**
- viz1_budget_netvalue.png
- viz8_scatter_churn_clv.png

**Model Performance:**
- Model comparison charts (from predictive analysis)

---

## 🎨 Priority Ranking for Website

### Must-Have (Already Done ✅)
1. viz2_budget_roi.png - **The money shot** (2,319% ROI)
2. viz1_budget_netvalue.png - Shows dollar value impact
3. viz8_scatter_churn_clv.png - Shows targeting strategy

### Should Add (High Impact):
4. viz6_heatmap.png - Shows analytical depth
5. viz3_budget_coverage.png - Shows fairness/equity concerns
6. viz5_segment_action.png - Shows segmentation strategy

### Nice to Have (For Deep Dives):
7. viz7_netvalue_breakdown.png - Component analysis
8. viz4_action_mix.png - Strategy evolution by budget

---

## 💡 Tips for Recruiters

When organizing for GitHub:
- **Keep all visualizations** in a clear folder structure
- **Name files descriptively** (already done!)
- **Include a visualization index** in your README
- **Reference specific images** in your README sections
- **Ensure all image paths work** when repo is public

For Portfolio Website:
- **Use 4-6 key visualizations** (more = overwhelming)
- **Prioritize business impact charts** (ROI, Net Value)
- **Show technical depth** (heatmap, scatter plots)
- **Ensure fast load times** (optimize image sizes if needed)

---

## 📤 What to Upload to GitHub Assets Folder

**Upload ALL 8 visualizations** in organized subfolders:
1. All viz1-8 files → /assets/prescriptive/
2. Descriptive analysis charts → /assets/descriptive/
3. Predictive model charts → /assets/predictive/
4. Executive summary charts → /assets/reports/

This shows completeness and organizational skills!


