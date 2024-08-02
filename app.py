from flask import Flask, request, jsonify, render_template
import subprocess
import os, re
from gdrive import Download_Colab_Notebook
import nbformat
from nbconvert import MarkdownExporter
from datetime import datetime
from pathlib import Path

app = Flask(__name__)


import subprocess

def convert_notebook_to_qmd(notebook_path, output_path):
    subprocess.run(["quarto", "convert", notebook_path, "--output", output_path])


def render_quarto_site(quarto_project_path):
    subprocess.run(["quarto", "render"], cwd=quarto_project_path)

def to_snake_case(name):
    wds = name.split()
    return '_'.join(wds)

def extract_file_id(file_url):
    wds = file_url.split("/drive/")
    print(wds)
    if len(wds) <= 1:
        return ""
    last_part = wds[1].split("#")
    return last_part[0]


def replace_qmd_header(qmd_path, date, title, author, tags):
    # Define the new header content
    new_header = f"""---
title: "{title}"
author: "{author}"
date: "{date}"
tags: {tags}
---
"""

    # Read the contents of the .qmd file
    with open(qmd_path, 'r') as file:
        lines = file.readlines()

    # Find the header section and the body
    in_header = False
    body_lines = []
    for line in lines:
        if line.strip() == '---':
            if in_header:
                # End of the header section
                in_header = False
                # Skip the existing header lines
                continue
            else:
                # Start of the header section
                in_header = True
        if not in_header:
            body_lines.append(line)

    # Write the new header and the original body back to the .qmd file
    with open(qmd_path, 'w') as file:
        file.write(new_header)
        file.writelines(body_lines)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/publish', methods=['POST'])
def publish():
    notebook_url = request.form['notebookUrl']
    title = request.form['title']
    author = request.form['author']
    tags = request.form.get('tags', '').split(',')
    notebook_name = to_snake_case(title)
    # Get the current date
    current_date = datetime.now()
    # Format the date as 'YYYY-MM-DD
    formatted_date = current_date.strftime('%Y-%m-%d')


    cwd = os.path.dirname(os.path.realpath(__file__))

    # Download notebook from Google Colab
    notebook_path = cwd + '/downloaded/{0}.ipynb'.format(notebook_name)
    Download_Colab_Notebook(extract_file_id(notebook_url), notebook_path)

    # Convert notebook to QMD
    qmd_output_dir = './posts/{0}'.format(notebook_name)
    qmd_file_path = '{0}/{1}.qmd'.format(qmd_output_dir, notebook_name)
    Path("{0}".format(qmd_output_dir)).mkdir(parents=True, exist_ok=True)
    convert_notebook_to_qmd(notebook_path, qmd_file_path)
    replace_qmd_header(qmd_file_path, formatted_date,title, author, tags)


    # Render Quarto site
    quarto_project_path = cwd
    render_quarto_site(quarto_project_path)

    return jsonify({'message': 'Notebook published successfully'})


def TestCamelCase():
    print(to_snake_case("Data INterviiew"))
    publish()
    Download_Colab_Notebook()

if __name__ == '__main__':
    app.run(debug=True)
    # TestCamelCase()
    # f = extract_file_id("https://colab.research.google.com/drive/1c_BRX7waz8nBRMFVSoJnz1SMGorFqZhS#scrollTo=3sieAtTFYg9n")
    # print("here....")
    # print(f)