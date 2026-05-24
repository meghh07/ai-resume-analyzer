from gemini_helper import analyze_resume
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills Database
skills_db = [
    "python",
    "docker",
    "jenkins",
    "aws",
    "linux",
    "git",
    "github",
    "terraform",
    "kubernetes",
    "sql",
    "flask",
    "ci/cd"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Gemini Analysis
    try:
        ai_analysis = analyze_resume(text)
    except Exception as e:
        ai_analysis = f"Gemini Error: {str(e)}"

    # Skill Detection Logic
    resume_text = text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    total_skills = len(skills_db)

    ats_score = int(
        (len(found_skills) / total_skills) * 100
    )

    missing_skills = [
        skill
        for skill in skills_db
        if skill not in found_skills
    ]

    # Resume Rating
    if ats_score >= 80:
        rating = "Excellent ⭐⭐⭐⭐"
    elif ats_score >= 60:
        rating = "Good ⭐⭐⭐"
    elif ats_score >= 40:
        rating = "Average ⭐⭐"
    else:
        rating = "Needs Improvement ⭐"

    # Suggestions
    suggestions = []

    if "linux" in missing_skills:
        suggestions.append(
            "Add Linux experience or projects."
        )

    if "flask" in missing_skills:
        suggestions.append(
            "Build and mention Flask projects."
        )

    if "terraform" in missing_skills:
        suggestions.append(
            "Learn Infrastructure as Code using Terraform."
        )

    if "kubernetes" in missing_skills:
        suggestions.append(
            "Add Kubernetes deployment experience."
        )

    if not suggestions:
        suggestions.append(
            "Strong profile. Keep building projects."
        )

    return render_template(
        "result.html",
        extracted_text=text,
        found_skills=found_skills,
        missing_skills=missing_skills,
        ats_score=ats_score,
        rating=rating,
        suggestions=suggestions,
        ai_analysis=ai_analysis
    )


if __name__ == "__main__":
    app.run(debug=True)