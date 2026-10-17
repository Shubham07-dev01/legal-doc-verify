from fastapi import FastAPI, UploadFile, File, HTTPException
from app.ocr_engine import extract_text_from_pdf
from app.extractor import parse_legal_entities
from app.rules_engine import run_verification_checks
from app.schemas import VerificationReport

app = FastAPI(title="Legal Document Verification API", version="1.0.0")

@app.post("/verify-document", response_model=VerificationReport)
async def verify_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.PDF')):
        raise HTTPException(status_code=400, detail="Only PDF files are supported currently.")

    contents = await file.read()
    
    text = extract_text_from_pdf(contents)
    if not text.strip():
        raise HTTPException(status_code=422, detail="Document appears blank or unreadable.")

    extracted_data = parse_legal_entities(text)
    is_valid, confidence_score, checks = run_verification_checks(extracted_data)

    return VerificationReport(
        filename=file.filename,
        confidence_score=confidence_score,
        is_valid=is_valid,
        extracted_data=extracted_data,
        checks=checks
    )