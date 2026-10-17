from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ExtractedDocumentData(BaseModel):
    document_type: str
    parties: List[str]
    stamp_date: Optional[date] = None
    execution_date: Optional[date] = None
    consideration_amount: Optional[float] = None
    has_signature: bool = False
    has_stamp: bool = False

class ValidationIssue(BaseModel):
    check_name: str
    status: str  # "PASSED", "FAILED", "WARNING"
    details: str

class VerificationReport(BaseModel):
    filename: str
    confidence_score: float
    is_valid: bool
    extracted_data: ExtractedDocumentData
    checks: List[ValidationIssue]