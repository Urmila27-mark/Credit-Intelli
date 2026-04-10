from typing import Dict, List
from datetime import datetime
import json

def generate_cam(gst_data: Dict, bank_data: Dict, risk_result: Dict, circular_flags: List) -> str:
    """
    Generate Credit Appraisal Memo summary
    """
    company_name = gst_data.get('company_name', 'Unknown Company')
    risk_score = risk_result.get('score', 0)
    recommendation = risk_result.get('recommendation', 'REVIEW')
    
    # Calculate loan eligibility (simplified)
    turnover = gst_data.get('turnover', 0)
    eligible_limit = turnover * 0.25  # 25% of turnover as working capital
    
    # Adjust based on risk
    if risk_score < 30:
        eligible_limit = 0  # Reject
    elif risk_score < 50:
        eligible_limit *= 0.5  # 50% of eligible
    elif risk_score < 70:
        eligible_limit *= 0.75  # 75% of eligible
    
    # Calculate interest rate
    base_rate = 10.0  # Base rate 10%
    if risk_score >= 80:
        premium = 0.5  # Low risk: +0.5%
    elif risk_score >= 60:
        premium = 2.0  # Medium risk: +2%
    elif risk_score >= 40:
        premium = 4.0  # High risk: +4%
    else:
        premium = 10.0  # Very high risk: +10% (effectively reject)
    
    interest_rate = base_rate + premium
    
    # Generate CAM text
    cam = f"""
CREDIT APPRAISAL MEMO
======================
Generated: {datetime.now().strftime('%d-%b-%Y %H:%M')}

1. EXECUTIVE SUMMARY
-------------------
Borrower: {company_name}
Risk Score: {risk_score}/100
Recommendation: {recommendation}
Proposed Limit: ₹{eligible_limit:,.0f}
Interest Rate: {interest_rate:.1f}% p.a.

2. FINANCIAL HIGHLIGHTS
----------------------
• Annual Turnover: ₹{gst_data.get('turnover', 0):,.0f}
• Average Bank Balance: ₹{bank_data.get('avg_balance', 0):,.0f}
• GST Compliance: {'✅ Good' if gst_data.get('gst_mismatch_percent', 1) < 0.1 else '⚠️ Needs Review'}
• Cash Flow Pattern: {'✅ Stable' if bank_data.get('total_inflows', 0) > bank_data.get('total_outflows', 0) else '⚠️ Negative'}

3. KEY RISK FACTORS
-------------------
"""
    
    # Add risk flags
    for flag in risk_result.get('flags', []):
        cam += f"• {flag['severity']}: {flag['message']}\n"
    
    cam += """
4. FIVE Cs ANALYSIS
------------------
Character: """
    
    # Character assessment
    if len(bank_data.get('bounces', [])) > 0:
        cam += "⚠️ Concern due to cheque bounces"
    else:
        cam += "✅ No adverse behavior"
    
    cam += """
Capacity: """
    if risk_score > 60:
        cam += "✅ Strong repayment capacity"
    elif risk_score > 40:
        cam += "⚠️ Adequate but monitored"
    else:
        cam += "❌ Weak repayment capacity"
    
    cam += """
Capital: """
    if turnover > 10000000:  # >1Cr
        cam += "✅ Strong capital base"
    else:
        cam += "⚠️ Limited capital"
    
    cam += """
Collateral: Not assessed in this analysis
Conditions: """
    if 'regulatory' in str(risk_result).lower():
        cam += "⚠️ Sectoral concerns"
    else:
        cam += "✅ Favorable conditions"

    cam += f"""

5. EXPLANATION & RECOMMENDATION
------------------------------
{risk_result.get('explanation', 'Analysis complete.')}

Based on the above assessment, we recommend:
{recommendation.replace('_', ' ')} with {'no' if eligible_limit > 0 else ''} sanction of ₹{eligible_limit:,.0f} at {interest_rate:.1f}% p.a.

6. KEY DECISION DRIVERS
----------------------
"""
    
    # Add top 3 decision drivers
    drivers = []
    if gst_data.get('gst_mismatch_percent', 0) > 0.1:
        drivers.append(f"GST mismatch of {gst_data['gst_mismatch_percent']:.1%}")
    
    if len(circular_flags) > 0:
        drivers.append(f"Circular trading indicators ({len(circular_flags)} flags)")
    
    if len(bank_data.get('bounces', [])) > 0:
        drivers.append(f"Cheque bounces ({len(bank_data['bounces'])} incidents)")
    
    if len(drivers) == 0:
        drivers.append("Strong financial metrics")
        drivers.append("Clean banking history")
        drivers.append("Good GST compliance")
    
    for i, driver in enumerate(drivers[:3], 1):
        cam += f"{i}. {driver}\n"
    
    return cam