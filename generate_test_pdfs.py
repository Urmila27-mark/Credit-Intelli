# Simple PDF generator with NO special characters
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

# Create test_data folder
os.makedirs("test_data", exist_ok=True)

# ============================================
# CASE 1: HEALTHY COMPANY - GOOD FOR APPROVAL
# ============================================
def create_healthy_gst():
    filename = 'test_data/healthy_company_gst.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "GSTR-3B RETURN")
    
    # Company details
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "GSTIN: 27AABCT1234E1Z5")
    c.drawString(50, 680, "Legal Name: ABC STEEL PVT LTD")
    c.drawString(50, 660, "Trade Name: ABC STEEL")
    c.drawString(50, 640, "Return Period: Jul-2024")
    
    # Financial data - Using "Rs." instead of rupee symbol
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 600, "Financial Summary:")
    
    c.setFont("Helvetica", 12)
    c.drawString(70, 580, "Total Turnover: Rs. 1,25,00,000")
    c.drawString(70, 560, "Total Tax Liability: Rs. 22,50,000")
    c.drawString(70, 540, "Input Tax Credit: Rs. 18,00,000")
    c.drawString(70, 520, "Net Tax Payable: Rs. 4,50,000")
    
    # GSTR Comparison
    c.drawString(50, 480, "GSTR-2A Total: Rs. 22,80,000")
    c.drawString(50, 460, "GSTR-3B Total: Rs. 22,50,000")
    c.drawString(50, 440, "Mismatch: 1.3% (Within limits)")
    
    c.save()
    print(f"✅ Created: {filename}")

def create_healthy_bank():
    filename = 'test_data/healthy_company_bank.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "BANK STATEMENT")
    
    # Bank details
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Bank: HDFC BANK")
    c.drawString(50, 680, "Account No: 12345678901")
    c.drawString(50, 660, "Period: 01-Jul-2024 to 31-Jul-2024")
    c.drawString(50, 640, "Company: ABC STEEL PVT LTD")
    
    # Column headers
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 600, "Date")
    c.drawString(120, 600, "Type")
    c.drawString(180, 600, "Description")
    c.drawString(300, 600, "Amount")
    c.drawString(380, 600, "Balance")
    
    # Draw line
    c.line(50, 595, 450, 595)
    
    # Transactions
    c.setFont("Helvetica", 10)
    y = 575
    transactions = [
        ('01-07-2024', 'CR', 'SALE - ABC CORP', '12,50,000', '25,00,000'),
        ('05-07-2024', 'DR', 'RENT PAYMENT', '1,00,000', '24,00,000'),
        ('10-07-2024', 'CR', 'SALE - XYZ LTD', '8,50,000', '32,50,000'),
        ('15-07-2024', 'DR', 'SALARY', '5,00,000', '27,50,000'),
        ('20-07-2024', 'DR', 'VENDOR PAYMENT', '3,00,000', '24,50,000'),
        ('25-07-2024', 'CR', 'SALE - PQR CO', '5,50,000', '30,00,000'),
        ('28-07-2024', 'CR', 'INTEREST', '25,000', '30,25,000'),
    ]
    
    for t in transactions:
        c.drawString(50, y, t[0])
        c.drawString(120, y, t[1])
        c.drawString(180, y, t[2])
        c.drawString(300, y, t[3])
        c.drawString(380, y, t[4])
        y -= 20
    
    # Summary
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y-20, "Average Balance: Rs. 27,50,000")
    c.drawString(50, y-40, "No Bounces/Issues Found")
    
    c.save()
    print(f"✅ Created: {filename}")

# ============================================
# CASE 2: RISKY COMPANY - HIGH CIRCULAR TRADING
# ============================================
def create_risky_gst():
    filename = 'test_data/risky_company_gst.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "GSTR-3B RETURN")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "GSTIN: 27XYZ9876F2Z5")
    c.drawString(50, 680, "Legal Name: XYZ TRADING CO")
    c.drawString(50, 660, "Return Period: Jul-2024")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 620, "Financial Summary:")
    
    c.setFont("Helvetica", 12)
    c.drawString(70, 600, "Total Turnover: Rs. 85,00,000")
    c.drawString(70, 580, "Total Tax Liability: Rs. 15,30,000")
    c.drawString(70, 560, "Input Tax Credit: Rs. 12,00,000")
    
    # High mismatch
    c.drawString(50, 520, "GSTR-2A Total: Rs. 19,50,000")
    c.drawString(50, 500, "GSTR-3B Total: Rs. 15,30,000")
    
    c.setFillColorRGB(1, 0, 0)  # Red
    c.drawString(50, 480, "Mismatch: 27% (CRITICAL)")
    
    c.save()
    print(f"✅ Created: {filename}")

