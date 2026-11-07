# PDF to Excel - Tables, XLSX Downloads & PDF转Excel

PDF to Excel provides tables and downloads for automated workflows, with JSON export, repeat monitoring and bounded pay-per-result delivery. Turn recurring reports, catalog tables and statements with digital text into reviewable spreadsheet inputs.

## PDF to Excel: scope and source behavior

Extracts tables from digital PDFs with pdfplumber. lines uses drawn table boundaries; text estimates cells from aligned text. Choose one strategy per run. Every page containing tables yields one Excel workbook with one worksheet per extracted table, plus nested cells in JSON. It does not infer accounting semantics, merge tables across pages, recognize scanned tables or guarantee spreadsheet formatting. A page without detected tables produces zero billed rows. Text alignment can misidentify columns; inspect a sample before automation. Cell strings are written as text, including values beginning with =, to prevent source content becoming executable spreadsheet formulas. Numeric-looking strings remain text so leading zeros are preserved.

This is an independent Kestrel utility. It is not an official product of the source, registry, browser vendor or document library. It accepts the documented inputs and returns observed or extracted data with source references. It does not create source accounts, buy data subscriptions, send messages, alter websites or submit forms. The exact supported operation matters more than a generic promise to handle every possible agent request.

## PDF to Excel for AI agents: which input answers which request?

Use this Actor when the requested output matches the scope above. Read the input schema before constructing a call. Required target values are explicit lists, while optional settings have documented defaults. A run with omitted target fields uses the demonstration values; production callers should always send their intended targets. A source account or source API key is not required for the supported operation.

| Request | Input approach |
| --- | --- |
| Try the documented example | Use the small JSON sample below. |
| Process a batch | Put up to 100 targets in `documentUrls`. |
| Return at most three paid results | Set `maxResults` to 3. |
| Skip previously delivered identities | Copy previous `id` values into `excludeIds`. |
| Skip previously seen snapshots | Copy previous `content_hash` values into `excludeContentHashes`. |
| Limit spending | Set `maxTotalChargeUsd` in the Apify run options, outside input JSON. |

```json
{
  "documentUrls": [
    "https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"
  ],
  "startPage": 1,
  "maxPagesPerDocument": 5,
  "tableStrategy": "lines",
  "maxResults": 3
}
```

The example is a small test, not a promise of a fixed row count. A document may contain empty pages, a website may display no email address, or an image may have no recognizable text. Valid empty extractions are distinguished from upstream errors. Keep the free summary alongside the dataset so your agent can explain what actually happened.

## Tables inputs and limits

| Input | Behavior |
| --- | --- |
| `documentUrls` | Public PDF URLs, e.g. the prefilled pdfplumber sample. Up to 100; 12 MB each. One billed row per qualifying page; digital text only, no scanned-page OCR. |
| `startPage` | First PDF page to inspect, one-based, e.g. 2. Default 1. Pages before this are not inspected or billed. |
| `maxPagesPerDocument` | Maximum PDF pages inspected per document, 1–20. Default 5. Blank pages or pages with no tables still consume this scan limit but are free. |
| `tableStrategy` | "lines" (default) detects ruled tables; "text" uses text alignment for borderless tables. Review a sample. No OCR; one billed page includes every detected table. |
| `maxResults` | Maximum paid rows across the run, 1–1000, default 20. Example: 3 for a sample. Exclusions and empty results apply before the cap. |
| `excludeIds` | Prior output id values to skip before billing, up to 5,000. Empty [] disables. Suppresses that identity even if content changed. |
| `excludeContentHashes` | Prior output content_hash values (64 lowercase hex characters), up to 5,000. Empty [] disables. Matching snapshots are skipped before billing. |

All fields reject incompatible types. Boolean values must be JSON booleans, not strings. Lists contain strings rather than nested request objects. Unknown property names fail validation to catch misspelled agent inputs early. Duplicate target strings are removed within a run. Domain names are normalized before deduplication. Exclusion lists are optional and bounded so a single run cannot grow without limit.

