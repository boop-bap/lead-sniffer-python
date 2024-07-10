import os

from flask_cors import CORS
from flask import Flask, request, send_from_directory

from dotenv import load_dotenv
from modules.json_functions import read_json, update_json_instructions
from modules.data_functions import combine_data, create_excel_file, get_data_from_file, get_data_from_gpt

load_dotenv()

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))

allowed_origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://boop-bap.github.io",
]

CORS(app, resources={r"/*": {"origins": allowed_origins}})


## POST REQUESTS
@app.route("/upload", methods=["POST"])
async def upload_file():
    try:
        file = list(request.files.values())[0]
        file_data_list = get_data_from_file(file)

        gpt_data = await get_data_from_gpt(file_data_list)
        combined_data_list = combine_data(file_data_list, gpt_data)

        create_excel_file(combined_data_list)

        return "<p style='font-size: 24px;'>File uploaded successfully!</p>", 200
    except Exception as e:
        return f"<p style='font-size: 24px; color: red;'>An error occurred: {str(e)}</p>", 500


@app.route("/instructions/update", methods=["POST"])
def update_instructions():
    try:
        new_instructions = request.get_json()

        update_json_instructions("instructions", new_instructions)

        return "Instructions updated successfully", 200
    except Exception as e:
        return f"<p>An error occurred: {str(e)}</p>", 500


## GET REQUESTS
@app.route("/download", methods=["GET"])
def download_file():
    try:
        filename = "output.xlsx"

        return send_from_directory("xlsx_files", filename, as_attachment=True), 200
    except Exception as e:
        return f"<p>An error occurred: {str(e)}</p>", 500


@app.route("/instructions/default", methods=["GET"])
def get_default_instructions():
    try:
        instructions = read_json("json/instructions.json")["defaultInstructions"]

        return instructions, 200
    except Exception as e:
        return f"<p>An error occurred: {str(e)}</p>", 500


@app.route("/instructions/user", methods=["GET"])
def get_user_instructions():
    try:
        instructions = read_json("json/instructions.json")["userInstructions"]

        return instructions, 200
        
    except Exception as e:
        return f"<p>An error occurred: {str(e)}</p>", 500


app.run(port=PORT, host='0.0.0.0')

