"""
Real Alert System for WeatherEyes
Prawdziwe alerty przez Telegram Bot i SMS
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from twilio.rest import Client
from pathlib import Path

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', 'demo_token')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', 'demo_chat')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_message(self, message: str, parse_mode: str = "HTML") -> Dict:
        """Wysyła wiadomość przez Telegram"""
        
        if self.bot_token == 'demo_token':
            return self._demo_send_message(message)
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            return {
                'success': True,
                'message_id': response.json()['result']['message_id'],
                'timestamp': datetime.now().isoformat(),
                'platform': 'telegram'
            }
            
        except Exception as e:
            print(f"Telegram Error: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'platform': 'telegram'
            }
    
    def send_photo(self, photo_path: str, caption: str = "") -> Dict:
        """Wysyła zdjęcie z opisem przez Telegram"""
        
        if self.bot_token == 'demo_token':
            return self._demo_send_photo(photo_path, caption)
        
        try:
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                
                return {
                    'success': True,
                    'message_id': response.json()['result']['message_id'],
                    'timestamp': datetime.now().isoformat(),
                    'platform': 'telegram',
                    'type': 'photo'
                }
                
        except Exception as e:
            print(f"Telegram Photo Error: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'platform': 'telegram'
            }
    
    def _demo_send_message(self, message: str) -> Dict:
        """Demo wysyłania wiadomości"""
        print(f"📱 [TELEGRAM DEMO] Wysłano: {message[:50]}...")
        return {
            'success': True,
            'message_id': f"demo_{int(datetime.now().timestamp())}",
            'timestamp': datetime.now().isoformat(),
            'platform': 'telegram_demo'
        }
    
    def _demo_send_photo(self, photo_path: str, caption: str) -> Dict:
        """Demo wysyłania zdjęcia"""
        print(f"📷 [TELEGRAM DEMO] Wysłano zdjęcie: {Path(photo_path).name}")
        print(f"📝 [TELEGRAM DEMO] Opis: {caption[:50]}...")
        return {
            'success': True,
            'message_id': f"demo_photo_{int(datetime.now().timestamp())}",
            'timestamp': datetime.now().isoformat(),
            'platform': 'telegram_demo',
            'type': 'photo'
        }

class SMSAlert:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'demo_sid')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'demo_token')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER', '+1234567890')
        self.to_number = os.getenv('TWILIO_TO_NUMBER', '+1987654321')
        
        if self.account_sid != 'demo_sid':
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def send_sms(self, message: str) -> Dict:
        """Wysyła SMS przez Twilio"""
        
        if self.client is None:
            return self._demo_send_sms(message)
        
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            return {
                'success': True,
                'message_sid': message_obj.sid,
                'timestamp': datetime.now().isoformat(),
                'platform': 'sms'
            }
            
        except Exception as e:
            print(f"SMS Error: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'platform': 'sms'
            }
    
    def _demo_send_sms(self, message: str) -> Dict:
        """Demo wysyłania SMS"""
        print(f"📞 [SMS DEMO] Wysłano na {self.to_number}: {message[:50]}...")
        return {
            'success': True,
            'message_sid': f"demo_sms_{int(datetime.now().timestamp())}",
            'timestamp': datetime.now().isoformat(),
            'platform': 'sms_demo'
        }

class RealAlertSystem:
    def __init__(self):
        self.telegram = TelegramBot()
        self.sms = SMSAlert()
        self.alert_history = []
        
        # Templates wiadomości
        self.templates = {
            'weather_change': {
                'telegram': """
🌤️ <b>WeatherEyes Alert</b>

⚠️ <b>Zmiana Pogody Wykryta!</b>
📍 Lokalizacja: {location}
🕐 Czas: {timestamp}

📊 <b>Analiza:</b>
• Poprzednia pogoda: {previous_weather}
• Aktualna pogoda: {current_weather}
• Pewność: {confidence}%

🔍 <b>Źródło:</b> Analiza social media
📱 <i>WeatherEyes - SHAMAN 2024</i>
                """,
                'sms': "🌤️ WeatherEyes Alert: Zmiana pogody z {previous_weather} na {current_weather} w {location}. Pewność: {confidence}%"
            },
            'event_weather': {
                'telegram': """
🎯 <b>Event Weather Alert</b>

📅 <b>Wydarzenie:</b> {event_name}
📍 Lokalizacja: {location}
🕐 Czas wydarzenia: {event_time}

🌤️ <b>Prognoza Pogody:</b>
• Warunki: {weather_condition}
• Temperatura: {temperature}°C
• Deszcz: {rain_chance}%

💡 <b>Rekomendacja:</b>
{recommendation}