The overall result limit applies after exclusions. A qualifying result removed by an exclusion does not consume that result allowance. Source page limits, download limits and processing limits remain independent: excluding an old result does not refund the work needed to discover it. A request for twenty rows can therefore finish with fewer than twenty rows without indicating a bug.

## Downloads output and download contract

One paid row represents one **PDF page with tables**. The principal observed row fields are shown below. Optional source fields can be missing or null; consumers should not invent replacements. The output remains structured JSON even when a downloadable file is also produced.

| Field | Meaning |
| --- | --- |
| `page` | page |
| `total_pages` | total pages |
| `source_url` | source url |
| `extraction` | extraction |
| `tables` | tables |
| `table_count` | table count |
| `table_strategy` | table strategy |
| `id` | Stable identity within this Actor and target scope. |
| `content_hash` | SHA-256 of the normalized result for comparison. |
| `fetched_at` | UTC extraction or observation time. |

```json
{
  "page": 1,
  "total_pages": 1,
  "source_url": "https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf",
  "extraction": "digital_text_no_ocr",
  "tables": [
    [
      [
        "NICS Firearm Background Checks\nNovember - 2015",
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ],
      [
        "State / Territory",
        "Permit Handgun Long Gun *Other **Multiple Admin",
        null,
        null,
        null,
        null,
        null,
        "Pre-Pawn\nHandgun Long Gun *Other",
        null,
        null,
        "Redemption\nHandgun Long Gun *Other",
        null,
        null,
        "Returned/Disposition\nHandgun Long Gun *Other",
        null,
        null,
        "Rentals\nHandgun Long Gun",
        null,
        "Private Sale\nHandgun Long Gun *Other",
        null,
        null,
        "Return to Seller - Private Sale\nHandgun Long Gun *Other",
        null,
        null,
        "Totals"
      ],
      [
        "Alabama\nAlaska\nArizona\nArkansas\nCalifornia",
        "18,870\n209\n2,303\n3,298\n98452",
        "23,022\n3,062\n12,382\n6,359\n41181",
        "22,650\n3,209\n9,041\n11,611\n35007",
        "859\n191\n707\n168\n4559",
        "1,178\n184\n618\n376\n0",
        "0\n0\n0\n0\n0",
        "14\n9\n5\n12\n0",
        "15\n3\n3\n6\n0",
        "0\n0\n0\n1\n0",
        "2,179\n100\n1,273\n922\n480",
        "2,307\n100\n648\n2,275\n433",
        "11\n0\n4\n1\n4",
        "0\n18\n76\n0\n0",
        "0\n9\n8\n0\n0",
        "0\n1\n1\n0\n0",
        "",
        "",
        "13\n0\n9\n6\n0",
        "14\n0\n6\n12\n0",
        "0\n0\n1\n1\n0",
        "3\n0\n1\n0\n0",
        "2\n0\n1\n0\n0",
        "0\n0\n0\n0\n0",
        "71,137\n7,095\n27,087\n25,048\n180116"
      ],
      [
        "Colorado\nConnecticut\nDelaware\nDistrict of Columbia\nFlorida",
        "4,144\n9,631\n204\n8\n15,907",
        "19,784\n11,594\n2,152\n54\n50,796",
        "16,082\n5,072\n2,424\n2\n28,981",
        "932\n134\n65\n0\n2,268",
        "1,151\n0\n72\n0\n1,957",
        "0\n7\n0\n0\n121",
        "0\n0\n3\n0\n8",
        "0\n0\n4\n0\n9",
        "0\n0\n0\n0\n0",
        "0\n0\n17\n0\n2,248",
        "0\n0\n12\n0\n1,135",
        "0\n0\n0\n0\n2",
        "144\n0\n0\n0\n40",
        "34\n0\n0\n0\n5",
        "0\n0\n0\n0\n0",
        "",
        "",
        "0\n0\n59\n0\n36",
        "0\n0\n24\n0\n19",
        "0\n0\n0\n0\n0",
        "0\n0\n4\n0\n0",
        "0\n0\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "42,271\n26,438\n5,040\n64\n103,532"
      ],
      [
        "Georgia\nGuam\nHawaii\nIdaho\nIllinois",
        "14,111\n0\n1,248\n1,944\n87,190",
        "16,635\n100\n0\n3,609\n24,412",
        "15,227\n55\n0\n5,227\n17,227",
        "448\n12\n0\n190\n0",
        "758\n3\n0\n189\n1,032",
        "0\n0\n0\n0\n0",
        "10\n0\n0\n0\n0",
        "14\n0\n0\n4\n0",
        "0\n0\n0\n0\n0",
        "1,772\n1\n0\n273\n0",
        "1,796\n0\n0\n455\n0",
        "4\n0\n0\n1\n0",
        "0\n0\n1\n22\n0",
        "0\n0\n3\n4\n0",
        "0\n0\n0\n1\n0",
        "",
        "",
        "10\n0\n0\n1\n0",
        "9\n0\n0\n2\n0",
        "1\n0\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "0\n0\n0\n3\n0",
        "0\n0\n0\n0\n0",
        "50,795\n171\n1,252\n11,925\n129,861"
      ],
      [
        "Indiana\nIowa\nKansas\nKentucky\nLouisiana",
        "81,935\n8,785\n894\n264,140\n1,945",
        "25,519\n267\n7,086\n12,155\n14,708",
        "20,227\n4,596\n8,702\n14,847\n17,368",
        "1,113\n27\n311\n254\n697",
        "808\n4\n396\n648\n793",
        "0\n37\n3\n1\n0",
        "2\n0\n1\n9\n5",
        "3\n1\n3\n11\n11",
        "0\n0\n1\n0\n2",
        "13\n0\n486\n1,491\n884",
        "629\n71\n530\n2,315\n1,323",
        "5\n0\n2\n2\n3",
        "28\n4\n2\n2\n0",
        "0\n2\n0\n2\n0",
        "0\n0\n0\n0\n0",
        "",
        "",
        "31\n0\n6\n6\n1",
        "13\n0\n10\n8\n10",
        "1\n0\n0\n0\n1",
        "2\n0\n0\n0\n0",
        "4\n0\n0\n0\n1",
        "0\n0\n0\n0\n0",
        "130,333\n13,794\n18,433\n295,891\n37,752"
      ],
      [
        "Maine\nMariana Islands\nMaryland\nMassachusetts\nMichigan",
        "299\n0\n1,512\n5,214\n16,786",
        "4,048\n0\n3,220\n6,083\n13,634",
        "4,387\n0\n8,310\n3,931\n17,604",
        "135\n0\n96\n402\n385",
        "171\n0\n9\n175\n238",
        "2\n0\n0\n0\n1,025",
        "0\n0\n0\n0\n1",
        "0\n0\n3\n1\n4",
        "0\n0\n0\n0\n0",
        "70\n0\n72\n2\n5",
        "165\n0\n213\n5\n489",
        "0\n0\n2\n0\n2",
        "6\n0\n14\n1\n69",
        "7\n0\n3\n0\n24",
        "0\n0\n1\n1\n0",
        "",
        "",
        "4\n0\n1\n42\n4",
        "3\n0\n6\n23\n1",
        "0\n0\n1\n5\n1",
        "0\n0\n0\n0\n2",
        "0\n0\n0\n0\n3",
        "0\n0\n0\n0\n1",
        "9,297\n0\n13,463\n15,885\n50,278"
      ],
      [
        "Minnesota\nMississippi\nMissouri\nMontana\nNebraska",
        "18,939\n618\n5,884\n852\n4,258",
        "9,373\n9,785\n21,135\n2,848\n173",
        "14,173\n13,191\n22,852\n5,170\n3,724",
        "486\n267\n1,004\n90\n23",
        "330\n523\n1,060\n197\n10",
        "0\n9\n0\n10\n0",
        "1\n28\n11\n1\n1",
        "2\n20\n16\n4\n0",
        "0\n0\n0\n6\n0",
        "176\n1,171\n1,131\n391\n5",
        "512\n1,874\n1,754\n828\n96",
        "0\n1\n3\n1\n1",
        "8\n0\n99\n11\n7",
        "11\n0\n11\n4\n0",
        "0\n0\n4\n0\n0",
        "",
        "",
        "2\n6\n33\n0\n0",
        "6\n6\n25\n2\n0",
        "0\n3\n6\n0\n1",
        "0\n2\n0\n0\n0",
        "2\n0\n3\n0\n0",
        "2\n0\n0\n0\n0",
        "44,023\n27,504\n55,031\n10,415\n8,299"
      ],
      [
        "Nevada\nNew Hampshire\nNew Jersey\nNew Mexico\nNew York",
        "1,543\n3,630\n0\n829\n2,906",
        "4,889\n4,847\n3,462\n5,247\n8,650",
        "3,272\n4,165\n4,704\n4,974\n23,519",
        "193\n95\n147\n334\n665",
        "287\n2\n0\n277\n149",
        "0\n1\n0\n0\n0",
        "0\n0\n0\n2\n0",
        "0\n0\n0\n3\n3",
        "0\n0\n0\n1\n0",
        "284\n0\n0\n397\n16",
        "163\n23\n0\n618\n25",
        "0\n1\n0\n1\n0",
        "1\n69\n0\n33\n0",
        "0\n11\n0\n0\n0",
        "0\n1\n0\n0\n0",
        "",
        "",
        "0\n2\n0\n0\n243",
        "0\n2\n0\n4\n220",
        "0\n0\n0\n0\n16",
        "0\n0\n0\n1\n5",
        "0\n1\n0\n0\n4",
        "0\n0\n0\n0\n0",
        "10,632\n12,850\n8,313\n12,721\n36,421"
      ],
      [
        "North Carolina\nNorth Dakota\nOhio\nOklahoma\nOregon",
        "22,469\n453\n9,338\n0\n35",
        "1,370\n1,720\n34,878\n15,005\n13,586",
        "20,107\n3,744\n31,817\n14,753\n11,832",
        "576\n65\n1,392\n778\n0",
        "202\n79\n1,483\n998\n0",
        "0\n0\n0\n0\n0",
        "16\n0\n24\n11\n0",
        "25\n3\n16\n7\n0",
        "0\n0\n1\n1\n0",
        "1,771\n65\n1,228\n1,639\n0",
        "2,644\n157\n1,389\n2,226\n0",
        "7\n0\n4\n6\n0",
        "0\n0\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "",
        "",
        "2\n1\n21\n11\n0",
        "26\n1\n22\n21\n0",
        "1\n0\n1\n0\n0",
        "1\n0\n1\n0\n0",
        "0\n0\n0\n1\n0",
        "0\n0\n1\n0\n0",
        "49,217\n6,288\n81,616\n35,457\n25,453"
      ],
      [
        "Pennsylvania\nPuerto Rico\nRhode Island\nSouth Carolina\nSouth Dakota",
        "24,136\n0\n0\n7,284\n819",
        "62,752\n1,033\n954\n11,452\n2,765",
        "16,297\n170\n932\n10,393\n5,484",
        "0\n11\n57\n561\n143",
        "0\n20\n135\n438\n151",
        "58\n0\n0\n0\n0",
        "0\n0\n0\n3\n0",
        "0\n0\n0\n8\n1",
        "0\n0\n0\n0\n0",
        "0\n6\n3\n979\n123",
        "0\n1\n4\n912\n239",
        "0\n0\n0\n3\n0",
        "446\n0\n0\n16\n0",
        "147\n0\n0\n4\n0",
        "0\n0\n0\n0\n0",
        "",
        "",
        "0\n0\n12\n4\n1",
        "0\n0\n2\n6\n1",
        "0\n0\n1\n0\n0",
        "0\n0\n1\n1\n0",
        "0\n1\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "103,836\n1,242\n2,101\n32,064\n9,727"
      ],
      [
        "Tennessee\nTexas\nUtah\nVermont\nVirgin Islands",
        "9,509\n21,550\n10,429\n0\n93",
        "28,815\n56,941\n4,314\n1,189\n13",
        "24,023\n51,670\n5,857\n1,826\n2",
        "0\n2,532\n195\n49\n0",
        "1,300\n3,048\n262\n70\n1",
        "0\n0\n0\n0\n0",
        "0\n29\n0\n0\n0",
        "0\n20\n1\n1\n0",
        "0\n0\n0\n0\n0",
        "0\n5,748\n209\n0\n0",
        "0\n5,331\n285\n1\n0",
        "0\n21\n1\n0\n0",
        "17\n1\n140\n0\n0",
        "1\n2\n58\n0\n0",
        "5\n1\n21\n0\n0",
        "",
        "",
        "0\n42\n0\n0\n0",
        "0\n36\n0\n0\n0",
        "0\n4\n0\n0\n0",
        "0\n1\n0\n0\n0",
        "0\n5\n0\n0\n0",
        "0\n0\n0\n0\n0",
        "63,670\n146,982\n21,772\n3,136\n109"
      ],
      [
        "Virginia\nWashington\nWest Virginia\nWisconsin\nWyoming",
        "622\n10,314\n2,217\n5,867\n383",
        "24,052\n15,822\n6,953\n13,700\n1,745",
        "22,348\n12,425\n11,561\n17,759\n2,372",
        "974\n1,238\n224\n458\n87",
        "0\n606\n478\n45\n104",
        "0\n4\n2\n0\n1",
        "0\n8\n4\n0\n0",
        "0\n8\n9\n3\n4",
        "0\n0\n0\n0\n0",
        "0\n1,096\n923\n124\n132",
        "0\n1,129\n2,678\n513\n184",
        "0\n3\n3\n3\n0",
        "10\n356\n0\n15\n0",
        "4\n159\n0\n20\n0",
        "0\n3\n0\n4\n0",
        "",
        "",
        "0\n444\n3\n10\n1",
        "0\n340\n8\n15\n2",
        "0\n19\n0\n1\n0",
        "0\n6\n0\n0\n0",
        "0\n9\n0\n3\n2",
        "0\n0\n0\n1\n0",
        "48,010\n43,989\n25,063\n38,541\n5,017"
      ],
      [
        "Totals",
        "804,006",
        "671,330",
        "636,903",
        "26,597",
        "23,015",
        "1,281",
        "218",
        "249",
        "13",
        "29,905",
        "38,487",
        "102",
        "1,656",
        "533",
        "44",
        "0",
        "0",
        "1,067",
        "905",
        "65",
        "31",
        "45",
        "5",
        "2,236,457"
      ],
      [
        "",
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ],
      [
        "*Refers to frames, receivers and other firearms that are not either handguns or long guns (rifles or shotguns), such as firearms having a pistol grip that expel a shotgun shell\nNOTES:\n**Multiple (multiple types of firearms selected)\nSome states may reflect lower than expected numbers for handgun checks based on varying state laws pertaining to handgun permits Since the permit check is done in place of the NICS check in most of the affected states, the low handgun statistics are often balanced out by a higher number of handgun permit checks\nDISCLAIMERS:\nThese statistics represent the number of firearm background checks initiated through the NICS They do not represent the number of firearms sold Based on varying state laws and purchase scenarios, a one-to-one correlation cannot be made between a firearm background check and a firearm sale",
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ],
      [
        "",
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ]
    ]
  ],
  "table_count": 1,
  "table_strategy": "lines"
}
```

