def classify_expense(text):
    text = text.lower()
    if "travel" in text or "uber" in text or "flight" in text:
        return "Deductible"
    if "office" in text or "supplies" in text:
        return "Deductible"
    return "Not Deductible"
