📝 정보처리산업기사 CBT 웹 애플리케이션

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-DB-4479A1?logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Style-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Logic-F7DF1E?logo=javascript&logoColor=black) 

<div align="center">

실제 자격증 시험 환경을 웹으로 완벽하게 구현한 모의고사 플랫폼입니다.




사용자는 실제 시험과 유사한 UI에서 문제를 풀고,




자동 채점 및 오답 노트를 통해 학습 효율을 극대화할 수 있습니다.

</div>

📑 목차 (Table of Contents)

📸 스크린샷 (Screenshots)

🛠 기술 스택 (Tech Stack)

✨ 주요 기능 (Key Features)

📂 폴더 구조 (Directory Structure)

🚀 설치 및 실행 방법 (Installation)

🔮 향후 계획 (Roadmap)

📧 Contact

📸 스크린샷 (Screenshots)

| 구분            | 화면                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------- |
| 메인 시험 화면 (PC) | <img src="https://github.com/user-attachments/assets/77f0cb4f-e01a-44b1-9936-82c9d9d59133" width="50%"> |
| 모바일 반응형 뷰     | <img src="https://github.com/user-attachments/assets/d9c13361-c523-40a7-8f9d-cddf3e11daf6" width="20%">          |



| 구분            | 화면                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------- |
| 로그인 / 회원가입    | <img src="https://github.com/user-attachments/assets/a80aa7be-8709-4ad8-84ec-6052271e2f6e" width="50%">  |
| 시험 결과 & 오답 노트 | <img src="https://github.com/user-attachments/assets/9b3ea482-09d7-4748-9c8d-947f33202d04" width="50%"><img src="https://github.com/user-attachments/assets/1d755dd0-cbbc-4a31-a13f-f7654708e58c" width="50%"><img src="https://github.com/user-attachments/assets/8d167d47-a9a7-4d46-8b2a-7699476345f1" width="50%">|


🛠 기술 스택 (Tech Stack)

| 분류       | 기술명                     | 설명                                      |
| -------- | ----------------------- | --------------------------------------- |
| Backend  | Flask, Python           | Core Logic, REST API 서버, SQLAlchemy ORM |
| Frontend | HTML, CSS, Vanilla JS   | Semantic Markup, Flexbox/Grid 기반 UI     |
| Database | SQLite / MySQL          | 개발용(SQLite) · 배포용(MySQL)                |


✨ 주요 기능 (Key Features)

1. 🎯 실전 같은 시험 환경

    시험 모드: 제한 시간(90분) 타이머와 실제 시험과 유사한 OMR 카드 UI를 제공하여 현장감을 높였습니다.

    연습 모드: 문제를 풀면서 즉시 해설을 확인하고 학습할 수 있는 모드입니다.

    자동 채점: 시험 종료 즉시 점수 계산 및 합격/불합격 여부를 판별합니다.

2. 📱 완벽한 반응형 디자인 (Mobile First)

    데스크탑: 우측에 고정된(Sticky) OMR 패널과 타이머로 편리한 탐색 제공.

    모바일: 상단 고정 헤더(Header)에 남은 시간 표시.
           하단 고정 시트(Bottom Sheet)로 문제 이동 패널 구현하여 터치 편의성 증대.

4. 💾 데이터 보존 및 복구 (UX)

    진행 상황 자동 저장: LocalStorage를 활용하여 시험 도중 실수로 브라우저를 종료하거나 새로고침해도, 풀던 문제와 남은 시간을 그대로 복구합니다.

5. 📊 개인화된 결과 분석

    시험 기록 관리: 회차별 점수, 소요 시간, 합격 여부를 히스토리로 관리합니다.

    오답 노트: 틀린 문제만 모아서 다시 풀어보고 상세 해설을 확인할 수 있습니다.

6. 🔒 보안 및 사용자 관리

    회원 시스템: 회원가입/로그인 및 게스트(비회원) 체험 모드를 지원합니다.
    
    보안 강화: python-dotenv를 도입하여 환경변수(.env)로 민감한 정보(Secret Key, DB URL)를 분리 관리합니다.

📂 폴더 구조 (Directory Structure)

    cbt-project/
    ├── app.py                  # 메인 애플리케이션 진입점
    ├── models.py               # DB 모델 정의
    ├── import_questions.py     # JSON → DB 마이그레이션
    ├── requirements.txt        # 의존성 패키지
    ├── .env                    # 환경변수 (Git 제외)
    ├── data/                   # 기출문제 JSON
    ├── static/
    │   └── style.css           # 메인 스타일
    └── templates/
        ├── index.html
        ├── login.html
        ├── exam_select.html
        └── ...


🚀 설치 및 실행 방법 (Installation)

1. 프로젝트 클론

    git clone [https://github.com/your-username/cbt-project.git](https://github.com/your-username/cbt-project.git)
    cd cbt-project


2. 가상환경 설정 (권장)

    python -m venv venv
    ## Windows
    venv\Scripts\activate
    ## Mac/Linux
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

    #### JSON 파일에 있는 기출문제를 DB에 적재합니다.
    python import_questions.py


6. 서버 실행

    python app.py


    브라우저에서 http://localhost:8080 접속

🔮 향후 계획 (Roadmap)

[ ] 정보처리기능사, 컴퓨터활용능력 등 타 자격증 과목 데이터 추가

[ ] 오답 노트 PDF 다운로드 기능 구현

[ ] 커뮤니티(질문 게시판) 기능 추가

📧 Contact

| 항목     | 내용                                            |
| ------ | --------------------------------------------- |
| Name   | 홍예림                                           |
| Email  | [hogogo7@naver.com](mailto:hogogo7@naver.com) |
| GitHub | [Hong0531](https://github.com/Hong0531)       |
