"""
WeatherEyes REAL DEMO - SHAMAN 2024
Kompletny demo z prawdziwymi API i alertami
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Add project to path
sys.path.append(str(Path(__file__).parent))

from ai_model.openai_vision import OpenAIVisionAnalyzer
from bot.real_alerts import RealAlertSystem
from utils.weather_api import WeatherAPI

def print_banner():
    """Wyświetla banner aplikacji"""
    print("\n" + "="*60)
    print("🌤️  WEATHEREYES - REAL DEMO")
    print("   SHAMAN 2024 - Dane pogodowe jako sojusznik człowieka")
    print("="*60)
    print("🤖 OpenAI Vision API - Prawdziwa analiza zdjęć")
    print("📱 Telegram & SMS - Prawdziwe alerty")
    print("🔍 Social Media as Weather Sensors")
    print("="*60 + "\n")

def check_api_keys():
    """Sprawdza czy API keys są skonfigurowane"""
    
    print("🔑 Sprawdzam konfigurację API...")
    
    openai_key = os.getenv('OPENAI_API_KEY', 'demo_key')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', 'demo_token')
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', 'demo_sid')
    
    config_status = {
        'openai': openai_key != 'demo_key',
        'telegram': telegram_token != 'demo_token',
        'twilio': twilio_sid != 'demo_sid'
    }
    
    print(f"  OpenAI Vision API: {'✅ Skonfigurowane' if config_status['openai'] else '⚠️  Demo mode'}")
    print(f"  Telegram Bot: {'✅ Skonfigurowane' if config_status['telegram'] else '⚠️  Demo mode'}")
    print(f"  Twilio SMS: {'✅ Skonfigurowane' if config_status['twilio'] else '⚠️  Demo mode'}")
    
    if not any(config_status.values()):
        print("\n🔧 Aby użyć prawdziwych API, skonfiguruj zmienne w pliku .env:")
        print("   OPENAI_API_KEY=your_openai_key")
        print("   TELEGRAM_BOT_TOKEN=your_bot_token")
        print("   TELEGRAM_CHAT_ID=your_chat_id")
        print("   TWILIO_ACCOUNT_SID=your_sid")
        print("   TWILIO_AUTH_TOKEN=your_token")
        print("   TWILIO_FROM_NUMBER=+1234567890")
        print("   TWILIO_TO_NUMBER=+1987654321")
        print("\n📱 Teraz używam demo mode dla prezentacji.")
    
    return config_status

def find_event_images() -> List[str]:
    """Znajduje zdjęcia z wydarzenia"""
    
    event_dir = Path("data/event_images")
    if not event_dir.exists():
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    images = []
    
    for file_path in event_dir.iterdir():
        if file_path.suffix.lower() in image_extensions:
            images.append(str(file_path))
    
    return sorted(images)

def analyze_event_images() -> Dict:
    """Analizuje wszystkie zdjęcia z wydarzenia"""
    
    print("📸 Szukam zdjęć z wydarzenia...")
    
    # Find event images
    event_images = find_event_images()
    
    if not event_images:
        print("⚠️  Brak zdjęć z wydarzenia!")
        print("💡 Uruchom: python upload_event_images.py żeby dodać zdjęcia")
        return None
    
    print(f"🔍 Znaleziono {len(event_images)} zdjęć z wydarzenia")
    for img in event_images:
        print(f"   • {Path(img).name}")
    
    # Initialize analyzer
    print("\n🤖 Inicjalizuję OpenAI Vision Analyzer...")
    analyzer = OpenAIVisionAnalyzer()
    
    # Analyze images
    print("🔍 Analizuję zdjęcia z wydarzenia SHAMAN 2024...")
    context = "Zdjęcia z wydarzenia SHAMAN 2024 - hackathon technologiczny w Polsce"
    
    analyses = analyzer.batch_analyze_images(event_images, context)
    
    # Get summary
    summary = analyzer.get_weather_summary_from_images(analyses)
    
    return {
        'images': event_images,
        'analyses': analyses,
        'summary': summary
    }

def display_analysis_results(results: Dict):
    """Wyświetla wyniki analizy"""
    
    if not results:
        return
    
    analyses = results['analyses']
    summary = results['summary']
    
    print("\n" + "="*60)
    print("📊 WYNIKI ANALIZY AI")
    print("="*60)
    
    # Individual results
    for i, analysis in enumerate(analyses, 1):
        image_name = Path(analysis.get('image_path', '')).name
        weather = analysis.get('weather_condition', 'unknown')
        confidence = analysis.get('confidence', 0)
        description = analysis.get('description', 'Brak opisu')
        
        print(f"\n[{i}] {image_name}")
        print(f"    🌤️  Pogoda: {weather}")
        print(f"    📊 Pewność: {confidence:.1%}")
        print(f"    📝 Opis: {description[:100]}...")
        
        if analysis.get('reasoning'):
            print(f"    🤔 Uzasadnienie: {analysis['reasoning'][:100]}...")
    
    # Summary
    if 'error' not in summary:
        print("\n" + "="*60)
        print("📈 PODSUMOWANIE")
        print("="*60)
        print(f"🌤️  Dominująca pogoda: {summary['dominant_weather']}")
        print(f"📊 Średnia pewność: {summary['confidence']:.1%}")
        print(f"📸 Przeanalizowane zdjęcia: {summary['valid_analyses']}/{summary['total_images_analyzed']}")
        
        print(f"\n📈 Rozkład warunków pogodowych:")
        for weather, info in summary.get('weather_distribution', {}).items():
            avg_conf = info['total_confidence'] / info['count']
            print(f"   • {weather}: {info['count']} zdjęć ({avg_conf:.1%} śr. pewność)")

def send_real_alerts(results: Dict) -> Dict:
    """Wysyła prawdziwe alerty na podstawie analizy"""
    
    if not results:
        return {'error': 'Brak wyników do wysłania'}
    
    print("\n" + "="*60)
    print("🚨 WYSYŁANIE PRAWDZIWYCH ALERTÓW")
    print("="*60)
    
    # Initialize alert system
    alert_system = RealAlertSystem()
    analyses = results['analyses']
    summary = results['summary']
    
    sent_alerts = []
    
    # Send individual image analysis alerts
    print("📸 Wysyłam alerty dla każdego zdjęcia...")
    for i, analysis in enumerate(analyses, 1):
        if analysis.get('weather_condition') != 'unknown':
            print(f"   [{i}] Wysyłam alert dla {Path(analysis['image_path']).name}...")
            
            alert_result = alert_system.send_image_analysis_alert(
                analysis['image_path'], analysis
            )
            sent_alerts.append(alert_result)
            
            # Show status
            telegram_ok = alert_result['results']['telegram']['success']
            sms_ok = alert_result['results']['sms']['success']
            print(f"        Telegram: {'✅' if telegram_ok else '❌'}")
            print(f"        SMS: {'✅' if sms_ok else '❌'}")
    
    # Send summary alert
    if 'error' not in summary:
        print(f"\n📊 Wysyłam podsumowanie wydarzenia...")
        summary_alert = alert_system.send_daily_summary_alert(
            summary, "SHAMAN 2024 Event"
        )
        sent_alerts.append(summary_alert)
        
        telegram_ok = summary_alert['results']['telegram']['success']
        sms_ok = summary_alert['results']['sms']['success']
        print(f"     Telegram: {'✅' if telegram_ok else '❌'}")
        print(f"     SMS: {'✅' if sms_ok else '❌'}")
    
    # Send weather change alert (if conditions changed)
    if len(analyses) >= 2:
        first_weather = analyses[0].get('weather_condition')
        last_weather = analyses[-1].get('weather_condition')
        
        if first_weather != last_weather and first_weather != 'unknown' and last_weather != 'unknown':
            print(f"\n🔄 Wykryto zmianę pogody: {first_weather} → {last_weather}")
            change_alert = alert_system.send_weather_change_alert(
                first_weather, last_weather, 0.85, "SHAMAN 2024 Event"
            )
            sent_alerts.append(change_alert)
            
            telegram_ok = change_alert['results']['telegram']['success']
            sms_ok = change_alert['results']['sms']['success']
            print(f"     Telegram: {'✅' if telegram_ok else '❌'}")
            print(f"     SMS: {'✅' if sms_ok else '❌'}")
    
    # Statistics
    stats = alert_system.get_alert_stats()
    
    print("\n" + "="*60)
    print("📊 STATYSTYKI ALERTÓW")
    print("="*60)
    print(f"🚨 Łączna liczba alertów: {stats['total_alerts']}")
    print(f"📱 Telegram sukces: {stats['successful_telegram']}/{stats['total_alerts']} ({stats['success_rate_telegram']:.1%})")
    print(f"📞 SMS sukces: {stats['successful_sms']}/{stats['total_alerts']} ({stats['success_rate_sms']:.1%})")
    
    print(f"\n📈 Alerty według typu:")
    for alert_type, count in stats.get('by_type', {}).items():
        print(f"   • {alert_type.replace('_', ' ').title()}: {count}")
    
    return {
        'sent_alerts': sent_alerts,
        'stats': stats
    }

def interactive_mode():
    """Tryb interaktywny"""
    
    print("\n🎮 TRYB INTERAKTYWNY")
    print("=" * 30)
    
    while True:
        print("\n🌤️ WeatherEyes - Wybierz opcję:")
        print("1. 📸 Dodaj zdjęcia z wydarzenia (GUI)")
        print("2. 🔍 Analizuj istniejące zdjęcia")
        print("3. 🚨 Wyślij alerty")
        print("4. 📊 Pełne demo (analiza + alerty)")
        print("5. ⚙️  Sprawdź konfigurację API")
        print("6. 🚪 Wyjście")
        
        choice = input("\n👉 Twój wybór (1-6): ").strip()
        
        if choice == '1':
            print("\n🚀 Uruchamiam interfejs do dodawania zdjęć...")
            try:
                from upload_event_images import main as upload_main
                upload_main()
            except Exception as e:
                print(f"❌ Błąd uruchomienia GUI: {e}")
                print("💡 Spróbuj: python upload_event_images.py")
        
        elif choice == '2':
            results = analyze_event_images()
            if results:
                display_analysis_results(results)
        
        elif choice == '3':
            results = analyze_event_images()
            if results:
                send_real_alerts(results)
        
        elif choice == '4':
            results = analyze_event_images()
            if results:
                display_analysis_results(results)
                input("\n⏸️  Naciśnij Enter aby wysłać alerty...")
                send_real_alerts(results)
        
        elif choice == '5':
            check_api_keys()
        
        elif choice == '6':
            print("\n👋 Do widzenia! Dziękuję za używanie WeatherEyes!")
            break
        
        else:
            print("❌ Nieprawidłowy wybór. Spróbuj ponownie.")

def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description="WeatherEyes Real Demo - SHAMAN 2024")
    parser.add_argument('--mode', choices=['auto', 'interactive'], default='interactive',
                       help="Tryb uruchomienia (auto/interactive)")
    parser.add_argument('--upload', action='store_true',
                       help="Uruchom interfejs uploadu zdjęć")
    
    args = parser.parse_args()
    
    print_banner()
    config = check_api_keys()
    
    if args.upload:
        print("\n🚀 Uruchamiam interfejs do dodawania zdjęć...")
        try:
            from upload_event_images import main as upload_main
            upload_main()
        except Exception as e:
            print(f"❌ Błąd uruchomienia GUI: {e}")
        return
    
    if args.mode == 'auto':
        print("\n🤖 TRYB AUTOMATYCZNY - Pełne demo")
        print("=" * 40)
        
        # Analyze images
        results = analyze_event_images()
        if not results:
            print("❌ Brak zdjęć do analizy. Zakończenie.")
            return
        
        # Display results
        display_analysis_results(results)
        
        # Send alerts
        print(f"\n⏳ Za 3 sekundy wysyłam prawdziwe alerty...")
        import time
        time.sleep(3)
        
        alert_results = send_real_alerts(results)
        
        print("\n✅ Demo zakończone!")
        print("📱 Sprawdź swój telefon/Telegram aby zobaczyć alerty!")
    
    else:
        interactive_mode()

if __name__ == "__main__":
    main() 