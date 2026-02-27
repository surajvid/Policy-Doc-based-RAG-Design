"""
embeddings.py

Non-technical explanation:
- An embedding is a numeric representation of text meaning.
- Similar meanings → similar numbers.

We use OpenAI embeddings to convert:
- each chunk (paragraph) into a vector
- later: each question into a vector for search
"""

from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIConnectionError
from app.core.config import settings

openai_client = OpenAI(api_key=settings.openai_api_key)

def embed_texts(texts: list[str]) -> list[list[float]]:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your .env and restart.")

    try:
        response = openai_client.embeddings.create(
            model=settings.model_embed,
            input=texts,
        )
        return [item.embedding for item in response.data]

    except AuthenticationError as e:
        raise RuntimeError("OpenAI authentication failed. Check OPENAI_API_KEY.") from e
    except RateLimitError as e:
        raise RuntimeError("OpenAI rate limit exceeded. Try again later.") from e
    except APIConnectionError as e:
        raise RuntimeError("Could not connect to OpenAI. Check network.") from e
