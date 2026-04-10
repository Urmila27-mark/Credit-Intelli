import pdfplumber
import re
from typing import Dict, List, Optional
import PyPDF2

def extract_gst_data(pdf_path: str) -> Dict:
    """
    Extract key information from GST return PDF
    """
    text = ""
    
    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:3]:  # Check first 3 pages
            text += page.extract_text() or ""
    
    # Dictionary to store extracted data
    gst_data = {
        "company_name": extract_company_name(text),
        "gstin": extract_gstin(text),
        "turnover": extract_turnover(text),
        "gst_liability": extract_gst_liability(text),
        "input_tax_credit": extract_itc(text),
        "gstr_2a_total": extract_gstr_2a(text),
        "gstr_3b_total": extract_gstr_3b(text),
        "month": extract_month(text),
    }
    
    # Calculate mismatch
    if gst_data["gstr_2a_total"] and gst_data["gstr_3b_total"]:
        mismatch = abs(gst_data["gstr_2a_total"] - gst_data["gstr_3b_total"])
        if gst_data["gstr_3b_total"] > 0:
            gst_data["gst_mismatch_percent"] = mismatch / gst_data["gstr_3b_total"]
        else:
            gst_data["gst_mismatch_percent"] = 0
    else:
        gst_data["gst_mismatch_percent"] = 0
    
    return gst_data

def extract_bank_data(pdf_path: str) -> Dict:
    """
    Extract key information from Bank Statement PDF
    """
    transactions = []
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            
            # Extract tables if present
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and len(row) >= 3:
                        # Try to identify transaction rows
                        if any(x for x in row if x and ('₹' in x or 'Rs' in x)):
                            transactions.append(row)
    
    # Calculate bank metrics
    bank_data = {
        "account_number": extract_account_number(text),
        "avg_balance": calculate_avg_balance(transactions),
        "total_inflows": calculate_total_inflows(transactions),
        "total_outflows": calculate_total_outflows(transactions),
        "bounces": detect_bounces(text),
        "transactions": transactions[:10]  # Store first 10 for analysis
    }
    
    return bank_data

def extract_company_name(text: str) -> Optional[str]:
    """Extract company name using patterns"""
    patterns = [
        r"Name of Business\s*[:\-]\s*([A-Za-z\s]+)",
        r"Trade Name\s*[:\-]\s*([A-Za-z\s]+)",
        r"Legal Name\s*[:\-]\s*([A-Za-z\s]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

def extract_gstin(text: str) -> Optional[str]:
    """Extract GSTIN (15 characters: 2 state + 10 PAN + 1 entity + 1 check + 1 digit)"""
    pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_turnover(text: str) -> float:
    """Extract total turnover"""
    patterns = [
        r'Total Turnover\s*[:\-]?\s*[₹Rs.]?\s*([0-9,]+)',
        r'Gross Turnover\s*[:\-]?\s*[₹Rs.]?\s*([0-9,]+)',
        r'Turnover\s*[:\-]?\s*[₹Rs.]?\s*([0-9,]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Remove commas and convert to float
            return float(match.group(1).replace(',', ''))
    return 0.0

def extract_gst_liability(text: str) -> float:
    """Extract total GST liability"""
    pattern = r'Total Tax Liability\s*[:\-]?\s*[₹Rs.]?\s*([0-9,]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else 0.0

def extract_itc(text: str) -> float:
    """Extract Input Tax Credit"""
    pattern = r'Input Tax Credit.*?[₹Rs.]?\s*([0-9,]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else 0.0

def extract_gstr_2a(text: str) -> float:
    """Extract GSTR-2A total"""
    pattern = r'GSTR-2A.*?[₹Rs.]?\s*([0-9,]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else 0.0

def extract_gstr_3b(text: str) -> float:
    """Extract GSTR-3B total"""
    pattern = r'GSTR-3B.*?[₹Rs.]?\s*([0-9,]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else 0.0

def extract_month(text: str) -> Optional[str]:
    """Extract return month"""
    pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+20[0-9]{2}'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_account_number(text: str) -> Optional[str]:
    """Extract bank account number"""
    pattern = r'A[/]c No[.:]\s*([0-9]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

def calculate_avg_balance(transactions: List) -> float:
    """Simple average balance calculation"""
    if not transactions:
        return 0.0
    
    balances = []
    for row in transactions:
        for cell in row:
            if cell and 'Balance' in str(cell):
                # Extract balance amount
                numbers = re.findall(r'[0-9,]+\.?[0-9]*', str(cell))
                if numbers:
                    try:
                        balances.append(float(numbers[-1].replace(',', '')))
                    except:
                        pass
    
    return sum(balances) / len(balances) if balances else 0.0

def calculate_total_inflows(transactions: List) -> float:
    """Calculate total credits"""
    total = 0.0
    for row in transactions:
        row_str = str(row).upper()
        if 'CR' in row_str or 'DEPOSIT' in row_str:
            numbers = re.findall(r'[0-9,]+\.?[0-9]*', row_str)
            if numbers:
                try:
                    total += float(numbers[-1].replace(',', ''))
                except:
                    pass
    return total

def calculate_total_outflows(transactions: List) -> float:
    """Calculate total debits"""
    total = 0.0
    for row in transactions:
        row_str = str(row).upper()
        if 'DR' in row_str or 'WITHDRAWAL' in row_str or 'CHEQUE' in row_str:
            numbers = re.findall(r'[0-9,]+\.?[0-9]*', row_str)
            if numbers:
                try:
                    total += float(numbers[-1].replace(',', ''))
                except:
                    pass
    return total

def detect_bounces(text: str) -> List:
    """Detect cheque bounces or dishonors"""
    bounces = []
    bounce_patterns = [
        r'cheque.*?return',
        r'cheque.*?dishonour',
        r'insufficient funds',
        r'returned unpaid',
        r'bounce'
    ]
    
    for pattern in bounce_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            bounces.append({
                'date': extract_date_around_match(text, match.start()),
                'reason': match.group(0)
            })
    
    return bounces

def extract_date_around_match(text: str, position: int, window: int = 50) -> Optional[str]:
    """Extract date near a match"""
    surrounding = text[max(0, position - window):min(len(text), position + window)]
    date_pattern = r'\d{2}[/-]\d{2}[/-]\d{4}'
    match = re.search(date_pattern, surrounding)
    return match.group(0) if match else None