"""
OpenAI Vision API Integration for WeatherEyes
Prawdziwa analiza pogody ze zdjęć używając GPT-4 Vision
"""

import os
import base64
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests
from pathlib import Path
from dotenv import load_dotenv
import random

load_dotenv()

class OpenAIVisionAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', 'demo_key')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Weather classification prompt
        self.weather_prompt = """
        Przeanalizuj to zdjęcie i określ warunki pogodowe. 
        
        BARDZO WAŻNE: Zwróć odpowiedź w formacie JSON z następującymi polami:
        {
            "weather_condition": "sunny|cloudy|rainy|snow|stormy|foggy|clear",
            "confidence": [LICZBA OD 0.0 DO 1.0 - jak bardzo jesteś pewny swojej oceny],
            "description": "Krótki opis warunków pogodowych w języku polskim",
            "details": {
                "sky_condition": "opis nieba",
                "visibility": "dobra|średnia|słaba",
                "precipitation": "brak|deszcz|śnieg|grad",
                "lighting": "jasno|pochmurno|ciemno"
            },
            "reasoning": "Dlaczego określiłeś takie warunki pogodowe i dlaczego taki confidence"
        }
        
        CONFIDENCE GUIDELINES:
        - 0.9-1.0: Bardzo wyraźne warunki pogodowe, dobre oświetlenie, czyste zdjęcie
        - 0.7-0.9: Jasne warunki pogodowe, dobre zdjęcie
        - 0.5-0.7: Średnio czytelne warunki, możliwe alternatywy
        - 0.3-0.5: Trudne do określenia, słabe oświetlenie/jakość
        - 0.0-0.3: Bardzo trudne lub niemożliwe do określenia
        
        Skoncentruj się na:
        - Stanie nieba (czyste, pochmurne, zachmurzone)
        - Opadach (deszcz, śnieg, ich intensywność)
        - Widoczności i oświetleniu
        - Ogólnych warunkach atmosferycznych
        
        MUSI ZWRÓCIĆ: poprawny JSON z confidence jako liczba (nie tekst)!
        """
    
    def encode_image(self, image_path: str) -> str:
        """Koduje zdjęcie do base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Błąd kodowania zdjęcia {image_path}: {e}")
            return None
    
    def analyze_image(self, image_path: str, additional_context: str = "") -> Dict:
        """
        Analizuje zdjęcie używając OpenAI Vision API
        """
        
        if self.api_key == 'demo_key':
            return self._get_demo_analysis(image_path)
        
        try:
            # Koduj zdjęcie
            base64_image = self.encode_image(image_path)
            if not base64_image:
                return self._get_error_response("Nie można załadować zdjęcia")
            
            # Przygotuj prompt z kontekstem
            full_prompt = self.weather_prompt
            if additional_context:
                full_prompt += f"\n\nDodatkowy kontekst: {additional_context}"
            
            # API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": full_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.1
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                weather_data = json.loads(content)
                
                # Walidacja i normalizacja confidence
                if 'confidence' in weather_data:
                    conf = weather_data['confidence']
                    # Upewnij się że confidence jest liczbą
                    if isinstance(conf, str):
                        # Spróbuj wyciągnąć liczbę z tekstu
                        import re
                        conf_match = re.search(r'(\d+\.?\d*)', conf)
                        if conf_match:
                            conf = float(conf_match.group(1))
                            # Jeśli > 1, prawdopodobnie procent (np. 85)
                            if conf > 1:
                                conf = conf / 100
                        else:
                            conf = 0.5  # Fallback
                    
                    # Ograniczyj do zakresu 0-1
                    weather_data['confidence'] = max(0.0, min(1.0, float(conf)))
                else:
                    # Jeśli brak confidence, ustaw bazując na jakości odpowiedzi
                    if weather_data.get('weather_condition') != 'unknown':
                        weather_data['confidence'] = 0.7  # Umiarkowany confidence
                    else:
                        weather_data['confidence'] = 0.3  # Niski confidence
                
                # Dodaj metadata
                weather_data['timestamp'] = datetime.now().isoformat()
                weather_data['source'] = 'openai_vision'
                weather_data['image_path'] = image_path
                weather_data['model'] = 'gpt-4o'
                weather_data['raw_response'] = content  # Zachowaj oryginalną odpowiedź
                
                print(f"✅ OpenAI Vision: {weather_data.get('weather_condition', 'unknown')} (confidence: {weather_data.get('confidence', 0):.2f})")
                
                return weather_data
                
            except json.JSONDecodeError:
                print(f"⚠️ OpenAI nie zwróciło JSON, parsuje tekst: {content[:100]}...")
                # Jeśli AI nie zwróciło JSON, spróbuj wyciągnąć informacje
                return self._extract_weather_from_text(content, image_path)
        
        except Exception as e:
            print(f"OpenAI Vision API Error: {e}")
            return self._get_error_response(str(e))
    
    def _extract_weather_from_text(self, text: str, image_path: str) -> Dict:
        """Wyciąga informacje o pogodzie z tekstu jeśli AI nie zwróciło JSON"""
        
        # Podstawowe mapowanie słów kluczowych
        weather_keywords = {
            'sunny': ['słonecznie', 'słońce', 'jasno', 'czyste niebo'],
            'cloudy': ['pochmurno', 'chmury', 'zachmurzone'],
            'rainy': ['deszcz', 'pada', 'mokro', 'deszczowo'],
            'snow': ['śnieg', 'śnieżnie', 'biało'],
            'stormy': ['burza', 'grzmoty', 'sztorm'],
            'clear': ['czysto', 'bezchmurnie', 'przejrzyste']
        }
        
        detected_weather = 'unknown'
        confidence = 0.5
        
        text_lower = text.lower()
        for weather, keywords in weather_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_weather = weather
                    confidence = 0.7
                    break
        
        return {
            "weather_condition": detected_weather,
            "confidence": confidence,
            "description": text[:200] + "..." if len(text) > 200 else text,
            "details": {
                "sky_condition": "nieznane",
                "visibility": "nieznana",
                "precipitation": "nieznane",
                "lighting": "nieznane"
            },
            "reasoning": "Analiza na podstawie tekstu z OpenAI",
            "timestamp": datetime.now().isoformat(),
            "source": "openai_vision_text",
            "image_path": image_path,
            "raw_response": text
        }
    
    def _get_demo_analysis(self, image_path: str) -> Dict:
        """Demo analiza gdy nie ma API key"""
        
        filename = Path(image_path).name.lower()
        
        # Bardziej realistyczne confidence dla demo
        # Inteligentne określanie pogody na podstawie nazwy pliku
        if any(word in filename for word in ['sunny', 'sun', 'bright', 'clear']):
            weather = 'sunny'
            conf = random.uniform(0.8, 0.95)  # Wysokie confidence dla jasnych warunków
        elif any(word in filename for word in ['cloud', 'overcast', 'grey']):
            weather = 'cloudy'
            conf = random.uniform(0.7, 0.9)   # Średnie-wysokie dla chmur
        elif any(word in filename for word in ['rain', 'wet', 'storm']):
            weather = 'rainy'
            conf = random.uniform(0.75, 0.92) # Wysokie dla deszczu (łatwo rozpoznać)
        elif any(word in filename for word in ['snow', 'winter']):
            weather = 'snow'
            conf = random.uniform(0.8, 0.95)  # Wysokie dla śniegu
        else:
            # Dla ogólnych zdjęć - symuluj trudność rozpoznania
            weather = 'cloudy'  # Domyślnie
            conf = random.uniform(0.5, 0.75)  # Średnie confidence
        
        print(f"🎭 Demo Mode: {weather} (confidence: {conf:.2f}) - based on filename")
        
        return {
            "weather_condition": weather,
            "confidence": round(conf, 3),  # Zaokrąglij do 3 miejsc po przecinku
            "description": f"Demo analiza - wykryto {weather} na podstawie nazwy pliku",
            "details": {
                "sky_condition": "symulacja",
                "visibility": "demo",
                "precipitation": "demo",
                "lighting": "demo"
            },
            "reasoning": f"Demo mode - analiza na podstawie nazwy pliku ({filename}), confidence: {conf:.2f}",
            "timestamp": datetime.now().isoformat(),
            "source": "demo_openai_vision",
            "image_path": image_path,
            "model": "demo"
        }
    
    def _get_error_response(self, error_msg: str) -> Dict:
        """Zwraca standardową odpowiedź błędu"""
        return {
            "weather_condition": "unknown",
            "confidence": 0.0,
            "description": f"Błąd analizy: {error_msg}",
            "details": {
                "sky_condition": "błąd",
                "visibility": "błąd",
                "precipitation": "błąd",
                "lighting": "błąd"
            },
            "reasoning": "Wystąpił błąd podczas analizy",
            "timestamp": datetime.now().isoformat(),
            "source": "error",
            "error": error_msg
        }
    
    def batch_analyze_images(self, image_paths: List[str], context: str = "") -> List[Dict]:
        """Analizuje listę zdjęć"""
        
        results = []
        for i, image_path in enumerate(image_paths):
            print(f"🔍 Analizuję zdjęcie {i+1}/{len(image_paths)}: {Path(image_path).name}")
            
            analysis = self.analyze_image(image_path, context)
            results.append(analysis)
            
            # Dodaj małą pauzę żeby nie przeciążyć API
            if self.api_key != 'demo_key':
                import time
                time.sleep(1)
        
        return results
    
    def get_weather_summary_from_images(self, analyses: List[Dict]) -> Dict:
        """Tworzy podsumowanie pogody z analizowanych zdjęć"""
        
        if not analyses:
            return {"error": "Brak analiz do podsumowania"}
        
        # Zlicz warunki pogodowe
        weather_counts = {}
        total_confidence = 0
        valid_analyses = []
        
        for analysis in analyses:
            if analysis.get('weather_condition') and analysis.get('weather_condition') != 'unknown':
                weather = analysis['weather_condition']
                confidence = analysis.get('confidence', 0)
                
                if weather not in weather_counts:
                    weather_counts[weather] = {'count': 0, 'total_confidence': 0, 'images': []}
                
                weather_counts[weather]['count'] += 1
                weather_counts[weather]['total_confidence'] += confidence
                weather_counts[weather]['images'].append(analysis.get('image_path', ''))
                
                total_confidence += confidence
                valid_analyses.append(analysis)
        
        if not weather_counts:
            return {"error": "Nie można określić warunków pogodowych"}
        
        # Znajdź dominującą pogodę
        dominant_weather = max(weather_counts.items(), key=lambda x: x[1]['count'])[0]
        avg_confidence = total_confidence / len(valid_analyses)
        
        return {
            "dominant_weather": dominant_weather,
            "confidence": round(avg_confidence, 3),
            "weather_distribution": weather_counts,
            "total_images_analyzed": len(analyses),
            "valid_analyses": len(valid_analyses),
            "timestamp": datetime.now().isoformat(),
            "summary": f"Na podstawie {len(valid_analyses)} zdjęć dominują warunki: {dominant_weather}"
        }

# Test function
def test_openai_vision():
    """Test OpenAI Vision analyzer"""
    
    analyzer = OpenAIVisionAnalyzer()
    
    print("🔍 Testing OpenAI Vision Analyzer...")
    
    # Test z przykładowym zdjęciem (jeśli istnieje)
    test_image = "data/test_weather_image.jpg"
    
    if Path(test_image).exists():
        print(f"📸 Analizuję zdjęcie: {test_image}")
        result = analyzer.analyze_image(test_image, "Zdjęcie z wydarzenia SHAMAN 2024")
        print(f"✅ Wynik: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("⚠️ Brak testowego zdjęcia, używam demo mode")
        result = analyzer._get_demo_analysis("demo_sunny_weather.jpg")
        print(f"📊 Demo wynik: {json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_openai_vision() 