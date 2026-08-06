from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import yfinance as yf

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
def home():
    return '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DART Pro Max</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont; background: #FFFFFF; color: #191F28; }
.container { max-width: 600px; margin: 0 auto; padding: 20px; }
.header { text-align: center; padding: 40px 0 30px; }
.header-title { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
.header-subtitle { font-size: 15px; color: #4E5937; }
.search-box { position: relative; margin-bottom: 30px; }
input { width: 100%; padding: 16px; font-size: 16px; border: 1px solid #F3F4F6; border-radius: 12px; background: #F3F4F6; font-family: inherit; }
input:focus { outline: none; border-color: #0040FF; background: #FFFFFF; }
.autocomplete { position: absolute; top: 100%; left: 0; right: 0; background: #FFFFFF; border: 1px solid #F3F4F6; border-top: none; border-radius: 0 0 12px 12px; max-height: 300px; overflow-y: auto; display: none; z-index: 100; }
.autocomplete.active { display: block; }
.autocomplete-item { padding: 12px 16px; cursor: pointer; border-bottom: 1px solid #F3F4F6; font-size: 14px; }
.autocomplete-item:hover { background: #F3F4F6; }
.btn { width: 100%; padding: 16px; background: #0040FF; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; margin-bottom: 30px; }
.quick { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 30px; }
.quick-btn { padding: 12px; background: #F3F4F6; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit; }
.section { margin-bottom: 16px; border: 1px solid #F3F4F6; border-radius: 16px; overflow: hidden; }
.section-header { cursor: pointer; padding: 16px; background: #F3F4F6; font-weight: 600; display: flex; justify-content: space-between; align-items: center; user-select: none; }
.section-header:hover { background: #E5E7EB; }
.section-content { display: none; padding: 20px; background: #FAFBFC; }
.section-content.show { display: block; }
table { width: 100%; border-collapse: collapse; margin: 0; }
th { background: #F3F4F6; padding: 12px; text-align: left; font-size: 13px; font-weight: 600; }
td { padding: 12px; border-bottom: 1px solid #F3F4F6; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.info-item { background: #F3F4F6; padding: 12px; border-radius: 8px; }
.info-label { font-size: 12px; color: #4E5937; margin-bottom: 4px; }
.info-value { font-size: 14px; font-weight: 600; }
.result { margin-top: 30px; margin-bottom: 100px; }
.result-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.result-sector { font-size: 13px; color: #4E5937; margin-bottom: 30px; }
.chart-container { position: relative; height: 300px; margin: 20px 0; }
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="header-title">DART Pro Max</div>
<div class="header-subtitle">기업 재무 분석, 한눈에</div>
</div>

<div class="search-box">
<input type="text" id="ticker" placeholder="회사명 또는 티커 입력" onkeyup="updateAutocomplete()">
<div class="autocomplete" id="autocomplete"></div>
</div>

<button class="btn" onclick="search()">검색</button>

<div class="quick">
<button class="quick-btn" onclick="quick('AAPL')">AAPL</button>
<button class="quick-btn" onclick="quick('MSFT')">MSFT</button>
<button class="quick-btn" onclick="quick('GOOGL')">GOOGL</button>
<button class="quick-btn" onclick="quick('TSLA')">TSLA</button>
<button class="quick-btn" onclick="quick('AMZN')">AMZN</button>
<button class="quick-btn" onclick="quick('META')">META</button>
<button class="quick-btn" onclick="quick('NVDA')">NVDA</button>
<button class="quick-btn" onclick="quick('NFLX')">NFLX</button>
</div>

<div id="result"></div>
</div>

<script>
const COMPANIES = [["AAPL", "Apple"], ["MSFT", "Microsoft"], ["GOOGL", "Google"], ["TSLA", "Tesla"], ["AMZN", "Amazon"], ["META", "Meta"], ["NVDA", "NVIDIA"], ["NFLX", "Netflix"], ["AMD", "AMD"], ["CRM", "Salesforce"], ["JPM", "JP Morgan"], ["BAC", "Bank of America"], ["WFC", "Wells Fargo"], ["JNJ", "J&J"], ["PFE", "Pfizer"], ["MRK", "Merck"]];

function updateAutocomplete() {
  const val = document.getElementById('ticker').value.toUpperCase();
  const autocomplete = document.getElementById('autocomplete');
  if (!val) { autocomplete.classList.remove('active'); return; }
  const filtered = COMPANIES.filter(c => c[0].includes(val) || c[1].includes(val)).slice(0, 5);
  if (filtered.length === 0) { autocomplete.classList.remove('active'); return; }
  autocomplete.innerHTML = filtered.map(c => '<div class="autocomplete-item" onclick="selectCompany(' + "'" + c[0] + "'" + ')">' + c[0] + ' · ' + c[1] + '</div>').join('');
  autocomplete.classList.add('active');
}

function selectCompany(symbol) {
  document.getElementById('ticker').value = symbol;
  document.getElementById('autocomplete').classList.remove('active');
  search();
}

function quick(s) {
  document.getElementById('ticker').value = s;
  search();
}

function toggle(id) {
  document.getElementById(id).classList.toggle('show');
}

function search() {
  const ticker = document.getElementById('ticker').value.toUpperCase().trim();
  if (!ticker) return;
  document.getElementById('result').innerHTML = '<div class="result"><p>로딩 중...</p></div>';
  fetch('/api/search/' + ticker)
    .then(r => r.json())
    .then(d => {
      if (d.error) {
        document.getElementById('result').innerHTML = '<div class="result"><p style="color: #FF3B30;">데이터를 찾을 수 없습니다</p></div>';
      } else {
        displayResult(d);
      }
    });
}

function displayResult(d) {
  let html = '<div class="result"><div class="result-title">' + d.name + '</div><div class="result-sector">📊 ' + d.sector + '</div>';
  
  html += '<div class="section"><div class="section-header" onclick="toggle(' + "'s1'" + ')">📈 주가 정보</div><div class="section-content" id="s1"><div class="info-grid"><div class="info-item"><div class="info-label">현재가</div><div class="info-value">$' + d.stock_price + '</div></div></div></div></div>';
  
  html += '<div class="section"><div class="section-header" onclick="toggle(' + "'s2'" + ')">📊 연간 재무제표</div><div class="section-content" id="s2"><table><tr><th>연도</th><th>매출</th><th>영업이익</th><th>순이익</th></tr>';
  d.years.forEach(y => { html += '<tr><td>' + y.year + '</td><td>$' + y.revenue.toFixed(1) + 'B</td><td>$' + y.operating_income.toFixed(1) + 'B</td><td>$' + y.net_income.toFixed(1) + 'B</td></tr>'; });
  html += '</table><div class="chart-container"><canvas id="chart"></canvas></div></div></div>';
  
  html += '<div class="section"><div class="section-header" onclick="toggle(' + "'s3'" + ')">📈 재무비율</div><div class="section-content" id="s3"><div class="info-grid"><div class="info-item"><div class="info-label">ROE</div><div class="info-value">' + d.roe + '%</div></div><div class="info-item"><div class="info-label">ROA</div><div class="info-value">' + d.roa + '%</div></div></div></div></div>';
  
  html += '<div class="section"><div class="section-header" onclick="toggle(' + "'s4'" + ')">📅 분기별 데이터</div><div class="section-content" id="s4"><table><tr><th>분기</th><th>매출</th><th>순이익</th></tr>';
  if (d.quarterly_data) { d.quarterly_data.forEach(q => { html += '<tr><td>' + q.period + '</td><td>$' + q.revenue.toFixed(1) + 'B</td><td>$' + q.net_income.toFixed(1) + 'B</td></tr>'; }); }
  html += '</table></div></div>';
  
  html += '<div class="section"><div class="section-header" onclick="toggle(' + "'s5'" + ')">🏢 기업 정보</div><div class="section-content" id="s5"><div class="info-grid"><div class="info-item"><div class="info-label">CEO</div><div class="info-value">' + d.ceo + '</div></div><div class="info-item"><div class="info-label">직원 수</div><div class="info-value">' + d.employees + '</div></div></div></div></div>';
  
  html += '</div>';
  document.getElementById('result').innerHTML = html;
  
  setTimeout(() => {
    const canvas = document.getElementById('chart');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: d.years.map(y => y.year),
          datasets: [
            { label: '매출액', data: d.years.map(y => y.revenue), backgroundColor: '#0040FF' },
            { label: '영업이익', data: d.years.map(y => y.operating_income), backgroundColor: '#3182F6' },
            { label: '순이익', data: d.years.map(y => y.net_income), backgroundColor: '#A8CBFF' }
          ]
        },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true } } }
      });
    }
  }, 100);
}
</script>
</body>
</html>'''

@app.get("/api/search/{symbol}")
def search(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        income = ticker.income_stmt
        quarterly_income = ticker.quarterly_income_stmt
        if income.empty:
            return {"error": "데이터 없음"}
        
        years = []
        for col in income.columns[:3]:
            row = income[col]
            years.append({
                'year': str(col.year),
                'revenue': float(row.get('Total Revenue', 0)) / 1e9,
                'operating_income': float(row.get('Operating Income', 0)) / 1e9,
                'net_income': float(row.get('Net Income', 0)) / 1e9
            })
        
        quarterly_data = []
        if not quarterly_income.empty:
            for col in quarterly_income.columns[:4]:
                row = quarterly_income[col]
                quarterly_data.append({
                    'period': str(col.date()),
                    'revenue': float(row.get('Total Revenue', 0)) / 1e9,
                    'net_income': float(row.get('Net Income', 0)) / 1e9
                })
        
        return {
            'name': ticker.info.get('longName', symbol),
            'sector': ticker.info.get('sector', '?'),
            'stock_price': ticker.info.get('currentPrice', 'N/A'),
            'roe': round(ticker.info.get('returnOnEquity', 0) * 100, 2) if ticker.info.get('returnOnEquity') else 'N/A',
            'roa': round(ticker.info.get('returnOnAssets', 0) * 100, 2) if ticker.info.get('returnOnAssets') else 'N/A',
            'ceo': ticker.info.get('companyOfficers', [{}])[0].get('name', 'N/A') if ticker.info.get('companyOfficers') else 'N/A',
            'employees': ticker.info.get('fullTimeEmployees', 'N/A'),
            'years': years,
            'quarterly_data': quarterly_data
        }
    except:
        return {'error': '검색 실패'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
