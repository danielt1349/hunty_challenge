from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import vacancy, user, skill

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(vacancy.router, tags=['Vacancies'], prefix='/api/vacancies')
app.include_router(skill.router, tags=['Skill'], prefix='/api/skills')


@app.get('/api/healthchecker')
def root():
    return {'message': 'UP'}
