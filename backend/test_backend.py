import asyncio
from app import ask
from pydantic import BaseModel

class Question(BaseModel):
    question: str

async def test():
    q = Question(question="How to manage time effectively?")
    result = ask(q)
    print("Answer:", result["answer"])

if __name__ == "__main__":
    asyncio.run(test())