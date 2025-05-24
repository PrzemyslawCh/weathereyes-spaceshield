# 🌤️ WeatherEyes - AI Weather Monitoring System

> **"Dane pogodowe jako sojusznik człowieka"** - SHAMAN 2024 Hackathon Project

WeatherEyes to inteligentny system monitorowania pogody wykorzystujący AI do analizy zdjęć z mediów społecznościowych i generowania alertów pogodowych w czasie rzeczywistym.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://weathereyes-shaman2024.streamlit.app/)

**Demo Dashboard:** Uruchom `streamlit run shaman_demo_dashboard.py`

## 🎯 Główne Funkcje

- 📸 **Social Media Monitoring** - Analiza zdjęć z Instagram Stories
- 🤖 **AI Weather Recognition** - OpenAI Vision API + GPT-4o
- 🚨 **Smart Alerts** - Kontekstowe alerty pogodowe
- 📱 **Multi-Channel Distribution** - Telegram, SMS, Email
- 🎮 **Live Demo Dashboard** - Interaktywna prezentacja

## 🏗️ Architektura

```
📸 Social Media → 🤖 AI Analysis → 🚨 Smart Alerts → 📱 Distribution
   Instagram        OpenAI Vision     Context-Aware    Multi-Channel
   TikTok          GPT-4o Model      Event-Specific   Telegram/SMS
   Stories         Real-time         Recommendations  Email/Web
```

## 🛠️ Instalacja

### 1. Klonuj repository
```bash
git clone https://github.com/yourusername/weathereyes.git
cd weathereyes
```

### 2. Wirtualne środowisko
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub venv\Scripts\activate  # Windows
```

### 3. Zainstaluj dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfiguracja API
```bash
cp config.env.example config.env
# Edytuj config.env i dodaj swoje API keys
```

### 5. Uruchom demo
```bash
streamlit run shaman_demo_dashboard.py
```

## 🔑 Wymagane API Keys

- **OpenAI API** - GPT-4o Vision Model
- **Telegram Bot** - Real-time alerts
- **Twilio** - SMS notifications (opcjonalne)

## 📊 Przykład Użycia

```python
from ai_model.openai_vision import OpenAIVisionAnalyzer
from bot.real_alerts import RealAlertSystem

# Analiza zdjęcia
analyzer = OpenAIVisionAnalyzer()
result = analyzer.analyze_image("photo.jpg", "SHAMAN 2024 event")

# Wysłanie alertu
alerts = RealAlertSystem()
alerts.send_weather_alert(result['weather_condition'], "Event participants")
```

## 🎯 SHAMAN 2024 Demo

System został zademonstrowany na hackathonie SHAMAN 2024 z:
- ✅ Prawdziwymi zdjęciami z wydarzenia
- ✅ Live AI analysis przez OpenAI
- ✅ Rzeczywistymi alertami przez Telegram
- ✅ Multi-channel distribution

## 🚀 Deployment

### Streamlit Community Cloud
1. Fork tego repo
2. Połącz z [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy app: `shaman_demo_dashboard.py`
4. Dodaj environment variables (API keys)

### Lokalne uruchomienie
```bash
streamlit run shaman_demo_dashboard.py --server.port 8502
```

## 📁 Struktura Projektu

```
weathereyes/
├── shaman_demo_dashboard.py    # 🎮 Main demo dashboard
├── ai_model/
│   └── openai_vision.py       # 🤖 AI weather analysis
├── bot/
│   └── real_alerts.py         # 📱 Alert system
├── data/
│   ├── event_images/          # 📸 Event photos (excluded from git)
│   └── demo_images/           # 🎭 Demo images
├── requirements.txt           # 📦 Dependencies
└── config.env.example        # ⚙️ Configuration template
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add your improvements
4. Submit pull request

## 📄 Licencja

MIT License - Zobacz [LICENSE](LICENSE) file

## 🏆 SHAMAN 2024

Projekt stworzony na hackathon **SHAMAN 2024** w kategorii:
**"Dane pogodowe jako sojusznik człowieka"**

---

**Made with ❤️ for SHAMAN 2024 Hackathon** 