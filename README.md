# Review Pro coding exercise

A Scrapy spider that scrapes the [ReviewPro page](https://www.shijigroup.com/reviewpro-reputation) and extracts the products and solutions listed on the page.

## Output

The spider yields a single item structured and export into a JSON.

Results are written to `data/review_pro_<timestamp>.json`.

## Usage

Clone repository:

```bash
git clone https://github.com/0xthedance/rp-scraper
cd rp-scraper
```

Use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate 
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the spider from inside the `reviewproscrapy/` directory:

```bash
scrapy crawl review_pro
```

Output is saved automatically to `data/review_pro_<timestamp>.json`.


## Notes

### Selectors

The spider mixes CSS selectors and XPath deliberately:
- CSS is used for class-based selection (`p.nav-side-pannel__title::text`) as it handles multi-class elements more robustly and less verbose. Explain [here](https://docs.scrapy.org/en/latest/topics/selectors.html#when-querying-by-class-consider-using-css)
- XPath is kept where attribute-based selection is needed (example: `./a/@href`) or when establishing a sibling relationship.

### Output format

- All URLs are resolved to absolute URLs using `response.urljoin()` before being stored.
- If a `href` attribute is missing, the `url` field is set to `None` rather than raising an error.
- Strip potential whitespaces from title field
- If no products and no solutions are extracted, the spider logs a warning to signal a likely selector regression.
- The output is saved in a JSON file with the date in the file name. The reasons to choose this format are:
    - The scrapped data has a variable nested structure. Solutions items has a variable number and types of sections. This irregular shape dont fit with rigid tables that will result in wasting columns or splitting into multiple files. JSON represents this naturally. Worth mention that this format is also more aligned with NoSQL databases.
    - The 1:N relation is more human-readable with this format. 
    - JSON is the most common standard exchange format for web APIs and it is the common format used by most data tools, making it easy to feed the output into downstream scripts or applications without a parsing step.
 
- Scrapy [Feed Exports](https://docs.scrapy.org/en/latest/topics/feed-exports.html) is used to export the data. It is defined in `settings`.

## Further works

1. **Develop pipelines**: Potential useful pipeline worth consider are:
   - Filter out entries where `title` or `url` is `None`
   - Load the result in a database

2. **Enable HTTP caching**: Scrapped data is very stable by nature (not many changes are expected), for this reason, consider uncomment the `HTTPCACHE_*` settings in `settings.py` to avoid re-fetching unchanged pages between runs. 
