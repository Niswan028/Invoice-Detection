import pdfplumber
import re
from datetime import datetime

def extract_invoice_fields(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    result = {}

    # Extract total amount
    amount_match = re.search(r"Total Amount\s*[:\-]?\s*\$?([\d,]+\.?\d*)", text, re.I)
    if amount_match:
        result['invoice_amount'] = float(amount_match.group(1).replace(',', ''))

    # Extract invoice, due, settled dates
    date_format = "%d/%m/%Y"
    invoice_date = re.search(r"Invoice Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    due_date = re.search(r"Due Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    settled_date = re.search(r"Settled Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)

    if invoice_date and due_date and settled_date:
        i_date = datetime.strptime(invoice_date.group(1), date_format)
        d_date = datetime.strptime(due_date.group(1), date_format)
        s_date = datetime.strptime(settled_date.group(1), date_format)

        result['days_late'] = (s_date - d_date).days
        result['days_to_settle'] = (s_date - i_date).days

    return result
