from typing import Dict, Any
from pathlib import Path


class ImuraFundReporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        report_file = self.report_dir / "report.md"
        with open(report_file, "w") as f:
            f.write(
                f"# Imura Fund Analysis Report\n\nAnalysis result: {analysis_payload}"
            )
        return {"report_path": str(report_file)}
