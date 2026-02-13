# TODO Manager (FastAPI)

Веб-приложение для управления задачами, построенное на **FastAPI** с соблюдением принципов **Clean Architecture**.

Проект демонстрирует разделение ответственности, внедрение зависимостей и изоляцию бизнес-логики от инфраструктуры.

---

## Возможности

- Создание и удаление задач
- Отметка задач как выполненных
- Daily-задачи со счётчиком серии (streak)
- Автоматический ежедневный сброс (один раз в день)
- Focus of the Day (только одна задача в фокусе в день)
- Группировка задач:
  - Daily
  - Active
  - Future
  - Overdue
  - Done

---

## Технологический стек

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Jinja2 (серверный рендеринг)
- Dependency Injection (FastAPI `Depends`)

---

## Архитектура

Проект построен в соответствии с принципами **Clean Architecture**.

### Структура слоев

```
Client → API → Services → Repositories → Database

Ответственность слоёв
API
Обрабатывает HTTP-запросы

Не содержит бизнес-логики

Использует Dependency Injection

Преобразует DomainError в HTTP-ответы

Services
Содержит все бизнес-правила и прикладную логику:

TaskService — управление задачами

FocusService — логика задачи дня (focus-of-the-day)

DailyService — логика ежедневного сброса

Реализованные бизнес-правила:

Выполненная задача не может стать фокусом

В день может быть только одна задача в фокусе

Daily-задачи сбрасываются один раз в сутки

Domain
Модель Task

Исключения DomainError

Интерфейсы репозиториев (TaskRepository, MetaRepository)

Слой Domain не зависит от FastAPI или SQLAlchemy.

Infrastructure
Реализация ORM на SQLAlchemy

База данных SQLite

Альтернативная реализация репозитория на JSON

Инфраструктура может быть заменена без изменения бизнес-логики.
```

Структура проекта
```
app/
├── api/
├── domain/
├── infrastructure/
├── services/
└── utils/
```



How to Run
```
git clone <repo-url>
cd todo
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python start.py
```


Приложение будет доступно по адресу:
```
http://127.0.0.1:8000
```



Будущие улучшения
```
Аутентификация пользователей

Поддержка нескольких пользователей

REST API (JSON-эндпоинты)

Миграции через Alembic

Поддержка Docker

Юнит-тесты для сервисов
```

Цель проекта

Проект создан для практики проектирования backend-архитектуры, внедрения зависимостей и чистого разделения бизнес-логики и инфраструктуры.

[ENG version](README.md)