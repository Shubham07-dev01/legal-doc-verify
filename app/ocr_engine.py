import pypdf

def extract_text_from_pdf(file_bytes: bytes) -> str:
    full_text = ""
    try:
        import io
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"
    except Exception as e:
        print(f"Error reading PDF text: {e}")

    # Fallback to OCR only if text extraction yielded nothing and tools exist
    if len(full_text.strip()) < 20:
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
            images = convert_from_bytes(file_bytes)
            ocr_texts = [pytesseract.image_to_string(img) for img in images]
            full_text = "\n".join(ocr_texts)
        except Exception as ocr_err:
            print(f"OCR fallback skipped/failed: {ocr_err}")

    return full_text