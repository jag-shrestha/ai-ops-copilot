Post Commit 1
## What changed
- Added  Savings report parser
- Added portfolio-level KPI calculations - Statistics Matrix
- Added site-level performance analysis - Site Health Matrix
- Added negative/zero savings identification - Data Quality Checks
- Added structured analysis output - JSON made up of DQ, Statistics and Site Health JSONs

## Why
This acts as a deterministic analysis layer that will later feed the AI insight generation layer.

## Testing
- Tested against a June 2026 report
- Validated portfolio totals against source report
- Tested missing values
- Tested negative savings
