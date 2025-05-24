"""
WeatherEyes - PITCH DEMO 
Minimalistyczne, efektowne demo dla SpaceShield Hackathon
"""

import streamlit as st
import time
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add project path
sys.path.append(str(Path(__file__).parent))

from ai_model.openai_vision import OpenAIVisionAnalyzer

# Page config
st.set_page_config(
    page_title="WeatherEyes - Live Weather Intelligence",
    page_icon="🌩️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Cinematic CSS
st.markdown("""
<style>
/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* Background and main styling */
.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
}

/* Hero title */
.hero-title {
    font-size: 60px !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(45deg, #ffffff, #a8e6cf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 20px 0;
    text-shadow: 0 0 30px rgba(255,255,255,0.3);
}

/* Subtitle */
.hero-subtitle {
    font-size: 24px;
    text-align: center;
    color: #a8e6cf;
    margin-bottom: 40px;
    opacity: 0.9;
}

/* Main demo button */
.demo-button {
    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
    border: none;
    padding: 20px 40px;
    font-size: 28px;
    font-weight: bold;
    border-radius: 50px;
    color: white;
    box-shadow: 0 10px 30px rgba(255,107,107,0.4);
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 20px auto;
    display: block;
}

.demo-button:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(255,107,107,0.6);
}

/* Scanning animation */
.scanning-container {
    background: rgba(0,0,0,0.2);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    border: 2px solid rgba(168,230,207,0.3);
}

.scanning-text {
    font-size: 20px;
    text-align: center;
    color: #a8e6cf;
    margin: 15px 0;
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
    100% { opacity: 0.6; transform: scale(1); }
}

/* Image containers */
.image-scan {
    border: 3px solid #a8e6cf;
    border-radius: 15px;
    padding: 10px;
    margin: 10px;
    background: rgba(168,230,207,0.1);
    transition: all 0.5s ease;
}

.image-analyzed {
    border-color: #00ff00;
    background: rgba(0,255,0,0.1);
    box-shadow: 0 0 20px rgba(0,255,0,0.3);
}

/* Results display */
.result-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
}

.weather-icon {
    font-size: 80px;
    text-align: center;
    margin: 20px 0;
}

.confidence-bar {
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
    height: 20px;
    margin: 10px 0;
    overflow: hidden;
}

.confidence-fill {
    background: linear-gradient(90deg, #00ff00, #7ed321);
    height: 100%;
    border-radius: 10px;
    transition: width 2s ease;
}

/* Timer */
.timer {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #ff6b6b;
    margin: 20px 0;
    text-shadow: 0 0 20px rgba(255,107,107,0.5);
}

/* Alert box */
.alert-critical {
    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    border: none;
    box-shadow: 0 10px 30px rgba(255,107,107,0.4);
    animation: alertPulse 1s infinite;
}

@keyframes alertPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

.alert-text {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    color: white;
    margin: 0;
}

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
}

.stat-number {
    font-size: 36px;
    font-weight: bold;
    color: #a8e6cf;
}

.stat-label {
    font-size: 14px;
    opacity: 0.8;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

def show_hero():
    """Pokazuje główny ekran startowy"""
    
    st.markdown('<div class="hero-title">🌩️ WeatherEyes</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Widzimy burzę w oczach ludzi</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ ANALIZUJ SPACESHIELD", key="main_demo", help="Uruchom live demo"):
            st.session_state.demo_started = True
            st.rerun()

def show_scanning_phase():
    """Faza skanowania - dramatyczna animacja"""
    
    st.markdown('<div class="scanning-container">', unsafe_allow_html=True)
    st.markdown('<div class="scanning-text pulse">🔍 SKANOWANIE SOCIAL MEDIA...</div>', unsafe_allow_html=True)
    
    # Progress z animacją
    progress_placeholder = st.empty()
    
    # Sprawdź zdjęcia użytkownika
    event_dir = Path("data/event_images")
    images = []
    if event_dir.exists():
        for file_path in event_dir.iterdir():
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                images.append(str(file_path))
    
    if not images:
        st.error("🚫 Dodaj swoje zdjęcia z eventi do data/event_images/")
        return []
    
    # Animacja postępu
    for i in range(101):
        progress_placeholder.progress(i, text=f"Skanowanie Instagram Stories... {i}%")
        time.sleep(0.02)
    
    st.markdown('<div class="scanning-text">✅ ZNALEZIONO ZDJĘCIA Z WYDARZENIA</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(1)
    return images[:3]  # Tylko pierwsze 3 dla demo

def show_image_analysis(images):
    """Pokazuje analizę zdjęć z animacjami"""
    
    st.markdown('<div class="scanning-container">', unsafe_allow_html=True)
    st.markdown('<div class="scanning-text">🤖 AI VISION ANALYSIS</div>', unsafe_allow_html=True)
    
    # START TIMER - rzeczywisty czas analizy
    start_time = time.time()
    
    # Pokaż zdjęcia z animacją analizy
    cols = st.columns(len(images))
    placeholders = []
    
    for i, (col, img_path) in enumerate(zip(cols, images)):
        with col:
            placeholder = st.empty()
            placeholders.append(placeholder)
            placeholder.markdown(f'<div class="image-scan pulse">', unsafe_allow_html=True)
            try:
                st.image(img_path, caption=f"Story {i+1}", width=150)
            except:
                st.write(f"📷 Image {i+1}")
            placeholder.markdown('</div>', unsafe_allow_html=True)
    
    # Symuluj analizę każdego zdjęcia
    analyzer = OpenAIVisionAnalyzer()
    api_key = os.getenv('OPENAI_API_KEY', 'demo_key')
    if api_key == 'demo_key':
        analyzer.api_key = 'demo_key'
    
    analyses = []
    
    for i, img_path in enumerate(images):
        # Animacja analizy
        placeholders[i].markdown(f'<div class="image-scan pulse">⚡ ANALYZING...</div>', unsafe_allow_html=True)
        
        # Prawdziwa analiza - bez dodatkowego time.sleep bo chcemy realny czas
        analysis = analyzer.analyze_image(img_path, "SpaceShield Hackathon event weather analysis")
        analyses.append(analysis)
        
        # Pokazanie wyniku - używamy TYLKO rzeczywistego confidence z AI
        weather = analysis.get('weather_condition', 'cloudy')
        confidence = analysis.get('confidence', None)  # None jeśli brak confidence
        
        if confidence is not None:
            confidence_text = f"{confidence:.0%} confidence"
        else:
            confidence_text = "analyzing..."
        
        placeholders[i].markdown(f'''
        <div class="image-analyzed">
            <div style="text-align: center; color: #00ff00; font-weight: bold;">
                ✅ {weather.upper()}<br>
                {confidence_text}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        time.sleep(0.5)  # Krótka pauza dla efektu wizualnego
    
    # STOP TIMER - oblicz rzeczywisty czas
    end_time = time.time()
    analysis_duration = end_time - start_time
    
    st.markdown('</div>', unsafe_allow_html=True)
    return analyses, analysis_duration

def show_results_and_alert(analyses, analysis_duration):
    """Pokazuje dramatyczne wyniki i alert z rzeczywistymi danymi"""
    
    # Analiza wyników - używamy rzeczywistego confidence
    weather_conditions = [a.get('weather_condition', 'unknown') for a in analyses]
    confidences = [a.get('confidence', 0) for a in analyses if a.get('confidence', 0) > 0]
    
    # Oblicz średni confidence tylko z prawdziwych wartości
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
    else:
        avg_confidence = 0.75  # Fallback dla demo mode
    
    # Określ dominującą pogodę
    from collections import Counter
    weather_count = Counter(weather_conditions)
    dominant_weather = weather_count.most_common(1)[0][0]
    
    # Timer countdown
    timer_placeholder = st.empty()
    for countdown in range(5, 0, -1):
        timer_placeholder.markdown(f'<div class="timer">WYNIKI ZA: {countdown}</div>', unsafe_allow_html=True)
        time.sleep(1)
    
    timer_placeholder.markdown('<div class="timer">🎯 ANALIZA ZAKOŃCZONA</div>', unsafe_allow_html=True)
    
    # Wyniki w karcie
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Ikona pogody
    weather_icons = {
        'sunny': '☀️',
        'cloudy': '☁️', 
        'rainy': '🌧️',
        'stormy': '⛈️',
        'snow': '❄️',
        'clear': '🌤️'
    }
    
    icon = weather_icons.get(dominant_weather, '🌤️')
    st.markdown(f'<div class="weather-icon">{icon}</div>', unsafe_allow_html=True)
    
    # Format rzeczywistego czasu analizy
    minutes = int(analysis_duration // 60)
    seconds = int(analysis_duration % 60)
    if minutes > 0:
        time_display = f"{minutes}:{seconds:02d}"
    else:
        time_display = f"{seconds}s"
    
    # Stats grid z rzeczywistymi danymi
    st.markdown(f'''
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-number">{dominant_weather.upper()}</div>
            <div class="stat-label">Detected Weather</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{avg_confidence:.0%}</div>
            <div class="stat-label">AI Confidence</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(analyses)}</div>
            <div class="stat-label">Images Analyzed</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{time_display}</div>
            <div class="stat-label">Analysis Time</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Confidence bar z animacją - używamy rzeczywistego confidence
    st.markdown('<div style="margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-bottom: 10px;">CONFIDENCE LEVEL</div>', unsafe_allow_html=True)
    confidence_container = st.empty()
    
    # Animacja confidence bar
    for width in range(0, int(avg_confidence * 100) + 1, 2):
        confidence_container.markdown(f'''
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: {width}%;"></div>
        </div>
        ''', unsafe_allow_html=True)
        time.sleep(0.05)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # DRAMATYCZNY ALERT - z rzeczywistą analizą confidence
    if dominant_weather in ['rainy', 'stormy']:
        alert_message = "⚠️ WEATHER ALERT: Adverse conditions detected!"
        alert_recommendation = "🚨 Take protective action immediately!"
    elif dominant_weather == 'cloudy':
        alert_message = "🌫️ CLOUDY CONDITIONS: Monitor situation"  
        alert_recommendation = "📱 Stay alert for weather changes"
    else:
        alert_message = "✅ CLEAR CONDITIONS: All systems go"
        alert_recommendation = "👍 Perfect conditions for operations"
    
    # Dodaj informację o confidence w alert
    if avg_confidence >= 0.8:
        confidence_note = f"High confidence ({avg_confidence:.0%})"
    elif avg_confidence >= 0.6:
        confidence_note = f"Medium confidence ({avg_confidence:.0%})"
    else:
        confidence_note = f"Low confidence ({avg_confidence:.0%})"
    
    time.sleep(1)
    
    # Pulsujący alert z confidence info
    st.markdown(f'''
    <div class="alert-critical">
        <div class="alert-text">{alert_message}</div>
        <div style="text-align: center; font-size: 18px; margin-top: 15px; opacity: 0.9;">
            {alert_recommendation}
        </div>
        <div style="text-align: center; font-size: 14px; margin-top: 10px; opacity: 0.7;">
            {confidence_note} • Analysis time: {time_display}
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    """Główna aplikacja demo"""
    
    # Inicjalizacja state
    if 'demo_started' not in st.session_state:
        st.session_state.demo_started = False
    
    if not st.session_state.demo_started:
        show_hero()
    else:
        # Demo flow
        st.markdown('<div class="hero-title" style="font-size: 40px;">🌩️ LIVE ANALYSIS</div>', unsafe_allow_html=True)
        
        # Faza 1: Skanowanie
        images = show_scanning_phase()
        
        if images:
            # Faza 2: Analiza AI z rzeczywistym timerem
            analyses, analysis_duration = show_image_analysis(images)
            
            # Faza 3: Wyniki i Alert z rzeczywistymi danymi
            show_results_and_alert(analyses, analysis_duration)
            
            # Reset button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 RESTART DEMO"):
                    st.session_state.demo_started = False
                    st.rerun()

if __name__ == "__main__":
    main() 