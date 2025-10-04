# Reputation Horizon

Монорепозиторій проєкту Reputation Horizon з фронтендом та бекендом.

## 🏗️ Структура проєкту

```
reputation_horizon/
├── apps/
│   ├── frontend/          # React + TypeScript + Vite
│   └── backend/           # Node.js + Express + TypeScript
├── package.json           # Кореневий package.json (workspaces)
└── README.md
```

## 🚀 Швидкий старт

### Встановлення залежностей

```bash
npm install
```

### Запуск в режимі розробки

**Запустити все:**
```bash
npm run dev
```

**Запустити тільки фронтенд:**
```bash
npm run dev:frontend
```

**Запустити тільки бекенд:**
```bash
npm run dev:backend
```

## 📦 Frontend (React + Vite)

- **Порт:** `http://localhost:5173`
- **Технології:** React 19, TypeScript, Vite
- **Папка:** `apps/frontend`

### Команди:
```bash
cd apps/frontend
npm run dev      # Запустити dev сервер
npm run build    # Збілдити для продакшену
npm run preview  # Переглянути prod збірку
```

## 🔧 Backend (Express + TypeScript)

- **Порт:** `http://localhost:3001`
- **Технології:** Express, TypeScript, Node.js
- **Папка:** `apps/backend`

### Команди:
```bash
cd apps/backend
npm run dev      # Запустити з hot-reload
npm run build    # Скомпілювати TypeScript
npm run start    # Запустити prod версію
```

### API Endpoints:
- `GET /api/health` - Статус сервера
- `GET /api/hello` - Тестовий endpoint

## 🛠️ Корисні команди

```bash
# Білд всього проєкту
npm run build

# Запустити лінтер
npm run lint

# Очистити всі node_modules та dist
npm run clean
```

## 📝 Налаштування

### Backend Environment

Створіть файл `.env` в `apps/backend/` на основі `.env.example`:

```env
PORT=3001
NODE_ENV=development
```

## 🧰 Технології

### Frontend
- React 19.1
- TypeScript 5.9
- Vite 7.1
- ESLint

### Backend
- Node.js
- Express 4.21
- TypeScript 5.9
- tsx (для dev)
- CORS підтримка

## 📚 Workspaces

Цей проєкт використовує npm workspaces для управління монорепозиторієм. Всі залежності встановлюються з кореня проєкту.