Document conversion, OCR, website Markdown and screenshots include `download_url`, `artifact_key`, `artifact_bytes` and `artifact_sha256` when a file is delivered. Those fields identify a file in the run's Apify key-value store. Do not remove the signature query parameter from a generated download URL. The generated link includes a record-specific signature for downloading without an Apify token. Files remain available only while the store and record are retained. Export important artifacts into your own storage rather than treating a run as a permanent archive.

Email, DNS, registration and weather rows are dataset records and do not create a separate file download. Use Apify dataset export to obtain JSON or CSV where useful. Nested values such as tables, words, entities and forecasts are better preserved as JSON than flattened CSV. A download does not contain more coverage than the associated row; a PDF page workbook, for example, does not silently include unprocessed document pages.

## What does a successful run mean?

A successful run means the requested bounded work finished without a reported target error. It does not guarantee complete website coverage, perfect OCR, a reachable mailbox, future weather accuracy or a registry field that the source did not provide. Each product's limitations are specified in the scope section. Callers should verify a representative output before placing it into a consequential downstream workflow.

The free `SUMMARY` record contains `status`, `rows`, `excluded`, `targets_attempted`, `targets_requested`, `stop_reason`, `errors`, `artifacts` and `coverage`. It also reports `source_http_requests` (including redirects and failed connection attempts), `source_downloaded_bytes` (decoded response bytes) and `dns_cache_hits` for workload inspection. These counters exclude Apify storage traffic and system DNS resolution. The row count is the number delivered into the paid dataset. The artifact list contains file keys only for successfully delivered file-bearing rows. A budget or result limit can stop the run before every requested target is attempted.