📱 <i>WeatherEyes - Twój pogodowy asystent</i>
                """,
                'sms': "🎯 Event Alert: {event_name} - Pogoda: {weather_condition}, {temperature}°C. {recommendation}"
            },
            'daily_summary': {
                'telegram': """
📊 <b>WeatherEyes - Dzienny Raport</b>

📅 Data: {date}
📍 Lokalizacja: {location}

🌤️ <b>Podsumowanie Pogody:</b>
• Dominujące warunki: {dominant_weather}
• Średnia pewność: {avg_confidence}%
• Analizowane posty: {posts_count}

📈 <b>Trendy:</b>
{weather_trends}

🔍 <b>Źródła:</b> Social Media Analysis
📱 <i>WeatherEyes - SHAMAN 2024</i>
                """,
                'sms': "📊 WeatherEyes Raport: {dominant_weather} ({avg_confidence}% pewności) z {posts_count} postów."
            }
        }
    
    def send_weather_change_alert(self, previous_weather: str, current_weather: str, 
                                  confidence: float, location: str = "SHAMAN Event") -> Dict:
        """Wysyła alert o zmianie pogody"""
        
        timestamp = datetime.now().strftime("%H:%M, %d.%m.%Y")
        
        # Przygotuj dane do template
        data = {
            'previous_weather': previous_weather,
            'current_weather': current_weather,
            'confidence': round(confidence * 100, 1),
            'location': location,
            'timestamp': timestamp
        }
        
        # Wysyłanie przez Telegram
        telegram_msg = self.templates['weather_change']['telegram'].format(**data)
        telegram_result = self.telegram.send_message(telegram_msg)
        
        # Wysyłanie SMS
        sms_msg = self.templates['weather_change']['sms'].format(**data)
        sms_result = self.sms.send_sms(sms_msg)
        
        # Zapisz w historii
        alert_record = {
            'type': 'weather_change',
            'data': data,
            'results': {
                'telegram': telegram_result,
                'sms': sms_result
            },
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert_record)
        
        return alert_record
    
    def send_event_weather_alert(self, event_name: str, event_time: str, 
                                weather_data: Dict, location: str = "SHAMAN Event") -> Dict:
        """Wysyła alert pogodowy dla wydarzenia"""
        
        # Przygotuj rekomendację
        weather_condition = weather_data.get('condition', 'unknown')
        temperature = weather_data.get('temperature', 20)
        rain_chance = weather_data.get('rain_chance', 0)
        
        if rain_chance > 70:
            recommendation = "🌂 Zabierz parasol! Wysokie prawdopodobieństwo deszczu."
        elif rain_chance > 30:
            recommendation = "☁️ Możliwy deszcz - warto mieć parasol."
        elif temperature < 10:
            recommendation = "🧥 Ubierz się ciepło - będzie chłodno."
        elif temperature > 25:
            recommendation = "🌞 Przyjemna pogoda - lekkie ubrania będą idealne."
        else:
            recommendation = "👍 Dobre warunki pogodowe dla wydarzenia."
        
        data = {
            'event_name': event_name,
            'event_time': event_time,
            'location': location,
            'weather_condition': weather_condition,
            'temperature': temperature,
            'rain_chance': rain_chance,
            'recommendation': recommendation
        }
        
        # Wysyłanie alertów
        telegram_msg = self.templates['event_weather']['telegram'].format(**data)
        telegram_result = self.telegram.send_message(telegram_msg)
        
        sms_msg = self.templates['event_weather']['sms'].format(**data)
        sms_result = self.sms.send_sms(sms_msg)
        
        # Zapisz w historii
        alert_record = {
            'type': 'event_weather',
            'data': data,
            'results': {
                'telegram': telegram_result,
                'sms': sms_result
            },
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert_record)
        
        return alert_record
    
    def send_daily_summary_alert(self, weather_summary: Dict, location: str = "SHAMAN Event") -> Dict:
        """Wysyła dzienny raport pogodowy"""
        
        date = datetime.now().strftime("%d.%m.%Y")
        
        # Przygotuj trendy
        weather_dist = weather_summary.get('weather_distribution', {})
        trends = []
        for weather, info in weather_dist.items():
            trends.append(f"• {weather}: {info['count']} postów")
        
        data = {
            'date': date,
            'location': location,
            'dominant_weather': weather_summary.get('dominant_weather', 'unknown'),
            'avg_confidence': round(weather_summary.get('confidence', 0) * 100, 1),
            'posts_count': weather_summary.get('total_images_analyzed', 0),
            'weather_trends': '\n'.join(trends) if trends else 'Brak danych'
        }
        
        # Wysyłanie alertów
        telegram_msg = self.templates['daily_summary']['telegram'].format(**data)
        telegram_result = self.telegram.send_message(telegram_msg)
        
        sms_msg = self.templates['daily_summary']['sms'].format(**data)
        sms_result = self.sms.send_sms(sms_msg)
        
        # Zapisz w historii
        alert_record = {
            'type': 'daily_summary',
            'data': data,
            'results': {
                'telegram': telegram_result,
                'sms': sms_result
            },
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert_record)
        
        return alert_record
    
    def send_image_analysis_alert(self, image_path: str, analysis: Dict) -> Dict:
        """Wysyła alert z analizą zdjęcia"""
        
        caption = f"""