def create_risky_bank():
    filename = 'test_data/risky_company_bank.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "BANK STATEMENT")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Bank: SBI")
    c.drawString(50, 680, "Account No: 98765432109")
    c.drawString(50, 660, "Company: XYZ TRADING CO")
    
    # Column headers
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 620, "Date")
    c.drawString(120, 620, "Type")
    c.drawString(180, 620, "Description")
    c.drawString(300, 620, "Amount")
    c.drawString(380, 620, "Balance")
    
    c.line(50, 615, 450, 615)
    
    # Suspicious circular trading pattern
    c.setFont("Helvetica", 10)
    y = 595
    transactions = [
        ('01-07-2024', 'CR', 'M/S A ENTERPRISES', '5,00,000', '8,00,000'),
        ('03-07-2024', 'DR', 'M/S B TRADERS', '5,00,000', '3,00,000'),
        ('05-07-2024', 'CR', 'M/S B TRADERS', '5,00,000', '8,00,000'),
        ('07-07-2024', 'DR', 'M/S A ENTERPRISES', '5,00,000', '3,00,000'),
        ('09-07-2024', 'CR', 'M/S A ENTERPRISES', '5,00,000', '8,00,000'),
        ('11-07-2024', 'DR', 'M/S B TRADERS', '5,00,000', '3,00,000'),
        ('13-07-2024', 'CR', 'M/S B TRADERS', '5,00,000', '8,00,000'),
        ('15-07-2024', 'DR', 'CHEQUE BOUNCE', '5,00,000', '3,00,000'),
    ]
    
    for i, t in enumerate(transactions):
        if i == 7:  # Last transaction - the bounce
            c.setFillColorRGB(1, 0, 0)  # Red
        
        c.drawString(50, y, t[0])
        c.drawString(120, y, t[1])
        c.drawString(180, y, t[2])
        c.drawString(300, y, t[3])
        c.drawString(380, y, t[4])
        y -= 20
    
    # Warnings
    c.setFillColorRGB(1, 0, 0)  # Red
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y-20, "⚠️ Cheque Bounce Detected on 15-07-2024")
    c.drawString(50, y-40, "⚠️ Multiple Round-Trip Transactions Detected")
    
    c.save()
    print(f"✅ Created: {filename}")

# ============================================
# CASE 3: EDGE CASE - HIGH MISMATCH + BOUNCES
# ============================================
def create_edge_gst():
    filename = 'test_data/edge_case_gst.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "GSTR-3B RETURN")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "GSTIN: 29LMN4567G3H8")
    c.drawString(50, 680, "Legal Name: PQR INFRASTRUCTURE")
    c.drawString(50, 660, "GSTR-2A Total: Rs. 45,00,000")
    c.drawString(50, 640, "GSTR-3B Total: Rs. 28,00,000")
    
    c.setFillColorRGB(1, 0, 0)  # Red
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 600, "Mismatch: 60% (SEVERE)")
    
    c.save()
    print(f"✅ Created: {filename}")

def create_edge_bank():
    filename = 'test_data/edge_case_bank.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "BANK STATEMENT")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Multiple Cheque Bounces Recorded:")
    
    c.setFillColorRGB(1, 0, 0)  # Red
    y = 660
    bounces = [
        ('05-07-2024', 'Cheque #1245', 'Insufficient Funds'),
        ('12-07-2024', 'Cheque #1256', 'Account Frozen'),
        ('19-07-2024', 'Cheque #1267', 'Signature Mismatch'),
        ('26-07-2024', 'Cheque #1278', 'Stop Payment'),
    ]
    
    for b in bounces:
        c.drawString(70, y, f"⚠️ {b[0]} - {b[1]}: {b[2]}")
        y -= 25
    
    c.save()
    print(f"✅ Created: {filename}")

# ============================================
# GENERATE ALL FILES
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("📄 Generating Test PDF Files")
    print("="*50)
    
    # Check if reportlab is installed
    try:
        from reportlab.pdfgen import canvas
        print("✅ reportlab library found")
    except ImportError:
        print("Installing reportlab library...")
        os.system("pip install reportlab")
        from reportlab.pdfgen import canvas
    
    # Generate all test files
    create_healthy_gst()
    create_healthy_bank()
    create_risky_gst()
    create_risky_bank()
    create_edge_gst()
    create_edge_bank()
    
    print("\n" + "="*50)
    print("✅ ALL TEST FILES CREATED SUCCESSFULLY!")
    print("📁 Location: C:\\Credit Intelli\\test_data\\")
    print("="*50)
    print("\nTest Files Available:")
    print("1️⃣ HEALTHY COMPANY (Should APPROVE):")
    print("   - healthy_company_gst.pdf")
    print("   - healthy_company_bank.pdf")
    print("\n2️⃣ RISKY COMPANY (Should FLAG):")
    print("   - risky_company_gst.pdf")
    print("   - risky_company_bank.pdf")
    print("\n3️⃣ EDGE CASE (Should REJECT):")
    print("   - edge_case_gst.pdf")
    print("   - edge_case_bank.pdf")