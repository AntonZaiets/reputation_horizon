#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки AI аналізу репутації
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_reputation_analysis():
    """Тестує API аналізу репутації"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 Тестування AI аналізу репутації...")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # 1. Перевірка здоров'я API
            print("1. Перевірка здоров'я API...")
            health_response = await client.get(f"{base_url}/api/health")
            if health_response.status_code == 200:
                print("✅ API працює")
                health_data = health_response.json()
                print(f"   LLM Provider: {health_data.get('llm_provider', 'N/A')}")
            else:
                print(f"❌ API не працює: {health_response.status_code}")
                return
            
            # 2. Тест швидкого огляду
            print("\n2. Тест швидкого огляду...")
            summary_response = await client.get(f"{base_url}/api/reputation/summary?hours=24")
            if summary_response.status_code == 200:
                print("✅ Швидкий огляд працює")
                summary_data = summary_response.json()
                print(f"   Всього відгуків: {summary_data['summary']['total_reviews']}")
                print(f"   Середній рейтинг: {summary_data['summary']['average_rating']}")
                print(f"   Тональність: {summary_data['summary']['sentiment_overview']}")
            else:
                print(f"❌ Швидкий огляд не працює: {summary_response.status_code}")
                print(f"   Помилка: {summary_response.text}")
            
            # 3. Тест повного аналізу (з обмеженням)
            print("\n3. Тест повного AI аналізу...")
            print("   (Аналіз 10 відгуків за останні 24 години)")
            
            analysis_response = await client.get(
                f"{base_url}/api/reputation/analyze?hours=24&max_reviews=10"
            )
            
            if analysis_response.status_code == 200:
                print("✅ AI аналіз працює")
                analysis_data = analysis_response.json()
                
                # Загальна статистика
                print(f"\n📊 Результати аналізу:")
                print(f"   Проаналізовано відгуків: {len(analysis_data['insights'])}")
                print(f"   Загальний бал репутації: {analysis_data['reputation_score']['overall_score']}")
                print(f"   Тренд: {analysis_data['reputation_score']['trend']}")
                
                # Розподіл тональності
                sentiment_dist = analysis_data['reputation_score']['sentiment_distribution']
                print(f"\n😊 Розподіл тональності:")
                print(f"   Позитивні: {sentiment_dist['positive']}")
                print(f"   Нейтральні: {sentiment_dist['neutral']}")
                print(f"   Негативні: {sentiment_dist['negative']}")
                
                # Топ проблеми
                if analysis_data['reputation_score']['top_issues']:
                    print(f"\n⚠️ Топ проблеми:")
                    for i, issue in enumerate(analysis_data['reputation_score']['top_issues'][:3], 1):
                        print(f"   {i}. {issue}")
                
                # Позитивні аспекти
                if analysis_data['reputation_score']['positive_aspects']:
                    print(f"\n✅ Позитивні аспекти:")
                    for i, aspect in enumerate(analysis_data['reputation_score']['positive_aspects'][:3], 1):
                        print(f"   {i}. {aspect}")
                
                # Пріоритетні проблеми
                if analysis_data['priority_issues']:
                    print(f"\n🚨 Пріоритетні проблеми:")
                    for i, issue in enumerate(analysis_data['priority_issues'][:3], 1):
                        print(f"   {i}. {issue['issue']} (серйозність: {issue['severity']})")
                        print(f"      Частота: {issue['frequency']} разів")
                        print(f"      Відділ: {issue['department']}")
                        print(f"      Рекомендація: {issue['recommended_response']}")
                        print()
                
                # Приклад аналізу окремого відгуку
                if analysis_data['insights']:
                    print(f"\n🔍 Приклад аналізу відгуку:")
                    first_insight = analysis_data['insights'][0]
                    print(f"   ID відгуку: {first_insight['review_id']}")
                    print(f"   Тональність: {first_insight['sentiment']['sentiment']}")
                    print(f"   Впевненість: {first_insight['sentiment']['confidence']:.2f}")
                    print(f"   Намір: {first_insight['intent']['primary_intent']}")
                    print(f"   Пріоритет: {first_insight['priority_score']:.1f}")
                    print(f"   Рекомендована дія: {first_insight['recommended_action']}")
                    if first_insight['topics']['main_topics']:
                        print(f"   Теми: {', '.join(first_insight['topics']['main_topics'])}")
                
            else:
                print(f"❌ AI аналіз не працює: {analysis_response.status_code}")
                print(f"   Помилка: {analysis_response.text}")
            
            print("\n" + "=" * 50)
            print("🎉 Тестування завершено!")
            
        except httpx.RequestError as e:
            print(f"❌ Помилка з'єднання: {e}")
            print("💡 Переконайтесь, що backend запущений на http://localhost:8000")
        except Exception as e:
            print(f"❌ Неочікувана помилка: {e}")

async def test_without_openai():
    """Тестує систему без OpenAI (mock дані)"""
    print("🧪 Тестування з mock даними (без OpenAI)...")
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Тест з mock даними
            response = await client.get(f"{base_url}/api/reputation/analyze?hours=24&max_reviews=5")
            
            if response.status_code == 200:
                print("✅ Mock аналіз працює")
                data = response.json()
                print(f"   Проаналізовано: {len(data['insights'])} відгуків")
                print(f"   Бал репутації: {data['reputation_score']['overall_score']}")
            else:
                print(f"❌ Mock аналіз не працює: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    print("🤖 Reputation Horizon - Тест AI аналізу")
    print("=" * 50)
    
    # Запуск тестів
    asyncio.run(test_reputation_analysis())
    
    print("\n" + "=" * 50)
    print("💡 Для повного тестування налаштуйте OPENAI_API_KEY в .env файлі")
    print("📖 Детальні інструкції: REPUTATION_ANALYSIS.md")
