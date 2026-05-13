"""Pydantic schema for sentiment classification output."""
from pydantic import BaseModel, Field
from typing import Literal


class SentimentResult(BaseModel):
    """Schema for a single headline's sentiment classification."""
    headline: str = Field(..., description="The original headline text")
    sentiment: Literal["bullish", "bearish", "neutral"] = Field(
        ..., description="Market sentiment of the headline"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    tickers: list[str] = Field(default_factory=list, description="Stock tickers affected")
    rationale: str = Field(..., description="One-line explanation for the classification")
