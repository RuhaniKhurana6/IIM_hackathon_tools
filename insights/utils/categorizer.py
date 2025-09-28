# insights/utils/categorizer.py
CATEGORY_KEYWORDS = {
    "Food": ["restaurant","cafe","dominos","mcdonald","zomato","swiggy","coffee","dine"],
    "Travel": ["uber","ola","taxi","flight","airasia","indigo","train","bus","travel","ola"],
    "Bills": ["electricity","water","bill","ga bills","phone bill","isp","internet","broadband","payment"],
    "Groceries": ["grocer","supermarket","bigbasket","grocery","dmart"],
    "Subscriptions": ["spotify","netflix","amazon prime","primevideo","hotstar","subscription","payment to"],
    "Shopping": ["amazon","flipkart","myntra","shopping","store"],
    "Healthcare": ["clinic","hospital","pharmacy","medicare","medicines","chemist"]
}

def categorize_transaction(raw_text, merchant=None):
    txt = (merchant or "") + " " + (raw_text or "")
    t = txt.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return cat
    return "Other"
