from crewai import Agent, Task
from ai_trading_crew.config import PROJECT_LLM, AGENT_OUTPUTS_FOLDER, settings
from ai_trading_crew.utils.dates import get_today_str_no_min
import yaml
import os


today_str_no_min = get_today_str_no_min()


class MarketOverviewAnalyst:
    """Market Overview Analysis crew component"""
    
    def __init__(self, symbol = settings.STOCK_MARKET_OVERVIEW_SYMBOL):
        """Initialize with config loading"""
        # Load configurations
        self.symbol = symbol
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        
        with open(os.path.join(config_dir, 'agents.yaml'), 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        with open(os.path.join(config_dir, 'tasks.yaml'), 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    def market_overview_agent(self) -> Agent:
        """Creates the market overview agent"""
        return Agent(
            config=self.agents_config['market_overview_agent'],
            verbose=False,
            llm=PROJECT_LLM
        )

    def market_overview_task(self) -> Task:
        """Creates the market overview analysis task"""
        agent = self.market_overview_agent()
        task_config = self.tasks_config['market_overview_task']
        
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=agent,
            verbose=False,
            output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'market_overview_summary_report.md')
        )

    def get_agent_and_task(self):
        """Returns the agent and task for use with additional_agents and additional_tasks"""
        agent = self.market_overview_agent()
        task = self.market_overview_task()
        return agent, task