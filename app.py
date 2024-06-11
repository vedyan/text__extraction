from flask import Flask, request, jsonify
import fitz
import requests
import re
from utils import extract_projects, extract_experience, extract_skills

app = Flask(__name__)


def extract_mobile_number(text):
    mobile_number = re.findall(r'[7-9][0-9]{9}', text)
    return mobile_number


def extract_email(text):
    email_pattern = r"\b([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{1,64})\b"  # Optimized pattern
    email_match = re.search(email_pattern, text)
    return email_match.group(0) if email_match else ""


def extract_name(text):
    name_match = re.search(r"([A-Z][a-z]+\s+){1,3}", text)
    name = name_match.group(0).strip() if name_match else ""
    return name


@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        pdf_file = request.files['pdf_file']
        pdf_data = pdf_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        name = extract_name(text)
        email = extract_email(text)
        number = extract_mobile_number(text)

        return jsonify({
            "text": text,
            "name": name,
            "email": email,
            "number": number
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/extract_text_from_url", methods=["POST"])
def extract_text_from_url():
    try:
        pdf_url = request.form.get("pdf_url")
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_data = response.content

        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        name = extract_name(text)
        email = extract_email(text)
        number = extract_mobile_number(text)

        return jsonify({
            "text": text,
            "name": name,
            "email": email,
            "number": number
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching PDF from URL: {str(e)}"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/extract_experience", methods=["POST"])
def extract_experience_from_text():
    try:
        text = request.json.get("text")
        experience = extract_experience(text)

        return jsonify({
            "experience": experience
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/extract_projects", methods=["POST"])
def extract_projects_from_text():
    try:
        text = request.json.get("text")
        projects = extract_projects(text)

        return jsonify({
            "projects": projects
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/extract_skills", methods=["POST"])
def extract_skills_from_text():
    try:
        text = request.json.get("text")
        skills = extract_skills(text)

        return jsonify({
            "skills": skills
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
