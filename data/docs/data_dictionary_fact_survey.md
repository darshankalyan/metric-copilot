# Data Dictionary: analytics.fact_survey_response
Grain: one row per valid survey response.
Columns:
- response_id (PK), customer_id, journey_id (FK to dim_journey), date_id (FK to dim_date)
- region_id (FK to dim_region), channel_id (FK to dim_channel: app, branch, call centre, web)
- segment_id (FK to dim_segment: mass, affluent, NRI), nps_score (0-10, nullable)
- verbatim (free-text comment), language_code (ISO 639-1, e.g. hi, kn, ta, en)
Notes:
- NPS is calculated from this table; never pre-aggregate scores before applying the 30-response base rule.
- Deleted or test responses are flagged with is_valid = false and must be filtered out.