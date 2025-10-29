#!/usr/bin/env python
import asyncio
import datetime
import os
import pandas as pd
import pickle
from ai_trading_crew.crew import StockComponentsSummarizeCrew, AiArticlesPickerCrew, DayTraderAdvisorCrew
from ai_trading_crew.analysts.social import get_stocktwits_context
from ai_trading_crew.analysts.technical_indicators import get_ti_context
from ai_trading_crew.utils.company_info import get_company_name
from ai_trading_crew.analysts.fundamental_analysis import get_fundamental_context
from ai_trading_crew.analysts.timegpt import format_timegpt_forecast
from ai_trading_crew.config import settings, RELEVANT_ARTICLES_FILE, AGENT_INPUTS_FOLDER, AGENT_OUTPUTS_FOLDER
from ai_trading_crew.utils.dates import get_today_str, get_yesterday_str, get_yesterday_18_est, get_today_str_no_min
from ai_trading_crew.analysts.stock_headlines_fetcher import get_news_context
from ai_trading_crew.analysts.stock_articles_fetcher import get_stock_news


def load_timegpt_forecasts():
    """
    Load TimeGPT forecasts from pickle file in agents_inputs folder with current date.
    If the file doesn't exist, return an empty DataFrame.
    """
    today_str_no_min = get_today_str_no_min()
    input_dir = os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min)
    pickle_file = os.path.join(input_dir, "timegpt_forecasts.pkl")
    
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)
    else:
        # Return empty DataFrame if no cached forecasts available
        print(f"Warning: {pickle_file} not found. TimeGPT forecasts will not be available.")
        return pd.DataFrame()


