from fastapi import APIRouter, Depends, status, Request, HTTPException, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas

router = APIRouter()


@router.post('/vacancy', status_code=status.HTTP_201_CREATED)
async def register_vacancy(payload: schemas.RegisterVacancySchema, request: Request, db: Session = Depends(get_db)):
    vacancy_data = payload.dict()
    skills = vacancy_data["skills"]
    del vacancy_data["skills"]
    new_vacancy = models.Vacancy(**vacancy_data)
    db.add(new_vacancy)
    db.commit()
    db.refresh(new_vacancy)

    for skill in skills:
        skill_data = {"vacancy_id": new_vacancy.id, "skill_id": skill["id"], "years": skill["years"]}
        new_skill = models.VacancySkill(**skill_data)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

    return {'status': 'success', 'message': 'Vacancy has been created successfully'}


@router.get('/{id}', response_model=schemas.VacancyResponse)
def get_vacancy(id: str, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == id).first()
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No vacancy with this id: {id} found")
    return vacancy


@router.delete('/{id}')
def delete_vacancy(id: str, db: Session = Depends(get_db)):
    vacancy_query = db.query(models.Vacancy).filter(models.Vacancy.id == id)
    vacancy = vacancy_query.first()
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No vacancy with this id: {id} found')

    vacancy_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def vacancy_skills_match(vacancy_skills, user_skills, db):
    vacancy_skills_qty = len(vacancy_skills)
    match_skills = []

    for vacancy_skill in vacancy_skills:
        if match_skill(vacancy_skill, user_skills):
            match_skills.append(vacancy_skill)

    if len(match_skills) > 0:
        match_percent = vacancy_skills_qty * 100 / len(match_skills)
        if match_percent >= 50:
            return db.query(models.Vacancy).filter(models.Vacancy.id == match_skills[0].vacancy_id).one()


def match_skill(vacancy_skill, user_skills):
    if vacancy_skill.skill_id in [data.skill_id for data in user_skills]:
        if [p.years for p in user_skills if p.skill_id == vacancy_skill.skill_id][0] >= vacancy_skill.years:
            return True
