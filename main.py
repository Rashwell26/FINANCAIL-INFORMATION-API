from fastapi import Header, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class FinancialData(BaseModel):
    revenue: float
    net_income: float
    assets: float
    liabilities: float
    equity: float
    industry: str

# Fake industry averages (for now)
industry_averages = {
    "retail": 0.12,
    "tech": 0.18,
    "manufacturing": 0.10
}

@app.post("/analyze")
def analyze(data: FinancialData, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    profit_margin = data.net_income / data.revenue
    roe = data.net_income / data.equity
    debt_to_equity = data.liabilities / data.equity

    industry_avg = industry_averages.get(data.industry.lower(), 0.15)

    comparison = "Above industry average" if profit_margin > industry_avg else "Below industry average"

    return {
        "profit_margin": round(profit_margin, 3),
        "roe": round(roe, 3),
        "debt_to_equity": round(debt_to_equity, 3),
        "industry_average_profit_margin": industry_avg,
        "comparison": comparison
    }

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "supersecretkey":
        raise HTTPException(status_code=403, detail="Invalid API Key")
