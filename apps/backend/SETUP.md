# Інструкції для запуску Backend

## Швидкий старт

### 1. Активуйте віртуальне середовище

**Windows (PowerShell):**
```powershell
cd apps\backend
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
cd apps\backend
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
cd apps/backend
source venv/bin/activate
```

### 2. Встановіть залежності

```bash
pip install -r requirements.txt
```

### 3. Запустіть сервер

```bash
python main.py
```

або

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Перевірте роботу

Відкрийте в браузері:
- **API документація**: http://localhost:8000/docs
- **Тест API**: http://localhost:8000/api/reviews?hours=168&country=us

## Приклади запитів

### Отримати відгуки за останні 24 години (США)
```bash
curl "http://localhost:8000/api/reviews?hours=24&country=us"
```

### Отримати відгуки за останній тиждень (Україна)
```bash
curl "http://localhost:8000/api/reviews?hours=168&country=ua"
```

### Тільки Google Play відгуки
```bash
curl "http://localhost:8000/api/reviews/google?hours=24&country=us"
```

### Тільки App Store відгуки
```bash
curl "http://localhost:8000/api/reviews/apple?hours=24&country=us"
```

## Налаштування країни

Підтримувані коди країн (ISO 3166-1 alpha-2):
- `us` - США (за замовчуванням)
- `ua` - Україна
- `gb` - Великобританія
- `pl` - Польща
- `de` - Німеччина
- `fr` - Франція
- `es` - Іспанія
- `it` - Італія
- та інші...

## Troubleshooting

### Проблема: "ModuleNotFoundError"
```bash
# Переконайтесь, що venv активоване та встановіть залежності знову
pip install -r requirements.txt
```

### Проблема: Мало відгуків
```bash
# Збільште кількість годин (наприклад, тиждень)
curl "http://localhost:8000/api/reviews?hours=168&country=us&limit=200"
```

### Проблема: Порт зайнятий
```bash
# Використайте інший порт
uvicorn main:app --reload --port 8001
```

## Інтеграція з фронтендом

У файлі `apps/frontend/src/App.tsx` замініть функцію `loadMockData()`:

```typescript
const loadReviews = async () => {
  setLoading(true)
  try {
    const response = await fetch('http://localhost:8000/api/reviews?hours=24&country=us')
    const data = await response.json()
    setReviews(data.reviews)
    setStats(data.stats)
  } catch (error) {
    console.error('Error loading reviews:', error)
  } finally {
    setLoading(false)
  }
}
```

## Production

Для production використайте:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

