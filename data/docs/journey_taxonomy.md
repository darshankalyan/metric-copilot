# Customer Journey Taxonomy (6 journeys)
- account_opening: new savings or current account, documents, verification status.
- card_activation: activating new or replacement debit/credit cards, PIN generation.
- fund_transfer: NEFT/IMPS/UPI transfers, failed or pending transfers, reversals.
- loan_disbursal: status and receipt of sanctioned loan amounts.
- kyc_update: address, phone, ID and other KYC detail changes.
- charges_and_fees: annual fees, penalty charges, fee reversal requests.
Rules:
- Each call maps to exactly one primary journey: the customer's first stated reason.
- If the classifier's confidence is below 0.6, map to "other" and send for manual review.
- Card PIN issues belong to card_activation, not charges_and_fees.