Status `no_matches` means no qualifying row was produced without a target failure. Status `error` means a failure with no valid delivered row, and `partial_error` means valid rows were delivered before or alongside a failure. Error states fail the Actor run so automation does not mistake an unavailable source for an empty result. Invalid inputs are reported as `invalid_input` before any target access.

## How much does it cost?

The event price is **$0.02 per delivered PDF page with tables**, equivalent to **$20 per 1,000 rows**. Ten rows cost $0.2; one hundred cost $2. There is no Actor start fee. Compute and network access are included in the event price. Nested data and files described for a row are included in that row's price.

Within-run duplicates, excluded identities, excluded matching snapshots and empty extractions are free. Failures without delivered data produce no result charge. An invalid-syntax email is a valid diagnostic result and is billed as an email check; a DNS NXDOMAIN response and a registry not-found response are likewise useful observations, not failed requests. The Actor never charges a separate event for every nested word, cell, DNS record or forecast step.

Set `maxTotalChargeUsd` in Apify run options for a monetary ceiling. It is not an Actor input field. The charging manager is checked before starting a target and before delivering a result; delivery stops when no complete result event fits the remaining budget. Previously delivered rows remain available and retain their charges if a later target fails. Customer event prices and developer infrastructure costs are different figures; a test run's compute cost is not a customer revenue measurement.

