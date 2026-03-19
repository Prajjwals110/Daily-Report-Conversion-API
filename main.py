from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.extractor import extract_report, generate_summary
from db.database import engine, Base, SessionLocal
from db.models import Report

Base.metadata.create_all(bind=engine)

app = FastAPI()

class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "System Running"}


@app.post("/webhook")
async def receive_data(data: MessageRequest):
    db = SessionLocal()

    try:
        text = data.message

        structured = extract_report(text)

        # 🔍 DEBUG (important for now)
        print("STRUCTURED DATA:", structured)

        # ❌ if AI fails
        if "error" in structured:
            raise HTTPException(status_code=400, detail=structured)

        report = Report(
            workers=structured.get("workers", 0),
            delay_hours=structured.get("delay_hours", 0),
            work_done=structured.get("work_done", ""),
            issues=structured.get("issues", None),
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "message": "Saved successfully",
            "data": structured
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

@app.get("/reports")
def get_reports():
    db = SessionLocal()

    try:
        reports = db.query(Report).all()

        return [
            {
                "id": r.id,
                "workers": r.workers,
                "delay_hours": r.delay_hours,
                "work_done": r.work_done,
                "issues": r.issues,
            }
            for r in reports
        ]

    finally:
        db.close()

@app.get("/summary")
def get_summary():
    db = SessionLocal()

    try:
        reports = db.query(Report).all()

        if not reports:
            return {"message": "No data available"}

        # 🔢 Aggregate data
        total_workers = sum(r.workers or 0 for r in reports)
        total_delay = sum(r.delay_hours or 0 for r in reports)

        work_done_list = [r.work_done for r in reports if r.work_done]
        issues_list = [r.issues for r in reports if r.issues]

        # 🧠 Send to AI for summary
        summary_input = f"""
        Total workers: {total_workers}
        Total delay hours: {total_delay}
        Work done: {", ".join(work_done_list)}
        Issues: {", ".join(issues_list) if issues_list else "None"}

        Generate a clean professional daily report summary.
        """

        summary = generate_summary(summary_input)  # reuse AI (we'll adjust)

        return {
            "summary": summary
        }

    finally:
        db.close()