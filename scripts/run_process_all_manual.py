import subprocess
import sys
from datetime import datetime

commands = [
    # Fetch Phase
    "uv run python -m crew.imura.data_pipeline",
    "uv run python -m crew.oracle.data_pipeline",
    "uv run python -m crew.credit.data_pipeline",
    "uv run python -m crew.etf.data_pipeline",
    "uv run python -m crew.loan.data_pipeline",
    "uv run python -m crew.metals.data_pipeline",
    "uv run python -m crew.portfolio.data_pipeline",
    "uv run python -m crew.yields.data_pipeline",
    "uv run python -m crew.semiconductors.data_pipeline",
    "uv run python -m crew.legendary_investors.data_pipeline",
    # Analyze Phase
    "uv sync",
    "uv run ruff check . --fix",
    "uv run ruff format .",
    "uv run python -m crew.imura.analysis",
    "uv run python -m crew.oracle.analysis",
    "uv run python -m crew.credit.analysis",
    "uv run python -m crew.etf.analysis",
    "uv run python -m crew.loan.analysis",
    "uv run python -m crew.metals.analysis",
    "uv run python -m crew.portfolio.analysis",
    "uv run python -m crew.yields.analysis",
    "uv run python -m crew.use_case_runner semiconductors --config config/use_cases/semiconductors.yaml",
    "uv run python -m crew.use_case_runner legendary_investors --config config/use_cases/legendary_investors.yaml",
]


def run_commands():
    print(f"Starting process:all execution at {datetime.now()}")
    for cmd in commands:
        print(f"\nExample: Running command: {cmd}")
        try:
            # shell=True is used to properly handle arguments and uv execution environment
            result = subprocess.run(cmd, shell=True, check=True)
            print(f"Command finished with return code {result.returncode}")
        except subprocess.CalledProcessError as e:
            if "ruff" in cmd:
                print(f"Lint/Format command failed (non-critical): {cmd}")
                print(f"Return code: {e.returncode}")
                continue
            print(f"Error executing command: {cmd}")
            print(f"Return code: {e.returncode}")
            sys.exit(e.returncode)
    print(f"\nAll commands executed successfully at {datetime.now()}")


if __name__ == "__main__":
    run_commands()
