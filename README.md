📝 정보처리산업기사 CBT 웹 애플리케이션

실제 자격증 시험 환경(CBT)을 웹으로 구현한 모의고사 플랫폼입니다.
사용자는 실제 시험과 유사한 UI에서 문제를 풀고, 자동 채점 및 오답 노트를 통해 학습 효율을 높일 수 있습니다.

✨ 주요 기능 (Key Features)

1. 🎯 실전 같은 시험 환경

시험 모드: 제한 시간(90분)과 OMR 카드 기능을 제공하여 실제 시험 현장감을 제공합니다.

연습 모드: 문제를 풀면서 즉시 해설을 확인하고 학습할 수 있습니다.

자동 채점: 시험 종료 즉시 점수와 합격 여부를 확인할 수 있습니다.

2. 📱 완벽한 반응형 디자인 (Mobile First)

데스크탑: 우측에 고정된(Sticky) OMR 패널과 타이머로 편리한 탐색 제공.

모바일:

상단 고정 헤더에 남은 시간 표시.

하단 고정 시트(Bottom Sheet)로 문제 이동(OMR) 패널 구현.

터치 친화적인 UI/UX 설계.

3. 💾 데이터 보존 및 복구

진행 상황 자동 저장: 시험 도중 실수로 브라우저를 종료하거나 새로고침해도, LocalStorage를 활용하여 풀던 문제와 남은 시간을 그대로 복구합니다.

4. 📊 개인화된 결과 분석

시험 기록 관리: 회차별 점수, 소요 시간, 합격 여부를 히스토리로 관리합니다.

오답 노트: 틀린 문제만 모아서 다시 풀어보고 해설을 확인할 수 있습니다.

5. 🔒 보안 및 사용자 관리

회원 시스템: 회원가입/로그인 및 게스트(비회원) 체험 모드 지원.

보안 강화: 환경변수(.env)를 사용하여 민감한 설정 정보(Secret Key, DB URL) 분리.

🛠 기술 스택 (Tech Stack)

Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login

Frontend: HTML5, CSS3 (Modern Flexbox/Grid), Vanilla JavaScript

Database: SQLite (개발용) / MySQL (배포 가능)

Deployment: Render

🚀 설치 및 실행 방법 (Installation)

1. 프로젝트 클론

git clone [https://github.com/your-username/cbt-project.git](https://github.com/your-username/cbt-project.git)
cd cbt-project


2. 가상환경 설정 (권장)

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


3. 의존성 패키지 설치

pip install -r requirements.txt


4. 환경 변수 설정

프로젝트 루트에 .env 파일을 생성하고 아래 내용을 작성하세요.
(.env.example 파일을 참고하세요)

FLASK_APP=app.py
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///dev.db


5. 데이터베이스 초기화 및 문제 데이터 로드

# JSON 파일에 있는 기출문제를 DB에 적재합니다.
python import_questions.py


6. 서버 실행

python app.py


브라우저에서 http://localhost:8080 접속

📂 폴더 구조 (Directory Structure)

cbt-project/
├── app.py                  # 메인 애플리케이션 파일
├── models.py               # 데이터베이스 모델 정의 (User, Question, Answer 등)
├── import_questions.py     # JSON 문제 데이터를 DB로 가져오는 스크립트
├── requirements.txt        # 파이썬 의존성 목록
├── .env                    # 환경변수 (Git 제외)
├── data/                   # 기출문제 JSON 데이터 폴더
├── static/                 # 정적 파일 (CSS, JS, Images)
│   └── style.css           # 메인 스타일시트
└── templates/              # HTML 템플릿 파일
    ├── index.html          # 시험 메인 화면
    ├── login.html          # 로그인
    ├── exam_select.html    # 과목 선택
    └── ...


🔮 향후 계획 (Roadmap)

[ ] 정보처리기능사, 컴퓨터활용능력 등 과목 추가

[ ] 오답 노트 PDF 다운로드 기능

[ ] 커뮤니티(질문 게시판) 기능

📧 Contact

Name: (홍예림)

Email: (hogogo7@naver.com)

GitHub: (https://github.com/Hong0531)