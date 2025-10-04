# 🎓 Reputation Horizon

Full-stack додаток для моніторингу відгуків про Preply з Google Play Store та Apple App Store.

## 🚀 Швидкий старт

### Запуск обох серверів однією командою:

```bash
npm run dev
```

або

```bash
npm start
```

Це запустить:
- 🔹 **Backend (Python FastAPI)** на http://localhost:8000
- 🔹 **Frontend (React + Vite)** на http://localhost:5173

### Окремий запуск:

**Frontend:**
```bash
npm run dev:frontend
```

**Backend:**
```bash
npm run dev:backend
```

## 📦 Встановлення

### 1. Встановіть Node.js залежності:

```bash
npm install
```

### 2. Встановіть Python залежності для backend:

```bash
cd apps/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Запустіть проект:

```bash
npm run dev
```

## 🎯 Особливості

### Backend (Python + FastAPI)
- ✅ Збір відгуків з **Google Play Store**
- ✅ Збір відгуків з **App Store**
- ✅ Фільтрація за часом (останні N годин)
- ✅ Вибір країни пошуку
- ✅ REST API з документацією (Swagger)
- ✅ Автоматичний підрахунок статистики

### Frontend (React + TypeScript + Vite)
- ✅ Сучасний градієнтний UI
- ✅ Плавні анімації та hover-ефекти
- ✅ Адаптивний дизайн (mobile-friendly)
- ✅ Фільтрація по джерелу (Google/Apple)
- ✅ Сортування (за датою/рейтингом)
- ✅ Детальні картки відгуків
- ✅ Статистичні метрики в реальному часі

## 📊 API Endpoints

### GET `/api/reviews`
Отримати відгуки з обох магазинів

**Параметри:**
- `hours` (int) - кількість годин назад (за замовчуванням: 24)
- `country` (str) - код країни (за замовчуванням: "us")
- `limit` (int) - макс. кількість відгуків (за замовчуванням: 100)

**Приклад:**
```bash
curl "http://localhost:8000/api/reviews?hours=168&country=ua&limit=200"
```

### GET `/api/reviews/google`
Тільки Google Play відгуки

### GET `/api/reviews/apple`
Тільки App Store відгуки

### GET `/docs`
Swagger UI документація

## 🌍 Підтримувані країни

- 🇺🇸 `us` - США
- 🇺🇦 `ua` - Україна
- 🇬🇧 `gb` - Великобританія
- 🇵🇱 `pl` - Польща
- 🇩🇪 `de` - Німеччина
- 🇫🇷 `fr` - Франція
- та інші ISO 3166-1 alpha-2 коди

## 📁 Структура проекту

```
reputation_horizon/
├── apps/
│   ├── frontend/              # React + TypeScript + Vite
│   │   ├── src/
│   │   │   ├── components/   # React компоненти
│   │   │   ├── App.tsx       # Головний компонент
│   │   │   └── ...
│   │   └── package.json
│   │
│   └── backend/              # Python + FastAPI
│       ├── services/         # Сервіси для скрапінгу
│       │   ├── google_play_service.py
│       │   ├── app_store_service.py
│       │   └── review_aggregator.py
│       ├── main.py           # FastAPI додаток
│       └── requirements.txt
│
├── package.json              # Root package.json з командами
├── QUICKSTART.md             # Швидкий старт
└── README.md                 # Цей файл
```

## 🎨 Скріншоти

Інтерфейс включає:
- 📊 Статистичні картки (загальна к-ть, середній рейтинг, розподіл)
- 🔍 Фільтри та сортування
- 💬 Детальні картки відгуків з рейтингами
- 🎨 Градієнтний дизайн з плавними анімаціями

## ⚙️ Налаштування

### Змінити країну пошуку

У `apps/frontend/src/App.tsx`:

```typescript
const response = await fetch('http://localhost:8000/api/reviews?hours=168&country=ua&limit=200')
```

### Змінити період збору

Параметр `hours`:
- `24` - останні 24 години
- `168` - останній тиждень
- `720` - останній місяць

## 🛠️ Доступні команди

```bash
npm run dev           # Запустити frontend + backend
npm start            # Те саме що npm run dev
npm run dev:frontend # Тільки frontend
npm run dev:backend  # Тільки backend
npm run build        # Збілдити проект
npm run lint         # Запустити linter
npm run clean        # Очистити node_modules
```

## 📝 Вимоги

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0
- **Python** >= 3.10

## 🔧 Troubleshooting

### Мало відгуків
- Збільште параметр `hours` (наприклад, до 168 для тижня)
- Збільште `limit` (наприклад, до 500)
- Спробуйте іншу країну

### Повільне завантаження
Це нормально! Скрапінг реальних даних займає 10-30 секунд.

### Backend не запускається
Переконайтесь що:
1. Python venv створено і активовано
2. Всі залежності встановлені (`pip install -r requirements.txt`)
3. Порт 8000 не зайнятий

## 📚 Документація

- [Frontend README](apps/frontend/README.md) - детальна інформація про фронтенд
- [Backend README](apps/backend/README.md) - детальна інформація про backend
- [Backend SETUP](apps/backend/SETUP.md) - інструкції по запуску backend
- [QUICKSTART](QUICKSTART.md) - швидкий старт проекту

## 🎓 Про додаток

**App ID Google Play**: `com.preply.android`  
**App ID App Store**: `1400521332`  
**Назва**: Preply - Language Learning

## 📄 Ліцензія

MIT

---

**Створено з ❤️ для моніторингу репутації Preply**
