import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from models import db, User, Answer, ExamRecord, Question
from datetime import datetime, timedelta
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)

# 보안 키 및 DB 설정 (환경변수에서 가져오기)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            return render_template("signup.html", error="이름을 입력해주세요.")
        existing = User.query.filter_by(name=name).first()
        if existing:
            return render_template("signup.html", error=f"이미 존재하는 이름입니다: {name}")
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return render_template("signup.html", success="회원가입 완료! 로그인해주세요.")
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        user = User.query.filter_by(name=name).first()
        if not user:
            return render_template("login.html", error="존재하지 않는 사용자입니다.")
        session['user_id'] = user.id
        session['user_name'] = user.name
        return redirect(url_for('select_subject'))
    return render_template("login.html")

@app.route('/guest')
def guest_login():
    session.clear()
    session['user_id'] = None
    session['user_name'] = '게스트'
    return redirect(url_for('select_subject'))

@app.route('/select')
def select_subject():
    return render_template('exam_select.html', user_name=session.get('user_name'))

@app.route('/exam')
def exam_page():
    subject = request.args.get('subject')
    version = request.args.get('version')

    if not subject or not version:
        return redirect(url_for('select_subject'))

    session['subject'] = subject
    session['version'] = version
    session['start_time'] = (datetime.utcnow() + timedelta(hours=9)).isoformat()

    user_id = session.get('user_id')
    user_name = session.get('user_name', '게스트')

    return render_template('index.html', user_id=user_id, user_name=user_name,
                            subject=subject, version=version)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/questions')
def get_questions():
    subject = request.args.get('subject') or session.get('subject', '정보처리산업기사')
    version = request.args.get('version') or session.get('version', '2024-1')
    
    questions = Question.query.filter_by(subject=subject, version=version).all()
    result = [{
        "id": q.id,
        "question": q.question,
        "options": q.options,
        "answer": q.answer,
        "explanation": q.explanation
    } for q in questions]
    return jsonify(result)

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    user_id = session.get('user_id')
    data = request.get_json()
    answers = data.get('answers', [])
    mode = data.get('mode', 'exam')

    subject = session.get('subject')
    version = session.get('version')
    questions = Question.query.filter_by(subject=subject, version=version).all()
    if not questions:
        return jsonify({"message": "문제를 불러올 수 없습니다."}), 400

    start_time_str = session.get('start_time')
    start_time = datetime.fromisoformat(start_time_str) if start_time_str else datetime.utcnow() + timedelta(hours=9)
    end_time = datetime.utcnow() + timedelta(hours=9)

    correct_count = 0
    for idx, ans in enumerate(answers):
        if idx >= len(questions):
            continue
        q = questions[idx]
        selected = ans if ans is not None else None
        is_correct = (selected + 1) == q.answer if selected is not None else False
        if is_correct:
            correct_count += 1
        if mode == 'exam' and user_id:
            db.session.add(Answer(
                user_id=user_id,
                question_id=q.id,
                selected=selected,
                is_correct=is_correct,
                timestamp=end_time
            ))

    if mode == 'exam' and user_id:
        db.session.add(ExamRecord(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            correct_count=correct_count
        ))
        db.session.commit()
        session['last_duration'] = (end_time - start_time).total_seconds()
        session['last_correct'] = correct_count
        return jsonify({"message": "시험 응시 기록이 저장되었습니다."})

    return jsonify({
        "message": "✅ 연습 모드 - 기록은 저장되지 않음",
        "correct_count": correct_count,
        "total": len(questions)
    })

@app.route('/wrong/<int:user_id>')
def view_wrong_answers(user_id):
    from sqlalchemy import desc
    answers = Answer.query.filter_by(user_id=user_id).order_by(Answer.question_id, desc(Answer.timestamp)).all()
    latest_per_question = {}
    for ans in answers:
        if ans.question_id not in latest_per_question:
            latest_per_question[ans.question_id] = ans
    wrong_answers = [ans for ans in latest_per_question.values() if not ans.is_correct]

    question_ids = [ans.question_id for ans in wrong_answers]
    question_lookup = {q.id: q for q in Question.query.filter(Question.id.in_(question_ids)).all()}

    enriched = []
    for ans in wrong_answers:
        q = question_lookup.get(ans.question_id)
        if q:
            enriched.append({
                "question_id": ans.question_id,
                "question": q.question,
                "options": q.options,
                "answer": q.answer,
                "explanation": q.explanation,
                "selected": ans.selected,
                "timestamp": ans.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

    return render_template("wrong_answers.html", wrong=enriched)

@app.route('/api/answers')
def get_user_answers():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    answers = Answer.query.filter_by(user_id=user_id).order_by(Answer.timestamp.desc()).all()
    result = [{
        "question_id": a.question_id,
        "selected": a.selected,
        "is_correct": a.is_correct,
        "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for a in answers]
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
            "completed_at": record.end_time.strftime("%Y년%m월%d일 %H시%M분%S초"),
            "duration": f"{minutes:02}분 {seconds:02}초",
            "subject": session.get("subject", "정보처리산업기사"),
            "total": record.correct_count,
            "score": f"{round(record.correct_count / 60 * 100)}점"
        })

    return render_template('results.html', user=user, records=records)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app.run(host=host, port=port)