import os
import re
import sys
import json

from openai import OpenAI
from typechat import TypeChatJsonTranslator, TypeChatValidator, create_openai_language_model

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schemas.lead_schema import LeadTarget as schema


API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = create_openai_language_model(API_KEY, "gpt-3.5-turbo")
VALIDATOR = TypeChatValidator(schema)
TRANSLATOR = TypeChatJsonTranslator(MODEL, VALIDATOR, schema)

CLIENT = OpenAI(api_key=API_KEY)


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def getInstructions() -> str:
    user_instructions = read_json("json/userInstructionsSave.json")["userInstructions"]

    gpt_instructions: str = f"""Answer should be as broad and as big as possible with no speculation and really extensively

    long and detailed with exclusive analysis on each point where and what was found. Try to aim for 1000 words.

    1. Must include the id and url provided in the answer and display it with a title only here once.

    2. Please check if the website provided is online. If offline answer offline in all of the checks.

    3. {user_instructions["monthlyOrMoreCatalogs"]}

    4. {user_instructions["type"]}

    5. {user_instructions["model"]}"""

    return gpt_instructions


async def run_gpt(website: str, recordId: str) -> str:
    print("Running GPT")

    chat_completion = CLIENT.chat.completions.create(
        messages=[
            {
                "role": "system",
                "name": "V1",
                "content": getInstructions(),
            },
            {"role": "user", "content": f"url: {website} id: {recordId}"},
        ],
        model="gpt-3.5-turbo",
        temperature=0,  # Higher values means the model will take more risks.
        max_tokens=1000,  # The maximum number of tokens to generate in the completion. 0-4096
    )

    initial_result: str = chat_completion.choices[0].message.content

    remove_breaks_result = re.sub(r"(\r\n|\n|\r)", " ", initial_result)

    final_result = await TRANSLATOR.translate(remove_breaks_result)

    return final_result
