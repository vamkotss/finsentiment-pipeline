"""Batch processor for classifying multiple headlines."""
import pandas as pd
from openai import OpenAI

from .classifier import classify_headline


def process_batch(headlines: list[str], verbose: bool = True) -> tuple[pd.DataFrame, list[str]]:
    """Process a list of headlines and return results.
    
    Args:
        headlines: List of headline strings to classify
        verbose: If True, print progress
        
    Returns:
        (DataFrame of results, list of failed headlines)
    """
    client = OpenAI()
    results = []
    failed = []
    
    for i, headline in enumerate(headlines, 1):
        if verbose:
            print(f"[{i}/{len(headlines)}] {headline[:70]}...")
        
        result = classify_headline(headline, client=client)
        
        if result:
            results.append(result.model_dump())
            if verbose:
                print(f"  -> {result.sentiment.upper()} | conf={result.confidence:.2f} | {result.tickers}")
        else:
            failed.append(headline)
            if verbose:
                print(f"  -> FAILED")
    
    df = pd.DataFrame(results)
    return df, failed
