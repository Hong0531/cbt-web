import json
from app import app, db
from models import Question

# JSON 파일 경로
input_path = "data/cbt_questions_2024_final_2.json"

with app.app_context():
    db.create_all()  # 테이블 생성 (이미 있다면 무시됨)

    # 기존 문제 삭제하고 새로 추가하고 싶다면 ↓ 이 줄도 사용 가능
    # Question.query.delete()
    # db.session.commit()

    # JSON 로드
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        q = Question(
            subject=item["subject"],
            version=item["version"],
            question=item["question"],
            options=item["options"],
            answer=item["answer"],
            explanation=item.get("explanation", "")
        )
        db.session.add(q)


    db.session.commit()
    print(f"{len(data)}개의 문제가 MySQL에 저장되었습니다.")
