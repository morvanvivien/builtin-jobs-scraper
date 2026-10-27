# BuiltIn.com Scraper: US Tech Job Postings, No Login

> **Run it now, no code: [builtin-jobs-scraper on the Apify Store](https://apify.com/bibian/builtin-jobs-scraper)** &nbsp;|&nbsp; $0.60 per 1,000 postings &nbsp;|&nbsp; no browser, no proxy

[BuiltIn.com](https://builtin.com) is a major US tech job board covering every region of the country (New York, LA, Boston, Austin, Colorado, Chicago, Seattle, SF Bay Area and the rest) from a single feed. It has no public export and no official API for third parties. This guide shows how to get its tech job postings as clean structured data — title, company, salary range, location, remote status, industry and full description — with a free Apify Actor, from the console or from code.

Searches this page answers: builtin.com scraper, builtin jobs scraper, US tech job postings scraper, tech jobs data extraction, remote tech jobs scraper.

## What you get

- US tech job postings from BuiltIn: title, company, location, remote status, employment type, industry and date posted.
- Salary range (`salaryMin`, `salaryMax`) when the posting discloses it.
- `isRemote` flag plus `city`/`region`/`country` for on-site and hybrid roles.
- Optional full description as plain text.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, no personal data, long text truncated) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | BuiltIn posting id and public link |
| `title` | Job title as published |
| `companyName` | Hiring company as displayed |
| `isRemote` | Whether the posting is fully remote |
| `city`, `region`, `country` | Where the job is based; `null` for fully remote roles with no stated base |
| `industries` | Array of industries BuiltIn tags the employer with |
| `salaryMin`, `salaryMax`, `salaryCurrency` | Salary range, as numbers, when disclosed |
| `employmentType` | For example `FULL_TIME` |
| `datePosted` | Publication date, ISO 8601 |
| `description` | Plain text, only when `includeDescription` is on; no personal data |

## Use cases

- **Monitor the US tech job market**: new postings across every tech company on BuiltIn, refreshed on your own schedule.
- **Feed a job alert or an aggregator**: run it daily and keep only the postings with a `datePosted` you have not seen yet.
- **Find companies that are hiring**: which employers are posting tech roles right now, and in which city or industry.
- **Benchmark tech salaries**: published salary ranges by role, company and location, including fully remote roles.

## Input

| Field | What it does |
|---|---|
| `maxItems` | The run stops once this many postings are saved (default 50). |
| `includeDescription` | Add the full job description as plain text. |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

The actor reads BuiltIn's default job listing (no keyword or location filter): `robots.txt` disallows the site's own `?search=` and per-city/per-category query filters, so this actor never targets them.

Example input:

```json
{
  "maxItems": 50,
  "includeDescription": true
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/builtin-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the short input form (maximum number of results, include description) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/builtin-jobs-scraper').call({
    "maxItems": 50,
    "includeDescription": true
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.companyName} | ${item.city ?? (item.isRemote ? 'Remote' : '-')} | ${item.salaryMin ?? '-'}-${item.salaryMax ?? '-'}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/builtin-jobs-scraper").call(run_input={
    "maxItems": 50,
    "includeDescription": True,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    location = item.get("city") or ("Remote" if item.get("isRemote") else "-")
    print(f"{item['title']} | {item.get('companyName')} | {location} | {item.get('salaryMin')}-{item.get('salaryMax')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$0.60 per 1,000 postings** (a 50-posting test run costs about $0.04), plus a tiny start fee. You only pay for the postings you receive. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/builtin-jobs-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- The actor reads BuiltIn's default job feed: no keyword or location filter, because the site's own search and per-city/per-category query filters are disallowed by `robots.txt` for every robot.
- Salary is `null` for postings where the employer did not disclose a range; this is common and visible in `sample-output.json`.
- The dataset contains job postings only. No personal contact details of individual recruiters are exported — only company names, which are public employer information.
- This is an unofficial tool, not affiliated with BuiltIn. Check the site terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
No. The Actor reads the data directly, so a 50-posting run finishes in about 30 seconds.

**Can I filter by city or technology?**  
Not server-side: BuiltIn disallows its own search and filter query parameters in `robots.txt`. Filter the returned items client-side instead, for example on `city`, `industries` or `title`.

**How do I only get new postings every day?**  
Set `onlyNew` on and schedule the Actor once a day. Results come newest first, so new postings are returned, and charged, only once.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open builtin-jobs-scraper on the Apify Store](https://apify.com/bibian/builtin-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
