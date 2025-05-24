"""
Weather Alert System for WeatherEyes
System powiadomień pogodowych z różnymi scenariuszami
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class AlertType(Enum):
    DAILY_SUMMARY = "daily_summary"      # Codzienne podsumowanie
    WEATHER_CHANGE = "weather_change"    # Zmiana pogody
    EVENT_ALERT = "event_alert"         # Alert przed wydarzeniem
    TRIP_PLANNING = "trip_planning"     # Planowanie wyjazdu

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    URGENT = "urgent"

class WeatherAlertSystem:
    def __init__(self):
        self.alert_history = []
        self.user_preferences = {
            "daily_summary_time": "08:00",
            "enable_change_alerts": True,
            "event_alert_hours_ahead": 2,
            "min_confidence_threshold": 0.7
        }
        
        # Templates for different alert types
        self.message_templates = {
            AlertType.DAILY_SUMMARY: {
                "title": "🌤️ Poranne podsumowanie pogody",
                "template": "Dzień dobry! Na podstawie analizy social media:\n{weather_info}\n\nMiej świetny dzień! 🌟"
            },
            AlertType.WEATHER_CHANGE: {
                "title": "⚡ Zmiana pogody wykryta!",
                "template": "Uwaga! Pogoda się zmienia:\n{change_info}\n\nPrzygotuj się odpowiednio! 🧥"
            },
            AlertType.EVENT_ALERT: {
                "title": "📅 Alert przed wydarzeniem",
                "template": "Za {time_until} zaczyna się {event_name}:\n{weather_forecast}\n\nPowodzenia! 🎯"
            },
            AlertType.TRIP_PLANNING: {
                "title": "🧳 Pogoda na wyjazd",
                "template": "Planowany wyjazd do {destination}:\n{trip_weather}\n\nDobrej podróży! ✈️"
            }
        }
    
    def create_daily_summary_alert(self, weather_data: Dict) -> Dict:
        """Tworzy codzienny alert podsumowujący"""
        
        dominant_weather = weather_data.get('dominant_weather', 'unknown')
        confidence = weather_data.get('confidence', 0)
        
        weather_emoji = {
            'sunny': '☀️',
            'cloudy': '☁️', 
            'rainy': '🌧️',
            'snow': '❄️',
            'clear': '🌙'
        }
        
        emoji = weather_emoji.get(dominant_weather, '🌤️')
        
        weather_info = f"{emoji} Dominująca pogoda: {dominant_weather}\n"
        weather_info += f"📊 Pewność: {confidence*100:.1f}%\n"
        weather_info += f"📱 Analizowano {weather_data.get('total_posts_analyzed', 0)} postów z social media"
        
        message = self.message_templates[AlertType.DAILY_SUMMARY]["template"].format(
            weather_info=weather_info
        )
        
        return self._create_alert(
            alert_type=AlertType.DAILY_SUMMARY,
            message=message,
            priority=AlertPriority.LOW,
            data=weather_data
        )
    
    def create_weather_change_alert(self, old_weather: str, new_weather: str, confidence: float) -> Dict:
        """Tworzy alert o zmianie pogody"""
        
        if confidence < self.user_preferences["min_confidence_threshold"]:
            return None  # Nie wysyłaj alertu jeśli pewność za niska
        
        change_info = f"🔄 {old_weather} → {new_weather}\n"
        change_info += f"📊 Pewność: {confidence*100:.1f}%\n"
        change_info += f"⏰ Wykryto: {datetime.now().strftime('%H:%M')}"
        
        # Określ priorytet na podstawie typu zmiany
        priority = self._get_change_priority(old_weather, new_weather)
        
        message = self.message_templates[AlertType.WEATHER_CHANGE]["template"].format(
            change_info=change_info
        )
        
        return self._create_alert(
            alert_type=AlertType.WEATHER_CHANGE,
            message=message,
            priority=priority,
            data={
                "old_weather": old_weather,
                "new_weather": new_weather,
                "confidence": confidence
            }
        )
    
    def create_event_alert(self, event_name: str, event_time: datetime, weather_forecast: Dict) -> Dict:
        """Tworzy alert przed wydarzeniem"""
        
        now = datetime.now()
        time_until = event_time - now
        hours_until = time_until.total_seconds() / 3600
        
        if hours_until > self.user_preferences["event_alert_hours_ahead"]:
            return None  # Za wcześnie na alert
        
        time_until_str = f"{int(hours_until)}h {int((hours_until % 1) * 60)}min"
        
        weather_info = f"🌤️ Przewidywana pogoda: {weather_forecast.get('condition', 'unknown')}\n"
        weather_info += f"🌡️ Temperatura: {weather_forecast.get('temperature', 'N/A')}°C\n"
        weather_info += f"💨 Wiatr: {weather_forecast.get('wind_speed', 'N/A')} km/h"
        
        message = self.message_templates[AlertType.EVENT_ALERT]["template"].format(
            time_until=time_until_str,
            event_name=event_name,
            weather_forecast=weather_info
        )
        
        return self._create_alert(
            alert_type=AlertType.EVENT_ALERT,
            message=message,
            priority=AlertPriority.MEDIUM,
            data={
                "event_name": event_name,
                "event_time": event_time.isoformat(),
                "weather_forecast": weather_forecast
            }
        )
    
    def create_trip_planning_alert(self, destination: str, departure_date: datetime, weather_forecast: List[Dict]) -> Dict:
        """Tworzy alert do planowania wyjazdu"""
        
        trip_weather = f"📍 Miejsce: {destination}\n"
        trip_weather += f"📅 Data wyjazdu: {departure_date.strftime('%d.%m.%Y')}\n\n"
        
        # Podsumowanie pogody na kilka dni
        for i, day_forecast in enumerate(weather_forecast[:3]):  # Pierwsze 3 dni
            date = departure_date + timedelta(days=i)
            trip_weather += f"🗓️ {date.strftime('%d.%m')}: {day_forecast.get('condition', 'unknown')}"
            trip_weather += f" ({day_forecast.get('temperature', 'N/A')}°C)\n"
        
        message = self.message_templates[AlertType.TRIP_PLANNING]["template"].format(
            destination=destination,
            trip_weather=trip_weather
        )
        
        return self._create_alert(
            alert_type=AlertType.TRIP_PLANNING,
            message=message,
            priority=AlertPriority.LOW,
            data={
                "destination": destination,
                "departure_date": departure_date.isoformat(),
                "weather_forecast": weather_forecast
            }
        )
    
    def _create_alert(self, alert_type: AlertType, message: str, priority: AlertPriority, data: Dict) -> Dict:
        """Tworzy obiekt alertu"""
        
        alert = {
            "id": f"alert_{len(self.alert_history) + 1}",
            "type": alert_type.value,
            "title": self.message_templates[alert_type]["title"],
            "message": message,
            "priority": priority.value,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "sent": False
        }
        
        self.alert_history.append(alert)
        return alert
    
    def _get_change_priority(self, old_weather: str, new_weather: str) -> AlertPriority:
        """Określa priorytet alertu na podstawie zmiany pogody"""
        
        high_priority_changes = [
            ("sunny", "rainy"),
            ("cloudy", "rainy"), 
            ("clear", "stormy"),
            ("sunny", "snow")
        ]
        
        urgent_changes = [
            ("sunny", "stormy"),
            ("clear", "stormy")
        ]
        
        change = (old_weather, new_weather)
        
        if change in urgent_changes:
            return AlertPriority.URGENT
        elif change in high_priority_changes:
            return AlertPriority.HIGH
        else:
            return AlertPriority.MEDIUM
    
    def get_pending_alerts(self) -> List[Dict]:
        """Zwraca niewyśłane alerty"""
        return [alert for alert in self.alert_history if not alert["sent"]]
    
    def mark_alert_sent(self, alert_id: str):
        """Oznacza alert jako wysłany"""
        for alert in self.alert_history:
            if alert["id"] == alert_id:
                alert["sent"] = True
                break
    
    def get_alert_stats(self) -> Dict:
        """Statystyki alertów"""
        total = len(self.alert_history)
        sent = sum(1 for alert in self.alert_history if alert["sent"])
        
        by_type = {}
        by_priority = {}
        
        for alert in self.alert_history:
            alert_type = alert["type"]
            priority = alert["priority"]
            
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total_alerts": total,
            "sent_alerts": sent,
            "pending_alerts": total - sent,
            "by_type": by_type,
            "by_priority": by_priority,
            "last_alert": self.alert_history[-1]["timestamp"] if self.alert_history else None
        }

# Demo function
def demo_alert_system():
    """Demo różnych typów alertów"""
    
    alert_system = WeatherAlertSystem()
    
    print("🚨 Demo Weather Alert System\n")
    
    # 1. Daily Summary
    print("1️⃣ Daily Summary Alert:")
    daily_data = {
        "dominant_weather": "cloudy",
        "confidence": 0.87,
        "total_posts_analyzed": 15
    }
    daily_alert = alert_system.create_daily_summary_alert(daily_data)
    print(f"Title: {daily_alert['title']}")
    print(f"Message: {daily_alert['message']}\n")
    
    # 2. Weather Change
    print("2️⃣ Weather Change Alert:")
    change_alert = alert_system.create_weather_change_alert("sunny", "rainy", 0.92)
    print(f"Title: {change_alert['title']}")
    print(f"Message: {change_alert['message']}\n")
    
    # 3. Event Alert  
    print("3️⃣ Event Alert:")
    event_time = datetime.now() + timedelta(hours=1.5)
    weather_forecast = {
        "condition": "sunny",
        "temperature": 22,
        "wind_speed": 8
    }
    event_alert = alert_system.create_event_alert("SHAMAN 2024 Prezentacja", event_time, weather_forecast)
    print(f"Title: {event_alert['title']}")
    print(f"Message: {event_alert['message']}\n")
    
    # 4. Trip Planning
    print("4️⃣ Trip Planning Alert:")
    departure = datetime.now() + timedelta(days=2)
    trip_forecast = [
        {"condition": "sunny", "temperature": 25},
        {"condition": "cloudy", "temperature": 20},
        {"condition": "rainy", "temperature": 18}
    ]
    trip_alert = alert_system.create_trip_planning_alert("Kraków", departure, trip_forecast)
    print(f"Title: {trip_alert['title']}")
    print(f"Message: {trip_alert['message']}\n")
    
    # Stats
    print("📊 Alert Statistics:")
    stats = alert_system.get_alert_stats()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    demo_alert_system() 