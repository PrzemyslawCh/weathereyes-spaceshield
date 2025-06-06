# WeatherEyes Project Documentation

## 🌤️ Overview

WeatherEyes is an AI-powered weather monitoring system that analyzes images from social media to generate real-time weather alerts. This project was created for the SpaceShield Hackathon in the "Weather data as a human ally" category.

## 🏗️ Project Structure

The project has been cleaned and optimized to include only working components:

```
weathereyes/
├── spaceshield_demo_dashboard.py    # Main demo dashboard (entry point)
├── ai_model/
│   ├── __init__.py                  # Package initialization
│   └── openai_vision.py             # OpenAI Vision API integration for weather analysis
├── bot/
│   ├── __init__.py                  # Package initialization  
│   └── real_alerts.py               # Alert system for multi-channel notifications
├── data/
│   ├── demo_images/                 # Folder for demo images
│   │   └── README.md                # Instructions for adding demo images
│   └── event_images/                # Folder for real event images (priority)
│       └── README.md                # Instructions for adding event images
├── config.env.example               # Template for API configuration
├── requirements.txt                 # Project dependencies
├── README.md                        # Project overview
├── PROJECT_DOCUMENTATION.md         # This file - detailed documentation
└── .gitignore                       # Git configuration
```

## 🚀 How It Works

### 1. **Main Application** (`spaceshield_demo_dashboard.py`)
- Streamlit-based web dashboard
- Orchestrates the entire weather analysis workflow
- Provides interactive demo interface
- Shows real-time analysis results

### 2. **AI Analysis** (`ai_model/openai_vision.py`)
- Integrates with OpenAI Vision API (GPT-4o)
- Analyzes images to detect weather conditions
- Provides confidence scores for weather detection
- Generates weather summaries from multiple images

### 3. **Alert System** (`bot/real_alerts.py`)
- Generates contextual weather alerts
- Supports multiple distribution channels:
  - Telegram Bot notifications
  - SMS alerts (via Twilio)
  - Email notifications
  - Web dashboard updates

## 📦 Dependencies

The project uses minimal dependencies for optimal performance:

- **streamlit**: Web dashboard framework
- **openai**: AI vision analysis
- **python-dotenv**: Environment configuration
- **requests**: HTTP requests
- **Pillow**: Image processing
- **python-telegram-bot**: Telegram notifications (optional)
- **twilio**: SMS notifications (optional)

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd weathereyes
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
cp config.env.example config.env
# Edit config.env and add your API keys:
# - OPENAI_API_KEY
# - TELEGRAM_BOT_TOKEN (optional)
# - TWILIO_ACCOUNT_SID (optional)
# - TWILIO_AUTH_TOKEN (optional)
```

### 5. Add Demo Images
Place image files (JPG, PNG) in the `data/demo_images/` folder for the demo to analyze.

### 6. Run the Application
```bash
streamlit run spaceshield_demo_dashboard.py
```

## 🎮 Using the Demo

1. **Launch the Dashboard**: Run the Streamlit app
2. **Click "START LIVE DEMO"**: Initiates the analysis workflow
3. **Watch the Process**:
   - Step 1: Collects images from the demo folder
   - Step 2: AI analyzes weather conditions
   - Step 3: Generates smart alerts
   - Step 4: Distributes across channels
4. **View Results**: See weather analysis, confidence scores, and generated alerts

## 🔑 Key Features

- **Real-time Analysis**: Processes images instantly using AI
- **High Accuracy**: OpenAI Vision provides accurate weather detection
- **Smart Alerts**: Context-aware notifications based on conditions
- **Multi-channel**: Supports various notification methods
- **Event-specific**: Tailored alerts for specific events/locations

## 📊 API Modes

The system can operate in two modes:

1. **Live Mode**: Uses real OpenAI API for actual analysis
2. **Demo Mode**: Simulates analysis when API key is not provided

## 🛠️ Extending the Project

To add new features:

1. **New Weather Conditions**: Modify `openai_vision.py` to detect additional weather types
2. **New Alert Channels**: Add distribution methods in `real_alerts.py`
3. **Custom UI**: Modify `spaceshield_demo_dashboard.py` for new interface elements

## 🤝 Contributing

1. Keep code clean and well-documented
2. Test changes before committing
3. Follow existing code structure
4. Update documentation for new features

## 📝 Notes

- The project is optimized for demonstration purposes
- Ensure you have valid API keys for full functionality
- Add actual weather images to `data/demo_images/` for best results
- The system is designed to be production-ready with minimal modifications

---

**Created for SpaceShield Hackathon** 🚀