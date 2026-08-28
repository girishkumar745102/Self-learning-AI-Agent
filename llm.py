"""
llm.py
-------
This module communicates with the Groq API and provides memory
to the LLM as context so that it can give personalized/relevant responses.
"""

import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_response(user_message: str, relevant_memories: list[str]) -> str:
    if relevant_memories:
        memory_context = "\n".join(f"- {m}" for m in relevant_memories)
    else:
        memory_context = "No previous memory found"

    system_prompt = f"""you are a helpfull AI assistant that learns abourt
    the user and remember things.
    Below are some known facts about the user (retrieved from memory).
    Use these to give a persionalized response,
    if relevant

    Always respond in English or Hinglish (Roman script),
    never in Devanagari/Hindi script , regardless of 
    what language the user writes in.

    known facts about user:
    {memory_context}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system","content": system_prompt},
            {"role": "user","content":user_message},
        ],

    )
    return response.choices[0].message.content




