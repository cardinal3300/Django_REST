# Django_REST (Online_Learning_Platform_API)

## Описание проекта

Online_Learning_Platform_API — это бэкенд-часть веб-приложения онлайн-обучения, реализованная в виде REST API с использованием Django REST Framework.

Проект предназначен для обеспечения работы фронтенд-приложения и предоставляет API для управления образовательными курсами, уроками и пользователями.  
Реализация ориентирована на принципы REST, разделение ответственности и безопасность.

---

## 🎯 Функциональные возможности

### Пользователи
- Регистрация пользователей
- Авторизация и аутентификация (JWT)
- Разграничение прав доступа (пользователь / администратор)

### Курсы (ViewSet)
- Создание курсов
- Редактирование курсов
- Удаление курсов
- Просмотр списка курсов
- Просмотр детальной информации о курсе

### Уроки (generic)
- CRUD-операции для уроков
- Привязка уроков к курсам
- Просмотр списка уроков внутри курса

### Права доступа
- Пользователь может управлять только своими курсами и уроками
- Неавторизованные пользователи имеют доступ только к публичным данным
- Администратор имеет полный доступ

---

## 📐 Архитектура проекта

Проект построен по классической архитектуре Django REST Framework:

- `models` — модели базы данных
- `serializers` — сериализация и валидация данных
- `views` / `viewsets` — логика обработки запросов
- `permissions` — кастомные права доступа
- `urls` — маршрутизация API

---

## 🛠️ Используемые технологии

- **Python 3.14.0**
- **Django 5.2.9**
- **Django REST Framework**
- **PostgreSQL**
- **JWT (djangorestframework-simplejwt)**
- **django-cors-headers**
- **Celery + Celery Beat**
- **drf-yasg (Swagger)**
- **APITestCase**
- **CORS**
- **Docker**
- **Docker Compose**

---

## ⚙️ Установка и запуск (требования Docker и Docker Compose)

- **Локально**
```bash
    git clone git@github.com:cardinal3300/Django_REST.git   # Клонирование репозитория
    cd online_learning_platform_api
    python -m venv venv                                     # Создание виртуального окружения
    source venv/bin/activate                                # Linux / macOS
    venv\Scripts\activate                                   # Windows
    pip install -r requirements.txt                         # Установка зависимостей
    python manage.py migrate                                # Применение миграций
    python manage.py createsuperuser                        # Создание суперпользователя
    python manage.py runserver                              # Запуск сервера разработки    
    docker compose up --build
```

 ---

## ⚙️ Проверка сервисов

Сервис - Как проверить

Django - http://localhost:8000

Admin - http://localhost:8000/admin/

Swagger	- http://localhost:8000/swagger/

PostgreSQL - docker compose exec db psql -U postgres

Redis - docker compose exec redis redis-cli ping

Celery - docker compose logs celery

Celery - Beat	docker compose logs celery-beat

### Остановка проекта

```docker compose down```

---

## 🚀 Deployment & CI/CD

### 📦 Требования к серверу

Удалённый сервер должен иметь:

- Ubuntu 20.04+

- Docker

- Docker Compose (опционально)

- Открытый порт `80`/`443`

- Открытый порт `22`

### Установка Docker

```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  
  sudo tee /etc/apt/sources.list.d/docker.sources <<EOF  
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
  
  sudo apt update
  
  sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Настройка файрвола и открытие портов

```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw allow 22/tcp   # Для обеспечения доступа к вашему серверу по SSH
```

---

## 🔐 Подготовка клонирования репозитория и `.env` файла в ручную (на сервере)
Создай директорию для репозитория, например:
```bash
  mkdir "name_directories"
  ```
Перейди в неё:
```bash
  cd "name_directories"
```
Клонируй репозиторий:
```bash
  git clone git@github.com:'your_name/project_name'.git
```
Создай .env файл и перенеси в него всё содержимое из своего .env файла в проекте. Сохрани.
```bash
  nano .env
```
Сделай запуск:
```bash
  docker compose up -d --build
```

---

## 🔑 GitHub Secrets

| Secret name               | Значение                |
| ------------------------- | ----------------------- |
| `SECRET_KEY`              | Django secret key       |
| `DOCKER_HUB_USERNAME`     | логин Docker Hub        |
| `DOCKER_HUB_ACCESS_TOKEN` | токен Docker Hub        |
| `SSH_KEY`                 | приватный SSH-ключ      |
| `SSH_USER`                | пользователь на сервере |
| `SERVER_IP`               | IP сервера              |

---

## 🔄 CI Pipeline (GitHub Actions)

Workflow автоматически запускается при `push`.

Этапы:

1. lint

   - Проверка кода (`flake8`)

2. test

   - Установка зависимостей

   - Django tests

3. build

   - Сборка Docker-образа

   - Пуш в Docker Hub

4. deploy

   - Подключение по SSH

   - Обновление контейнера

   - Сбор статики и применение миграций

---

## 🚢 Процесс деплоя

Во время `deploy` происходит:

```text
1. docker pull нового образа
2. docker stop старого контейнера
3. docker rm старого контейнера
4. docker run нового контейнера
5. python manage.py collectstatic
6. python manage.py migrate
```
Команды выполняются на сервере.

---




## 📘 Документация API

После запуска сервера документация доступна по следующим адресам:

- Swagger UI

    http://127.0.0.1:8000/swagger/


- ReDoc

    http://127.0.0.1:8000/redoc/

Документация автоматически генерируется на основе сериализаторов и представлений.

---

## ⚙️ Безопасность и CORS

В проекте настроен CORS для возможности подключения фронтенд-приложения:

- Разрешён доступ с указанных доменов
- Используется JWT-аутентификация
- Защита эндпоинтов через permissions

---

## 📂 Примеры эндпоинтов

- POST /users/register/ — регистрация пользователя
- POST /users/login/ — авторизация
- GET /courses/ — список курсов
- POST /courses/ — создание курса
- GET /courses/{id}/ — детали курса
- PUT /courses/{id}/ — обновление курса
- DELETE /courses/{id}/ — удаление курса
- GET /lessons/ — список уроков

---

## 💻 Тестирование

Проект предусматривает написание модульных тестов для:
- сериализаторов
- прав доступа
- CRUD-операций

Запуск тестов:
```bash
    python manage.py test
```

---

## 🌐 Статус проекта

Проект выполнен в рамках учебного курсового проекта по backend-разработке.
Код соответствует требованиям Django REST Framework и принципам REST API.

---

## 🧑‍ Автор

Backend-разработчик: [Жердев Игорь(cardinal3300)]

Учебный проект

---