## How do Python, JavaScript and curl integrations work?

The Python example uses apify-client 3.x and its typed Run object. Use an environment variable for the Apify token and the asynchronous run API for reliable orchestration. Start the run, wait for its terminal status, then read both the dataset and the free summary. Keep the run identifier in downstream records so an extraction can be traced to its inputs, build and status. Never paste credentials into target URLs.

```python
import os
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/pdf-to-excel-tables').call(
    run_input={'documentUrls': ['https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf'], 'startPage': 1, 'maxPagesPerDocument': 5, 'tableStrategy': 'lines', 'maxResults': 3}, max_total_charge_usd=Decimal('0.10'))
rows = list(client.dataset(run.default_dataset_id).iterate_items())
summary = client.key_value_store(run.default_key_value_store_id).get_record('SUMMARY')
print(rows, summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({token: process.env.APIFY_TOKEN});
const run = await client.actor('kestrel/pdf-to-excel-tables').call(
  {"documentUrls": ["https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"], "startPage": 1, "maxPagesPerDocument": 5, "tableStrategy": "lines", "maxResults": 3}, {maxTotalChargeUsd: 0.10});
const rows = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(rows.items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~pdf-to-excel-tables/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"documentUrls": ["https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"], "startPage": 1, "maxPagesPerDocument": 5, "tableStrategy": "lines", "maxResults": 3}'
```

