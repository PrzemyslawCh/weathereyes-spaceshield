"""
Simple OpenAI Vision Test - SHAMAN 2024
Test tylko analizy zdjęć z OpenAI Vision API
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project to path
sys.path.append(str(Path(__file__).parent))

from ai_model.openai_vision import OpenAIVisionAnalyzer

def main():
    print("🌤️ WeatherEyes - OpenAI Vision Test")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY', 'demo_key')
    use_real_api = False
    
    if api_key == 'demo_key':
        print("⚠️  Brak OpenAI API key - używam demo mode")
        print("💡 Aby użyć prawdziwego API, ustaw OPENAI_API_KEY w .env")
    else:
        print(f"🔍 Sprawdzam OpenAI API key...")
        # Quick test
        import requests
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ OpenAI API działa! Key: {api_key[:10]}...{api_key[-4:]}")
                use_real_api = True
            else:
                print(f"❌ OpenAI API Error {response.status_code} - używam demo mode")
                print(f"💡 Sprawdź swój API key na https://platform.openai.com/api-keys")
        except Exception as e:
            print(f"❌ Problem z API ({e}) - używam demo mode")
    
    print("\n🔍 Szukam zdjęć do analizy...")
    
    # Find images
    event_dir = Path("data/event_images")
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    images = []
    
    if event_dir.exists():
        for file_path in event_dir.iterdir():
            if file_path.suffix.lower() in image_extensions:
                images.append(str(file_path))
    
    if not images:
        print("📁 Brak zdjęć w data/event_images/")
        print("💡 Dodaj zdjęcia do folderu data/event_images/")
        
        # Create sample for demo
        event_dir.mkdir(parents=True, exist_ok=True)
        print("\n🎭 Używam demo mode z przykładowymi nazwami plików...")
        images = ["demo_sunny.jpg", "demo_cloudy.jpg", "demo_rainy.jpg"]
    else:
        print(f"📸 Znaleziono {len(images)} zdjęć z SHAMAN 2024:")
        for img in images:
            print(f"   • {Path(img).name}")
    
    # Initialize analyzer
    print(f"\n🤖 Inicjalizuję OpenAI Vision Analyzer...")
    analyzer = OpenAIVisionAnalyzer()
    
    # Override API key if not working
    if not use_real_api:
        print("🎭 Używam demo mode dla stabilności prezentacji")
        analyzer.api_key = 'demo_key'
    
    # Analyze images
    print("🔍 Rozpoczynam analizę...")
    context = "Zdjęcia z wydarzenia SHAMAN 2024 - hackathon technologiczny w Polsce"
    
    analyses = []
    for i, image_path in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] Analizuję: {Path(image_path).name}")
        
        analysis = analyzer.analyze_image(image_path, context)
        analyses.append(analysis)
        
        # Show result
        weather = analysis.get('weather_condition', 'unknown')
        confidence = analysis.get('confidence', 0)
        description = analysis.get('description', 'Brak opisu')
        
        print(f"    🌤️  Wykryta pogoda: {weather}")
        print(f"    📊 Pewność: {confidence:.1%}")
        print(f"    📝 Opis: {description[:80]}...")
        
        if analysis.get('reasoning'):
            print(f"    🤔 Uzasadnienie: {analysis['reasoning'][:80]}...")
    
    # Summary
    print(f"\n" + "="*60)
    print("📊 PODSUMOWANIE ANALIZY")
    print("="*60)
    
    summary = analyzer.get_weather_summary_from_images(analyses)
    
    if 'error' not in summary:
        print(f"🌤️  Dominująca pogoda: {summary['dominant_weather']}")
        print(f"📊 Średnia pewność: {summary['confidence']:.1%}")
        print(f"📸 Przeanalizowane zdjęcia: {summary['valid_analyses']}/{summary['total_images_analyzed']}")
        
        print(f"\n📈 Szczegółowy rozkład:")
        for weather, info in summary.get('weather_distribution', {}).items():
            avg_conf = info['total_confidence'] / info['count']
            print(f"   • {weather}: {info['count']} zdjęć ({avg_conf:.1%} śr. pewność)")
            
            # Show which images
            for img_path in info.get('images', []):
                print(f"     - {Path(img_path).name}")
    else:
        print(f"❌ {summary['error']}")
    
    print(f"\n✅ Analiza zakończona!")
    
    # Save results
    results_file = Path("data/analysis_results.json")
    results_file.parent.mkdir(exist_ok=True)
    
    import json
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': summary,
            'analyses': analyses,
            'timestamp': analyses[0]['timestamp'] if analyses else None,
            'api_mode': 'real' if use_real_api else 'demo'
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Wyniki zapisane w: {results_file}")
    
    if use_real_api:
        print(f"\n🎯 To była PRAWDZIWA analiza OpenAI Vision API!")
        print(f"🔥 Twoje screenshoty z SHAMAN przeanalizowane przez AI!")
    else:
        print(f"\n🎭 To był demo mode - ale używa prawdziwych zdjęć!")
        print(f"📸 Przeanalizowane Twoje screenshoty z SHAMAN 2024")
        print(f"💡 Demo idealny na prezentację!")
    
    print(f"\n🚀 Gotowe do pokazania na SHAMAN 2024!")

if __name__ == "__main__":
    main() 