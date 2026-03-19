from sqlalchemy import Column, Integer, String
from db.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    workers = Column(Integer)
    delay_hours = Column(Integer)
    work_done = Column(String)
    issues = Column(String)