# 🌤️ WeatherEyes - REAL DEMO EDITION
## SHAMAN 2024 - "Dane pogodowe jako sojusznik człowieka"

> **Prawdziwy system analizy pogody z social media + AI + alerty komunikatorów**

---

## 🚀 QUICK START - PRAWDZIWE DEMO

### 1. Przygotowanie środowiska
```bash
# Klonuj/pobierz projekt
cd WetEyes

# Aktywuj virtual environment (jeśli nie jest aktywny)
source venv/bin/activate  # macOS/Linux
# lub: venv\Scripts\activate  # Windows

# Zainstaluj nowe zależności
pip install openai twilio pillow
```

### 2. Konfiguracja API Keys (OPCJONALNE ale zalecane)

**Skopiuj i skonfiguruj plik .env:**
```bash
cp config.env.example .env
nano .env  # lub edytuj w VS Code
```

**Dodaj swoje API keys:**

#### 🤖 OpenAI Vision API (do analizy zdjęć)
1. Idź na https://platform.openai.com/api-keys
2. Stwórz nowy API key
3. Dodaj do .env: `OPENAI_API_KEY=sk-your-key-here`

#### 📱 Telegram Bot (do alertów)
1. Napisz do @BotFather na Telegram
2. Użyj `/newbot` i stwórz bota
3. Skopiuj token do .env: `TELEGRAM_BOT_TOKEN=your-token`
4. Napisz wiadomość do swojego bota
5. Otwórz: `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Znajdź chat_id i dodaj: `TELEGRAM_CHAT_ID=your-chat-id`

#### 📞 Twilio SMS (do SMS-ów)
1. Zarejestruj się na https://console.twilio.com/
2. Pobierz Account SID i Auth Token
3. Dodaj do .env numery telefonów

### 3. Dodaj swoje zdjęcia z wydarzenia

**GUI Upload (najłatwiejsze):**
```bash
python upload_event_images.py
```

**Lub ręcznie:**
```bash
mkdir -p data/event_images
# Skopiuj swoje screenshoty do folderu data/event_images/
```

### 4. Uruchom prawdziwe demo

**Interaktywny tryb (zalecany):**
```bash
python run_real_demo.py
```

**Automatyczny tryb (do prezentacji):**
```bash
python run_real_demo.py --mode auto
```

---

## 🎯 CO ROBI PRAWDZIWY SYSTEM

### 1. 📸 Analiza Prawdziwych Zdjęć
- **Input:** Twoje screenshoty z wydarzenia SHAMAN
- **AI:** OpenAI GPT-4 Vision analizuje warunki pogodowe
- **Output:** Szczegółowa analiza + poziom pewności

### 2. 🚨 Prawdziwe Alerty
- **Telegram:** Wysyła zdjęcia z analizą na Twój telefon
- **SMS:** Krótkie powiadomienia przez Twilio
- **Typy alertów:**
  - Analiza pojedynczego zdjęcia
  - Podsumowanie wydarzenia  
  - Wykrycie zmiany pogody

### 3. 📊 Live Dashboard
```bash
streamlit run dashboard/streamlit_app.py
```

---

## 🛠️ SYSTEM ARCHITECTURE

```
📸 Zdjęcia z wydarzenia
    ↓
🤖 OpenAI Vision API (analiza AI)
    ↓  
📊 Agregacja + podsumowanie
    ↓
🚨 System alertów:
   • 📱 Telegram Bot
   • 📞 SMS (Twilio)
```

---

## 📋 FUNKCJE DEMO

### ✅ Już działa:
- [x] Upload zdjęć z wydarzenia (GUI)
- [x] OpenAI Vision API analiza
- [x] Telegram Bot z załącznikami
- [x] SMS przez Twilio
- [x] Różne typy alertów
- [x] Live dashboard
- [x] Demo mode (bez API keys)

### 🎯 Wartość dla SHAMAN 2024:
- **Innowacyjność:** Social media jako sensory pogodowe
- **AI:** Prawdziwa analiza obrazów
- **Praktyczność:** Rzeczywiste alerty na telefon
- **Skalowalnośćć:** Gotowe do rozszerzenia

---

## 🎮 OPCJE URUCHOMIENIA

### Interaktywny menu:
```bash
python run_real_demo.py

# Wybierz:
# 1. 📸 Dodaj zdjęcia z wydarzenia (GUI)
# 2. 🔍 Analizuj istniejące zdjęcia  
# 3. 🚨 Wyślij alerty
# 4. 📊 Pełne demo (analiza + alerty)
# 5. ⚙️ Sprawdź konfigurację API
```

### Szybkie komendy:
```bash
# Upload zdjęć
python run_real_demo.py --upload

# Auto demo (do prezentacji)
python run_real_demo.py --mode auto

# Dashboard
streamlit run dashboard/streamlit_app.py

# Test alertów
python bot/real_alerts.py

# Test OpenAI Vision
python ai_model/openai_vision.py
```

---

## 🔧 TROUBLESHOOTING

### Problem: Brak GUI na macOS
```bash
pip install tk
# lub użyj: python run_real_demo.py --mode auto
```

### Problem: OpenAI API error
- Sprawdź API key w .env
- Sprawdź saldo na koncie OpenAI
- System automatycznie przełączy się na demo mode

### Problem: Telegram nie działa
- Sprawdź token bota
- Sprawdź chat_id
- Napisz wiadomość do bota najpierw

### Problem: SMS nie działa
- Sprawdź konfigurację Twilio
- Sprawdź numery telefonów (format +48...)

---

## 📱 PRZYKŁAD ALERTU

**Telegram:**
```
🔍 Analiza Zdjęcia WeatherEyes

📸 Zdjęcie: event_20241124_143022_001.jpg
🌤️ Wykryta pogoda: cloudy
📊 Pewność: 87.3%

💭 Opis:
Na zdjęciu widać pochmurne niebo przez okna sali konferencyjnej podczas wydarzenia SHAMAN 2024...

🕐 Czas analizy: 14:30, 24.11.2024
📱 WeatherEyes - SHAMAN 2024
```

**SMS:**
```
🔍 WeatherEyes: Wykryto cloudy na zdjęciu event_20241124_143022_001.jpg (87.3% pewności)
```

---

## 🏆 DEMO DLA JURY

1. **Pokaż upload zdjęć** - `python upload_event_images.py`
2. **Uruchom analizę AI** - `python run_real_demo.py`
3. **Wyślij prawdziwe alerty** - sprawdź telefon na żywo!
4. **Dashboard** - `streamlit run dashboard/streamlit_app.py`

**Kluczowa wartość:** To nie jest symulacja - to działa naprawdę! 📱✅

---

## 📞 SUPPORT

**W razie problemów podczas prezentacji:**
1. Użyj demo mode: wszystko działa bez API keys
2. Uruchom: `python run_demo.py --full` (stary system)  
3. Albo: `python quick_start.py` (menu z opcjami)

**System jest zabezpieczony - zawsze coś zadziała!** 🛡️ 