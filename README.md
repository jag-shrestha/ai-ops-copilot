# Sprint 1 - Deterministic Analysis
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
  
# Sprint 2 - AI Insight Generation
## What changed
- Merged in different matrices from Sprint 1 to create on main JSON having all information to provide to LLM.
- Written first level prompt with AI_Content JSON attached to it in order to derive summaried results
- Forced LLM to return data in given scheme

## Why
This acts as the first trial of result retrival which will further be analysed for refinement.


