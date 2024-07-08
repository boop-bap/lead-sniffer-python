import json


def read_json(file_to_read):
    with open(file_to_read, "r") as file:
        return json.load(file)


def update_json_instructions(file_to_write, new_instructions):

    # Load the existing instructions from the file
    with open(f"json/{file_to_write}.json", "r") as file:
        instructions = json.load(file)

    # Update the instructions in the data
    instructions["userInstructions"] = new_instructions

    # Write the updated data to the file
    with open(f"json/{file_to_write}.json", "w") as file:
        json.dump(instructions, file, indent=4)
