from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import yfinance as yf

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head><meta charset="UTF-8"><title>DART Pro Max</title></head>
    <body style="font-family: sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
        <h1>DART Pro Max</h1>
        <input type="text" id="ticker" placeholder="AAPL 입력" style="padding: 10px; width: 100%; font-size: 16px;">
        <button onclick="search()" style="padding: 10px 20px; margin-top: 10px; font-size: 16px; background: #0040FF; color: white; border: none; border-radius: 8px; cursor: pointer;">검색</button>
        <div id="result" style="margin-top: 20px;"></div>
        <script>
            function search() {
                const ticker = document.getElementById('ticker').value.toUpperCase();
                if (!ticker) return;
                fetch('/api/search/' + ticker)
                    .then(r => r.json())
                    .then(d => {
                        if (d.error) {
                            document.getElementById('result').innerHTML = '<div style="color: red;">오류: ' + d.error + '</div>';
                        } else {
                            document.getElementById('result').innerHTML = '<div style="border: 1px solid #ddd; padding: 20px; border-radius: 8px;"><h2>' + d.name + '</h2><p>심볼: ' + d.symbol + '</p></div>';
                        }
                    });
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/search/{symbol}")
def search(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        return {"name": ticker.info.get('longName', symbol), "symbol": symbol}
    except:
        return {"error": "데이터 없음"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
