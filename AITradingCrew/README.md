![0_zFUNL_p_C-IEeoAQ (1)](https://github.com/user-attachments/assets/97e29d19-3d73-413c-a51e-67f8ad579432)


*Photo by Igor Omilaev on Unsplash*

# AI Trading Crew 🤖

## Tired of Spending 2 Hours Daily on Stock Market Research? Use This Agentic AI System Instead

From VIX analysis to StockTwits sentiment, here's how six specialized AI agents using free LLMs provide surprisingly accurate trading signals.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Framework-green.svg)](https://github.com/crewAIInc/crewAI)

---

## 🎯 What This Does

This AI trading crew automates the entire daily stock research process using a team of specialized AI agents. Instead of manually browsing financial news, analyzing technical indicators, and monitoring social sentiment for hours each morning, you get **crystal-clear trading recommendations** in minutes.

**The system provides:**
- 🔍 **Comprehensive Market Analysis**: VIX volatility, global indices, currency movements
- 📰 **Breaking News Processing**: Dozens of articles from major financial sources  
- 📱 **Social Sentiment Analysis**: Thousands of StockTwits posts and retail trader sentiment
- 📊 **Technical Indicator Analysis**: 20+ indicators covering trend, momentum, volatility, and volume
- 🔮 **AI-Powered Forecasting**: Machine learning predictions using TimeGPT
- 💰 **Fundamental Analysis**: Financial ratios, analyst ratings, intrinsic value calculations
- ⚡ **Final Trading Signal**: Clear Bullish/Neutral/Bearish recommendation with confidence levels

### 🚀 Want to See This System in Action?

For a deep dive into how this AI agent system works in practice and to see a real-world example of the analysis in action, check out my detailed [hands-on demonstration and implementation guide](https://ostiguyphilippe.medium.com/d53bbc54075f). This article walks through the complete process and shows you exactly how the AI agents collaborate to generate trading insights.


---


## 🏗️ Architecture: How AI Agents Collaborate

The system follows a sophisticated three-phase approach:

### Phase 1: 🌍 Market Conditions Analysis
- Analyzes VIX volatility and global market environment
- Processes S&P 500 (SPY) as market overview indicator
- Monitors international indices, currencies, and overnight developments

### Phase 2: 🔍 Individual Stock Analysis (6 Specialized Agents)
1. **📰 News Summarizer Agent**: Processes breaking news from TipRanks, FinViz, Seeking Alpha, MarketWatch
2. **📱 Sentiment Summarizer Agent**: Analyzes 500+ StockTwits posts for retail sentiment
3. **📈 Technical Indicator Agent**: Calculates 20+ indicators (RSI, MACD, Bollinger Bands, etc.)
4. **🔮 TimeGPT Analyst Agent**: Machine learning forecasts using Nixtla's state-of-the-art model
5. **🔍 Fundamental Analysis Agent**: Financial health, valuation metrics, analyst opinions
6. **🎯 Day Trader Advisor Agent**: Synthesizes all data into actionable trading signals

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+ (< 3.13)
- [UV](https://docs.astral.sh/uv/) or [Poetry](https://python-poetry.org/) (recommended) or pip

### 1. Install CrewAI Framework

**Visit the official [CrewAI GitHub](https://github.com/crewAIInc/crewAI) for the latest installation instructions and requirements.**

```bash
# Using uv (recommended)
uv add crewai[tools]

# Or using poetry
poetry add "crewai[tools]"

# Or using pip
pip install "crewai[tools]"
```

### 2. Clone and Install the Project
```bash
# Clone the repository
git clone https://github.com/philippe-ostiguy/AITradingCrew.git
cd AITradingCrew

# Install with uv (recommended)
uv sync

# Or install with poetry
poetry install

# Or install with pip
pip install -e .
```

### 3. 🔑 Required API Keys

Create a `.env` file in the project root with the following API keys:

```bash
# LLM Provider (OpenRouter recommended)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_DEEPSEEK_R1=deepseek/deepseek-r1:free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Data Providers
TWELVE_API_KEY=your_twelvedata_api_key_here
TIMEGPT_API_KEY=your_nixtla_api_key_here
RAPID_API_KEY=your_rapidapi_key_here
```

### 🔑 How to Get API Keys (All Have Free Tiers):

1. **OpenRouter** (Free LLMs): [openrouter.ai](https://openrouter.ai) - Get free access to DeepSeek R1
2. **TwelveData** (Financial Data): [twelvedata.com](https://twelvedata.com) - Free tier available
3. **Nixtla TimeGPT** (Forecasting): [nixtla.io](https://nixtla.io) - AI forecasting API
4. **RapidAPI** (Social Data): [rapidapi.com](https://rapidapi.com) - For StockTwits sentiment data

### 4. 🎯 Run the System

```bash
# Simply run the trading crew
crewai run

# Or use the direct command
python -m ai_trading_crew.main
```

**That's it!** 🎉 The system will analyze your configured stocks and provide trading recommendations.

---

## 📊 Default Configuration

- **Analyzed Stocks**: AAPL, NVDA, MSFT, AMZN, GLD, GOOGL, TSLA
- **Market Overview**: SPY (S&P 500 ETF)
- **News Sources**: TipRanks, FinViz, Seeking Alpha, MarketWatch
- **Social Data**: 500 StockTwits posts per symbol
- **Technical Indicators**: 20+ indicators with 30-day historical context
- **Forecast Models**: TimeGPT 1-day ahead predictions

## 📝 Sample Output

```
**RECOMMENDATION**: Bullish  
**CONFIDENCE LEVEL**: High  

**KEY FACTORS**:  
- Dominant AI Leadership & Growth Catalysts: Q1 FY2026 Data Center revenue surged 73% YoY
- Technical Breakout Momentum: Price closed near 52-week highs with bullish MACD signals
- Overwhelming Social Sentiment: 213 bullish signals cite AI dominance and institutional FOMO
- ETF & Institutional Support: Top holding in semiconductor ETFs with record-high volume

**RETURN/RISK ASSESSMENT**: Upside to $150–$153 (5.3–6.6% gain) outweighs downside risk...

**TRADING RATIONALE**: Initiate long positions at market open, targeting breakout above $145.16...
```

---

## 🛠️ Customization

You can customize the analysis by modifying the configuration in `ai_trading_crew/config.py`:

- **Change Stock Symbols**: Update the `SYMBOLS` list
- **Adjust Data Limits**: Modify `NEWS_FETCH_LIMIT` and `SOCIAL_FETCH_LIMIT`  
- **Technical Indicators**: Customize periods and parameters
- **LLM Models**: Switch between different AI models

---

## ⚠️ Disclaimer

**This software is for informational purposes only and does not constitute financial advice.** Always conduct your own research or consult with a financial advisor before making any investment decisions. Past performance does not guarantee future results.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 💡 Liked this project? Show your support!

⭐ **Give the project a star**  
🤝 **Send me a [LinkedIn](https://www.linkedin.com/in/philippe-ostiguy/) connection request to stay in touch**

Happy automation! 🚀📈 
