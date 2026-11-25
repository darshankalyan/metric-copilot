# QC Checklist: Monthly CX Release
Run all checks before any dashboard or report reaches the client.
1. Row-count reconciliation: fact table valid rows must equal the source extract exactly (0% tolerance).
2. Freshness: max(response_date) must be within 3 days of the refresh date; otherwise the model is stale.
3. Journey NPS movement: flag any journey whose NPS changes by more than 15 points month-over-month for analyst review.
4. Trend arrows: arrow direction must equal sign(current period - previous period). Up = improved.
5. Base size: hide journey NPS below 30 responses (see the NPS KPI).
6. Sentiment-resolution independence: if more than 90% of unresolved calls are labelled negative, re-check the sentiment prompt.
Log every failure in the issue log with date, check number and fix.