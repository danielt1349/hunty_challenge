import uuid
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, default=None)
    name = Column(String, nullable=False)
    users = relationship("User", secondary="users_skills", back_populates='skills')
    vacancies = relationship("Vacancy", secondary="vacancies_skills", back_populates='skills')


class UserSkill(Base):
    __tablename__ = 'users_skills'
    skill_id = Column(ForeignKey('skills.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    years = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    years_prev_exp = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    skills = relationship("Skill", secondary=UserSkill.__table__, back_populates='users')


class VacancySkill(Base):
    __tablename__ = 'vacancies_skills'
    skill_id = Column(ForeignKey('skills.id'), primary_key=True)
    vacancy_id = Column(ForeignKey('vacancies.id'), primary_key=True)
    years = Column(Integer, nullable=False)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    position_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    skills = relationship("Skill", secondary="vacancies_skills", back_populates='vacancies')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
