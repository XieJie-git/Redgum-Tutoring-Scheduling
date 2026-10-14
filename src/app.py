from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# In-memory storage for allocations (replace with database later)
allocations = []

# US004: Check duplicate tutor session at same time
def is_tutor_time_duplicate(tutor_name, session_time):
    for record in allocations:
        if record["tutor_name"] == tutor_name and record["session_time"] == session_time:
            return True
    return False

@app.route('/')
def index():
    return "Redgum Tutoring Scheduling Web App"

@app.route("/allocation")
def allocation_page():
    return render_template("allocation.html", allocations=allocations)

@app.route("/add-allocation", methods=["POST"])
def add_allocation():
    tutor_name = request.form.get("tutor_name")
    student_name = request.form.get("student_name")
    session_time = request.form.get("session_time")

    # US004 validation rule
    if is_tutor_time_duplicate(tutor_name, session_time):
        flash(f"Error: Tutor {tutor_name} already has a session at {session_time}. Cannot create duplicate allocation.")
        return redirect(url_for("allocation_page"))

    new_record = {
        "tutor_name": tutor_name,
        "student_name": student_name,
        "session_time": session_time
    }
    allocations.append(new_record)
    flash("Allocation created successfully!")
    return redirect(url_for("allocation_page"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
