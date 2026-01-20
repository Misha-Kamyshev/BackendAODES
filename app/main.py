"""
Модуль инициализации FastAPI приложения и настройки middleware.

Создает основное FastAPI приложение, подключает CORS, роутеры и middleware для:
- Проверки IP-адресов по черному списку
- Валидации User-Agent заголовка
- Логирования запросов

Импорты:
    - fastapi.FastAPI: Основной класс приложения FastAPI
    - fastapi.Request: Для работы с HTTP запросами
    - fastapi.status: Коды статусов HTTP
    - fastapi.responses.JSONResponse: JSON-ответы
    - fastapi.middleware.cors.CORSMiddleware: Middleware для CORS
    - .routers.authorization: Роутер авторизации
    - .routers.user: Роутер пользователя
    - .routers.catalog: Роутер каталога
    - .logger.info_logger: Логгер для информации
    - .white_list.check_banned: Функция проверки IP в черном списке
    - .databases.ban.add_ip: Функция добавления IP в черный список
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.databases.postgres_asyncpg import asyncpg_db
from .routers import catalog
from .static import DATA_SOURCE

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "https://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["POST", 'GET'],
    allow_headers=["Content-Type", "Authorization", "*"]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncpg_db.connect(DATA_SOURCE)

    yield

    await asyncpg_db.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(catalog.router)
