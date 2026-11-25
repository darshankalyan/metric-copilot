# KPI: Customer Dissatisfaction Rate (Call Analytics)
Definition: Percentage of analysed calls in which the CUSTOMER expresses negative sentiment about the bank, its products or its service.
Formula: calls with customer sentiment = negative / total analysed calls * 100.
Rules:
- Sentiment is judged only from the customer's own words. Agent statements are ignored.
- Resolution status must NOT influence this metric. A polite customer with an unresolved issue is not dissatisfied; an angry customer whose issue was resolved IS dissatisfied.
- Calls shorter than 20 seconds or with no customer speech are excluded.
- Unresolved issues are tracked separately in the Unresolved Rate KPI.