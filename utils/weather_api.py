"""
Weather API Integration for WeatherEyes
Darmowe API do porównania z danymi z social media
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, city: str = "Warsaw") -> Dict:
        """Pobiera aktualną pogodę z OpenWeatherMap API"""
        
        # Mock data dla demo (żeby nie wymagać prawdziwego API key)
        if self.api_key == 'demo_key':
            return self._get_mock_weather_data(city)
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pl'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._normalize_weather_data(data)
            
        except Exception as e:
            print(f"Weather API Error: {e}")
            return self._get_mock_weather_data(city)
    
    def _get_mock_weather_data(self, city: str) -> Dict:
        """Mock dane pogodowe dla demo"""
        return {
            "city": city,
            "temperature": 15.2,
            "description": "pochmurno",
            "condition": "cloudy",
            "humidity": 67,
            "wind_speed": 12.5,
            "timestamp": datetime.now().isoformat(),
            "source": "mock_api"
        }
    
    def _normalize_weather_data(self, raw_data: Dict) -> Dict:
        """Normalizuje dane z API do naszego formatu"""
        
        # Mapowanie OpenWeather conditions na nasze kategorie
        condition_map = {
            "clear": "sunny",
            "clouds": "cloudy", 
            "rain": "rainy",
            "drizzle": "rainy",
            "snow": "snow",
            "thunderstorm": "stormy"
        }
        
        weather_main = raw_data['weather'][0]['main'].lower()
        condition = condition_map.get(weather_main, "unknown")
        
        return {
            "city": raw_data['name'],
            "temperature": raw_data['main']['temp'],
            "description": raw_data['weather'][0]['description'],
            "condition": condition,
            "humidity": raw_data['main']['humidity'],
            "wind_speed": raw_data['wind']['speed'],
            "timestamp": datetime.now().isoformat(),
            "source": "openweathermap"
        }
    
    def compare_with_social_data(self, social_weather: str, city: str = "Warsaw") -> Dict:
        """Porównuje dane z social media z oficjalnym API"""
        
        api_weather = self.get_current_weather(city)
        api_condition = api_weather['condition']
        
        # Sprawdza zgodność
        match = social_weather.lower() == api_condition.lower()
        
        return {
            "social_media": social_weather,
            "official_api": api_condition,
            "match": match,
            "confidence": 0.95 if match else 0.3,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "temperature": api_weather['temperature'],
                "description": api_weather['description']
            }
        }

# Test function
def test_weather_api():
    """Test funkcji weather API"""
    api = WeatherAPI()
    
    print("🌤️ Testing Weather API...")
    current = api.get_current_weather("Warsaw")
    print(f"Current weather: {current}")
    
    print("\n🔍 Testing comparison...")
    comparison = api.compare_with_social_data("sunny", "Warsaw")
    print(f"Comparison: {comparison}")
    
if __name__ == "__main__":
    test_weather_api() 