# Financial News Sentiment Pipeline

A production-style LLM pipeline that classifies financial news headlines as bullish, bearish, or neutral with structured JSON output, schema validation, and retry logic.

## Business problem

Trading desks and market intelligence teams need to classify the sentiment of breaking financial news at scale. Headlines about earnings, regulatory actions, M&A, and macro events can move markets within seconds, and a human reading 500 headlines a day is too slow. A general-purpose LLM is great at sentiment but expensive to call ad-hoc and unstructured. This pipeline takes batches of headlines and outputs clean, schema-validated signals ready for downstream trading or analytics systems.

## Architecture

```
Headlines (list)
    |
    v
Few-shot prompt with 3 anchored examples (bullish / bearish / neutral)
    |
    v
OpenAI gpt-4o-mini  (temperature=0, JSON mode)
    |
    v
JSON parse + Pydantic schema validation
    |
    v
Retry with exponential backoff (1s, 2s, 4s)
    |
    v
DataFrame + CSV output
```

## Key design decisions

**Few-shot prompting with 3 anchored examples** (bullish, bearish, neutral) calibrates the model on classification boundaries. Zero-shot tends to over-predict bullish on neutral headlines.

**Temperature 0 + JSON mode** for deterministic, parseable output. Sentiment classification should not vary across runs.

**Pydantic schema validation** with Literal types on the sentiment field and bounded floats on confidence. The model cannot return an invalid label or out-of-range confidence.

**Three-layer error handling** distinguishes JSON parse failures, schema validation failures, and API errors so we can retry intelligently.

**Exponential backoff** (1s, 2s, 4s) on retries to handle transient API issues without hammering the endpoint.

**Batch processing** returns both a DataFrame of successes and a list of failed headlines so downstream systems can route failures separately.

## Stack

- Python 3.11+
- OpenAI Python SDK (gpt-4o-mini with JSON mode)
- Pydantic for schema validation
- Pandas for tabular output

## Usage

```python
from finsentiment.src import process_batch

headlines = [
    "Nvidia stock surges 8% in pre-market after beating earnings",
    "SEC charges Goldman Sachs with misleading investors",
    "Federal Reserve holds rates steady as expected"
]

df, failed = process_batch(headlines)
df.to_csv("results.csv", index=False)
```

## Setup

```bash
pip install openai pydantic pandas
export OPENAI_API_KEY="sk-..."
```

## Sample output

| headline | sentiment | confidence | tickers | rationale |
|----------|-----------|------------|---------|-----------|
| Nvidia stock surges 8%... | bullish | 0.95 | NVDA | Beating earnings strongly positive |
| SEC charges Goldman Sachs... | bearish | 0.85 | GS | Regulatory action creates legal risk |
| Federal Reserve holds rates steady... | neutral | 0.75 | | Outcome was widely expected |

## Cost

At gpt-4o-mini pricing, ~$0.001 per headline. Batch of 1000 headlines: ~$1.

## What I would improve next

- **Hybrid model routing**: cheap model for clear cases, escalate to stronger model for low-confidence cases
- **Multi-headline batching** in a single API call to reduce per-call overhead
- **Async parallelization** with rate limit handling for higher throughput
- **Eval harness** with a labeled gold set to measure accuracy per sentiment class
- **Drift monitoring** on confidence distributions to catch model degradation
- **Tool calling** instead of JSON mode for stronger structured output guarantees

## License

MIT