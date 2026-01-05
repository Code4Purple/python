import PyPDF2
import re
import csv
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

def parse_transactions(text):
    """Parse transactions from extracted text."""
    lines = text.split('\n')
    transactions = []
    
    # Date patterns (adjust based on your bank's format)
    date_patterns = [
        r'(\d{1,2}/\d{1,2}/\d{2,4})',  # MM/DD/YYYY or M/D/YY
        r'(\d{1,2}-\d{1,2}-\d{2,4})',  # MM-DD-YYYY
        r'(\d{4}-\d{1,2}-\d{1,2})'     # YYYY-MM-DD
    ]
    
    # Amount pattern
    amount_pattern = r'(-?\$?\s*[\d,]+\.\d{2})'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Try to find a date
        date = None
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                date = match.group(1)
                break
        
        if not date:
            continue
        
        # Extract amounts
        amounts = re.findall(amount_pattern, line)
        if not amounts:
            continue
        
        # Get description (text between date and amount)
        date_index = line.find(date)
        first_amount_index = line.find(amounts[0])
        description = line[date_index + len(date):first_amount_index].strip()
        
        # Clean up description
        description = re.sub(r'\s+', ' ', description)
        if not description:
            description = "Transaction"
        
        # Determine transaction amount and type
        # Usually the last amount is balance, second to last is transaction
        transaction_amount = amounts[-2] if len(amounts) > 1 else amounts[0]
        clean_amount = transaction_amount.replace('$', '').replace(',', '').replace(' ', '')
        num_amount = float(clean_amount)
        
        # Determine if withdrawal or deposit
        if num_amount < 0 or 'withdrawal' in line.lower() or 'debit' in line.lower():
            trans_type = "Withdrawal"
        else:
            trans_type = "Deposit"
        
        transactions.append({
            'date': date,
            'description': description,
            'amount': abs(num_amount),
            'type': trans_type
        })
    
    return transactions

def export_to_text(transactions, output_file='bank_transactions.txt'):
    """Export transactions to text file."""
    with open(output_file, 'w') as f:
        f.write(f"{'Date':<12} {'Description':<40} {'Amount':>12} {'Type':<12}\n")
        f.write("=" * 80 + "\n")
        for t in transactions:
            f.write(f"{t['date']:<12} {t['description']:<40} ${t['amount']:>11.2f} {t['type']:<12}\n")
    print(f"Exported to {output_file}")

def export_to_csv(transactions, output_file='bank_transactions.csv'):
    """Export transactions to CSV file."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'description', 'amount', 'type'])
        writer.writeheader()
        writer.writerows(transactions)
    print(f"Exported to {output_file}")

def main():
    # Get PDF file path from user
    pdf_path = input("Enter the path to your bank PDF statement: ").strip()
    
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print("Parsing transactions...")
    transactions = parse_transactions(text)
    
    if not transactions:
        print("No transactions found. The PDF format may not be supported.")
        print("You may need to adjust the parsing patterns in the code.")
        return
    
    print(f"\nFound {len(transactions)} transactions:")
    print("-" * 80)
    for i, t in enumerate(transactions[:5], 1):  # Show first 5
        print(f"{i}. {t['date']} - {t['description'][:30]} - ${t['amount']:.2f} ({t['type']})")
    if len(transactions) > 5:
        print(f"... and {len(transactions) - 5} more")
    
    # Export options
    print("\n" + "=" * 80)
    print("Export options:")
    print("1. Export to Text file")
    print("2. Export to CSV file")
    print("3. Both")
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        export_to_text(transactions)
    if choice in ['2', '3']:
        export_to_csv(transactions)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
