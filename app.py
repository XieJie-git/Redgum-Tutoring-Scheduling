from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# flash消息需要密钥，用于页面提示
app.secret_key = "mysecretkey123"

# Sprint1 模拟内存数据
mock_students = [
    {"id": 1, "name": "Alice Smith", "year_level": "Year 9", "contact_phone":"12345678"},
    {"id": 2, "name": "Bob Jones", "year_level": "Year 10", "contact_phone":"87654321"}
]

mock_tutors = [
    {"id":1,"name":"Tom Wilson","specialty":"Math"},
    {"id":2,"name":"Lisa Brown","specialty":"Chemistry"}
]

allocations = []

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/students')
def student_page():
    return render_template('students/index.html', students=mock_students)

@app.route('/tutors/assign', methods=["GET","POST"])
def assign_tutor():
    # Sprint2：读取url参数，预选中学生
    pre_select_student_id = request.args.get("student_id", type=int)

    if request.method == "POST":
        student_id = int(request.form["student_id"])
        tutor_id = int(request.form["tutor_id"])

        # Sprint2 业务校验：不允许同一个学生重复分配
        for item in allocations:
            for s in mock_students:
                if s["id"] == student_id and item["student_name"] == s["name"]:
                    flash("Error: This student already has an allocation!")
                    return redirect(url_for("assign_tutor"))

        s = next(x for x in mock_students if x["id"] == student_id)
        t = next(x for x in mock_tutors if x["id"] == tutor_id)

        new_item = {
            "student_name": s["name"],
            "tutor_name": t["name"],
            "time": "Monday 14:00"
        }
        allocations.append(new_item)
        flash("Allocation created successfully!")
        return redirect(url_for("schedule_page"))

    return render_template('tutors/assign.html',
                           tutors=mock_tutors,
                           students=mock_students,
                           pre_select_student_id=pre_select_student_id)

# Sprint2 新增：删除单条分配记录路由
@app.route("/schedule/delete/<int:index>", methods=["POST"])
def delete_allocation(index):
    if 0 <= index < len(allocations):
        del allocations[index]
        flash("Allocation record removed.")
    return redirect(url_for("schedule_page"))

@app.route('/schedule')
def schedule_page():
    return render_template('schedule/index.html', schedule=allocations)

# ===================== US010 Session Report =====================
sessions = [
    {"session_id": 1, "student_name": "Alice", "tutor_name": "Tutor A", "subject": "Math", "time": "Mon 10:00"},
    {"session_id": 2, "student_name": "Bob", "tutor_name": "Tutor B", "subject": "English", "time": "Tue 14:00"},
    {"session_id": 3, "student_name": "Charlie", "tutor_name": "Tutor A", "subject": "Math", "time": "Wed 11:00"},
    {"session_id": 4, "student_name": "Diana", "tutor_name": "Tutor C", "subject": "Physics", "time": "Thu 15:30"}
]

@app.route('/report')
def session_report():
    """Render tutoring session report page for admin"""
    return render_template("report.html", session_list=sessions)
# ===============================================================

if __name__ == '__main__':
    app.run(debug=True)
