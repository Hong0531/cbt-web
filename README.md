# 정보처리산업기사 CBT 웹앱

## 소개
이 프로젝트는 정보처리산업기사 등 자격증 시험을 위한 CBT(Computer Based Test) 웹 애플리케이션입니다. Flask와 MySQL을 기반으로 하며, 회원가입, 로그인, 시험 응시, 오답노트, 기록 조회 등 다양한 기능을 제공합니다.

## 주요 기능
- 회원가입 및 로그인(게스트 모드 지원)
- 과목/회차별 CBT 문제 응시
- 오답노트 및 정답 해설 제공
- 시험 기록 저장 및 조회
- 관리자용 문제 데이터 일괄 등록

## 폴더 구조
```
├── app.py                # 메인 Flask 애플리케이션
├── models.py             # 데이터베이스 모델 정의
├── import_questions.py   # 문제 데이터(JSON) → DB 등록 스크립트
├── requirements.txt      # 파이썬 패키지 목록
├── data/                 # 문제 데이터(JSON 파일)
├── templates/            # HTML 템플릿(Jinja2)
├── static/               # 정적 파일(css, 이미지 등)
│   └── questions/        # 문제 관련 이미지
└── ...
```

## 설치 및 실행 방법

1. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **MySQL 데이터베이스 준비**
   - DB명: `cbt_db`
   - 사용자/비밀번호: `admin`/`1234` (app.py에서 수정 가능)
   - 테이블은 최초 실행 시 자동 생성

3. **문제 데이터 등록**
   ```bash
   python import_questions.py
   ```
   - `data/cbt_questions_2024_final_2.json` 파일을 DB에 등록

4. **서버 실행**
   ```bash
   python app.py
   ```
   - 기본 포트(5000)에서 실행

5. **웹 접속**
   - [http://localhost:5000](http://localhost:5000) 접속

## 주요 파일 설명

- **app.py**: 웹 서버 및 라우팅, 세션 관리, API 제공
- **models.py**: User, Answer, ExamRecord, Question 등 DB 모델 정의
- **import_questions.py**: JSON 문제 파일을 DB에 등록하는 스크립트
- **templates/**: 로그인, 회원가입, 시험, 결과, 오답노트 등 HTML 템플릿
- **static/**: CSS(`style.css`), 문제 이미지(`questions/` 폴더)

## 환경설정
`requirements.txt` 예시:
```
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
Flask-Login==0.6.1
gunicorn==20.1.0
sqlalchemy==1.4.48
werkzeug==2.3.8
```

## 데이터 구조 예시
- **문제 JSON 예시** (`data/cbt_questions_2024_final_2.json`)
  ```json
  {
    "subject": "정보처리산업기사",
    "version": "2024-1",
    "question": "다음 중 ...",
    "options": ["A", "B", "C", "D"],
    "answer": 2,
    "explanation": "정답 해설 ..."
  }
  ```

## 기타
- DB 접속 정보, 시크릿키 등은 실제 서비스 시 환경변수로 관리 권장
- 추가적인 문제 데이터는 `data/` 폴더에 JSON 형식으로 저장 후 import 스크립트 사용 