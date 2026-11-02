<!-- PARTIAL: Scribd preview of NIBSS NIP Technical Specification v7.0. Section 8 (Response Codes) is listed in the TOC at page 25 but the code table is not in the public preview. Do not treat as complete. -->

Skip to main content

[Open navigation menu](https://www.scribd.com/document/362360337/NIP-Technical-Specification-Document-Ver-7-0#sidebar) [![Scribd](<Base64-Image-Removed>)](https://www.scribd.com/)

Close suggestionsSearchSearch

enChange Language, English

[Upload](https://www.scribd.com/upload-document)
Sign in

Sign in
[Download free for 30 days](https://www.scribd.com/oauth/signup?doc_id=362360337)

# NIBSS Instant Payments Technical Specs

100%(3)100% found this document useful (3 votes)

4K views29 pages

AI-enhanced title and description

This document provides a technical specification for NIBSS Instant Payments (NIP), which enables real-time inter-bank funds transfers in Nigeria based on bank account numbers. It identifies …

Full description

## Uploaded by

[boyekole](https://www.scribd.com/user/56921039/boyekole)

Download

You are on page 1
29

![1            TECHNICAL SPECIFICATION DOCUMENT    FOR    NIBSS INSTANT PAYMENTS (NIP)                                Prepare](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/1.jpeg)

1

![2    Table of Content    Document Control..................................................................................](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/2.jpeg)

2

![3    Document Control    S/N Document Section  Changes  Version  1.  Section 5 Web Service  Specification  Two new Web Serv](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/3.jpeg)

3

![4    1.   Introduction    NIBSS Instant Payment (NIP) is an account – number – based, online real-time Inter-Bank  Funds Tr](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/4.jpeg)

4

![5    ii. Internet Banking:  Most banks provide internet banking facilities that enable  customers to generate financial tra](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/5.jpeg)

5

![6    1. The customer walks into the branch.  2. He / She requests for OLRT inter-bank transfer indicating account details,](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/6.jpeg)

6

![7                          4.  Transaction Type  The transaction types that would be supported on the NIP are:  1. Name Enq](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/7.jpeg)

7

![8    beneficiary account in the destination bank, before confirming a transfer. So the  sender bank makes a request with th](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/8.jpeg)

8

![9    9. Fund Transfer Advice Request (Direct Debit): This transaction type is sent after  timeout waiting for response to t](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/9.jpeg)

9

![10    011  Name Enquiry Response (Single Item):  <?xml version="1.0" encoding="UTF-8" ?>   <NESingleResponse>    <SessionID](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/10.jpeg)

10

![11      <BillerName>Adewale Hassan</BillerName>    <BillerID>1111111111</BillerID>  <Narration>Transfer from 0XX to 0YY</Na](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/11.jpeg)

11

![12      </Record>      <Record>      <RecID>0XX0YY100913103301000000000004</RecID>      <AccountNumber>2222000000012344</Ac](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/12.jpeg)

12

![13        <Narration>Fund Transfer</Narration>      <PaymentReference>1000000002</PaymentReference>      <Amount>1000.00</A](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/13.jpeg)

13

![14    <FTBulkDebitRequest>    <Header>      <DestinationBankCode>0XX</DestinationBankCode>      <ChannelCode>1</ChannelCode](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/14.jpeg)

14

![15        <BillerName>Adewale Hassan4</BillerName>      <BillerID>1111111111</BillerID>      <Narration>Fund Transfer</Narr](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/15.jpeg)

15

![16      <Record>      <RecID>0XX0YY100913103301000000000002</RecID>      <AccountNumber>2222000000012342</AccountNumber>](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/16.jpeg)

16

![17        <Record>      <RecID>0XX0YY100913103301000000000001</RecID>      <AccountNumber>2222000000012341</AccountNumber>](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/17.jpeg)

17

![18        <AccountName>Ajibade Oluwasegun5</AccountName>      <OriginatorName>Adewale Hassan5</OriginatorName>      <Narrat](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/18.jpeg)

18

![19        <Narration>Fund Transfer</Narration>      <PaymentReference>1000000002</PaymentReference>  <MandateReferenceNumbe](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/19.jpeg)

19

![20    <?xml version="1.0" encoding="UTF-8" ?>  <FTBulkDebitNotificationResponse>    <DestinationBankCode>0XX</DestinationBa](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/20.jpeg)

20

![21        <Amount>1000.00</Amount>      <ResponseCode>00</ResponseCode>    </Record>      <Record>      <RecID>0XX0YY100913](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/21.jpeg)

21

![22    032 Balance Enquiry Request  <?xml version="1.0" encoding="UTF-8" ?>   <BalanceEnquiryRequest>    <SessionID>0XX0YY10](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/22.jpeg)

22

![23    <PaymentReference>yyyyyyyyyyyyyy</PaymentReference>    <Amount>1000.00</Amount>    <ResponseCode>00</ResponseCode>  <](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/23.jpeg)

23

![24      It is important to note that Batch Number in bulk item transactions is 24 characters in  length and follow the form](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/24.jpeg)

24

![25    7.  Channel Codes  Find in the table the channel codes and their respective names:  Codes  Channel Names  1  Bank Tel](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/25.jpeg)

25

![26    63  Security violation  65  Exceeds withdrawal frequency  68  Response received too late  91  Beneficiary Bank not av](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/26.jpeg)

26

![27    pair of keys – public and private keys – will be generated and also, it would handle all  cryptographic functions bet](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/27.jpeg)

27

![28    Commission Account  Credit  NY.YY  Share of the transaction  fee that belongs to the  sender’s bank.  NIP Mirror Acco](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/28.jpeg)

28

![29    e.  The Beneficiary’s Bank receives the alert and verifies dispute from the  transaction traces and logs.  f.  The Be](https://screenshots.scribd.com/Scribd/252_100_85/356/362360337/29.jpeg)

29

1

TECHNICAL SPECIFICATION DOCUMENT FOR NIBSS INSTANT PAYMENTS (NIP)

Prepared by: Nigeria Inter – Bank Settlement System (NIBSS) Version: 7.0 April 20, 2012

![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/1-6361fd951c.jpg)![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/1-6361fd951c.jpg)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

2

Table of Content

Document Control

.....................................................................................................................3

1\. Introduction

......................................................................................................................4

2.

Identification of Delivery Channels

.................................................................................4

3.

Transaction Flow

...............................................................................................................5

4.

Transaction Type

...............................................................................................................7

5.

Web Service Specification

................................................................................................9

6.

Web Service Method Name

.......................................................................................... 24

7.

Channel Codes

................................................................................................................ 25

8\. Response Codes

............................................................................................................. 25

9.

Direct Debit Implementation

........................................................................................ 26

10.

Message Security

........................................................................................................... 26

11.

Transaction Settlement

................................................................................................. 27

12\. Account Entries

............................................................................................................... 27

13\. Reports

............................................................................................................................ 28

14\. Dispute Resolution

......................................................................................................... 28

15\. Requirements from Banks

............................................................................................. 29

![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/2-90b241d52a.jpg?token=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3OTYxOTcyNjYsImlhdCI6MTc5MzYwNTI2NiwiaXNzIjoic2NyaWJkLW1vbm9saXRoIiwiZm9ybWF0X3V1aWQiOiI2cTQ5aGx3NmY0NjN6bGhkIiwieF9zY3JpYmRfdXVpZCI6IjUxZjkzNTNlLTcxMTItNDNmNC04MDhkLTNkYjZjYTYwYjRiNiIsInhfcmVxdWVzdF9pZCI6IjM5N2Q0MDM2ZGQ1ODVkZTk0YmEyNzFkMmYyMDk0NTczNzBjOGVkMmUyZjBlMzM3YjljNGMwMzQ2ZDE0ZmFhMDIiLCJwYWdlX21pbiI6MSwicGFnZV9tYXgiOjI5LCJlbmZvcmNlIjp0cnVlfQ.8i5a_bhtuu44lUGaxKFkWH_wn3oL5da00BuEVKdF8tU)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

3

Document Control

S/N Document Section Changes Version

1\. Section 5 Web Service Specification Two new Web Service Methods added: 1.

Fund Transfer Advice (Direct Credit) 2.

Fund Transfer Advice (Direct Debit) 7.0 2\. Section 5 Web Service Specifications Narration pegged to 100 characters in length. 7.0 3\. Section 6\. Web Service Method Names Two method names added: 1.

fundtransferAdvice\_dc 2.

fundtransferAdvice\_dd 7.0 4\. Section 7\. Channel Code A new Channel Code ‘8 – Other Channels’ added. 7.0 5\. Section 8\. Response Codes A new Response Code ’97 – Timeout waiting for response from destination’ added. 7.0

![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/3-ca6ca42a62.jpg?token=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3OTYxOTcyNjYsImlhdCI6MTc5MzYwNTI2NiwiaXNzIjoic2NyaWJkLW1vbm9saXRoIiwiZm9ybWF0X3V1aWQiOiI2cTQ5aGx3NmY0NjN6bGhkIiwieF9zY3JpYmRfdXVpZCI6IjUxZjkzNTNlLTcxMTItNDNmNC04MDhkLTNkYjZjYTYwYjRiNiIsInhfcmVxdWVzdF9pZCI6IjM5N2Q0MDM2ZGQ1ODVkZTk0YmEyNzFkMmYyMDk0NTczNzBjOGVkMmUyZjBlMzM3YjljNGMwMzQ2ZDE0ZmFhMDIiLCJwYWdlX21pbiI6MSwicGFnZV9tYXgiOjI5LCJlbmZvcmNlIjp0cnVlfQ.8i5a_bhtuu44lUGaxKFkWH_wn3oL5da00BuEVKdF8tU)![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/3-ca6ca42a62.jpg?token=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3OTYxOTcyNjYsImlhdCI6MTc5MzYwNTI2NiwiaXNzIjoic2NyaWJkLW1vbm9saXRoIiwiZm9ybWF0X3V1aWQiOiI2cTQ5aGx3NmY0NjN6bGhkIiwieF9zY3JpYmRfdXVpZCI6IjUxZjkzNTNlLTcxMTItNDNmNC04MDhkLTNkYjZjYTYwYjRiNiIsInhfcmVxdWVzdF9pZCI6IjM5N2Q0MDM2ZGQ1ODVkZTk0YmEyNzFkMmYyMDk0NTczNzBjOGVkMmUyZjBlMzM3YjljNGMwMzQ2ZDE0ZmFhMDIiLCJwYWdlX21pbiI6MSwicGFnZV9tYXgiOjI5LCJlbmZvcmNlIjp0cnVlfQ.8i5a_bhtuu44lUGaxKFkWH_wn3oL5da00BuEVKdF8tU)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

4

1\. Introduction

NIBSS Instant Payment (NIP) is

an account – number – based, online real-time Inter-Bank Funds Transfer product. This new electronic payment system would enable banks to provide online real-time funds transfer services to their customers, based on bank account numbers, through channels such as Teller System, Internet Banking, Mobile, and Web (e-Commerce). Also, the NIBSS Instant Payments would support the Mobile Payments initiatives of Mobile Payment service providers who receive the relevant license from the Central Bank. NIBSS Instant Payments (NIP) would leverage on Banks’ connection to the Nigeria Central Switch (NCS). Our NIP engine would connect securely to Banks’ Core Banking Systems to receive and deliver electronic payment requests. Also every Bank is required to provide NIP customer interfaces on their respective Teller System and Internet Banking system. This document discusses the technical specification of NIP. Other available NIP related documents are: a.

Introduction to NIBSS Instant Payments b.

NIP Settlement Procedure c.

NIP Dispute Resolution System d.

NIP Message Security Management

2\. Identification of Delivery Channels

By delivery channels, we mean the channels that banks are required to provide to their respective customers for the origination of NIP transactions. The following are the typical delivery channels: i.

Branch Teller:

On the NIP platform, bank customers can walk into any branch of their respective banks, and request for a NIP (OLRT inter – bank transfer) service. Such transfers will be facilitated online real – time i.e value delivered to the beneficiary instantly. The Branch Teller or Customer Service personnel would perform the required customer authentication check, just as if the customer had requested a cash withdrawal.

![](https://html.scribdassets.com/6q49hlw6f463zlhd/images/4-3df72e55a0.jpg?token=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3OTYxOTcyNjYsImlhdCI6MTc5MzYwNTI2NiwiaXNzIjoic2NyaWJkLW1vbm9saXRoIiwiZm9ybWF0X3V1aWQiOiI2cTQ5aGx3NmY0NjN6bGhkIiwieF9zY3JpYmRfdXVpZCI6IjUxZjkzNTNlLTcxMTItNDNmNC04MDhkLTNkYjZjYTYwYjRiNiIsInhfcmVxdWVzdF9pZCI6IjM5N2Q0MDM2ZGQ1ODVkZTk0YmEyNzFkMmYyMDk0NTczNzBjOGVkMmUyZjBlMzM3YjljNGMwMzQ2ZDE0ZmFhMDIiLCJwYWdlX21pbiI6MSwicGFnZV9tYXgiOjI5LCJlbmZvcmNlIjp0cnVlfQ.8i5a_bhtuu44lUGaxKFkWH_wn3oL5da00BuEVKdF8tU)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

ad [Download to read ad-free](https://www.scribd.com/oauth/signup?behavior_tag=download&doc_id=362360337)

## Share this document

- [Share on Facebook, opens a new window](https://www.scribd.com/document/362360337/NIP-Technical-Specification-Document-Ver-7-0#)
- [Share on LinkedIn, opens a new window](https://www.scribd.com/document/362360337/NIP-Technical-Specification-Document-Ver-7-0#)
- [Share with Email, opens mail client](mailto:?subject=Read%20NIP%20Technical%20Specification%20Document%20Ver%207.0%20on%20Scribd&body=I%E2%80%99m%20reading%20NIP%20Technical%20Specification%20Document%20Ver%207.0%20on%20Scribd:%20https%3A%2F%2Fwww.scribd.com%2Fdocument%2F362360337%2FNIP-Technical-Specification-Document-Ver-7-0)
- Copy link

[![](https://s-f.scribdassets.com/webpack/assets/images/fallbacks/scribd_inhouse_728x90_en@1x.ec04e4d8.png)Millions of documents at your fingertips, ad-freeSubscribe with a free trial](https://www.scribd.com/oauth/signup?doc_id=362360337)

ad

576648e32a3d8b82ca71961b7a986505

scribd.scribd.scribd.scribd.scribd.scribd.scribd.