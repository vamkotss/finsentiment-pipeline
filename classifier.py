"""Core sentiment classification logic with retry and validation."""
import json
import time
from openai import OpenAI
from pydantic import ValidationError

from .schema import SentimentResult
from .prompt import SYSTEM_PROMPT


def classify_headline(
    headline: str,
    client: OpenAI = None,
    model: str = "gpt-4o-mini",
    max_retries: int = 3
) -> SentimentResult | None:
    """Classify a single headline with validation and retry logic.
    
    Args:
        headline: The financial news headline to classify
        client: OpenAI client (creates one if not provided)
        model: OpenAI model name
        max_retries: Number of retry attempts on failure
        
    Returns:
        SentimentResult on success, None on persistent failure
    """
    if client is None:
        client = OpenAI()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f'Headline: "{headline}"'}
                ]
            )
            
            raw_output = response.choices[0].message.content
            parsed = json.loads(raw_output)
            return SentimentResult(**parsed)
            
        except json.JSONDecodeError as e:
            print(f"  Attempt {attempt+1}: JSON parse failed - {e}")
        except ValidationError as e:
            print(f"  Attempt {attempt+1}: Schema validation failed - {e}")
        except Exception as e:
            print(f"  Attempt {attempt+1}: API error - {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    
    return None
