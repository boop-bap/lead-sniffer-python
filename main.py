import os

import pandas as pd
from flask_cors import cross_origin
from flask import Flask, request, send_from_directory

from dotenv import load_dotenv
from modules.data_functions import combine_data, create_excel_file, get_data_from_file, get_data_from_gpt

load_dotenv()

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))


@app.route("/upload", methods=["POST"])
async def upload_file():

    if request.method == "POST":

        file_data_list = get_data_from_file(request.files["hi"])

        gpt_data = await get_data_from_gpt(file_data_list)

        combined_data_list = combine_data(file_data_list, gpt_data)

        create_excel_file(combined_data_list)

    return "<p>Hello, World!</p>"


@app.route("/download", methods=["GET"])
def download_file():
    if request.method == "GET":
        filename = "output.xlsx"

        return send_from_directory("xlsx_files", filename)


app.run(port=PORT)
