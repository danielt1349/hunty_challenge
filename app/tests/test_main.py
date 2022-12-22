import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import models
from ..config import settings
from ..database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}" \
                          f"@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)
    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_skill(db):
    skills = ["python", "django", "aws"]

    for idx, skill in enumerate(skills):
        skill_data = {"id": idx + 1, "name": skill}
        new_skill = models.Skill(**skill_data)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)


@pytest.fixture
def create_user(db):
    user_data = {
        "id": "942db60d-eef8-469c-954a-67b62d8b9911",
        "first_name": "dani",
        "last_name": "filth",
        "email": "df@gmail.com",
        "years_prev_exp": 10,
        "skills": [
            {
                "id": 1,
                "name": "python",
                "years": 5
            },
            {
                "id": 2,
                "name": "django",
                "years": 5
            }
        ]
    }

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


@pytest.fixture
def create_user_junior(db):
    user_data = {
        "id": "942db60d-eef8-469c-954a-67b62d8b9912",
        "first_name": "dani",
        "last_name": "filth",
        "email": "df@gmail.com",
        "years_prev_exp": 0,
        "skills": [
            {
                "id": 1,
                "name": "python",
                "years": 0
            }
        ]
    }
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


@pytest.fixture
def create_vacancy(db):
    vacancy_data = {
        "position_name": "Python Dev",
        "company_name": "HUNTY",
        "salary": 9999999,
        "currency": "COP",
        "skills": [
            {
                "id": 1,
                "name": "python",
                "years": 5
            },
            {
                "id": 2,
                "name": "django",
                "years": 4
            },
            {
                "id": 3,
                "name": "aws",
                "years": 4
            }
        ]
    }

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


def test_get_recommend(client, create_skill, create_user, create_vacancy):
    response = client.get("api/users/user/recommender/942db60d-eef8-469c-954a-67b62d8b9911")

    assert response.status_code == 200
    assert response.json()[0]['position_name'] == "Python Dev"
    assert response.json()[0]['company_name'] == "HUNTY"
    assert response.json()[0]['salary'] == 9999999


def test_get_without_recommend(client, create_skill, create_user_junior, create_vacancy):
    response = client.get("api/users/user/recommender/942db60d-eef8-469c-954a-67b62d8b9912")

    assert response.status_code == 200
    assert response.json() == []


def test_get_user(client, create_skill, create_user):
    response = client.get("api/users/942db60d-eef8-469c-954a-67b62d8b9911")

    assert response.status_code == 200
    assert response.json()["first_name"] == "dani"
    assert response.json()["last_name"] == "filth"


def test_get_user_not_found(client, create_skill, create_user):
    response = client.get("api/users/942db60d-eef8-469c-954a-67b62d8b9912")

    assert response.status_code == 404