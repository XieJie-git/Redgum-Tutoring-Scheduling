from flask import Flask, render_template

# 初始化Flask应用
app = Flask(__name__)

# 首页路由
@app.route('/')
def index():
    return render_template('base.html')

# 学生页面路由
@app.route('/students')
def student_page():
    mock_students = [
        {"id": 1, "name": "Alice Smith", "subject": "Mathematics"},
        {"id": 2, "name": "Bob Jones", "subject": "Physics"}
    ]
    return render_template('students/index.html', students=mock_students)

# 导师分配页面路由
@app.route('/tutors/assign')
def assign_tutor():
    mock_tutors = [
        {"id": 1, "name": "Tom Wilson", "specialty": "Math"},
        {"id": 2, "name": "Lisa Brown", "specialty": "Chemistry"}
    ]
    return render_template('tutors/assign.html', tutors=mock_tutors)

if __name__ == '__main__':
    app.run(debug=True)
