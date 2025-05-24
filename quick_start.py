#!/usr/bin/env python3
"""
WeatherEyes Quick Start
Łatwy sposób uruchomienia różnych trybów demo
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    print("""
🌤️ ╔══════════════════════════════════════════════════════════╗
   ║                    WEATHEREYES                          ║
   ║                  Event Edition                          ║
   ║                                                         ║
   ║            Dane pogodowe jako sojusznik człowieka       ║
   ║                  SHAMAN 2024                           ║
   ╚══════════════════════════════════════════════════════════╝
""")

def check_dependencies():
    """Sprawdza czy wszystkie dependencje są zainstalowane"""
    
    print("🔍 Sprawdzanie dependencji...")
    
    required_packages = [
        'streamlit', 'plotly', 'pandas', 'requests', 'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Brakujące pakiety: {', '.join(missing)}")
        print("💡 Uruchom: pip install -r requirements.txt")
        return False
    else:
        print("✅ Wszystkie dependencje zainstalowane!")
        return True

def run_terminal_demo():
    """Uruchamia demo w terminalu"""
    print("🚀 Uruchamianie terminal demo...")
    try:
        subprocess.run([sys.executable, "run_demo.py", "--full"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Błąd uruchomienia terminal demo")
    except FileNotFoundError:
        print("❌ Nie znaleziono pliku run_demo.py")

def run_interactive_demo():
    """Uruchamia interaktywne demo"""
    print("🎮 Uruchamianie interactive demo...")
    try:
        subprocess.run([sys.executable, "run_demo.py", "--interactive"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Błąd uruchomienia interactive demo")

def run_streamlit_dashboard():
    """Uruchamia Streamlit dashboard"""
    print("🌐 Uruchamianie Streamlit dashboard...")
    print("📱 Dashboard będzie dostępny na: http://localhost:8501")
    
    dashboard_path = Path("dashboard/streamlit_app.py")
    if not dashboard_path.exists():
        print("❌ Nie znaleziono pliku dashboard/streamlit_app.py")
        return
    
    try:
        subprocess.run([
            "streamlit", "run", str(dashboard_path),
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except subprocess.CalledProcessError:
        print("❌ Błąd uruchomienia Streamlit")
    except FileNotFoundError:
        print("❌ Streamlit nie jest zainstalowany")
        print("💡 Uruchom: pip install streamlit")

def test_individual_components():
    """Testuje poszczególne komponenty"""
    print("🧪 Testowanie komponentów...")
    
    components = [
        ("Weather API", "utils/weather_api.py"),
        ("AI Classifier", "ai_model/weather_classifier.py"),
        ("Alert System", "bot/alert_system.py")
    ]
    
    for name, path in components:
        print(f"\n🔧 Testowanie: {name}")
        if Path(path).exists():
            try:
                subprocess.run([sys.executable, path], check=True, timeout=30)
                print(f"✅ {name} - OK")
            except subprocess.CalledProcessError:
                print(f"❌ {name} - BŁĄD")
            except subprocess.TimeoutExpired:
                print(f"⏰ {name} - TIMEOUT")
        else:
            print(f"❌ {name} - PLIK NIE ISTNIEJE")

def setup_environment():
    """Konfiguruje środowisko"""
    print("⚙️ Konfiguracja środowiska...")
    
    config_file = Path("config.env.example")
    env_file = Path(".env")
    
    if config_file.exists() and not env_file.exists():
        print("📝 Kopiowanie pliku konfiguracyjnego...")
        try:
            env_file.write_text(config_file.read_text())
            print("✅ Plik .env utworzony z przykładowej konfiguracji")
            print("💡 Możesz edytować .env aby dodać swoje API keys")
        except Exception as e:
            print(f"❌ Błąd kopiowania konfiguracji: {e}")
    else:
        print("ℹ️ Plik .env już istnieje lub brak przykładowej konfiguracji")

def show_menu():
    """Pokazuje główne menu"""
    
    options = {
        "1": ("🚀 Terminal Demo (Full)", run_terminal_demo),
        "2": ("🎮 Interactive Demo", run_interactive_demo), 
        "3": ("🌐 Streamlit Dashboard", run_streamlit_dashboard),
        "4": ("🧪 Test Components", test_individual_components),
        "5": ("⚙️ Setup Environment", setup_environment),
        "6": ("🔍 Check Dependencies", lambda: check_dependencies()),
        "0": ("👋 Exit", lambda: sys.exit(0))
    }
    
    while True:
        print("\n" + "="*50)
        print("🎯 WYBIERZ OPCJĘ:")
        print("="*50)
        
        for key, (description, _) in options.items():
            print(f"{key}. {description}")
        
        print("="*50)
        choice = input("Twój wybór (0-6): ").strip()
        
        if choice in options:
            _, action = options[choice]
            print()
            action()
        else:
            print("❌ Nieprawidłowy wybór! Spróbuj ponownie.")

def main():
    """Główna funkcja"""
    
    print_banner()
    
    # Sprawdź czy jesteśmy w odpowiednim katalogu
    if not Path("run_demo.py").exists():
        print("❌ Uruchom ten skrypt z głównego katalogu projektu WeatherEyes!")
        sys.exit(1)
    
    # Sprawdź dependencje
    if not check_dependencies():
        print("\n💡 Zalecane kroki:")
        print("1. pip install -r requirements.txt")
        print("2. Uruchom ponownie ten skrypt")
        
        install_now = input("\n🤔 Zainstalować dependencje teraz? (y/n): ")
        if install_now.lower().startswith('y'):
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
                print("✅ Dependencje zainstalowane!")
            except subprocess.CalledProcessError:
                print("❌ Błąd instalacji dependencji")
                sys.exit(1)
        else:
            sys.exit(1)
    
    # Setup environment if needed
    if not Path(".env").exists():
        setup_environment()
    
    # Pokaż menu
    show_menu()

if __name__ == "__main__":
    main() 