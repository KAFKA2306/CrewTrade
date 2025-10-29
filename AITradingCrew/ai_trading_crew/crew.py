from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import yaml
from ai_trading_crew.config import settings, DEFAULT_STOCKTWITS_LLM, PROJECT_LLM, DEFAULT_TI_LLM, DEEPSEEK_OPENROUTER_LLM, AGENT_OUTPUTS_FOLDER, AGENT_INPUTS_FOLDER, RELEVANT_ARTICLES_FILE, LOG_FOLDER
from ai_trading_crew.utils.dates import get_today_str, get_yesterday_str, get_today_str_no_min
import inspect

today_str = get_today_str()
yesterday_str = get_yesterday_str()
today_str_no_min = get_today_str_no_min()
yesterday_str = get_yesterday_str()
YESTERDAY_HOUR = "18:00"  # 6 PM EST
HISTORICAL_DAYS = 30


def ensure_log_date_folder():
	"""Ensure the log folder for today's date exists"""
	log_date_folder = os.path.join(LOG_FOLDER, today_str_no_min)
	if not os.path.exists(log_date_folder):
		os.makedirs(log_date_folder)
	return log_date_folder


class BaseCrewClass:
	"""Base class for all AI trading crews"""
	
	
	def __init__(self, symbol, stocktwit_llm=DEFAULT_STOCKTWITS_LLM, technical_ind_llm=DEFAULT_TI_LLM):
		self.symbol = symbol
		self.stocktwit_llm = stocktwit_llm
		self.technical_ind_llm = technical_ind_llm



@CrewBase
class AiArticlesPickerCrew(BaseCrewClass):
	"""AiTradingCrew crew base"""
	
	agents_config = 'config/agents_article.yaml'
	tasks_config = 'config/tasks_article.yaml'

	def __init__(self, symbol, stocktwit_llm=DEFAULT_STOCKTWITS_LLM, technical_ind_llm=DEFAULT_TI_LLM):
		super().__init__(symbol, stocktwit_llm, technical_ind_llm)

	@agent
	def relevant_news_filter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['relevant_news_filter_agent'],
			verbose=True,
			llm=DEEPSEEK_OPENROUTER_LLM
		)

	@task  # UN-commented but kept inactive through crew configuration
	def relevant_news_filter_task(self) -> Task:
		config = self.tasks_config['relevant_news_filter_task'].copy()
		
		return Task(
			config=config,
			output_file=os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min, f'{self.symbol}_{RELEVANT_ARTICLES_FILE}'),
			verbose=True
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the AiTradingCrew crew"""
		ensure_log_date_folder()
		return Crew(
			agents=[self.relevant_news_filter_agent()],
			tasks=[self.relevant_news_filter_task()],
			process=Process.sequential,
			verbose=True,
			output_log_file=os.path.join(LOG_FOLDER, today_str_no_min, f"ai_articles_picker_{self.symbol}_{today_str_no_min}.log")
		)

@CrewBase
class StockComponentsSummarizeCrew(BaseCrewClass):
	"""AiTradingCrew crew"""
	
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, symbol, stocktwit_llm=DEFAULT_STOCKTWITS_LLM, technical_ind_llm=DEFAULT_TI_LLM, additional_agents=None, additional_tasks=None):
		super().__init__(symbol, stocktwit_llm, technical_ind_llm)
		self.additional_agents = additional_agents or []
		self.additional_tasks = additional_tasks or []

	@agent
	def news_summarizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_summarizer_agent'],
			verbose=True,
			llm=DEEPSEEK_OPENROUTER_LLM
		)

	@agent  # UN-commented but kept inactive through crew configuration
	def sentiment_summarizer_agent(self) -> Agent:

		return Agent(
			config=self.agents_config['sentiment_summarizer_agent'],
			verbose=True,
			llm=self.stocktwit_llm
		)

	@agent
	def technical_indicator_summarizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_indicator_summarizer_agent'],
			verbose=True,
			llm=self.technical_ind_llm
		)

	@agent
	def fundamental_analysis_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['fundamental_analysis_agent'],
			verbose=True,
			llm=PROJECT_LLM
		)

	@agent
	def timegpt_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['timegpt_analyst_agent'],
			verbose=True,
			llm=PROJECT_LLM
		)


	@task
	def news_summarization_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_summarization_task'],
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'news_summary_report.md'),
			verbose=True,
			
		)


	@task  # UN-commented but kept inactive through crew configuration
	def sentiment_summarization_task(self) -> Task:
		config = self.tasks_config['sentiment_summarization_task'].copy()
		
		return Task(
			config=config,
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'sentiment_summary_report.md'),
			llm=self.stocktwit_llm,
			verbose=True
		)

	@task
	def technical_indicator_summarization_task(self) -> Task:
		config = self.tasks_config['technical_indicator_summarization_task'].copy()
		return Task(
			config=config,
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'technical_indicator_summary_report.md'),
			llm=self.technical_ind_llm,
			verbose=True
		)

	@task
	def fundamental_analysis_task(self) -> Task:
		config = self.tasks_config['fundamental_analysis_task'].copy()
		return Task(
			config=config,
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'fundamental_analysis_summary_report.md'),
			llm=PROJECT_LLM,
			verbose=True
		)

	@task
	def timegpt_forecast_task(self) -> Task:
		config = self.tasks_config['timegpt_forecast_task'].copy()
		return Task(
			config=config,
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'timegpt_forecast_summary_report.md'),
			verbose=True,
		
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the AiTradingCrew crew"""
		ensure_log_date_folder()
		# Combine main agents/tasks with additional ones
		main_agents = [
			self.news_summarizer_agent(),
			self.sentiment_summarizer_agent(),
			self.technical_indicator_summarizer_agent(),
			self.fundamental_analysis_agent(),
			self.timegpt_analyst_agent()
		]
		main_tasks = [
			self.news_summarization_task(),
			self.sentiment_summarization_task(),
			self.technical_indicator_summarization_task(),
			self.fundamental_analysis_task(),
			self.timegpt_forecast_task()
		]
		
		all_agents = main_agents + self.additional_agents
		all_tasks = main_tasks + self.additional_tasks
		
		return Crew(
			agents=all_agents,
			tasks=all_tasks,
			process=Process.sequential,  # Keep sequential for proper dependency handling
			verbose=True,
			output_log_file=os.path.join(LOG_FOLDER, today_str_no_min, f"stock_components_summarize_{self.symbol}_{today_str_no_min}.log")
		)

