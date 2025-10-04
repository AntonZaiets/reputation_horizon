# Reputation Horizon - Backend (FastAPI)

Python FastAPI backend для збору та обробки відгуків про додаток Preply з Google Play Store та Apple App Store.

## Особливості

🚀 **FastAPI** - сучасний, швидкий веб-фреймворк
📱 **Google Play Scraper** - збір відгуків з Google Play
🍎 **App Store Scraper** - збір відгуків з App Store
⏰ **Фільтрація за часом** - відгуки за останні N годин
🌍 **Підтримка країн** - вибір країни для пошуку
📊 **Статистика** - автоматичний підрахунок метрик

## Встановлення

### 1. Створіть віртуальне середовище

```bash
cd apps/backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Встановіть залежності

```bash
pip install -r requirements.txt
```

### 3. Налаштуйте змінні середовища (опціонально)

```bash
cp .env.example .env
# Відредагуйте .env за потреби
```

## Запуск

### Development режим (з auto-reload)

```bash
python main.py
```

або

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production режим

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

API буде доступне за адресою: **http://localhost:8000**

## API Endpoints

### 📋 Основні ендпоінти

#### `GET /api/reviews`
Отримати відгуки з обох магазинів за останні N годин

**Параметри:**
- `hours` (int, за замовчуванням: 24) - кількість годин назад
- `country` (str, за замовчуванням: "us") - код країни
- `limit` (int, за замовчуванням: 100) - макс. кількість відгуків

**Приклад:**
```bash
curl "http://localhost:8000/api/reviews?hours=24&country=us&limit=50"
```

#### `GET /api/reviews/google`
Тільки Google Play відгуки

#### `GET /api/reviews/apple`
Тільки App Store відгуки

### 📊 Формат відповіді

```json
{
  "reviews": [
    {
      "id": "review_id",
      "userName": "John Doe",
      "rating": 5,
      "text": "Great app!",
      "date": "2025-10-04T10:30:00",
      "source": "google",
      "version": "7.45.0",
      "thumbsUp": 12
    }
  ],
  "stats": {
    "totalReviews": 50,
    "avgRating": 4.5,
    "googlePlayReviews": 30,
    "appStoreReviews": 20,
    "positiveReviews": 40,
    "negativeReviews": 5
  }
}
```

## Підтримувані країни

- 🇺🇸 `us` - США
- 🇺🇦 `ua` - Україна
- 🇬🇧 `gb` - Великобританія
- 🇵🇱 `pl` - Польща
- 🇩🇪 `de` - Німеччина
- 🇫🇷 `fr` - Франція
- 🇪🇸 `es` - Іспанія
- 🇮🇹 `it` - Італія
- ... та інші ISO 3166-1 alpha-2 коди

## Структура проекту

```
apps/backend/
├── main.py                      # Головний файл FastAPI
├── requirements.txt             # Python залежності
├── .env.example                 # Приклад env змінних
├── services/
│   ├── __init__.py
│   ├── google_play_service.py   # Сервіс Google Play
│   ├── app_store_service.py     # Сервіс App Store
│   └── review_aggregator.py     # Агрегація відгуків
└── README.md
```

## Документація API

Після запуску сервера документація доступна за адресою:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Приклади використання

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://localhost:8000/api/reviews",
        params={"hours": 24, "country": "ua", "limit": 50}
    )
    data = response.json()
    print(f"Total reviews: {data['stats']['totalReviews']}")
```

### JavaScript (для фронтенду)

```javascript
const response = await fetch('http://localhost:8000/api/reviews?hours=24&country=us');
const data = await response.json();
console.log(data.stats);
```

## Troubleshooting

### Проблема: Не знаходить відгуки

**Рішення:**
- Збільште параметр `hours` (наприклад, до 168 для тижня)
- Перевірте правильність коду країни
- Спробуйте інший `limit` (100-200)

### Проблема: Повільна відповідь

**Рішення:**
- Зменште `limit`
- Використовуйте кешування (можна додати Redis)
- Запускайте в production режимі з workers

## Майбутні покращення

- [ ] Кешування відгуків (Redis)
- [ ] Періодичне оновлення в фоні (Celery)
- [ ] База даних для зберігання історії
- [ ] Сентимент-аналіз відгуків
- [ ] Webhooks для нових відгуків
- [ ] Rate limiting
- [ ] Аутентифікація API

## Ліцензія

MIT

