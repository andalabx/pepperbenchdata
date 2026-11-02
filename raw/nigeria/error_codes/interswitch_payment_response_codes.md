For AI agents: the docs index is at https://docs.interswitchgroup.com/llms.txt. Append .md to any documentation page URL to get its markdown version.

All transactions are valid for `30 minutes`. Any response received after 30 minutes should be considered final.

## Response Codes and Transaction Status   [Skip link to Response Codes and Transaction Status](https://docs.interswitchgroup.com/docs/payment-response-codes\#response-codes-and-transaction-status)

Response codes may change as a transaction progresses, as customers can retry the transaction until it expires. However, the final response code will indicate whether the transaction was successful, failed, or expired.

## Webhooks   [Skip link to Webhooks](https://docs.interswitchgroup.com/docs/payment-response-codes\#webhooks)

For webhook responses, the event type `TRANSACTION.COMPLETED` indicates a final webhook event for a particular transaction. No further updates will be sent for that transaction.

| Response Description | Response Code | Status |
| --- | --- | --- |
| **Final Response Codes(customer cannot retry)** |  |  |
|  |  |  |
| Approved by Financial Institution, Partial | 10 | Successful |
| Approved by Financial Institution, VIP | 11 | Successful |
| Approved by Financial Institution | 00 | Successful |
| Transaction In Progress | 09 | Pending |
| Customer Cancellation | Z6 | Cancelled |
| **Other Responses** |  |  |
|  |  |  |
| Approved by Financial Institution | 00 | Successful |
| Refer to Financial Institution | 01 | Declined |
| Refer to Financial Institution, Special Condition | 02 | Declined |
| Invalid Merchant | 03 | Declined |
| pick-Up card | 04 | Declined |
| Don Not Honor | 05 | Declined |
| Error | 06 | Declined |
| Pick-Up Card, Special Condition | 07 | Declined |
| Honor with Identification | 08 | Declined |
| Request In Progress | 09 |  |
| Partially Approved by Financial Institution | 10 | Successful |
| Approved by Financial Institution, VIP | 11 |  |
| Invalid Transaction | 12 | Declined |
| Invalid Amount | 13 | Declined |
| Invalid Card Number | 14 | Declined |
| No Such Financial Institution | 15 | Declined |
| Approved by Financial Institution, Update Track 3 | 16 |  |
| Customer Cancellation | 17 | Declined |
| Customer Dispute | 18 | Declined |
| Re-enter Transaction | 19 | Declined |
| Invalid Response From Financial Institution | 20 | Declined |
| No Action Taken by Financial Institution | 21 | Declined |
| Suspected Malfunction | 22 | Declined |
| Unacceptable Transaction Fee | 23 | Declined |
| File Update not Supported | 24 | Declined |
| Unable to Locate Record | 25 | Declined |
| Duplicate Record | 26 | Declined |
| First Update File Edit Error | 27 | Declined |
| File Update File Locked | 28 | Declined |
| File Update Failed | 29 | Declined |
| Format Error | 30 | Declined |
| Bank Not Supported | 31 | Declined |
| Completed Partially by Financial | 32 | Declined |
| Expired Card, Pick-Up | 33 | Declined |
| Suspected Fraud, Pick-Up | 34 | Declined |
| Restricted Card, Pick-Up | 36 | Declined |
| Incorrect Security Details Provided. PIN Tries Exceeded, Pick-Up | 38 | Declined |
| No Credit Account | 39 | Declined |
| Function not Supported | 40 | Declined |
| Lost Card, Pick-Up | 41 | Declined |
| No Universal Account | 42 | Declined |
| Stolen Card, Pick-Up Stolen Card, Pick-Up | 43 | Declined |
| No Investment Account | 44 | Declined |
| Declined by Bank for custom reasons | 45 | Declined |
| Declined by Bank for custom reasons | 46 | Declined |
| Declined by Bank for custom reasons | 47 | Declined |
| No customer record | 48 | Declined |
| Insufficient Funds | 51 | Declined |
| No Check Account | 52 | Declined |
| No Savings Account | 53 | Declined |
| Expired Card | 54 | Declined |
| Incorrect PIN | 55 | Declined |
| No Card Record | 56 | Declined |
| Transaction not Permitted to Cardholder | 57 | Declined |
| Transaction not Permitted on Terminal | 58 | Declined |
| Suspected Fraud | 59 | Declined |
| Contact Acquirer | 60 | Declined |
| Exceeds Withdrawal Limit | 61 | Declined |
| Restricted Card | 62 | Declined |
| Security Violation | 63 | Declined |
| Original Amount Incorrect | 64 | Declined |
| Exceeds withdrawal frequency | 65 | Declined |
| Call Acquirer Security | 66 | Declined |
| Hard Capture | 67 | Declined |
| Response Received Too Late | 68 | Declined |
| Incorrect Security Details Provided. PIN tries exceeded | 75 | Declined |
| Reserved for Future Postilion Use | 76 | Declined |
| Intervene, Bank Approval Required | 77 | Declined |
| Intervene, Bank Approval Required for Partial Amount | 78 | Declined |
| Invalid Digital Signature | 79 | Declined |
| Declined by Bank for custom reasons | 81 | Declined |
| Declined by Bank for custom reasons | 82 | Declined |
| Declined by Bank for custom reasons | 83 | Declined |
| Declined by Bank for custom reasons | 86 | Declined |
| Information not on file | 88 | Declined |
| Declined by Bank for custom reasons | 89 | Declined |
| Cut-off in Progress | 90 | Declined |
| Issuer or Switch Inoperative | 91 | Declined |
| Routing Error | 92 | Declined |
| Violation of law | 93 | Declined |
| Duplicate Transaction | 94 | Declined |
| Reconcile Error | 95 | Declined |
| System Malfunction | 96 | Declined |
| Declined by Bank for custom reasons | 97 | Declined |
| Exceeds Cash Limit | 98 | Declined |
| Declined by Bank for custom reasons | 99 | Declined |
| Unexpected Error | A0 | Declined |
| Transaction not Permitted to Card Holder, via channels | A4 | Declined |
| Stock has finished | A8 | Declined |
| Incorrect Phone Number | A9 | Declined |
| An unknown error has occurred, please contact system administrator. | E21 | Declined |
| Interswitch processing error | E42 | Declined |
| Interswitch processing error | E53 | Declined |
| Interswitch processing error | E60 | Declined |
| Declined by Bank for custom reasons | F4 | Declined |
| Declined by Bank for custom reasons | F5 | Declined |
| Declined by Bank for custom reasons | G3 | Declined |
| Declined by Bank for custom reasons | G4 | Declined |
| Declined by Bank for custom reasons | H4 | Declined |
| Time Out calling postilion service | S0 | Requery |
| Fraud Service Declined Transaction | S3 | Declined |
| Error processing transaction | SK | Declined |
| Exceeds Maximum Amount Allowed | X03 | Declined |
| Minimum Amount for Payment Item Not Met | X04 | Declined |
| The Amount Requested is above the Limit permitted by your Bank, please contact your Bank | X05 | Declined |
| Cannot Retrieve Collections Account | XGO | Declined |
| Successfully Retrieved Collections Account | XG1 | Declined |
| Exceeded time period to complete transaction | XS1 | Declined |
| Error processing transaction | XX | Declined |
| Transaction Not Completed | Z0 |  |
| Transaction Error | Z1 | Declined |
| Bank Account Error | Z2 | Declined |
| Bank Collections Account Error | Z3 | Declined |
| Interface Integration Error | Z4 | Declined |
| Duplicate Reference Error | Z5 | Declined |
| Incomplete Transaction | Z6 | Declined |
| Transaction Split Pre-Processing Error | Z7 | Declined |
| Invalid Card Number, via Channels | Z8 | Declined |
| Transaction not Found | Z25 | Declined |
| Recurrent transaction rate limit exceeded | Z162 | Declined |
| Payment Requires Token | Z61 |  |
| Request to Generate Token is Successful | Z62 |  |
| Token Not Generated. Customer Not Registered on Token Platform | Z63 |  |
| Error Occurred. Could Not Generate Token | Z64 |  |
| Payment Requires Token Authorization | Z65 |  |
| Token Authorization Successful | Z66 |  |
| Token Authorization Not Successful. Incorrect Token Supplied | Z67 |  |
| Error Occurred. Could Not Authenticate Token | Z68 |  |
| Customer Cancellation Secure3D | Z69 |  |
| Cardinal Authentication Required | Z70 |  |
| Cardinal Lookup Successful | Z71 |  |
| Cardinal Lookup Failed | Z72 |  |
| Cardinal Authenticate Successful | Z73 |  |
| Cardinal Authenticate Failed | Z74 |  |
| Wibmo Lookup Successful | Z76 |  |
| Wibmo Lookup Failed | Z77 |  |
| Error calling Cybersource Service | Z80 |  |
| Bin has not been configured | Z81 |  |
| Merchant not configured for BIN | Z82 |  |
| This is a http response that is returned on the API for different reasons(e.g; "Bad Request", "Card has expired", Correct pin not found, etc | 10400 |  |
| This is a http response that is returned on the API for different reasons | 10403 |  |
| This is a http response that is returned on the API for different reasons | 10500 |  |
| Cardholder not enrolled for OTP | M0 |  |
| Payment requires authentication | T0 |  |
| No Response received for 3DS auth | T1 |  |

**Refund API Response Codes**

Please refer to the standard HTTP response codes. Where anything starting with 2XX signifies approved, 4XX means client error and 5XX indicates server error. When the response codes start with 4XX or 5XX, an error object will be returned to explain further the reason for this failure. Find common response codes and their descriptions below:

| Code | Description |
| --- | --- |
| 60002 | Refund amount greater than transaction amount |
| 10400 | Error creating refund: This refund reference has already been used. |
| 10500 | Error processing request, please try again. |
| 404 | Transaction not found for merchant |
| 400 | Error creating refund: refund amount greater than transaction amount |
| 500 | Could not validate refund. |

**Other 10400 code meaning**

| Case | Error Description |
| --- | --- |
| If parent payment id or parent transaction reference is not passed | Please provide the initial transaction details |
| If transaction is found but id is null | Invalid transaction not found |
| If merchant code on parent transaction is not the merchant code of the merchant | User operation unauthorized |
| If merchant code on parent transaction does not match with merchant code passed | Invalid transaction. cannot perform refund on their transaction. |
| If transaction is not successful | Invalid transaction. Only successful transactions can be refunded |
| If transaction is a split transaction | Cannot perform refund on split transaction |
| If payment has non card provider id as credit | Cannot perform refund on this transaction |
| If currency code of transaction is not supported | Cannot perform refund on this transaction |
| If payment channel is not supported for refund | Cannot perform refund on this transaction |
| If refund has been created for the parent transaction | Transaction has been refunded or is logged for refunds |
| If transaction is older than certain number of days | Cannot refund transaction older than - days |
| If transaction account number cannot be retrieved | Refund account number not found |
| If parent transaction is not found or it has no response code | Could not validate refund |
| If refund amount is null | Please provide a refund Amount for the PARTIAL refund |
| If refund type or amount is null | Please provide a refund Type or a refund Amount |
| If refund is not full or partial | Invalid refund type |
| If refund amount is below minimum refundable amount | Refund amount cannot be less than minimum amount |
| If refund is full and refund amount is greater than parent transaction amount | Refund amount cannot exceed the transaction amount |

Updated6 months ago

* * *

Did this page help you?

Yes

No

Copy Page