import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

# Already provided implementation for latest_financial_index
def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

# Function to calculate total revenue
def total_revenue(data: dict, financial_index):
    try:
        financial_entry = data["financials"][financial_index]
        return financial_entry["pnl"]["lineItems"]["net_revenue"]
    except (IndexError, KeyError):
        return 0

# Function to calculate total borrowings
def total_borrowing(data: dict, financial_index):
    try:
        financial_entry = data["financials"][financial_index]
        long_term_borrowings = financial_entry["bs"]["liabilities"].get("long_term_borrowings", 0)
        short_term_borrowings = financial_entry["bs"]["liabilities"].get("short_term_borrowings", 0)
        return long_term_borrowings + short_term_borrowings
    except (IndexError, KeyError):
        return 0

# Function to determine ISCR flag
def iscr_flag(data: dict, financial_index):
    ratio = iscr(data, financial_index)
    return FLAGS.GREEN if ratio >= 2 else FLAGS.RED

# Function to check if total revenue exceeds 5 Crore
def total_revenue_5cr_flag(data: dict, financial_index):
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

# Function to calculate ISCR
def iscr(data: dict, financial_index):
    try:
        financial_entry = data["financials"][financial_index]
        profit_before_interest_and_tax = financial_entry["pnl"]["lineItems"].get("profit_before_interest_and_tax", 0)
        depreciation = financial_entry["pnl"]["lineItems"].get("depreciation", 0)
        interest = financial_entry["pnl"]["lineItems"].get("interest", 1)  # Adding 1 to avoid division by zero
        return (profit_before_interest_and_tax + depreciation + 1) / (interest + 1)
    except (IndexError, KeyError):
        return 1  # Returning 1 as a neutral value in case of missing data

# Function to determine the borrowing-to-revenue flag
def borrowing_to_revenue_flag(data: dict, financial_index):
    total_borrowings = total_borrowing(data, financial_index)
    revenue = total_revenue(data, financial_index)
    ratio = total_borrowings / revenue if revenue > 0 else 1  # Avoid division by zero
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
