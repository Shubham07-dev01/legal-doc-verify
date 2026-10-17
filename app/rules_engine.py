from typing import List, Tuple
from app.schemas import ExtractedDocumentData, ValidationIssue

def run_verification_checks(data: ExtractedDocumentData) -> Tuple[bool, float, List[ValidationIssue]]:
    checks = []
    score_points = 0
    total_points = 4

    if data.has_signature:
        checks.append(ValidationIssue(check_name="Signature Check", status="PASSED", details="Signatures/Execution marks found."))
        score_points += 1
    else:
        checks.append(ValidationIssue(check_name="Signature Check", status="FAILED", details="No signature block detected."))

    if data.has_stamp:
        checks.append(ValidationIssue(check_name="Stamp/Duty Verification", status="PASSED", details="Stamp paper/notary keywords present."))
        score_points += 1
    else:
        checks.append(ValidationIssue(check_name="Stamp/Duty Verification", status="WARNING", details="Stamp verification flag missing."))

    if data.stamp_date and data.execution_date:
        if data.stamp_date <= data.execution_date:
            checks.append(ValidationIssue(check_name="Date Chronology", status="PASSED", details="Stamp date is before or equal to execution date."))
            score_points += 1
        else:
            checks.append(ValidationIssue(check_name="Date Chronology", status="FAILED", details="Anomaly: Execution date is before stamp issue date."))
    else:
        checks.append(ValidationIssue(check_name="Date Chronology", status="WARNING", details="One or both dates could not be verified."))

    if len(data.parties) >= 2:
        checks.append(ValidationIssue(check_name="Parties Check", status="PASSED", details="Minimum two parties identified."))
        score_points += 1
    else:
        checks.append(ValidationIssue(check_name="Parties Check", status="FAILED", details="Missing party definitions."))

    confidence_score = (score_points / total_points) * 100
    is_valid = confidence_score >= 75.0

    return is_valid, confidence_score, checks