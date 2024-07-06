import os
import asyncio

from dotenv import load_dotenv
from data_functions.data_functions import combine_data, create_excel_file, get_data_from_file, get_data_from_gpt

load_dotenv()


async def main():
    file_path = os.path.join("xlsx_files", "2.xlsx")

    file_data_list = get_data_from_file(file_path)
    gpt_data = await get_data_from_gpt(file_data_list)

    combined_data_list = combine_data(file_data_list, gpt_data)
    create_excel_file(combined_data_list)


asyncio.run(main())
