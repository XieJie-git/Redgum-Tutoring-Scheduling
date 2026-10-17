from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
# flash消息需要密钥，用于页面提示
app.secret_key = "mysecretkey123"

# Sprint1 模拟内存数据（已扩充，页面内容更饱满）
mock_students = [
    {"id": 1, "name": "Alice Smith", "year_level": "Year 9", "contact_phone":"12345678", "username":"alice01"},
    {"id": 2, "name": "Bob Jones", "year_level": "Year 10", "contact_phone":"87654321", "username":"bob01"},
    {"id": 3, "name": "Charlie Lee", "year_level": "Year 9", "contact_phone":"23456789", "username":"charlie01"},
    {"id": 4, "name": "Diana Wilson", "year_level": "Year 11", "contact_phone":"34567890", "username":"diana01"},
    {"id": 5, "name": "Ella Brown", "year_level": "Year 12", "contact_phone":"45678901", "username":"ella01"},
    {"id": 6, "name": "Frank Miller", "year_level": "Year 10", "contact_phone":"56789012", "username":"frank01"}
]

mock_tutors = [
    {"id":1,"name":"Tom Wilson","specialty":"Mathematics"},
    {"id":2,"name":"Lisa Brown","specialty":"Chemistry"},
    {"id":3,"name":"James Clark","specialty":"Physics"},
    {"id":4,"name":"Sarah Taylor","specialty":"English Literature"}
]

allocations = []

# ====================== 权限装饰器 ======================
# 必须登录才能访问
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 仅管理员可访问
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login'))
        if session["user"]["role"] != "admin":
            flash("Unauthorised: Only admin can access this page")
            return redirect(url_for('session_report'))
        return f(*args, **kwargs)
    return decorated_function

# 仅学生角色访问
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login'))
        if session["user"]["role"] != "student":
            flash("This page is for student only")
            return redirect(url_for('home_page'))
        return f(*args, **kwargs)
    return decorated_function

# ==========根路由：访问 http://127.0.0.1:5000 直接跳转登录页面 ==========
@app.route('/')
def index():
    return redirect(url_for("login"))

# 登录成功后跳转的首页，渲染base.html（带导航栏）
@app.route('/home')
@login_required
def home_page():
    return render_template('base.html')


@app.route('/students')
@login_required
def student_page():
    # =========后端搜索过滤逻辑=========
    search_text = request.args.get("search", "").strip()
    year_filter = request.args.get("year", "").strip()
    result_list = mock_students

    if search_text:
        result_list = [s for s in result_list if search_text.lower() in s["name"].lower()]
    if year_filter and year_filter != "all":
        result_list = [s for s in result_list if s["year_level"] == year_filter]

    return render_template('students/index.html', students=result_list,
                           search=search_text, selected_year=year_filter)



@app.route('/tutors/assign', methods=["GET","POST"])
@login_required
def assign_tutor():
    # Sprint2: 读取url参数，预选中学生
    pre_select_student_id = request.args.get("student_id", type=int)
    if request.method == "POST":
        student_id = int(request.form["student_id"])
        tutor_id = int(request.form["tutor_id"])

        # Sprint2 业务校验: 不允许同一个学生重复分配
        for item in allocations:
            for s in mock_students:
                if s["id"] == student_id and item["student_name"] == s["name"]:
                    flash("Error: This student already has an allocation!")
                    return redirect(url_for("assign_tutor"))

        s = next(x for x in mock_students if x["id"] == student_id)
        t = next(x for x in mock_tutors if x["id"] == tutor_id)

        new_item = {
            "student_name": s["name"],
            "student_username": s["username"],
            "tutor_name": t["name"],
            "subject": t["specialty"],
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
@admin_required
def delete_allocation(index):
    if 0 <= index < len(allocations):
        del allocations[index]
        flash("Allocation record removed.")
    return redirect(url_for("schedule_page"))


@app.route('/schedule')
@login_required
def schedule_page():
    return render_template('schedule/index.html', schedule=allocations)

# =========学生个人课表路由 =========
@app.route("/student/my_timetable")
@login_required
@student_required
def student_my_timetable():
    stu_username = session["user"]["username"]
    my_schedule = [item for item in allocations if item["student_username"] == stu_username]
    return render_template("students/my_timetable.html", my_schedule=my_schedule)

# ===================== US010 Session Report 扩充会话数据 =====================
sessions = [
    {"session_id": 1, "student_name": "Alice", "tutor_name": "Tom W", "subject": "Mathematics", "time": "Mon 10:00"},
    {"session_id": 2, "student_name": "Bob", "tutor_name": "Lisa B", "subject": "Chemistry", "time": "Tue 14:00"},
    {"session_id": 3, "student_name": "Charlie", "tutor_name": "Tom W", "subject": "Mathematics", "time": "Wed 11:00"},
    {"session_id": 4, "student_name": "Diana", "tutor_name": "James C", "subject": "Physics", "time": "Thu 15:30"},
    {"session_id": 5, "student_name": "Ella", "tutor_name": "Sarah T", "subject": "English Literature", "time": "Fri 09:30"},
    {"session_id": 6, "student_name": "Frank", "tutor_name": "James C", "subject": "Physics", "time": "Fri 13:00"},
]

@app.route('/report')
@login_required
def session_report():
    """Render tutoring session report page for admin"""
    return render_template("report.html", session_list=sessions)

# ===================== Sprint2 US013 US014 Login & Permission Module =====================
# Demo test accounts for assignment demo only
demo_users = {
    "admin01": {
        "password": "pass123",
        "role": "admin",
        "is_active": True
    },
    "tutor01": {
        "password": "pass123",
        "role": "tutor",
        "is_active": True
    },
    "alice01": {
        "password": "pass123",
        "role": "student",
        "is_active": True
    },
    "disable01": {
        "password": "pass123",
        "role": "admin",
        "is_active": False
    }
}

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = demo_users.get(username)
        if not user:
            flash("Invalid username or password")
            return render_template("login.html")
        if user["password"] != password:
            flash("Invalid username or password")
            return render_template("login.html")
        # US014: Deactivated account cannot login
        if not user["is_active"]:
            flash("This account has been deactivated. Cannot log in.")
            return render_template("login.html")
        # Save full user info to session
        session["user"] = {
            "username": username,
            "role": user["role"]
        }
        # 登录成功跳转 /home 带导航首页
        return redirect(url_for('home_page'))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    flash("You have logged out")
    return redirect(url_for('login'))

# Admin only management page for US013 & US014 demo
@app.route("/user_manage")
@admin_required
def user_manage():
    current_role = session.get("user")["role"]
    return render_template("user_manage.html", current_role=current_role)


if __name__ == '__main__':
    app.run(debug=True)




