from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr

from .vacancy import vacancy_skills_match
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post('/register/user', status_code=status.HTTP_201_CREATED)
async def register_user(payload: schemas.RegisterUserSchema, request: Request, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(
        models.User.email == EmailStr(payload.email.lower()))
    user = user_query.first()

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exist')

    user_data = payload.dict()
    skills = user_data["skills"]
    del user_data["skills"]
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    for skill in skills:
        skill_data = {"user_id": new_user.id, "skill_id": skill["id"], "years": skill["years"]}
        new_skill = models.UserSkill(**skill_data)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

    return {'status': 'success', 'message': 'User has been created successfully'}


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with this id: {id} found")

    user_skills_query = db.query(models.UserSkill).filter(models.UserSkill.user_id == id).all()
    user_response = {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email,
                     "skills": [{
                         "id": data.skill_id,
                         "name": user.skills[idx].name,
                         "years": data.years
                     } for idx, data in enumerate(user_skills_query)
                     ]}
    return user_response


@router.put('/{id}', response_model=schemas.UpdateUserResponse)
def update_user(id: str, payload: schemas.UpdateUserSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    updated_user = user.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with this id: {id} found")

    user.update(payload.dict(), synchronize_session=False)
    db.commit()
    return updated_user


@router.get('/user/recommender/{id}', status_code=status.HTTP_200_OK)
async def get_recommend(id: str, request: Request, db: Session = Depends(get_db)):
    vacancies_recommended = []

    user_skills_query = db.query(models.UserSkill).filter(models.UserSkill.user_id == id).all()
    user_skills = user_skills_query
    vacancies = db.query(models.Vacancy).all()

    for vacancy in vacancies:
        vacancy_skills = db.query(models.VacancySkill). \
            filter(models.VacancySkill.vacancy_id == vacancy.id).all()
        vacancy_match = vacancy_skills_match(vacancy_skills, user_skills, db)
        if vacancy_match is not None:
            vacancies_recommended.append(vacancy_match)
    return vacancies_recommended
