import re
from dateutil import parser
from app.schemas import ExtractedDocumentData

def parse_legal_entities(text: str) -> ExtractedDocumentData:
    doc_type = "Agreement"
    if "SALE DEED" in text.upper():
        doc_type = "Sale Deed"
    elif "LEASE AGREEMENT" in text.upper() or "RENT AGREEMENT" in text.upper():
        doc_type = "Lease Agreement"
    elif "AFFIDAVIT" in text.upper():
        doc_type = "Affidavit"

    dates_found = re.findall(
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',
        text,
        re.IGNORECASE
    )
    parsed_dates = []
    for d in dates_found:
        try:
            parsed_dates.append(parser.parse(d).date())
        except Exception:
            continue

    execution_date = parsed_dates[0] if parsed_dates else None
    stamp_date = parsed_dates[1] if len(parsed_dates) > 1 else execution_date

    amounts = re.findall(r'(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    consideration = None
    if amounts:
        clean_amt = amounts[0].replace(",", "")
        try:
            consideration = float(clean_amt)
        except ValueError:
            pass

    has_sig = bool(re.search(r'(signature|signed by|witness|authorized signatory)', text, re.I))
    has_stamp = bool(re.search(r'(notary|e-stamp|stamp duty|certificate no)', text, re.I))

    return ExtractedDocumentData(
        document_type=doc_type,
        parties=["Party A", "Party B"],
        stamp_date=stamp_date,
        execution_date=execution_date,
        consideration_amount=consideration,
        has_signature=has_sig,
        has_stamp=has_stamp
    )