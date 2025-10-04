import { Review, Stats } from './App'

// Мок-дані для відгуків
export const mockReviews: Review[] = [
  {
    id: '1',
    userName: 'Олександр К.',
    rating: 5,
    text: 'Чудовий додаток для вивчення мов! Дуже зручний інтерфейс та якісні уроки. Рекомендую всім, хто серйозно ставиться до вивчення іноземних мов.',
    date: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 години тому
    source: 'google',
    version: '2.1.4',
    thumbsUp: 12
  },
  {
    id: '2',
    userName: 'Марія П.',
    rating: 4,
    text: 'Добре працює, але іноді є проблеми з синхронізацією. В цілому задоволена якістю уроків та підходом викладачів.',
    date: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 години тому
    source: 'apple',
    version: '2.1.3'
  },
  {
    id: '3',
    userName: 'Дмитро В.',
    rating: 5,
    text: 'Найкращий додаток для вивчення англійської! Викладачі професійні, матеріали актуальні. За місяць значно покращив рівень мови.',
    date: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 годин тому
    source: 'google',
    version: '2.1.4',
    thumbsUp: 8
  },
  {
    id: '4',
    userName: 'Анна С.',
    rating: 3,
    text: 'Середньо. Є як плюси, так і мінуси. Інтерфейс міг би бути зручнішим, але контент якісний.',
    date: new Date(Date.now() - 8 * 60 * 60 * 1000), // 8 годин тому
    source: 'apple',
    version: '2.1.2'
  },
  {
    id: '5',
    userName: 'Ігор М.',
    rating: 5,
    text: 'Відмінний сервіс! Вивчаю німецьку вже 3 місяці, прогресс очевидний. Викладачі дуже допомагають з вимовою.',
    date: new Date(Date.now() - 10 * 60 * 60 * 1000), // 10 годин тому
    source: 'google',
    version: '2.1.4',
    thumbsUp: 15
  },
  {
    id: '6',
    userName: 'Олена К.',
    rating: 2,
    text: 'Не дуже задоволена. Часто проблеми з підключенням до уроків, технічна підтримка відповідає повільно.',
    date: new Date(Date.now() - 12 * 60 * 60 * 1000), // 12 годин тому
    source: 'apple',
    version: '2.1.1'
  },
  {
    id: '7',
    userName: 'Сергій Л.',
    rating: 4,
    text: 'Хороший додаток для початківців. Структура уроків логічна, але хотілося б більше інтерактивних вправ.',
    date: new Date(Date.now() - 14 * 60 * 60 * 1000), // 14 годин тому
    source: 'google',
    version: '2.1.3',
    thumbsUp: 5
  },
  {
    id: '8',
    userName: 'Наталія Р.',
    rating: 5,
    text: 'Прекрасний додаток! Вивчаю французьку, дуже зручно планувати уроки. Викладачі знають свою справу.',
    date: new Date(Date.now() - 16 * 60 * 60 * 1000), // 16 годин тому
    source: 'apple',
    version: '2.1.4',
    thumbsUp: 9
  },
  {
    id: '9',
    userName: 'Володимир Т.',
    rating: 3,
    text: 'Нормально, але є кімната для покращення. Ціни трохи високі, але якість уроків компенсує.',
    date: new Date(Date.now() - 18 * 60 * 60 * 1000), // 18 годин тому
    source: 'google',
    version: '2.1.2'
  },
  {
    id: '10',
    userName: 'Катерина Б.',
    rating: 5,
    text: 'Найкращий інвестиція в освіту! Вивчаю іспанську, прогресс швидкий. Рекомендую всім друзям.',
    date: new Date(Date.now() - 20 * 60 * 60 * 1000), // 20 годин тому
    source: 'apple',
    version: '2.1.4',
    thumbsUp: 11
  },
  {
    id: '11',
    userName: 'Андрій Г.',
    rating: 4,
    text: 'Добре працює, зручний інтерфейс. Єдиний мінус - іноді довго завантажуються відео уроки.',
    date: new Date(Date.now() - 22 * 60 * 60 * 1000), // 22 години тому
    source: 'google',
    version: '2.1.3',
    thumbsUp: 3
  },
  {
    id: '12',
    userName: 'Тетяна М.',
    rating: 5,
    text: 'Чудовий додаток! Вивчаю італійську, дуже задоволена підходом та якістю матеріалів. Викладачі професійні.',
    date: new Date(Date.now() - 24 * 60 * 60 * 1000), // 24 години тому
    source: 'apple',
    version: '2.1.4',
    thumbsUp: 7
  },
  {
    id: '13',
    userName: 'Роман К.',
    rating: 2,
    text: 'Не рекомендую. Багато технічних проблем, гроші витрачені даремно. Краще знайти інший сервіс.',
    date: new Date(Date.now() - 26 * 60 * 60 * 1000), // 26 годин тому
    source: 'google',
    version: '2.1.1'
  },
  {
    id: '14',
    userName: 'Юлія П.',
    rating: 4,
    text: 'Хороший додаток для вивчення мов. Є недоліки, але в цілому задоволена результатами навчання.',
    date: new Date(Date.now() - 28 * 60 * 60 * 1000), // 28 годин тому
    source: 'apple',
    version: '2.1.3',
    thumbsUp: 4
  },
  {
    id: '15',
    userName: 'Максим С.',
    rating: 5,
    text: 'Відмінний сервіс! Вивчаю японську, дуже складну мову, але викладачі допомагають розібратися. Рекомендую!',
    date: new Date(Date.now() - 30 * 60 * 60 * 1000), // 30 годин тому
    source: 'google',
    version: '2.1.4',
    thumbsUp: 13
  }
]

// Мок-дані для статистики
export const mockStats: Stats = {
  totalReviews: 15,
  avgRating: 4.1,
  googlePlayReviews: 8,
  appStoreReviews: 7,
  positiveReviews: 9, // рейтинг 4-5
  negativeReviews: 2  // рейтинг 1-2
}

// Функція для отримання мок-даних з затримкою (імітація API)
export const getMockData = async (): Promise<{ reviews: Review[], stats: Stats }> => {
  // Імітуємо затримку API
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  return {
    reviews: mockReviews,
    stats: mockStats
  }
}
