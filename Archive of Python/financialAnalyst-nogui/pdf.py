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

def parse_wells_fargo_transactions(text):
    """Parse Wells Fargo bank statement transactions."""
    lines = text.split('\n')
    transactions = []
    
    # Look for transaction section
    in_transaction_section = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Start capturing after "Transaction history" or "Transaction History"
        if 'transaction history' in line.lower():
            in_transaction_section = True
            continue
        
        # Stop at totals line
        if line.startswith('Totals'):
            break
        
        if not in_transaction_section:
            continue
        
        # Skip header lines and empty lines
        if not line or 'Date' in line or 'Check' in line or 'Description' in line:
            continue
        if 'Deposits/' in line or 'Withdrawals/' in line or 'Ending daily' in line:
            continue
        if line.startswith('===') or line.startswith('---'):
            continue
        
        # Match date pattern at start of line (M/D or MM/DD)
        date_match = re.match(r'^(\d{1,2}/\d{1,2})\s', line)
        if not date_match:
            continue
        
        date = date_match.group(1)
        
        # Get the rest of the line after the date
        rest_of_line = line[len(date):].strip()
        
        # Look ahead to next lines for description and amounts
        description_parts = [rest_of_line]
        amount_withdrawal = None
        amount_deposit = None
        
        # Check next few lines for continuation and amounts
        j = i + 1
        while j < len(lines) and j < i + 5:
            next_line = lines[j].strip()
            
            # If next line starts with a date, we're done with this transaction
            if re.match(r'^\d{1,2}/\d{1,2}\s', next_line):
                break
            
            # Check if this line has amounts (withdrawal/deposit columns)
            # Amounts appear as standalone numbers with decimals
            amounts = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', next_line)
            
            if amounts:
                # Wells Fargo format: Description | Deposit | Withdrawal | Balance
                # If one amount: could be withdrawal or balance
                # If two amounts: first is transaction, second is balance
                # If three amounts: deposit, withdrawal, balance
                
                if len(amounts) == 1:
                    # Single amount - likely a withdrawal
                    amount_withdrawal = amounts[0]
                elif len(amounts) == 2:
                    # Two amounts: transaction amount and balance
                    # Need to check if it's in deposit or withdrawal column
                    # The transaction amount is the first one
                    amount_withdrawal = amounts[0]
                elif len(amounts) >= 3:
                    # Three or more amounts: deposit, withdrawal, balance
                    if amounts[0] != '':
                        amount_deposit = amounts[0]
                    if amounts[1] != '':
                        amount_withdrawal = amounts[1]
                
                break
            else:
                # No amounts yet, add to description
                if next_line and not next_line.startswith('Page'):
                    description_parts.append(next_line)
            
            j += 1
        
        # Build description
        description = ' '.join(description_parts).strip()
        
        # Clean up description - remove extra spaces
        description = re.sub(r'\s+', ' ', description)
        
        # Determine transaction type and amount
        if amount_deposit:
            amount = amount_deposit.replace(',', '')
            trans_type = "Deposit"
        elif amount_withdrawal:
            amount = amount_withdrawal.replace(',', '')
            trans_type = "Withdrawal"
        else:
            continue  # Skip if no amount found
        
        # Add year to date (using current statement year)
        # Extract year from statement if available
        year = '2025'  # Default, can be improved by parsing statement date
        full_date = f"{date}/{year}"
        
        transactions.append({
            'date': full_date,
            'description': description,
            'amount': float(amount),
            'type': trans_type
        })
    
    return transactions

def export_to_text(transactions, output_file='bank_transactions.txt'):
    """Export transactions to text file."""
    with open(output_file, 'w') as f:
        f.write(f"{'Date':<12} {'Description':<50} {'Amount':>12} {'Type':<12}\n")
        f.write("=" * 90 + "\n")
        for t in transactions:
            f.write(f"{t['date']:<12} {t['description']:<50} ${t['amount']:>11.2f} {t['type']:<12}\n")
    print(f"Exported {len(transactions)} transactions to {output_file}")

def export_to_csv(transactions, output_file='bank_transactions.csv'):
    """Export transactions to CSV file."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'description', 'amount', 'type'])
        writer.writeheader()
        writer.writerows(transactions)
    print(f"Exported {len(transactions)} transactions to {output_file}")

def main():
    print("=" * 80)
    print("Wells Fargo Bank Statement PDF Parser")
    print("=" * 80)
    
    # Get PDF file path from user
    pdf_path = input("\nEnter the path to your Wells Fargo PDF statement: ").strip()
    
    # Remove quotes if user wrapped path in quotes
    pdf_path = pdf_path.strip('"').strip("'")
    
    print("\nExtracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print("Parsing transactions...")
    transactions = parse_wells_fargo_transactions(text)
    
    if not transactions:
        print("\nNo transactions found. Please check:")
        print("1. The PDF is a Wells Fargo bank statement")
        print("2. The statement contains transaction history")
        print("3. The PDF is not password protected or corrupted")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(transactions)} transactions!")
    print(f"{'='*80}\n")
    
    # Show first 5 transactions as preview
    print("Preview of transactions:\n")
    for i, t in enumerate(transactions[:5], 1):
        desc = t['description'][:45] + '...' if len(t['description']) > 45 else t['description']
        print(f"{i}. {t['date']:<12} {desc:<48} ${t['amount']:>8.2f} ({t['type']})")
    
    if len(transactions) > 5:
        print(f"... and {len(transactions) - 5} more transactions")
    
    # Export options
    print(f"\n{'='*80}")
    print("Export options:")
    print("1. Export to Text file (.txt)")
    print("2. Export to CSV file (.csv)")
    print("3. Export to both formats")
    print("4. Cancel")
    
    choice = input("\nEnter your choice (1/2/3/4): ").strip()
    
    if choice == '1':
        export_to_text(transactions)
        print("\n✓ Done! Check bank_transactions.txt")
    elif choice == '2':
        export_to_csv(transactions)
        print("\n✓ Done! Check bank_transactions.csv")
    elif choice == '3':
        export_to_text(transactions)
        export_to_csv(transactions)
        print("\n✓ Done! Check bank_transactions.txt and bank_transactions.csv")
    elif choice == '4':
        print("\nCancelled.")
    else:
        print("\nInvalid choice. Please run the program again.")
    
    print("\nThank you for using the Wells Fargo Statement Parser!")

if __name__ == "__main__":
    main()