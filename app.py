from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
# flash消息需要密钥，用于页面提示
app.secret_key = "mysecretkey123"

# Sprint1 模拟内存数据（已扩充，页面内容更饱满）
mock_students = [
    {"id": 1, "name": "Alice Smith", "year_level": "Year 9", "contact_phone":"12345678"},
    {"id": 2, "name": "Bob Jones", "year_level": "Year 10", "contact_phone":"87654321"},
    {"id": 3, "name": "Charlie Lee", "year_level": "Year 9", "contact_phone":"23456789"},
    {"id": 4, "name": "Diana Wilson", "year_level": "Year 11", "contact_phone":"34567890"},
    {"id": 5, "name": "Ella Brown", "year_level": "Year 12", "contact_phone":"45678901"},
    {"id": 6, "name": "Frank Miller", "year_level": "Year 10", "contact_phone":"56789012"}
]

mock_tutors = [
    {"id":1,"name":"Tom Wilson","specialty":"Mathematics"},
    {"id":2,"name":"Lisa Brown","specialty":"Chemistry"},
    {"id":3,"name":"James Clark","specialty":"Physics"},
    {"id":4,"name":"Sarah Taylor","specialty":"English Literature"}
]

allocations = []

# ==========根路由：访问 http://127.0.0.1:5000 直接跳转登录页面 ==========
@app.route('/')
def index():
    return redirect(url_for("login"))

# 登录成功后跳转的首页，渲染base.html（带导航栏）
@app.route('/home')
def home_page():
    return render_template('base.html')


@app.route('/students')
def student_page():
    return render_template('students/index.html', students=mock_students)


@app.route('/tutors/assign', methods=["GET","POST"])
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
    "disable01": {
        "password": "pass123",
        "role": "admin",
        "is_active": False
    }
}

# 权限装饰器：未登录跳login；登录非admin跳report并弹出警告
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 如果完全没有登录，直接跳登录页
        if "role" not in session:
            return redirect(url_for('login'))
        # 已登录，但角色不是管理员
        if session.get("role") != "admin":
            flash("Unauthorised: Only admin can access this page")
            return redirect(url_for('session_report'))
        return f(*args, **kwargs)
    return decorated_function


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
        # Save user info to session
        session["username"] = username
        session["role"] = user["role"]
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
    current_role = session.get("role")
    return render_template("user_manage.html", current_role=current_role)


if __name__ == '__main__':
    app.run(debug=True)



