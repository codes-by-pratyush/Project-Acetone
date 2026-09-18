┌─────────────────────────────────────────────────────────────┐
│                         LOGIN PAGE                          │
│                                                             │
│  • Email / ID                                               │
│  • Password                                                 │
│  • Login button                                             │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                    INVESTIGATOR DASHBOARD                   │
│                                                             │
│  TOP BAR                                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Search Wallet / Transaction │ Live Status │ Profile   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  KPI SECTION                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ Active   │ │ High-Risk│ │ Wallets  │ │ Attribution  │    │
│  │ Cases    │ │ Alerts   │ │ Traced   │ │ Confidence   │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
│                                                             │
│  ┌──────────────────────────┐ ┌──────────────────────────┐  │
│  │       YOUR CASES         │ │    RECENT ACTIVITY       │  │
│  │                          │ │                          │  │
│  │ Case Card                │ │ • Investigation event    │  │
│  │ Case Card                │ │ • Risk alert             │  │
│  │ Case Card                │ │ • Evidence added         │  │
│  │ Case Card                │ │                          │  │
│  └─────────────┬────────────┘ └──────────────────────────┘  │
└────────────────┼────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                        CASES PAGE                           │
│                                                             │
│  Filters: [Status] [Priority]                               │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Case ID │ Title │ Status │ Priority │ Assigned │ Date  │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ Case   │ ...   │ ...    │ ...      │ ...      │ ...  │ │ |
│  │ Case   │ ...   │ ...    │ ...      │ ...      │ ...  │ │ |
│  └──────────────────────────┬─────────────────────────────┘ │
└─────────────────────────────┼───────────────────────────────┘
                              ↓
                    ┌──────────────────┐
                    │   SELECT CASE    │
                    └────────┬─────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                     CASE OVERVIEW                           │
│                                                             │
│  CASE HEADER                                                │
│  Case ID | Status | Priority | Investigator | Date          │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    CASE SUMMARY                        │ │
│  │                                                        │ │
│  │  Source Wallet                                         │ │
│  │  Number of Wallets                                     │ │
│  │  Number of Transactions                                │ │
│  │  Current Risk                                          │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│             INVESTIGATION NAVIGATION                        │
│                                                             │
│   [Transaction Graph] [Risk & Attribution]                  │
│   [Evidence]          [Reports]                             │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┴────────┬──────────────────┬─────────────────┐
       ↓                ↓                  ↓                 ↓
┌──────────────┐ ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
│ TRANSACTION  │ │ RISK &        │ │   EVIDENCE   │ │   REPORTS    │
│ GRAPH        │ │ ATTRIBUTION   │ │              │ │              │
└──────┬───────┘ └───────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                  │                │                │
       ↓                  ↓                ↓                ↓



TRANSACTION GRAPH PAGE : 

┌─────────────────────────────────────────────────────────────┐
│ CASE HEADER                                                 │
├─────────────────────────────────────────────────────────────┤
│ FILTER BAR                                                  │
│ [Date] [Amount] [Type] [Risk]                               │
├──────────────────────────────────┬──────────────────────────┤
│                                  │                          │
│                                  │      DETAIL PANEL        │
│                                  │                          │
│        WALLET GRAPH              │  Selected Wallet / TX    │
│                                  │                          │
│    ○ ─────→ ○ ─────→ ○           │  • Address               │
│     \       │       \            │  • Balance               │
│      → ○ ───┘        → ○         │  • Risk Score            │
│                                  │  • Transactions          │
│                                  │  • Related Wallets       │
│                                  │  • Flags                 │
│                                  │  • Notes                 │
│                                  │                          │
├──────────────────────────────────┴──────────────────────────┤
│              INVESTIGATION TIMELINE / ACTIVITY LOG          │
└─────────────────────────────────────────────────────────────┘

RISK & ATTRIBUTION PAGE :
┌─────────────────────────────────────────────────────────────┐
│ CASE HEADER                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐  ┌─────────────────────────────┐ │
│  │                      │  │     ATTRIBUTION ANALYSIS     │ │
│  │     RISK SCORE       │  │                             │ │
│  │                      │  │  Destination                │ │
│  │       78 / 100       │  │  Confidence %               │ │
│  │       HIGH           │  │  Supporting evidence        │ │
│  │                      │  │                             │ │
│  └──────────────────────┘  └─────────────────────────────┘ │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│              SUSPICIOUS ACTIVITY INDICATORS                │
│                                                             │
│  ⚠ Rapid forwarding                                         │
│  ⚠ Fan-out pattern                                           │
│  ⚠ Dust transaction                                          │
│  ⚠ Wallet age                                                │
│  ⚠ Suspicious destination                                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                  SUGGESTED NEXT ACTION                      │
│                                                             │
│              [ Prepare Evidence Package ]                   │
└─────────────────────────────────────────────────────────────┘


EVIDENCE PAGE :

┌─────────────────────────────────────────────────────────────┐
│ CASE HEADER                         [ + Add Evidence ]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     EVIDENCE LIST                           │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Evidence │ Type │ Linked To │ Added By │ Date │ Action │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ NCRP     │ Image│ Case      │ ...      │ ...  │ View   │ │
│  │ Tx Export│ CSV  │ Wallet    │ ...      │ ...  │ View   │ │
│  │ Match Log│ Doc  │ Wallet    │ ...      │ ...  │ View   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│                    [ Add Evidence ]                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘


REPORTS PAGE : 
┌─────────────────────────────────────────────────────────────┐
│ CASE HEADER                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    REPORT PREVIEW                           │
│                                                             │
│  Case Information                                           │
│       ↓                                                     │
│  Investigation Summary                                      │
│       ↓                                                     │
│  Transaction Findings                                      │
│       ↓                                                     │
│  Risk Analysis                                              │
│       ↓                                                     │
│  Attribution Findings                                       │
│       ↓                                                     │
│  Evidence                                                   │
│       ↓                                                     │
│  Investigation Timeline                                     │
│                                                             │
│              [ Generate Report ]                             │
│              [ Export Report ]                              │
└─────────────────────────────────────────────────────────────┘

OVERALL NAVIGATION :

                         LOGIN
                           │
                           ↓
                     DASHBOARD
                           │
                           ↓
                         CASES
                           │
                    ┌──────┴──────┐
                    ↓             ↓
              CASE OVERVIEW   ← Select Case
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓            ↓
    GRAPH         RISK        EVIDENCE     REPORTS
       │            │            │            │
       └────────────┴────────────┴────────────┘
                           │
                           ↓
                    CASE ACTIVITY
                    / TIMELINE