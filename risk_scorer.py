from typing import Dict, List, Tuple
import re

def calculate_risk_score(gst_data: Dict, bank_data: Dict, circular_flags: List) -> Dict:
    """
    Calculate comprehensive risk score
    """
    score = 70  # Base score
    flags = []
    
    # 1. GST Mismatch Check
    mismatch = gst_data.get('gst_mismatch_percent', 0)
    if mismatch > 0.20:
        score -= 15
        flags.append({
            'type': 'HIGH_GST_MISMATCH',
            'severity': 'HIGH',
            'message': f'GST 2A vs 3B mismatch of {mismatch:.1%} indicates possible revenue suppression',
            'impact': -15
        })
    elif mismatch > 0.10:
        score -= 5
        flags.append({
            'type': 'MEDIUM_GST_MISMATCH',
            'severity': 'MEDIUM',
            'message': f'GST mismatch of {mismatch:.1%} requires investigation',
            'impact': -5
        })
    
    # 2. Bank Balance Check
    avg_balance = bank_data.get('avg_balance', 0)
    turnover = gst_data.get('turnover', 0)
    
    if turnover > 0:
        balance_ratio = avg_balance / turnover
        if balance_ratio < 0.05:  # Less than 5% of turnover
            score -= 10
            flags.append({
                'type': 'LOW_BANK_BALANCE',
                'severity': 'HIGH',
                'message': f'Average bank balance ({avg_balance:,.0f}) is only {balance_ratio:.1%} of turnover',
                'impact': -10
            })
    
    # 3. Cash Flow Coverage
    inflows = bank_data.get('total_inflows', 0)
    outflows = bank_data.get('total_outflows', 0)
    
    if inflows > 0:
        coverage_ratio = outflows / inflows
        if coverage_ratio > 1.2:  # Spending more than coming in
            score -= 8
            flags.append({
                'type': 'NEGATIVE_CASH_FLOW',
                'severity': 'MEDIUM',
                'message': f'Outflows ({outflows:,.0f}) exceed inflows ({inflows:,.0f})',
                'impact': -8
            })
    
    # 4. Cheque Bounces
    bounces = bank_data.get('bounces', [])
    if len(bounces) > 0:
        bounce_penalty = min(len(bounces) * 5, 15)
        score -= bounce_penalty
        flags.append({
            'type': 'CHEQUE_BOUNCES',
            'severity': 'HIGH' if len(bounces) > 2 else 'MEDIUM',
            'message': f'{len(bounces)} cheque bounce(s) detected',
            'impact': -bounce_penalty
        })
    
    # 5. Circular Trading Flags
    for flag in circular_flags:
        score -= flag.get('impact', 10)
        flags.append(flag)
    
    # Ensure score stays within 0-100
    score = max(0, min(100, score))
    
    # Generate recommendation
    if score >= 70:
        recommendation = "APPROVE"
        explanation = "Strong financial health with minimal risk flags"
    elif score >= 50:
        recommendation = "APPROVE_WITH_CONDITIONS"
        explanation = "Acceptable risk with monitoring requirements"
    elif score >= 30:
        recommendation = "REDUCE_LIMIT"
        explanation = "Multiple risk factors suggest lower exposure"
    else:
        recommendation = "REJECT"
        explanation = "High risk profile exceeds tolerance"
    
    return {
        'score': score,
        'flags': flags,
        'recommendation': recommendation,
        'explanation': explanation
    }

def detect_circular_trading(gst_data: Dict, bank_data: Dict) -> List:
    """
    Detect potential circular trading patterns
    """
    flags = []
    
    # Get transaction data
    bank_transactions = bank_data.get('transactions', [])
    
    # Simple pattern: Look for round-trip amounts
    round_trip_candidates = {}
    
    for tx in bank_transactions:
        tx_str = ' '.join([str(x) for x in tx if x])
        
        # Look for amounts
        amounts = re.findall(r'[0-9,]+\.?[0-9]*', tx_str)
        if amounts:
            try:
                amount = float(amounts[-1].replace(',', ''))
                
                # Look for exact amounts appearing multiple times
                if amount in round_trip_candidates:
                    round_trip_candidates[amount] += 1
                else:
                    round_trip_candidates[amount] = 1
            except:
                pass
    
    # Flag amounts that appear frequently with different parties
    suspicious_threshold = 3
    for amount, frequency in round_trip_candidates.items():
        if frequency >= suspicious_threshold and amount >= 100000:  # ₹1L+
            
            # Check if it's a round number (common in circular trading)
            if amount % 100000 == 0 or amount % 50000 == 0:
                flags.append({
                    'type': 'CIRCULAR_TRADING',
                    'severity': 'HIGH',
                    'message': f'Amount ₹{amount:,.0f} appears {frequency} times - possible round-tripping',
                    'impact': -15
                })
    
    # Simple vendor loop detection (simplified for MVP)
    vendor_payments = {}
    
    for tx in bank_transactions[:20]:  # Check first 20 transactions
        tx_str = ' '.join([str(x) for x in tx if x])
        
        # Look for vendor names (simplified)
        words = tx_str.split()
        for i, word in enumerate(words):
            if any(x in word.upper() for x in ['PVT', 'LTD', 'LIMITED', 'ENTERPRISES']):
                vendor = word
                # Look for amount near vendor
                for j in range(max(0, i-3), min(len(words), i+3)):
                    if re.match(r'^[0-9,]+$', words[j].replace(',', '')):
                        try:
                            amount = float(words[j].replace(',', ''))
                            if vendor in vendor_payments:
                                vendor_payments[vendor].append(amount)
                            else:
                                vendor_payments[vendor] = [amount]
                        except:
                            pass
    
    # Check for payment cycles between same vendors
    for vendor, amounts in vendor_payments.items():
        if len(amounts) > 2:
            # Look for amounts that sum to each other (simplified circular detection)
            for i in range(len(amounts)):
                for j in range(i+1, len(amounts)):
                    if abs(amounts[i] - amounts[j]) < 1000:  # Nearly equal
                        flags.append({
                            'type': 'CIRCULAR_TRADING',
                            'severity': 'MEDIUM',
                            'message': f'Repeated payments to {vendor} of similar amounts suggests circular trading',
                            'impact': -10
                        })
                        break
    
    return flags