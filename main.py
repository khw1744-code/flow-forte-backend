from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import datetime as dt

app = FastAPI(title="Flow Forte Backend", version="0.1")

# CORS: Vercel 프론트에서 호출 가능하도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안 강화를 원하면 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 모의 데이터 스냅샷 (나중에 실제 API로 교체) ---
MOCK_SNAPSHOT = {
    "tvl": {"value": 178.3, "unit": "M USD", "wow": 16.8},
    "wallets": {"value": 1.92, "unit": "M", "wow": 11.4},
    "devs": {"value": 3.8, "unit": "k", "mom": 21.2},
    "stakingRatio": {"value": 58.6, "unit": "%", "wow": 3.2},
    "stableVol": {"value": 612, "unit": "M USD", "ath": True},
    "actionsApps": {"value": 37, "unit": "apps", "delta7d": 12},
    "cexListings": {"value": 24, "unit": "pairs", "delta30d": 2},
    "retention": {"value": 52, "unit": "%", "mom": 5.0},
    "ipDeals": {"value": 2, "unit": "new", "qoq": 2},
    "aiWins": {"value": 1, "unit": "news", "delta30d": 1},
}

# --- 모의 데이터 시계열 ---

def _gen_series(days: int) -> List[Dict[str, Any]]:
    now = dt.date.today()
    out = []
    base_tvl = 120.0
    for i in range(days):
        day = (now - dt.timedelta(days=days-1-i))
        out.append({
            "day": day.strftime("%m-%d"),
            "tvl": round(base_tvl + i * 2 + (6 if i % 7 == 0 else 0), 2),
            "wallets": round(50 + (i * 0.4) + 8 * __import__('math').sin(i / 3), 2),
            "staking": round(48 + 2 * __import__('math').sin(i / 5), 2),
        })
    return out

@app.get("/api/flow/snapshot")
async def snapshot() -> Dict[str, Any]:
    # TODO: 실제 데이터로 교체
    # 1) DeFiLlama TVL: https://api.llama.fi/charts/flow
    # 2) FlowScan (지갑/거래): https://flowscan.org API 참조
    # 3) Ankr Staking: https://www.ankr.com/docs/ (Validator/TVL)
    # 4) 기타 지표: 프로젝트 제공 API
    return MOCK_SNAPSHOT

@app.get("/api/flow/series")
async def series(days: int = Query(30, ge=7, le=180)) -> List[Dict[str, Any]]:
    return _gen_series(days)

@app.get("/")
async def root():
    return {"ok": True, "service": "flow-forte-backend", "version": "0.1"}
