"""Financial news sentiment pipeline."""
from .schema import SentimentResult
from .classifier import classify_headline
from .batch import process_batch

__all__ = ["SentimentResult", "classify_headline", "process_batch"]
