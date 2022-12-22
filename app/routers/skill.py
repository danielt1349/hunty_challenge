from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db

router = APIRouter()


@router.post('/skills', status_code=status.HTTP_201_CREATED, response_model=schemas.SkillResponse)
async def register_skill(payload: schemas.RegisterSKillSchema, db: Session = Depends(get_db)):
    skill_data = payload.dict()
    new_skill = models.Skill(**skill_data)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get('/', response_model=schemas.ListSkillResponse)
def get_skills(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    skills = db.query(models.Skill).group_by(models.Skill.id).filter(
        models.Skill.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(skills), 'skills': skills}


@router.put('/{id}', response_model=schemas.SkillResponse)
def update_skill(id: str, post: schemas.RegisterSKillSchema, db: Session = Depends(get_db)):
    skill_query = db.query(models.Skill).filter(models.Skill.id == id)
    updated_skill = skill_query.first()

    if not updated_skill:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No skill with this id: {id} found')

    skill_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_skill


@router.get('/{id}', response_model=schemas.SkillResponse)
def get_skill(id: str, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == id).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No skill with this id: {id} found")
    return skill


@router.delete('/{id}')
def delete_skill(id: str, db: Session = Depends(get_db)):
    skill_query = db.query(models.Skill).filter(models.Skill.id == id)
    skill = skill_query.first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No skill with this id: {id} found')

    skill_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