async def process_stock_symbol(symbol, vix_data={}, global_market_data={}, additional_agents=None, additional_tasks=None):
    """
    Process a stock symbol by gathering all necessary data and running the analysis crews.
    
    Args:
        symbol: Stock symbol to process
        vix_data: VIX data (optional, for market overview)
        global_market_data: Global market data (optional, for market overview)
        additional_agents: Additional agents for the crew (optional, for market overview)
        additional_tasks: Additional tasks for the crew (optional, for market overview)
    """
    today_str = get_today_str()
    today_str_no_min = get_today_str_no_min()
    yesterday_str = get_yesterday_str()
    YESTERDAY_HOUR = "18:00"  # 6 PM EST
    HISTORICAL_DAYS = 30
    
    # Create directories if they don't exist
    input_dir = os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min)
    output_dir = os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, symbol)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get company name
    company_name = get_company_name(symbol)
    
    # Get stock headlines
    stock_headlines = get_news_context(
        symbol=symbol,
        start_time=f"{yesterday_str} {YESTERDAY_HOUR}"
    )
    
    # Save market headlines to file
    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_market_headlines.txt"), "w") as f:
        f.write(stock_headlines)
    
    # Run AiArticlesPickerCrew
    inputs = {
        'company_name': company_name,
        'stocktwits_data': {},
        'stock_headlines': stock_headlines,
        'today_str': today_str,
    }
    
    await AiArticlesPickerCrew(symbol).crew().kickoff_async(inputs=inputs)
    
    # Get and save stock news
    stock_news = await get_stock_news(symbol, os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_{RELEVANT_ARTICLES_FILE}"))
    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_stock_news.txt"), "w") as f:
        f.write(stock_news)
    
    # Get and save technical indicators
    ti_data = get_ti_context(symbol=symbol)
    
    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_technical_indicators.txt"), "w") as f:
        f.write(ti_data)
    

    fundamental_data = get_fundamental_context(symbol=symbol)

    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_fundamental_analysis.txt"), "w") as f:
        f.write(fundamental_data)
    
    # Get and save stocktwits data
    stocktwits_data = get_stocktwits_context(
        symbol,
        settings.SOCIAL_FETCH_LIMIT,
        get_yesterday_18_est()
    )
    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_stocktwits.txt"), "w") as f:
        f.write(stocktwits_data)
    
    # Load real TimeGPT forecasts from pickle file
    timegpt_forecasts = load_timegpt_forecasts()
    
    # Get formatted TimeGPT forecast for this symbol
    timegpt_forecast = format_timegpt_forecast(timegpt_forecasts, symbol, company_name)
    
    with open(os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f"{symbol}_timegpt_forecast.txt"), "w") as f:
        f.write(timegpt_forecast)
    
    # Prepare final inputs
    final_inputs = {
        'company_name': company_name,
        'stocktwits_data': stocktwits_data,
        'technical_indicator_data': ti_data,
        'fundamental_analysis_data': fundamental_data,
        'timegpt_forecast': timegpt_forecast,
        'stock_headlines': stock_headlines,
        'stock_news': stock_news,
        'vix_data': vix_data or {},
        'global_market_data': global_market_data or {},
        'today_str': today_str,
        'historical_days': HISTORICAL_DAYS
    }
    
    # Run StockComponentsSummarizeCrew
    crew_result = await StockComponentsSummarizeCrew(
        symbol,
        additional_agents=additional_agents,
        additional_tasks=additional_tasks
    ).crew().kickoff_async(inputs=final_inputs)
    
    # After summaries are complete, run the Day Trader Advisor
    # Read the generated summary files
    def read_summary_file(symbol_folder, filename):
        """Helper function to read summary files safely"""
        file_path = os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, symbol_folder, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
       
    # Read individual stock summaries
    news_summary = read_summary_file(symbol, "news_summary_report.md")
    sentiment_summary = read_summary_file(symbol, "sentiment_summary_report.md")
    technical_summary = read_summary_file(symbol, "technical_indicator_summary_report.md")
    fundamental_summary = read_summary_file(symbol, "fundamental_analysis_summary_report.md")
    timegpt_summary = read_summary_file(symbol, "timegpt_forecast_summary_report.md")
    
    # Read market analysis summaries (using the market overview symbol)
    market_news_summary = read_summary_file(settings.STOCK_MARKET_OVERVIEW_SYMBOL, "news_summary_report.md")
    market_sentiment_summary = read_summary_file(settings.STOCK_MARKET_OVERVIEW_SYMBOL, "sentiment_summary_report.md")
    market_technical_summary = read_summary_file(settings.STOCK_MARKET_OVERVIEW_SYMBOL, "technical_indicator_summary_report.md")
    market_timegpt_summary = read_summary_file(settings.STOCK_MARKET_OVERVIEW_SYMBOL, "timegpt_forecast_summary_report.md")
    market_overview_summary = read_summary_file(settings.STOCK_MARKET_OVERVIEW_SYMBOL, "market_overview_summary_report.md")
    
    # Prepare inputs for Day Trader Advisor
    day_trader_inputs = {
        'company_name': company_name,
        'news_summary': news_summary,
        'sentiment_summary': sentiment_summary,
        'technical_summary': technical_summary,
        'fundamental_summary': fundamental_summary,
        'timegpt_summary': timegpt_summary,
        'market_news_summary': market_news_summary,
        'market_sentiment_summary': market_sentiment_summary,
        'market_technical_summary': market_technical_summary,
        'market_timegpt_summary': market_timegpt_summary,
        'market_overview_summary': market_overview_summary
    }
    
    # Run Day Trader Advisor Crew
    day_trader_result = await DayTraderAdvisorCrew(symbol).crew().kickoff_async(inputs=day_trader_inputs)
    
    return crew_result


def process_stock_symbol_sync(symbol, vix_data={}, global_market_data={}, additional_agents=None, additional_tasks=None):
    """
    Synchronous wrapper for process_stock_symbol that maintains backward compatibility.
    
    Args:
        symbol: Stock symbol to process
        vix_data: VIX data (optional, for market overview)
        global_market_data: Global market data (optional, for market overview)
        additional_agents: Additional agents for the crew (optional, for market overview)
        additional_tasks: Additional tasks for the crew (optional, for market overview)
    """
    return asyncio.run(process_stock_symbol(symbol, vix_data, global_market_data, additional_agents, additional_tasks))