🔍 <b>Analiza Zdjęcia WeatherEyes</b>

📸 <b>Zdjęcie:</b> {Path(image_path).name}
🌤️ <b>Wykryta pogoda:</b> {analysis.get('weather_condition', 'unknown')}
📊 <b>Pewność:</b> {round(analysis.get('confidence', 0) * 100, 1)}%

💭 <b>Opis:</b>
{analysis.get('description', 'Brak opisu')}

🕐 <b>Czas analizy:</b> {datetime.now().strftime("%H:%M, %d.%m.%Y")}
📱 <i>WeatherEyes - SHAMAN 2024</i>
        """
        
        # Wyślij zdjęcie z analizą przez Telegram
        telegram_result = self.telegram.send_photo(image_path, caption)
        
        # SMS z podstawowymi informacjami
        sms_msg = f"🔍 WeatherEyes: Wykryto {analysis.get('weather_condition', 'unknown')} na zdjęciu {Path(image_path).name} ({round(analysis.get('confidence', 0) * 100, 1)}% pewności)"
        sms_result = self.sms.send_sms(sms_msg)
        
        # Zapisz w historii
        alert_record = {
            'type': 'image_analysis',
            'data': {
                'image_path': image_path,
                'analysis': analysis
            },
            'results': {
                'telegram': telegram_result,
                'sms': sms_result
            },
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert_record)
        
        return alert_record
    
    def get_alert_history(self) -> List[Dict]:
        """Zwraca historię alertów"""
        return self.alert_history
    
    def get_alert_stats(self) -> Dict:
        """Zwraca statystyki alertów"""
        
        total = len(self.alert_history)
        successful_telegram = sum(1 for alert in self.alert_history 
                                  if alert['results']['telegram']['success'])
        successful_sms = sum(1 for alert in self.alert_history 
                            if alert['results']['sms']['success'])
        
        by_type = {}
        for alert in self.alert_history:
            alert_type = alert['type']
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
        
        return {
            'total_alerts': total,
            'successful_telegram': successful_telegram,
            'successful_sms': successful_sms,
            'success_rate_telegram': successful_telegram / max(total, 1),
            'success_rate_sms': successful_sms / max(total, 1),
            'by_type': by_type,
            'last_alert': self.alert_history[-1]['timestamp'] if self.alert_history else None
        }

# Test function
def test_real_alerts():
    """Test real alert system"""
    
    print("🚨 Testing Real Alert System...")
    
    alert_system = RealAlertSystem()
    
    # Test 1: Weather change alert
    print("\n1️⃣ Testing weather change alert...")
    result1 = alert_system.send_weather_change_alert(
        "sunny", "cloudy", 0.89, "SHAMAN 2024 Event"
    )
    print(f"✅ Weather change alert: {result1['results']['telegram']['success']}")
    
    # Test 2: Event weather alert
    print("\n2️⃣ Testing event weather alert...")
    weather_data = {
        'condition': 'partly_cloudy',
        'temperature': 22,
        'rain_chance': 30
    }
    result2 = alert_system.send_event_weather_alert(
        "SHAMAN Finał", "15:00, 24.11.2024", weather_data
    )
    print(f"✅ Event weather alert: {result2['results']['telegram']['success']}")
    
    # Test 3: Daily summary
    print("\n3️⃣ Testing daily summary...")
    summary = {
        'dominant_weather': 'sunny',
        'confidence': 0.87,
        'total_images_analyzed': 5,
        'weather_distribution': {
            'sunny': {'count': 3},
            'cloudy': {'count': 2}
        }
    }
    result3 = alert_system.send_daily_summary_alert(summary)
    print(f"✅ Daily summary alert: {result3['results']['telegram']['success']}")
    
    # Statistics
    print("\n📊 Alert Statistics:")
    stats = alert_system.get_alert_stats()
    print(f"Total alerts sent: {stats['total_alerts']}")
    print(f"Telegram success rate: {stats['success_rate_telegram']:.1%}")
    print(f"SMS success rate: {stats['success_rate_sms']:.1%}")

if __name__ == "__main__":
    test_real_alerts() 