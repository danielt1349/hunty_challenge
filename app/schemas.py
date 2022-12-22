from typing import List
import uuid
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserSkillsBase(BaseModel):
    user_id: uuid.UUID
    skill_id: int
    years: int

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SkillBaseYear(BaseModel):
    id: int
    name: str
    years: int

    class Config:
        orm_mode = True


class SkillResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ListSkillResponse(BaseModel):
    status: str
    results: int
    skills: List[SkillResponse]

    class Config:
        orm_mode = True


class SkillSchema(SkillBase):
    Users: List[UserBase]


class UserSchema(UserBase):
    skills: List[SkillBase]


class RegisterUserSchema(UserBase):
    email: str
    years_prev_exp: int
    skills: List[SkillBaseYear]


class UpdateUserSchema(UserBase):
    email: str
    years_prev_exp: int


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    skills: List[SkillBaseYear]

    class Config:
        orm_mode = True


class UpdateUserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class RegisterVacancySchema(BaseModel):
    position_name: str
    company_name: str
    salary: float
    currency: str
    skills: List[SkillBaseYear]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RegisterSKillSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class VacancySkillSchema(BaseModel):
    skill_id: int
    vacancy_id: uuid.UUID
    years: int

    class Config:
        orm_mode = True


class VacancyResponse(BaseModel):
    id: uuid.UUID
    position_name: str
    company_name: str
    salary: float
    currency: str

    class Config:
        orm_mode = True
