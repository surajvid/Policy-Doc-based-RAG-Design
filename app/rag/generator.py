"""
generator.py

Non-technical explanation:
- This file is responsible for generating the final answer.
- It takes:
  (a) user question
  (b) evidence chunks from Qdrant
- and asks the AI model to respond using ONLY those chunks.
"""

from openai import OpenAI
from app.core.config import settings
from app.rag.prompts import SYSTEM_PROMPT

openai_client = OpenAI(api_key=settings.openai_api_key)


def generate_answer(question: str, evidence_chunks: list[dict]) -> str:
    """
    Generate an answer using the AI model, grounded in evidence.

    If no evidence chunks are found, we return a refusal message.
    """

    # If we found nothing relevant, do not call the AI model.
    if not evidence_chunks:
        return "I don’t have enough information in the documents to answer that."

    # Create a readable evidence block for the AI model
    evidence_text = "\n\n".join(
        [
            f"[Source: {c['file']} | chunk {c['chunk_index']}]\n{c['text']}"
            for c in evidence_chunks
        ]
    )

    # Ask the AI model
    response = openai_client.chat.completions.create(
        model=settings.model_chat,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nEvidence snippets:\n{evidence_text}",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
