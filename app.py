
from flask import Flask, request, render_template_string, send_file
import pdfplumber
import re
import pandas as pd
from io import BytesIO

app = Flask(__name__)

SKILLS = [
    "Python", "Java", "C", "C++", "SQL", "HTML", "CSS",
    "JavaScript", "Flask", "Django", "Machine Learning",
    "Deep Learning", "Data Science", "Pandas", "NumPy",
    "Power BI", "Excel", "React", "Node.js",
    "TensorFlow", "Scikit-learn", "Git"
]

EDUCATION = [
    "B.Tech", "B.E", "M.Tech", "M.E", "B.Sc", "M.Sc",
    "B.Com", "M.Com", "MBA", "MCA", "BCA",
    "Bachelor", "Master", "Intermediate", "Diploma", "Ph.D"
]

def parse_resume(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    name = "Not Found"
    for line in lines[:8]:
        if (
            len(line.split()) in [2, 3, 4]
            and re.fullmatch(r"[A-Za-z]+(?:[ .'-][A-Za-z]+)*", line)
            and not any(word in line.lower()
                        for word in ["resume", "curriculum", "vitae", "profile"])
        ):
            name = line
            break

    emails = re.findall(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text
    )

    phones = re.findall(
        r'(?:\+91[\s-]?)?[6-9]\d{9}', text
    )

    skills = [
        skill for skill in SKILLS
        if re.search(r'(?<!\w)' + re.escape(skill) + r'(?!\w)',
                     text, re.IGNORECASE)
    ]

    education = list(dict.fromkeys(
        line for line in lines
        if any(re.search(re.escape(keyword), line, re.IGNORECASE)
               for keyword in EDUCATION)
    ))

    return {
        "Candidate Name": name,
        "Email": emails[0] if emails else "Not Found",
        "Phone": phones[0] if phones else "Not Found",
        "Technical Skills": ", ".join(skills) if skills else "Not Found",
        "Education": " | ".join(education) if education else "Not Found"
    }

HTML = """
<h1>Automated Resume Parser</h1>
<p>Upload a PDF resume to extract candidate information.</p>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="resume" accept=".pdf" required>
    <button type="submit">Parse Resume</button>
</form>
{% if data %}
    <h2>Extracted Information</h2>
    <table border="1" cellpadding="8">
    {% for key, value in data.items() %}
        <tr><th>{{ key }}</th><td>{{ value }}</td></tr>
    {% endfor %}
    </table>
    <p><a href="/download">Download CSV</a></p>
{% endif %}
"""

latest_data = None

@app.route("/", methods=["GET", "POST"])
def home():
    global latest_data

    data = None

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or not file.filename.lower().endswith(".pdf"):
            return "Please upload a valid PDF file.", 400

        try:
            latest_data = parse_resume(file)
            data = latest_data
        except Exception:
            return "Unable to read this PDF. Please try another file.", 400

    return render_template_string(HTML, data=data)

@app.route("/download")
def download():
    if latest_data is None:
        return "Please parse a resume first.", 400

    df = pd.DataFrame([latest_data])
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="parsed_resume_details.csv"
    )

if __name__ == "__main__":
    app.run(debug=True)
