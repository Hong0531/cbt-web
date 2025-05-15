from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from models import db, User, Answer, ExamRecord
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
REMOVED_SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            return "이름을 입력해주세요.", 400
        existing = User.query.filter_by(name=name).first()
        if existing:
            return f"""
            <p><strong>이미 존재하는 이름입니다:</strong> {name}</p>
            <form action="/signup" method="get">
            <button type="submit">다시 입력하기</button>
            </form>
            <form action="/login" method="get">
            <button type="submit">로그인하러 가기</button>
            </form>
            """
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return f"""
        <p>{name}님 가입 완료!</p>
        <p>3초 후 로그인 페이지로 이동합니다...</p>
        <form action="/login" method="get">
            <button type="submit">지금 로그인하기</button>
        </form>
        <meta http-equiv="refresh" content="3; url=/login">
        """
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        user = User.query.filter_by(name=name).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('exam_page'))
        else:
            return """
            <p style="font-weight:bold; color:red;">존재하지 않는 사용자입니다.</p>
            <form action="/login" method="get">
                <button type="submit">← 다시 로그인</button>
            </form>
            <form action="/signup" method="get">
                <button type="submit">회원가입하기</button>
            </form>
            """
    return render_template('login.html')

@app.route('/exam')
def exam_page():
    user_id = session.get('user_id')
    user_name = None
    session['start_time'] = (datetime.utcnow() + timedelta(hours=9)).isoformat()
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_name = user.name
    return render_template('index.html', user_id=user_id, user_name=user_name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    user_id = session.get('user_id')
    data = request.get_json()
    answers = data.get('answers', [])
    mode = data.get('mode', 'exam')
    if mode != 'exam' or not user_id:
        return jsonify({"message": "연습모드는 기록을 저장하지 않습니다."})
    with open('data/cbt_questions_2024_final.json', encoding='utf-8') as f:
        question_data = json.load(f)
    start_time_str = session.get('start_time')
    if start_time_str:
        start_time = datetime.fromisoformat(start_time_str)
    else:
        start_time = datetime.utcnow() + timedelta(hours=9)
    end_time = datetime.utcnow() + timedelta(hours=9)
    correct_count = 0
    for idx, ans in enumerate(answers):
        q = question_data[idx]
        correct_answer = q["answer"]
        selected = ans if ans is not None else None
        is_correct = (selected + 1) == correct_answer if selected is not None else False
        if is_correct:
            correct_count += 1
        answer_obj = Answer(
            user_id=user_id,
            question_id=idx + 1,
            selected=selected,
            is_correct=is_correct,
            timestamp=end_time
        )
        db.session.add(answer_obj)
    exam_record = ExamRecord(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        correct_count=correct_count
    )
    db.session.add(exam_record)
    db.session.commit()
    session['last_duration'] = (end_time - start_time).total_seconds()
    session['last_correct'] = correct_count
    return jsonify({"message": "시험 응시 기록이 저장되었습니다."})

@app.route('/wrong/<int:user_id>')
def view_wrong_answers(user_id):
    from sqlalchemy import desc
    answers = Answer.query.filter_by(user_id=user_id).order_by(Answer.question_id, desc(Answer.timestamp)).all()
    latest_per_question = {}
    for ans in answers:
        if ans.question_id not in latest_per_question:
            latest_per_question[ans.question_id] = ans
    wrong_answers = [ans for ans in latest_per_question.values() if not ans.is_correct]
    with open('data/cbt_questions_2024_final.json', encoding='utf-8') as f:
        question_data = json.load(f)
    enriched = []
    for ans in wrong_answers:
        q = question_data[ans.question_id - 1]
        enriched.append({
            "question_id": ans.question_id,
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q.get("explanation", ""),
            "selected": ans.selected,
            "timestamp": ans.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template("wrong_answers.html", wrong=enriched)

@app.route('/api/questions')
def get_questions():
    with open('data/cbt_questions_2024_final.json', encoding='utf-8') as f:
        questions = json.load(f)
    return jsonify(questions)

@app.route('/api/answers')
def get_user_answers():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    answers = Answer.query.filter_by(user_id=user_id).order_by(Answer.timestamp.desc()).all()
    result = []
    for ans in answers:
        result.append({
            "question_id": ans.question_id,
            "selected": ans.selected,
            "is_correct": ans.is_correct,
            "timestamp": ans.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(result)

@app.route('/records')
def records():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    exam_records = ExamRecord.query.filter_by(user_id=user_id).order_by(ExamRecord.end_time.desc()).all()

    records = []
    for idx, record in enumerate(exam_records):
        duration = record.end_time - record.start_time
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)

        records.append({
            "순번": idx + 1,
            "성명": user.name,
            "completed_at": (record.end_time).strftime("%Y년%m월%d일 %H시%M분%S초"),
            "duration": f"{minutes:02}분 {seconds:02}초",
            "subject": "정보처리산업기사",
            "total": record.correct_count,
            "score": f"{round(record.correct_count / 60 * 100)}점"
        })

    return render_template('results.html', user=user, records=records)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # 기본 포트 8080
    app.run(host="0.0.0.0", port=port)