class DayTraderAdvisorCrew:
	"""Day Trader Advisor crew for making trading recommendations based on summaries"""
	
	def __init__(self, symbol):
		self.symbol = symbol
		# Load configurations
		config_dir = os.path.join(os.path.dirname(__file__), 'config')
		
		with open(os.path.join(config_dir, 'agents_day_trader.yaml'), 'r') as f:
			self.agents_config = yaml.safe_load(f)
		
		with open(os.path.join(config_dir, 'tasks_day_trader.yaml'), 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	def day_trader_advisor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['day_trader_advisor_agent'],
			verbose=True,
			llm=DEEPSEEK_OPENROUTER_LLM
		)

	def day_trader_recommendation_task(self) -> Task:
		task_config = self.tasks_config['day_trader_recommendation_task']
		return Task(
			description=task_config['description'],
			expected_output=task_config['expected_output'],
			agent=self.day_trader_advisor_agent(),
			output_file=os.path.join(AGENT_OUTPUTS_FOLDER, today_str_no_min, self.symbol, 'day_trading_recommendation.md'),
			verbose=True
		)

	def crew(self) -> Crew:
		"""Creates the Day Trader Advisor crew"""
		ensure_log_date_folder()
		return Crew(
			agents=[self.day_trader_advisor_agent()],
			tasks=[self.day_trader_recommendation_task()],
			process=Process.sequential,
			verbose=True,
			output_log_file=os.path.join(LOG_FOLDER, today_str_no_min, f"day_trader_advisor_{self.symbol}_{today_str_no_min}.log")
		)
