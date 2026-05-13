"""Demo script: classify a batch of sample headlines."""
import os
from src import process_batch

# Sample headlines covering different sentiment patterns
HEADLINES = [
    "Nvidia stock surges 8% in pre-market after beating earnings and raising AI chip guidance",
    "SEC charges Goldman Sachs with misleading investors over crypto fund disclosures",
    "Microsoft announces $10 billion investment in OpenAI partnership extension",
    "Meta lays off another 5,000 employees as advertising revenue continues to decline",
    "Berkshire Hathaway reports steady Q3 earnings, in line with analyst expectations",
    "JPMorgan beats Q3 estimates with strong trading revenue, raises FY guidance",
    "Federal Reserve holds interest rates steady, signals possible cut in December",
    "Pfizer reports disappointing Phase 3 trial results for cancer drug, shares drop 12%",
]


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: Set OPENAI_API_KEY environment variable")
        return
    
    print(f"Processing {len(HEADLINES)} headlines...\n")
    df, failed = process_batch(HEADLINES)
    
    print(f"\n=== Results ===")
    print(df.to_string())
    
    print(f"\n=== Sentiment Distribution ===")
    print(df["sentiment"].value_counts())
    
    df.to_csv("data/sample_output.csv", index=False)
    print(f"\nSaved to data/sample_output.csv")


if __name__ == "__main__":
    main()
