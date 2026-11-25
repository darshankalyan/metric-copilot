# KPI: Unresolved Rate (Call Analytics)
Definition: Percentage of analysed calls where the customer's issue was not resolved by the end of the call.
Formula: calls with resolution_status = unresolved / total analysed calls * 100.
Rules:
- A call counts as resolved if the issue was fixed during the call, OR a fix was confirmed with a completion time under 48 hours.
- Promised callbacks without a confirmed time count as unresolved.
- Transferred calls are judged on the final segment only.
- This metric is independent of customer sentiment; see the Dissatisfaction Rate KPI.