from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# ---------------- BASIC DATA ----------------
REQUIRED_SKILLS = [
    "python", "java", "javascript", "sql", "html", "css",
    "flask", "django", "react", "git", "api", "machine learning"
]

ACTION_VERBS = [
    "developed", "designed", "implemented", "optimized",
    "built", "created", "led", "improved", "managed"
]

# ---------------- ANALYSIS LOGIC ----------------
def analyze_resume(text):
    text_lower = text.lower()
    score = 0
    feedback = []

    # Length check
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        score += 20
    else:
        feedback.append("Resume length should be between 300–800 words.")

    # Skills check
    found_skills = [s for s in REQUIRED_SKILLS if s in text_lower]
    skill_score = min(len(found_skills) * 4, 40)
    score += skill_score

    if len(found_skills) < 5:
        feedback.append("Add more technical skills relevant to the job.")

    # Action verbs check
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if found_verbs:
        score += 20
    else:
        feedback.append("Use strong action verbs (e.g., developed, implemented).")

    # Formatting check
    if re.search(r"\n[A-Z][a-z]+", text):
        score += 10
    else:
        feedback.append("Use clear section headings (Experience, Skills, Projects).")

    # Keyword density
    keyword_density = len(found_skills) / max(word_count, 1)
    if keyword_density >= 0.02:
        score += 10
    else:
        feedback.append("Increase keyword density for ATS optimization.")

    return {
        "score": min(score, 100),
        "skills_found": found_skills,
        "feedback": feedback
    }

# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Resume Analyzer</title>
<style>
body {
  background:#0f172a;
  color:white;
  font-family:Arial;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
}
.container {
  background:#020617;
  padding:20px;
  border-radius:12px;
  width:90%;
  max-width:700px;
}
textarea {
  width:100%;
  height:200px;
  padding:10px;
  border-radius:8px;
}
button {
  margin-top:10px;
  padding:10px;
  width:100%;
  border:none;
  border-radius:8px;
  background:#22c55e;
  font-weight:bold;
}
.score {
  font-size:24px;
  margin-top:10px;
}
.bad {
  color:#f87171;
}
.good {
  color:#4ade80;
}
</style>
</head>
<body>
<div class="container">
<h2>📄 AI Resume Analyzer</h2>
<form method="POST">
<textarea name="resume" placeholder="Paste your resume here...">{{resume}}</textarea>
<button type="submit">Analyze Resume</button>
</form>

{% if result %}
<div class="score">ATS Score: {{result.score}} / 100</div>

<h3>Skills Detected:</h3>
<p>{{result.skills_found}}</p>

<h3>Feedback:</h3>
<ul>
{% for f in result.feedback %}
<li class="bad">{{f}}</li>
{% endfor %}
{% if not result.feedback %}
<li class="good">Great resume! Minor improvements only.</li>
{% endif %}
</ul>
{% endif %}
</div>
</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resume = ""

    if request.method == "POST":
        resume = request.form.get("resume", "")
        result = analyze_resume(resume)

    return render_template_string(HTML, result=result, resume=resume)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
