# Pages audit contract

The Pages workflow must complete the following gates before deployment:

1. compile the `web/` Python modules;
2. build every publishable report under `output/use_cases/`;
3. reject ambiguous report sources unless a canonical `report.md` or `analysis_report.md` exists;
4. validate the site manifest against generated case and report pages;
5. reject unresolved templates, legacy UI fragments, broken local links, and paths escaping `docs/`;
6. upload and deploy the artifact only after all gates pass.

Multi-file analytical outputs may remain in their source directory, but one concise canonical report must identify the public reading view.
