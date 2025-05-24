#!/usr/bin/env python3
"""
WeatherEyes - Event Edition Demo
Główny skrypt demonstracyjny dla hackathonu SHAMAN 2024

Ten skrypt pokazuje pełny workflow:
1. Ładowanie mock danych z social media
2. Analiza AI pogody ze zdjęć  
3. Porównanie z oficjalnym API pogody
4. Generowanie różnych typów alertów
5. Live demo dashboard
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add project modules to path
sys.path.append(str(Path(__file__).parent))

from utils.weather_api import WeatherAPI
from ai_model.weather_classifier import WeatherClassifier
from bot.alert_system import WeatherAlertSystem, AlertType

class WeatherEyesDemo:
    def __init__(self):
        print("🌤️ Inicjalizacja WeatherEyes Demo...")
        self.weather_api = WeatherAPI()
        self.ai_classifier = WeatherClassifier()
        self.alert_system = WeatherAlertSystem()
        
        # Load mock data
        self.mock_data = self._load_mock_data()
        print(f"✅ Załadowano {len(self.mock_data['posts'])} postów z social media")
    
    def _load_mock_data(self):
        """Ładuje mock dane z Instagram postów"""
        try:
            with open('data/mock_instagram_posts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Mock data nie znaleziona, używam backup danych...")
            return self._create_backup_data()
    
    def _create_backup_data(self):
        """Backup dane jeśli plik nie istnieje"""
        return {
            "posts": [
                {
                    "id": "demo_001",
                    "hashtags": ["#shaman2024", "#demo"],
                    "location": "Warsaw, Poland",
                    "timestamp": datetime.now().isoformat(),
                    "image_url": "demo_sunny.jpg",
                    "description": "Beautiful sunny day at SHAMAN! ☀️",
                    "user": "demo_user"
                }
            ],
            "metadata": {
                "total_posts": 1,
                "date_range": datetime.now().strftime("%Y-%m-%d"),
                "location": "Warsaw, Poland"
            }
        }
    
    def run_full_demo(self):
        """Uruchamia pełne demo wszystkich funkcjonalności"""
        
        print("\n" + "="*60)
        print("🚀 WEATHEREYES - LIVE DEMO SHAMAN 2024")
        print("="*60)
        
        # Step 1: Analiza AI postów z social media
        print("\n1️⃣ ANALIZA AI POSTÓW Z SOCIAL MEDIA")
        print("-" * 40)
        
        ai_results = self.ai_classifier.batch_classify(self.mock_data['posts'])
        weather_summary = self.ai_classifier.get_weather_summary(ai_results)
        
        print(f"🧠 Analizowano {len(ai_results)} postów")
        print(f"🌤️ Dominująca pogoda: {weather_summary['dominant_weather']}")
        print(f"📊 Średnia pewność: {weather_summary['confidence']*100:.1f}%")
        
        time.sleep(2)  # Dramatic pause for demo
        
        # Step 2: Porównanie z oficjalnym API
        print("\n2️⃣ PORÓWNANIE Z OFICJALNYM API POGODY")
        print("-" * 40)
        
        official_weather = self.weather_api.get_current_weather("Warsaw")
        comparison = self.weather_api.compare_with_social_data(
            weather_summary['dominant_weather'], "Warsaw"
        )
        
        print(f"🌍 Oficjalna pogoda: {official_weather['condition']}")
        print(f"📱 Social media: {weather_summary['dominant_weather']}")
        print(f"✅ Zgodność: {'TAK' if comparison['match'] else 'NIE'}")
        print(f"🌡️ Temperatura: {official_weather['temperature']}°C")
        
        time.sleep(2)
        
        # Step 3: Generowanie alertów
        print("\n3️⃣ GENEROWANIE ALERTÓW POGODOWYCH")
        print("-" * 40)
        
        # Daily summary alert
        daily_alert = self.alert_system.create_daily_summary_alert(weather_summary)
        print(f"📅 {daily_alert['title']}")
        print(f"   {daily_alert['message'][:100]}...")
        
        # Weather change alert (symulacja)
        change_alert = self.alert_system.create_weather_change_alert(
            "sunny", "rainy", 0.89
        )
        if change_alert:
            print(f"⚡ {change_alert['title']}")
            print(f"   Wykryto zmianę pogody z wysoką pewnością!")
        
        # Event alert
        event_time = datetime.now() + timedelta(hours=1)
        event_alert = self.alert_system.create_event_alert(
            "Finał SHAMAN 2024", event_time, official_weather
        )
        if event_alert:
            print(f"📅 {event_alert['title']}")
            print(f"   Alert przed wydarzeniem!")
        
        time.sleep(2)
        
        # Step 4: Statystyki i podsumowanie
        print("\n4️⃣ STATYSTYKI I PODSUMOWANIE")
        print("-" * 40)
        
        alert_stats = self.alert_system.get_alert_stats()
        print(f"🚨 Wygenerowane alerty: {alert_stats['total_alerts']}")
        print(f"📊 Typy alertów: {list(alert_stats['by_type'].keys())}")
        print(f"⏰ Ostatni alert: {alert_stats['last_alert']}")
        
        print("\n" + "="*60)
        print("✅ DEMO ZAKOŃCZONE POMYŚLNIE!")
        print("💡 WeatherEyes: Dane pogodowe jako sojusznik człowieka")
        print("="*60)
        
        return {
            "ai_analysis": weather_summary,
            "official_weather": official_weather,
            "comparison": comparison,
            "alerts": alert_stats
        }
    
    def run_interactive_demo(self):
        """Interaktywne demo z wyborem opcji"""
        
        while True:
            print("\n🌤️ WEATHEREYES - INTERACTIVE DEMO")
            print("1. Pełna analiza postów")
            print("2. Test alertów")
            print("3. Porównanie z API")
            print("4. Statystyki")
            print("5. Live feed simulation")
            print("0. Wyjście")
            
            choice = input("\nWybierz opcję (0-5): ").strip()
            
            if choice == "0":
                print("👋 Do widzenia!")
                break
            elif choice == "1":
                self._demo_ai_analysis()
            elif choice == "2":
                self._demo_alerts()
            elif choice == "3":
                self._demo_api_comparison()
            elif choice == "4":
                self._demo_stats()
            elif choice == "5":
                self._demo_live_feed()
            else:
                print("❌ Nieprawidłowy wybór!")
    
    def _demo_ai_analysis(self):
        """Demo analizy AI"""
        print("\n🧠 Analiza AI w toku...")
        results = self.ai_classifier.batch_classify(self.mock_data['posts'])
        
        for result in results:
            post = result['original_post']
            analysis = result['classification']
            print(f"\n📱 Post: {post['description'][:50]}...")
            print(f"🌤️ Wykryta pogoda: {analysis['predicted_weather']}")
            print(f"📊 Pewność: {analysis['confidence']*100:.1f}%")
    
    def _demo_alerts(self):
        """Demo różnych alertów"""
        print("\n🚨 Generowanie przykładowych alertów...")
        
        # Different alert scenarios
        scenarios = [
            ("Codzienny raport", lambda: self.alert_system.create_daily_summary_alert({
                "dominant_weather": "sunny", "confidence": 0.92, "total_posts_analyzed": 25
            })),
            ("Zmiana pogody", lambda: self.alert_system.create_weather_change_alert(
                "cloudy", "rainy", 0.87
            )),
            ("Przed wydarzeniem", lambda: self.alert_system.create_event_alert(
                "Prezentacja finałowa", datetime.now() + timedelta(hours=1), 
                {"condition": "clear", "temperature": 18, "wind_speed": 5}
            ))
        ]
        
        for name, alert_func in scenarios:
            alert = alert_func()
            if alert:
                print(f"\n📢 {name}:")
                print(f"   {alert['message'][:100]}...")
    
    def _demo_api_comparison(self):
        """Demo porównania z API"""
        print("\n🌍 Porównanie z oficjalnym API...")
        
        current = self.weather_api.get_current_weather("Warsaw")
        comparison = self.weather_api.compare_with_social_data("sunny", "Warsaw")
        
        print(f"API: {current['condition']} ({current['temperature']}°C)")
        print(f"Social: sunny")
        print(f"Zgodność: {'✅' if comparison['match'] else '❌'}")
    
    def _demo_stats(self):
        """Demo statystyk"""
        print("\n📊 Statystyki systemu:")
        stats = self.alert_system.get_alert_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    def _demo_live_feed(self):
        """Symulacja live feed"""
        print("\n📡 Symulacja live feed (30 sekund)...")
        
        for i in range(6):
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Analizuję nowe posty...")
            
            # Symuluj nowy post
            new_weather = ["sunny", "cloudy", "rainy"][i % 3]
            print(f"   🆕 Wykryto: {new_weather}")
            
            time.sleep(5)
        
        print("✅ Live feed zakończony")

def main():
    """Główna funkcja demo"""
    
    try:
        demo = WeatherEyesDemo()
        
        # Sprawdź argumenty CLI
        if len(sys.argv) > 1:
            if sys.argv[1] == "--full":
                demo.run_full_demo()
            elif sys.argv[1] == "--interactive":
                demo.run_interactive_demo()
            else:
                print("Dostępne opcje: --full, --interactive")
        else:
            # Domyślnie uruchom pełne demo
            demo.run_full_demo()
            
            # Opcja przejścia do trybu interaktywnego
            response = input("\n🤔 Chcesz uruchomić tryb interaktywny? (y/n): ")
            if response.lower().startswith('y'):
                demo.run_interactive_demo()
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo przerwane przez użytkownika")
    except Exception as e:
        print(f"\n❌ Błąd demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 