## How should repeat monitoring work?

Persist returned identities and hashes in your own database. On subsequent runs, supply the relevant exclusion list. An identity exclusion suppresses that target or page even if its content changes. A hash exclusion suppresses only a previously seen normalized state. Choose hashes for change monitoring and identities for one-time collection. The Actor does not maintain a hidden shared contact history across customers.

The hash is for comparison, not proof of authenticity. It excludes the observation timestamp and storage download URL. Screenshot image bytes contribute to their hash, so dynamic banners, animations or dates can make a new screenshot differ even when the site's main content is unchanged. DNS TTLs and evolving forecasts also make snapshots change. Use field-specific downstream comparisons when your business definition of change is narrower.

Batch related targets and choose a schedule that matches the source update cadence. A repeated run cannot force a registry, weather model or website to publish new information. Avoid retry loops on permanent input errors. A transient upstream failure can justify a later bounded retry, with exclusions for rows already delivered. There is no built-in notification, email sending or schedule creation; those actions belong to the calling workflow.

## How do n8n, Make and MCP agents use this?

Use an Apify connector or an HTTP request module to start the run and wait for completion. In n8n and Make, branch on the run status before iterating rows. Download file artifacts only when a row actually contains an artifact key. Store the summary on both successful and failed branches. This makes partial results usable without hiding unobserved targets.

