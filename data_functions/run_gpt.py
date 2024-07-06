import asyncio
import os
import re
import sys
import json

from openai import OpenAI
from typechat import TypeChatJsonTranslator, TypeChatValidator, create_openai_language_model


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import answer_schemas.lead_schema as answer_schemas


API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = create_openai_language_model(API_KEY, "gpt-3.5-turbo")
VALIDATOR = TypeChatValidator(answer_schemas.LeadTarget)
TRANSLATOR = TypeChatJsonTranslator(MODEL, VALIDATOR, answer_schemas.LeadTarget)

CLIENT = OpenAI(api_key=API_KEY)


def read_json(file_to_read):
    with open(file_to_read, "r") as file:
        return json.load(file)


def get_instructions() -> str:
    user_instructions = read_json("json/userInstructionsSave.json")["userInstructions"]

    gpt_instructions: str = f"""Answer should be as broad and as big as possible with no speculation and really extensively

    long and detailed with exclusive analysis on each point where and what was found. Try to aim for 1000 words.

    1. Must include the id and url provided in the answer and display it with a title only here once.

    2. Please check if the website provided is online. If offline answer offline in all of the checks.

    3. {user_instructions["monthlyOrMoreCatalogs"]}

    4. {user_instructions["type"]}

    5. {user_instructions["model"]}"""

    return gpt_instructions


async def run_gpt(website: str, record_id: str) -> str:
    print("Running GPT")
    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "name": "V1", "content": get_instructions()},
            {"role": "user", "content": f"url: {website}"},
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1000,
    )
    initial_result = chat_completion.choices[0].message.content

    remove_breaks_result = re.sub(r"(\r\n|\n|\r)", " ", initial_result)

    final_result = await TRANSLATOR.translate(remove_breaks_result)
    final_result.value["provided_id"] = record_id

    return final_result
