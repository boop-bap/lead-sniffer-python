import os
import asyncio
import pandas as pd

from data_functions.run_gpt import run_gpt


def split_array_into_chunks(list, chunk_size: int = 1) -> list[list]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


def get_data_from_file(path):
    if os.path.exists(path):
        # Read the file into a DataFrame
        data = pd.read_excel(path)

        # Convert the DataFrame to a list of dictionaries
        data_list = data.to_dict(orient="records")

        return split_array_into_chunks(data_list, 1)
    else:
        # Raise an exception if the file was not found
        raise FileNotFoundError(f"File not found: {path}")


async def get_data_from_gpt(chunk_data):
    final_results = []

    for i, chunk in enumerate(chunk_data):
        gpt_tasks = []
        for item in chunk:
            website = item["Website URL"]
            record_id = item["Record ID"]
            gpt_tasks.append(run_gpt(website, record_id))

        # Wait for all coroutines to complete and get their results
        results = await asyncio.gather(*gpt_tasks)
        final_results.extend(results)

        print(f"Chunk {i+1} of {len(chunk_data)}")

        # Wait for 1 second before processing the next chunk
        await asyncio.sleep(1)
        print(final_results)

    return final_results


def combine_data(file_data_list, gpt_data):
    combined_data = []

    for item_list in file_data_list:
        for item in item_list:

            record_id = item["Record ID"]
            gpt_result = next((result.value for result in gpt_data if result.value["provided_id"] == record_id), None)

            if gpt_result:
                combined_item = {**item, **gpt_result}
                combined_data.append(combined_item)

    return combined_data


def create_excel_file(data_list):
    # Convert the list of dictionaries to a DataFrame
    data = pd.DataFrame(data_list)

    # Define the folder path and file path
    folder_path = "xlsx_files"
    file_path = "xlsx_files/output.xlsx"

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write the DataFrame to an Excel file
    data.to_excel(file_path, index=False)
