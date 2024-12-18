from fastapi import APIRouter
from openai import OpenAI

router = APIRouter()

@router.post("/")
async def chat(user_id: int, message: str):
    client = OpenAI()

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        
        response = completion.choices[0].message

        # TODO: Store conversation in database
        # Add database logic here to store user_id, message and response

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}
