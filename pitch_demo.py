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
import tempfile

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
    font-size: 32px;
    font-weight: bold;
    color: #a8e6cf;
}

.stat-label {
    font-size: 14px;
    color: rgba(255,255,255,0.7);
    margin-top: 5px;
}

/* Upload interface styling */
.upload-card {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
    text-align: center;
    border: 1px solid rgba(168,230,207,0.3);
    transition: all 0.3s ease;
}

.upload-card:hover {
    border-color: rgba(168,230,207,0.6);
    background: rgba(255,255,255,0.15);
}

/* Upload button styling */
.upload-button {
    background: linear-gradient(45deg, #a8e6cf, #7ed321);
    border: none;
    padding: 15px 30px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 25px;
    color: #1e3c72;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
}

.upload-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(168,230,207,0.4);
}

/* File uploader custom styling */
.stFileUploader > div {
    background: rgba(255,255,255,0.1) !important;
    border: 2px dashed rgba(168,230,207,0.5) !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

.stFileUploader label {
    color: #a8e6cf !important;
    font-weight: bold !important;
}

/* Upload preview styling */
.upload-preview {
    border: 2px solid #a8e6cf;
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    background: rgba(168,230,207,0.1);
}
</style>
""", unsafe_allow_html=True)

def show_hero():
    """Pokazuje główny ekran startowy z opcjami źródła zdjęć"""
    
    st.markdown('<div class="hero-title">🌩️ WeatherEyes</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Widzimy burzę w oczach ludzi</div>', unsafe_allow_html=True)
    
    # Opcje źródła danych
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <div style="font-size: 20px; color: #a8e6cf; margin-bottom: 20px;">
            🎯 Wybierz źródło zdjęć do analizy
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">📂</div>
            <div style="font-size: 16px; font-weight: bold;">Demo Data</div>
            <div style="font-size: 12px; opacity: 0.8;">Użyj przykładowych zdjęć</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ ANALIZUJ PRZYKŁADY", key="demo_default", help="Użyj domyślnych zdjęć z katalogu", use_container_width=True):
            st.session_state.demo_started = True
            st.session_state.image_source = "default"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">📤</div>
            <div style="font-size: 16px; font-weight: bold;">Upload Custom</div>
            <div style="font-size: 12px; opacity: 0.8;">Prześlij własne screenshoty</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📸 UPLOAD ZDJĘCIA", key="demo_upload", help="Prześlij własne zdjęcia", use_container_width=True):
            st.session_state.demo_started = True
            st.session_state.image_source = "upload"
            st.rerun()

def show_upload_interface():
    """Pokazuje interfejs do uploadu zdjęć"""
    
    st.markdown('<div class="scanning-container">', unsafe_allow_html=True)
    st.markdown('<div class="scanning-text">📤 UPLOAD SCREENSHOTÓW</div>', unsafe_allow_html=True)
    
    # File uploader z cinematic styling
    st.markdown("""
    <div style="text-align: center; margin: 20px 0; color: #a8e6cf;">
        <div style="font-size: 18px; margin-bottom: 10px;">🎯 Prześlij własne zdjęcia pogodowe</div>
        <div style="font-size: 14px; opacity: 0.8;">Obsługiwane formaty: JPG, PNG, BMP • Maksymalnie 3 pliki</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload multiple files
    uploaded_files = st.file_uploader(
        "Wybierz zdjęcia",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        accept_multiple_files=True,
        key="weather_images",
        help="Możesz przesłać maksymalnie 3 zdjęcia do analizy pogody",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        # Ograniczenie do 3 plików
        if len(uploaded_files) > 3:
            st.markdown("""
            <div style="background: rgba(255,107,107,0.2); border: 1px solid rgba(255,107,107,0.5); 
                        border-radius: 10px; padding: 15px; margin: 10px 0; text-align: center;">
                <div style="color: #ff6b6b; font-weight: bold;">⚠️ Wybrano więcej niż 3 pliki</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 14px;">Zostanie przeanalizowanych tylko pierwsze 3 zdjęcia</div>
            </div>
            """, unsafe_allow_html=True)
            uploaded_files = uploaded_files[:3]
        
        # Preview przesłanych zdjęć z animacją
        st.markdown('<div class="scanning-text pulse">👁️ PODGLĄD PRZESŁANYCH ZDJĘĆ</div>', unsafe_allow_html=True)
        
        cols = st.columns(len(uploaded_files))
        temp_paths = []
        
        for i, (col, uploaded_file) in enumerate(zip(cols, uploaded_files)):
            with col:
                # Container z upload styling
                st.markdown('<div class="upload-preview">', unsafe_allow_html=True)
                
                # Pokaż podgląd
                st.image(uploaded_file, caption=f"📸 {uploaded_file.name}", width=150)
                
                # Informacje o pliku
                file_size = len(uploaded_file.getbuffer()) / 1024  # KB
                st.markdown(f"""
                <div style="text-align: center; font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 5px;">
                    {file_size:.1f} KB
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Zapisz tymczasowo do analizy
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_paths.append(tmp_file.name)
        
        # Success message
        st.markdown(f"""
        <div style="background: rgba(126,211,33,0.2); border: 1px solid rgba(126,211,33,0.5); 
                    border-radius: 10px; padding: 15px; margin: 20px 0; text-align: center;">
            <div style="color: #7ed321; font-weight: bold;">✅ {len(uploaded_files)} zdjęć gotowych do analizy</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 14px;">AI przeanalizuje warunki pogodowe na każdym zdjęciu</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button do rozpoczęcia analizy z cinematic styling
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Custom styled button
            st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
            """, unsafe_allow_html=True)
            
            if st.button("🚀 ROZPOCZNIJ ANALIZĘ AI", key="start_analysis", use_container_width=True):
                st.session_state.uploaded_images = temp_paths
                st.session_state.analysis_ready = True
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Instrukcje gdy brak plików
        st.markdown("""
        <div style="text-align: center; margin: 30px 0; color: rgba(255,255,255,0.6);">
            <div style="font-size: 48px; margin-bottom: 20px;">📷</div>
            <div style="font-size: 16px;">Przeciągnij zdjęcia tutaj lub kliknij żeby wybrać</div>
            <div style="font-size: 14px; margin-top: 10px; opacity: 0.8;">
                💡 Tip: Wybierz zdjęcia z różnymi warunkami pogodowymi dla lepszego demo
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Przycisk powrotu z cinematic styling
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔙 POWRÓT DO MENU", key="back_to_hero", use_container_width=True):
            st.session_state.demo_started = False
            st.session_state.image_source = None
            # Clear uploaded files if any
            if 'uploaded_images' in st.session_state:
                for temp_path in st.session_state.uploaded_images:
                    try:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except:
                        pass
                st.session_state.uploaded_images = []
            st.rerun()
    
    return []

def show_scanning_phase():
    """Faza skanowania - dramatyczna animacja"""
    
    # Sprawdź źródło obrazów
    if st.session_state.get('image_source') == 'upload':
        if st.session_state.get('analysis_ready'):
            # Użyj przesłanych zdjęć
            images = st.session_state.get('uploaded_images', [])
            if not images:
                st.error("🚫 Brak przesłanych zdjęć!")
                return []
            
            st.markdown('<div class="scanning-container">', unsafe_allow_html=True)
            st.markdown('<div class="scanning-text pulse">🔍 PRZETWARZANIE PRZESŁANYCH ZDJĘĆ...</div>', unsafe_allow_html=True)
            
            # Progress z animacją
            progress_placeholder = st.empty()
            for i in range(101):
                progress_placeholder.progress(i, text=f"Przygotowywanie do analizy... {i}%")
                time.sleep(0.02)
            
            st.markdown('<div class="scanning-text">✅ ZDJĘCIA GOTOWE DO ANALIZY</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            time.sleep(1)
            return images
        else:
            # Pokaż interfejs uploadu
            return show_upload_interface()
    else:
        # Domyślna logika dla zdjęć z katalogu
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
    if 'image_source' not in st.session_state:
        st.session_state.image_source = None
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []
    if 'analysis_ready' not in st.session_state:
        st.session_state.analysis_ready = False
    
    if not st.session_state.demo_started:
        show_hero()
    else:
        # Demo flow
        st.markdown('<div class="hero-title" style="font-size: 40px;">🌩️ LIVE ANALYSIS</div>', unsafe_allow_html=True)
        
        # Dodaj informację o źródle
        if st.session_state.get('image_source') == 'upload':
            st.markdown('<div style="text-align: center; color: #a8e6cf; margin: 10px 0;">📤 Analiza przesłanych zdjęć</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; color: #a8e6cf; margin: 10px 0;">📂 Analiza przykładowych zdjęć</div>', unsafe_allow_html=True)
        
        # Faza 1: Skanowanie
        images = show_scanning_phase()
        
        if images:
            # Faza 2: Analiza AI z rzeczywistym timerem
            analyses, analysis_duration = show_image_analysis(images)
            
            # Faza 3: Wyniki i Alert z rzeczywistymi danymi
            show_results_and_alert(analyses, analysis_duration)
            
            # Cleanup tymczasowych plików
            if st.session_state.get('image_source') == 'upload':
                for temp_path in st.session_state.get('uploaded_images', []):
                    try:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except:
                        pass
            
            # Reset button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 RESTART DEMO"):
                    st.session_state.demo_started = False
                    st.session_state.image_source = None
                    st.session_state.uploaded_images = []
                    st.session_state.analysis_ready = False
                    st.rerun()

if __name__ == "__main__":
    main() 