An MCP agent should inspect the Actor details, choose literal input fields and begin with a small sample. It should quote observed values and source URLs, preserve units and page numbers, and describe source limitations when they affect the answer. A structured result is easier to use correctly than an undocumented text blob, but it still requires interpretation. Do not treat a confidence score as certainty or a missing field as a negative fact.

## FAQ: common operational questions

### Does this accept authenticated sites or private-network URLs?

No. Only public HTTP(S) targets on standard ports are supported for website and document inputs. Embedded credentials, loopback, private, link-local and reserved addresses are rejected. DNS resolution is checked before connections, and redirects are revalidated. The screenshot browser routes public GET resources through the same bounded fetch layer. This protects the execution environment and keeps the supported input contract predictable.

### Does it translate or invent missing content?

No. Chinese discovery text helps users find the utility, while output values retain their source meaning. OCR language selection controls recognition, not translation. A missing field stays missing or null. Document extraction does not infer a table that was not detected, and website conversion does not summarize text with an LLM. Downstream agents can translate or analyze the output separately while retaining the original evidence.

### What happens with a large or malformed file?

Downloads are capped, and parsing takes place in a separate process with a wall-time limit. An oversized, encrypted or malformed document can fail explicitly. This is preferable to returning a silently incomplete conversion. The supported page and image limits are documented in the input descriptions and scope. Split large batches into smaller runs so one problematic target is easy to isolate and retry.

### Are results deterministic?

The same stable source and settings usually produce equivalent normalized text or structured data, but upstream pages and endpoints change. Browser screenshots also depend on timing, responsive layout, fonts and dynamic content. Workbook binary metadata can differ even when extracted table cells match; the comparison hash uses normalized cells rather than requiring byte-identical workbooks. Preserve both hashes and source references when building an audit trail.

### Can I claim completeness from an empty dataset?

No. Read the run status and summary first. A genuinely empty extraction, a scan cap and an upstream failure are different outcomes. An email-free starting page does not establish that a company has no email address. A PDF page without extractable text may be a scan. A missing registry object does not establish that a domain is available to buy. The utility reports the observed operation, not a broader unsupported conclusion.

### What legal and source-use considerations apply?

Use public data and documents for purposes you are authorized to pursue, and retain applicable source notices. Public availability does not remove copyright or database restrictions. Source names identify the tool or service used and do not imply endorsement. MET Norway data requires attribution and its license reference, which the forecast row includes. Registry notices are preserved. The utility does not grant rights over supplied documents or collected website content.

## 中文说明：输入、结果与费用

本工具支持PDF 转 Excel、表格提取、电子表格下载。输入参数名保持英文，便于 AI 智能体和 MCP 客户端正确调用。结果包含来源、采集时间、稳定标识和内容哈希。请先使用少量目标验证结果，再扩大批量任务。

每条实际交付的结果计费；重复、排除和空提取结果不收费。请在 Apify 运行选项设置 `maxTotalChargeUsd`，不要放进输入 JSON。`maxResults` 限制整个任务的付费结果数量。文件转换工具会提供下载链接和文件键，访问权限由 Apify 存储设置决定。

本工具不会编造缺失字段，也不保证源站完整覆盖。邮箱 DNS 检查不等于邮箱可投递验证；数字 PDF 提取不等于扫描件 OCR；天气预报不等于历史实测数据。失败任务与真正的空结果明确区分，请同时检查数据集及免费的 `SUMMARY`。

Source documentation: https://github.com/jsvine/pdfplumber

Last verified working: 2026-10-17
