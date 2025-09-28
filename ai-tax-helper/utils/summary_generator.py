def generate_summary(expenses):
    deductible = [e for e in expenses if e["category"] == "Deductible"]
    total = sum(e["amount"] for e in deductible)
    return {
        "deductible_count": len(deductible),
        "deductible_total": total,
        "summary": f"Total deductible expenses: Rs {total}"
    }
