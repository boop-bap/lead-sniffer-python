import os
import asyncio
from dotenv import load_dotenv
from data_functions.run_gpt import run_gpt

load_dotenv()


async def main(website, id):
    test = await run_gpt(website, id)

    print(test)


asyncio.run(main("bilka.dk", "1225878896"))
