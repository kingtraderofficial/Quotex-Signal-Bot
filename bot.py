import os, yfinance as yf, google.generativeai as genai, json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

assets = {
    "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "USDJPY=X", "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X", "USD/CHF": "USDCHF=X", "NZD/USD": "NZDUSD=X", "EUR/GBP": "EURGBP=X",
    "EUR/JPY": "EURJPY=X", "GBP/JPY": "GBPJPY=X", "BTC/USDT": "BTC-USD", "ETH/USDT": "ETH-USD",
    "SOL/USDT": "SOL-USD", "BNB/USDT": "BNB-USD", "XRP/USDT": "XRP-USD", "LTC/USDT": "LTC-USD"
}

def get_balanced_logic(ticker):
    """Calculates Reversal Signals for 50/50 Balance (No Math.Random)"""
    try:
        df = yf.download(ticker, period="1d", interval="15m", progress=False).tail(14)
        close = df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=7).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
        rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
        
        curr = close.iloc[-1]
        # Reversal Logic
        if rsi > 60: return "1M PUT ↓"
        elif rsi < 40: return "1M CALL ↑"
        else: return "1M PUT ↓" if curr > close.iloc[-3] else "1M CALL ↑"
    except: return "1M CALL ↑"

def fetch_hub_data():
    signals_dict = {}
    market_snapshot = ""
    
    # 1. Base technicals
    for name, ticker in assets.items():
        signals_dict[name] = {"sig": get_balanced_logic(ticker)}
        try:
            d = yf.download(ticker, period="1d", interval="15m", progress=False).tail(5)
            market_snapshot += f"{name}: {d['Close'].tolist()}\n"
        except: continue

    # 2. Gemini Refinement for Symmetrical Balance
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze market data and provide a balanced mix of BUY and SELL signals based on mean reversion. Return strictly JSON: {list(assets.keys())}"
        response = model.generate_content(prompt)
        ai_data = json.loads(response.text.replace("```json", "").replace("```", "").strip())
        for k, v in ai_data.items():
            if k in signals_dict: signals_dict[k]["sig"] = v["sig"]
    except: pass

    return json.dumps(signals_dict)

try:
    final_json = fetch_hub_data()
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    marker = 'const HUB_DATA = { "signals": {} }; //MARKER:V20_ELITE'
    new_html = html.replace(marker, f'const HUB_DATA = {{ "signals": {final_json} }}; //MARKER:V20_ELITE')

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("V20 Titan Core Sync Success!")
except Exception as e:
    print(f"FAILED: {e}")
