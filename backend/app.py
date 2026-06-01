
from flask import Flask, render_template, redirect

app = Flask(__name__)

# ท่าปัจจุบัน (ยังจำไว้ได้)
exercise = "bicep"

# =========================
# หน้าเว็บ
# =========================
@app.route('/')
def home():
    return render_template("index.html", exercise=exercise)

# =========================
# เปลี่ยนท่า
# =========================
@app.route('/set/<name>')
def set_exercise(name):

    global exercise

    exercises = [
        "bicep",
        "shoulder",
        "lateral",
        "squat"
    ]

    if name in exercises:
        exercise = name

    return redirect('/')

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )