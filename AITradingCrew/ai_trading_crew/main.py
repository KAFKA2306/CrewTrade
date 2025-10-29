#!/usr/bin/env python
import asyncio
import os
import sys
import warnings
import pytz
import pandas as pd
import datetime
from ai_trading_crew.config import settings
from ai_trading_crew.analysts.market_overview import HistoricalMarketFetcher
from ai_trading_crew.market_overview_agents import MarketOverviewAnalyst
from ai_trading_crew.stock_processor import process_stock_symbol_sync as process_stock_symbol, process_stock_symbol as process_stock_symbol_async
from ai_trading_crew.crew import StockComponentsSummarizeCrew
from ai_trading_crew.analysts.timegpt import get_timegpt_forecast

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew using async for maximum performance.
    """
    asyncio.run(run_async_execution())
    

async def run_async_execution():
    """
    Run the crew asynchronously with concurrent processing.
    """
    
    vix_data = HistoricalMarketFetcher().get_vix(days=30)
    global_market_data = HistoricalMarketFetcher().get_global_market(days=30)
    
    # Create market overview analyst for additional agents/tasks
    market_analyst = MarketOverviewAnalyst()
    market_agent, market_task = market_analyst.get_agent_and_task()
    
    # Get TimeGPT forecasts (calls API once per day, uses cache thereafter)
    timegpt_forecasts = get_timegpt_forecast()
    
    # Process market overview first
    await process_stock_symbol_async(
        settings.STOCK_MARKET_OVERVIEW_SYMBOL,
        vix_data=vix_data,
        global_market_data=global_market_data,
        additional_agents=[market_agent],
        additional_tasks=[market_task]
    )
    
    # Process individual symbols concurrently for maximum performance
    tasks = []
    for symbol in settings.SYMBOLS:
        task = process_stock_symbol_async(symbol)
        tasks.append(task)
    
    # Wait for all symbol processing to complete
    await asyncio.gather(*tasks)


async def run_async():
    """
    Run the crew asynchronously for better performance.
    """
    
    # Keep only essential data as requested
    vix_data = HistoricalMarketFetcher().get_vix(days=30)
    global_market_data = HistoricalMarketFetcher().get_global_market(days=30)
    
    # Create market overview analyst for additional agents/tasks
    market_analyst = MarketOverviewAnalyst()
    market_agent, market_task = market_analyst.get_agent_and_task()
    
    # Process market overview symbol first
    await process_stock_symbol_async(
        settings.STOCK_MARKET_OVERVIEW_SYMBOL,
        vix_data=vix_data,
        global_market_data=global_market_data,
        additional_agents=[market_agent],
        additional_tasks=[market_task]
    )
    
    # Process individual symbols concurrently for maximum performance
    tasks = []
    for symbol in settings.SYMBOLS:
        task = process_stock_symbol_async(symbol)
        tasks.append(task)
    
    # Wait for all symbol processing to complete
    await asyncio.gather(*tasks)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'symbol': settings.SYMBOLS,
        'current_time_est': datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
    }
    
    StockComponentsSummarizeCrew().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs=inputs
    )

def replay():
    """
    Replay the crew execution from a specific task.
    """
    StockComponentsSummarizeCrew().crew().replay(task_id=sys.argv[1])

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    StockComponentsSummarizeCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)


def run_fast():
    """
    Run the crew using async for maximum performance.
    """
    asyncio.run(run_async())