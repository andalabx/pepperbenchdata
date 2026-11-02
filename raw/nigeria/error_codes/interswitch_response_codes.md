For AI agents: the docs index is at https://docs.interswitchgroup.com/llms.txt. Append .md to any documentation page URL to get its markdown version.

| Status Code | Description |  |
| --- | --- | --- |
| 00 | Transaction Approved |  |
| 51 | Insufficient Funds |  |
| 55 | Incorrect PIN |  |
| 91 | Issuer or switch inoperative |  |
| 30 | Format Error |  |
| 06 | Error |  |
| 57 | Transaction not permitted to cardholder |  |
| 58 | Transaction not permitted to terminal |  |
| 59 | Suspected Fraud |  |
| 92 | Routing Error |  |
| 96 | System Malfunction |  |
| 63 | Security Violation |  |
| 70120 | Beneficiary bank service Unavailability | Indicates service unavailability of the third-party service provider (eg beneficiary bank, Billers etc) |

## Response Codes for Cashout   [Skip link to Response Codes for Cashout](https://docs.interswitchgroup.com/docs/response-codes-1\#response-codes-for-cashout)

| Status Code | Params | Values/Description |
| --- | --- | --- |
| 1 | app | Transfer |
| 2 | merchantId | Merchant ID: 15 alphanumeric characters |
| 3 | terminalType | Terminal Type: E.g PAX, Verifone, Telpo,<br>Ingenico |
| 4 | terminalId | Terminal ID: 8 alphanumeric characters |
| 5 | uniqueId | Terminal/device Serial number (read from the<br>sdk) |
| 6 | merchantLoc | Merchant name/address/location |
| 7 | batteryInformation | Terminal Battery percentage (read from the<br>sdk) |
| 8 | transactionDate | Current Transaction Time (YYYY-MM-DD T<br>HH:MM:SS)<br>T is the separator |
| 9 | printerStatus | Printer Status: 1 = paper present, 0 = no<br>paper/out of paper/ no printer / faulty<br>printer) |
| 10 | languageInfo | Device language: EN |
| 11 | posConditionCode | POS condition code: n2 |
| 12 | posGeoCode | POS geographical code: n38 |
| 13 | TerminalCurrencyCode | Currency code: n3 |
| 14 | originalTransmissionDateTime | Last transaction time (YYYY-MM-DDTHH:MM:SS) |
| 15 | stan | Transaction stan |
| 16 | minorAmount | Transaction amount in minor (i.e: if amount<br>is N1, this value would be 1 multiplied by<br>100 to give 100) |
| 17 | track2 | Track2 data of customer’s card |
| 18 | pinData | pindata(for online PIN transactions) |
| 19 | ksn | Key serial number |
| 20 | ksnd | Value = 605 |
| 21 | fromAccount | Card account type (savings, current, credit,<br>default) |
| 22 | posDataCode | POS Data Code |
| 23 | posEntryMode | POS Entry mode |
| 24 | cardSequenceNumber | Card sequence number |
| 25 | keyLabel | keyset ID: use 000002 for production<br>environment and 000006 for test environment. |
| 26 | cvmResults | Cardholder verification method |
| 27 | surcharge | This should be the surcharge field value: it<br>is in minor just like the amt tag above:<br>Mandatory |
| 28 | amountAuthorized | Amount authorized in minor: use postillion<br>format |
| 29 | Amount others | amountOther |
| 30 | applicationInterchangeProfile | application interchange profile |
| 31 | atc | Application transaction counter |
| 32 | Cryptogram | Cryptogram |
| 33 | CryptogramInformationData | Cryptogram Information Data |
| 34 | iad | Issuer Application Data |
| 35 | TerminalCurrencyCode | Terminal Currency Code |
| 36 | TerminalVerificationResult | Terminal Verification Result |
| 37 | TerminalCountryCode | Terminal country code |
| 38 | Terminal type | TerminalType |
| 39 | TransactionDate | Transaction date: YYMMDD |
| 40 | TransactionType | Transaction type |
| 41 | UnpredictableNumber | Unpredictable Number |
| 42 | DedicatedFileName | Dedicated file name |
| 43 | TerminalCapability | Terminal Capabilities |
| 44 | receivingInstitutionId | Receiving Institution ID of the Settlement<br>Bank. |
| 45 | DestinationAccountNumber | Settlement Account number |
| 46 | extendedTransactionType | Extended Transaction Type |
| 47 | retrievalReferenceNumber | Retrieval Reference Number (RRN) |
|  |  |  |

Updated12 months ago

* * *

Did this page help you?

Yes

No

Copy Page