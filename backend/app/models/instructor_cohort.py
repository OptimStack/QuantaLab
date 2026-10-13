import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db import Base

cohort_members = Table(
    'cohort_members',
    Base.metadata,
    Column('cohort_id', String(36), ForeignKey('instructor_cohorts.id'), primary_key=True),
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True)
)

class InstructorCohort(Base):
    __tablename__ = "instructor_cohorts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instructor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)

    instructor = relationship("User", foreign_keys=[instructor_id])
    course = relationship("Course")
    members = relationship("User", secondary=cohort_members)
