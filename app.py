from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from models import db, User, Answer
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '0531'  # 🛑 진짜 서비스에서는 강력한 랜덤 키로!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# DB 초기화 함수
def create_tables():
    with app.app_context():
        db.create_all()

# 로그인 화면이 기본 페이지
@app.route('/')
def index():
    return render_template('login.html')

# 회원가입 처리 (이름만으로 등록)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()

        if not name:
            return "이름을 입력해주세요.", 400

        # 중복 체크
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

        # 사용자 생성
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        # ✅ 가입 완료 메시지 + 자동 리디렉션
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

    if user_id:
        user = User.query.get(user_id)
        if user:
            user_name = user.name

    return render_template('index.html', user_id=user_id, user_name=user_name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API: 답안 제출
@app.route('/api/submit', methods=['POST'])
def submit_answers():
    user_id = session.get('user_id')
    data = request.get_json()
    answers = data.get('answers', [])
    mode = data.get('mode', 'exam')  # 기본값은 'exam'

    # 연습모드이거나 로그인 안 했으면 저장하지 않음
    if mode != 'exam' or not user_id:
        return jsonify({"message": "연습모드는 기록을 저장하지 않습니다."})

    # 문제 불러오기
    with open('data/cbt_questions_2024_final.json', encoding='utf-8') as f:
        question_data = json.load(f)

    for idx, ans in enumerate(answers):
        q = question_data[idx]
        correct_answer = q["answer"]
        selected = ans if ans is not None else None

        answer_obj = Answer(
            user_id=user_id,
            question_id=idx + 1,
            selected=selected,
            is_correct=((selected + 1) == correct_answer) if selected is not None else False,
            timestamp=datetime.utcnow()
        )
        db.session.add(answer_obj)

    db.session.commit()
    return jsonify({"message": "시험 응시 기록이 저장되었습니다."})

@app.route('/records')
def records():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    
    # 사용자별 시험 기록 불러오기
    records = Answer.query.filter_by(user_id=user_id).order_by(Answer.timestamp.desc()).all()

    # enumerate 처리 후 전달
    records_with_idx = [(idx + 1, record) for idx, record in enumerate(records)]

    return render_template('results.html', user=user, records=records_with_idx)

# API: 문제 불러오기
@app.route('/api/questions')
def get_questions():
    with open('data/cbt_questions_2024_final.json', encoding='utf-8') as f:
        questions = json.load(f)
    return jsonify(questions)

# API: 답안 조회
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

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
