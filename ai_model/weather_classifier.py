"""
Weather Classification Model for WeatherEyes
Prosty classifier do rozpoznawania pogody ze zdjęć
"""

import os
import json
import random
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np

class WeatherClassifier:
    def __init__(self):
        self.weather_classes = [
            "sunny", "cloudy", "rainy", "snow", "stormy", "foggy", "clear"
        ]
        
        # Mock confidence scores for different weather types
        self.confidence_ranges = {
            "sunny": (0.85, 0.98),
            "cloudy": (0.75, 0.92), 
            "rainy": (0.80, 0.95),
            "snow": (0.88, 0.97),
            "stormy": (0.70, 0.90),
            "foggy": (0.65, 0.85),
            "clear": (0.82, 0.94)
        }
        
        # Keywords that help classify weather from image metadata/description
        self.weather_keywords = {
            "sunny": ["sun", "sunny", "bright", "blue sky", "słońce", "słonecznie"],
            "cloudy": ["clouds", "cloudy", "overcast", "chmury", "pochmurno"],
            "rainy": ["rain", "wet", "umbrella", "deszcz", "mokro", "parasol"],
            "snow": ["snow", "white", "winter", "śnieg", "biały", "zima"],
            "stormy": ["storm", "dark", "thunder", "burza", "ciemno", "grzmot"],
            "clear": ["clear", "evening", "night", "czyste", "wieczór", "noc"]
        }
    
    def classify_image(self, image_path: str, description: str = "") -> Dict:
        """
        Klasyfikuje pogodę na zdjęciu
        Na razie mock - ale infrastruktura gotowa na prawdziwy model
        """
        
        # Analiza opisu (jeśli dostępny) 
        weather_from_text = self._analyze_description(description)
        
        # Mock analiza obrazu (tutaj by był prawdziwy CNN model)
        weather_from_image = self._mock_image_analysis(image_path)
        
        # Kombinacja wyników
        final_weather = weather_from_text if weather_from_text else weather_from_image
        confidence = self._calculate_confidence(final_weather, weather_from_text is not None)
        
        return {
            "predicted_weather": final_weather,
            "confidence": confidence,
            "analysis": {
                "from_text": weather_from_text,
                "from_image": weather_from_image,
                "description_available": len(description) > 0
            },
            "timestamp": datetime.now().isoformat(),
            "model_version": "mock_v1.0"
        }
    
    def _analyze_description(self, description: str) -> str:
        """Analizuje opis zdjęcia w poszukiwaniu wskazówek pogodowych"""
        if not description:
            return None
            
        description_lower = description.lower()
        
        # Sprawdza każdą kategorię pogody
        for weather, keywords in self.weather_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return weather
        
        return None
    
    def _mock_image_analysis(self, image_path: str) -> str:
        """
        Mock analiza obrazu
        W prawdziwej implementacji tutaj by był model CNN/Vision Transformer
        """
        
        # Losowy wybór pogody na podstawie nazwy pliku (dla demo)
        filename = os.path.basename(image_path).lower()
        
        for weather in self.weather_classes:
            if weather in filename:
                return weather
        
        # Jeśli nie można wywnioskować z nazwy, losowy wybór
        return random.choice(self.weather_classes)
    
    def _calculate_confidence(self, weather: str, has_text_hint: bool) -> float:
        """Kalkuluje confidence score"""
        
        base_min, base_max = self.confidence_ranges.get(weather, (0.5, 0.8))
        
        # Wyższy confidence jeśli mamy wskazówki tekstowe
        if has_text_hint:
            confidence = random.uniform(base_max - 0.05, base_max)
        else:
            confidence = random.uniform(base_min, base_max - 0.1)
            
        return round(confidence, 3)
    
    def batch_classify(self, posts: List[Dict]) -> List[Dict]:
        """Klasyfikuje pogodę dla listy postów z social media"""
        
        results = []
        for post in posts:
            image_path = post.get('image_url', '')
            description = post.get('description', '')
            
            classification = self.classify_image(image_path, description)
            
            result = {
                "post_id": post.get('id'),
                "classification": classification,
                "original_post": post
            }
            results.append(result)
        
        return results
    
    def get_weather_summary(self, classifications: List[Dict]) -> Dict:
        """Tworzy podsumowanie pogody z analizowanych postów"""
        
        weather_counts = {}
        total_confidence = 0
        
        for item in classifications:
            weather = item['classification']['predicted_weather']
            confidence = item['classification']['confidence']
            
            if weather not in weather_counts:
                weather_counts[weather] = {'count': 0, 'total_confidence': 0}
            
            weather_counts[weather]['count'] += 1
            weather_counts[weather]['total_confidence'] += confidence
            total_confidence += confidence
        
        # Znajduje dominującą pogodę
        dominant_weather = max(weather_counts.items(), 
                              key=lambda x: x[1]['count'])[0]
        
        avg_confidence = total_confidence / len(classifications) if classifications else 0
        
        return {
            "dominant_weather": dominant_weather,
            "confidence": round(avg_confidence, 3),
            "weather_distribution": weather_counts,
            "total_posts_analyzed": len(classifications),
            "timestamp": datetime.now().isoformat()
        }

# Test function
def test_classifier():
    """Test weather classifier"""
    classifier = WeatherClassifier()
    
    print("🧠 Testing Weather Classifier...")
    
    # Test single image
    result = classifier.classify_image(
        "mock_images/sunny_event.jpg", 
        "Amazing weather at SHAMAN hackathon! ☀️"
    )
    print(f"Single image result: {result}")
    
    # Test batch classification
    from data.mock_instagram_posts import mock_posts
    mock_posts = [
        {
            "id": "test_1",
            "image_url": "sunny_event.jpg",
            "description": "Great sunny day! ☀️"
        },
        {
            "id": "test_2", 
            "image_url": "rainy_outside.jpg",
            "description": "It's raining cats and dogs! 🌧️"
        }
    ]
    
    batch_results = classifier.batch_classify(mock_posts)
    print(f"\nBatch results: {json.dumps(batch_results, indent=2)}")
    
    # Test summary
    summary = classifier.get_weather_summary(batch_results)
    print(f"\nWeather summary: {summary}")

if __name__ == "__main__":
    test_classifier() 