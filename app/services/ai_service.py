from openai import OpenAI
import os


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def get_ai_response(message: str):

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Med Assist AI chatbot.

                    Rules:
                    - Give general health guidance only.
                    - Do not diagnose serious diseases.
                    - Suggest doctor consultation when needed.
                    - Support Hindi and English.
                    """
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )


        return response.choices[0].message.content


    except Exception as e:

        return "AI service temporarily unavailable."