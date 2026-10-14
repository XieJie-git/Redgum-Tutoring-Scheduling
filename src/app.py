from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Redgum Tutoring Scheduling Web App"

# ========== 新增 US008 tutor filter 接口 ==========
tutors = [
    {"id":1, "name":"Tutor A", "subject":"Math"},
    {"id":2, "name":"Tutor B", "subject":"English"},
    {"id":3, "name":"Tutor C", "subject":"Math"}
]

@app.route('/api/tutors', methods=['GET'])
def filter_tutors():
    subject_filter = request.args.get('subject')
    result = tutors
    if subject_filter:
        result = [t for t in tutors if t["subject"] == subject_filter]
    return jsonify(result)
# ==============================================

if __name__ == "__main__":
    app.run(port=5000)
