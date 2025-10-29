import os
import warnings
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from crewai import LLM
from datetime import datetime, timedelta


# Suppress Pydantic v2 deprecation warnings from dependencies
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*PydanticDeprecatedSince20.*"
)


# Valid LLM providers
VALID_PROVIDERS = ["OPENROUTER"]

BASE_SYMBOLS = ["AAPL", "NVDA", "MSFT", "AMZN", "GLD", "GOOGL", "TSLA"]

# top_30_us = [
#     "MSFT", "NVDA", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "BRK.B", "TSM",
#     "WMT", "JPM", "V", "LLY", "MA", "NFLX", "ORCL", "COST", "XOM", "PG",
#     "JNJ", "HD", "SAP", "BAC", "ABBV", "KO", "NVO", "ASML", "PLTR", "PM"
# ]

#base_symbols.extend([s for s in top_30_us if s not in base_symbols])


class Settings(BaseSettings):
    """
    Pydantic v2 settings class using pydantic-settings.
    """
    model_config = SettingsConfigDict(
        env_file=".env",            # Automatically load variables from .env
        env_file_encoding="utf-8",  # Handle UTF-8 environment variables
        case_sensitive=True,        # Environment variable names are case-sensitive
        extra="ignore"              # Ignore extra env vars not defined here
    )

    SYMBOLS: List[str] = Field(
        default=BASE_SYMBOLS,
        description="Symbols to the analysis on."
    )


    STOCK_MARKET_OVERVIEW_SYMBOL: str = Field(
        default="SPY",
        description="Single stock market symbol to fetch market overview for."
    )


    TIME_SERIES_DEFAULTS: dict = Field(
        default={
            "nb_years": 5,
            "max_missing_data": 0.05,
            "data_folder": 'resources/data',
            "end_date_offset": 0,
        },
        description="Default time series parameters for TimeGPT functionality."
    )

    NEWS_FETCH_LIMIT: int = Field(
        default=20,
        description="Maximum number of news articles to fetch per symbol."
    )
    SOCIAL_FETCH_LIMIT: int = Field(
        default=500,
        description="Maximum number of social media posts to fetch per symbol."
    )
    TECHNICAL_INDICATOR_DEFAULTS: dict = Field(
        default={
            "adx_time_period": 21,
            "bbands_time_period": 20,
            "ema_time_period": 10,
            "macd_fast_period": 12,
            "macd_slow_period": 26,
            "percent_b_time_period": 21,
            "rsi_time_period": 21,
            "sma_time_period": 21,
            "stoch_fast_period": 14,
            "stoch_slow_period": 1,
            "stoch_d_period": 3,
            "cci_time_period": 20,
            "mom_time_period": 10,
            "willr_time_period": 14,
            "mfi_time_period": 14,
            "rsi_length": 21,
            "stoch_length": 14,
            "k_period": 3,
            "d_period": 3,
            "tenkan_period": 9,
            "kijun_period": 26,
            "senkou_span_b_period": 52
        },
        description="Default technical indicator parameters."
    )


    @property
    def time_series_dates(self):
        offset = self.TIME_SERIES_DEFAULTS["end_date_offset"]
        return {
            "end_date": datetime.today() - timedelta(days=offset),
            "start_date": datetime.today() - timedelta(days=offset) - timedelta(days=self.TIME_SERIES_DEFAULTS["nb_years"] * 365),
        }

    @field_validator("SYMBOLS")
    def parse_symbols(cls, value):
        if isinstance(value, str):
            return [symbol.strip() for symbol in value.split(",")]
        return value


def get_env_var(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
    return value


def create_default_llm(api: str, model: str, url: str) -> LLM:
    return LLM(
        api_key=get_env_var(api),
        model=get_env_var(model),
        base_url=get_env_var(url),
        temperature=0.0
    )


def extract_provider_name(model_name: str) -> str:
    """
    Extract provider name from model name string.
    Example: "OPENROUTER_GEMINI_2.5" -> "OPENROUTER"
    
    Raises ValueError if provider is not valid.
    """
    for provider in VALID_PROVIDERS:
        if model_name.startswith(provider):
            return provider
    
    raise ValueError(f"Model name '{model_name}' does not start with a valid provider: {', '.join(VALID_PROVIDERS)}")


#OpenRouter DeepSeek R1 is used for all LLM operations in the system

DEFAULT_PROJECT_LLM = "OPENROUTER_DEEPSEEK_R1"
DEFAULT_STOCKTWITS_LLM = create_default_llm("OPENROUTER_API_KEY", "OPENROUTER_DEEPSEEK_R1", "OPENROUTER_BASE_URL")
DEFAULT_TI_LLM = create_default_llm("OPENROUTER_API_KEY", "OPENROUTER_DEEPSEEK_R1", "OPENROUTER_BASE_URL")
DEEPSEEK_OPENROUTER_LLM = create_default_llm("OPENROUTER_API_KEY", "OPENROUTER_DEEPSEEK_R1", "OPENROUTER_BASE_URL")


OUTPUT_FOLDER  = "output"
AGENT_INPUTS_FOLDER = OUTPUT_FOLDER + "/agents_inputs"
AGENT_OUTPUTS_FOLDER = OUTPUT_FOLDER + "/agents_outputs"
LOG_FOLDER = "logs"

# File paths
RELEVANT_ARTICLES_FILE = "relevant_articles.txt"


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
if not os.path.exists(AGENT_INPUTS_FOLDER):
    os.makedirs(AGENT_INPUTS_FOLDER)
if not os.path.exists(AGENT_OUTPUTS_FOLDER):
    os.makedirs(AGENT_OUTPUTS_FOLDER)
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Extract provider name from model name
provider_name = extract_provider_name(DEFAULT_PROJECT_LLM)

PROJECT_LLM = create_default_llm(
    f"{provider_name}_API_KEY",
    DEFAULT_PROJECT_LLM,
    f"{provider_name}_BASE_URL"
)

# Instantiate settings object
settings = Settings()