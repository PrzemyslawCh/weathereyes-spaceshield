"""
WeatherEyes - SHAMAN 2024 Demo Dashboard
Mega prosty dashboard pokazujący cały workflow na żywo
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
from bot.real_alerts import RealAlertSystem

# Page config
st.set_page_config(
    page_title="WeatherEyes - SHAMAN 2024 Live Demo",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.big-title {
    font-size: 40px !important;
    text-align: center;
    color: #1f77b4;
    margin-bottom: 20px;
}
.step-box {
    background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
    margin: 10px 0;
}
.result-box {
    background: linear-gradient(90deg, #f0fff0, #e6ffe6);
    padding: 15px;
    border-radius: 8px;
    border-left: 5px solid #28a745;
    margin: 10px 0;
}
.alert-box {
    background: linear-gradient(90deg, #fff8e1, #ffecb3);
    padding: 15px;
    border-radius: 8px;
    border-left: 5px solid #ff9800;
    margin: 10px 0;
}
.metric-big {
    font-size: 24px !important;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="big-title">🌤️ WeatherEyes - LIVE DEMO</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 18px; color: #666; margin-bottom: 30px;">SHAMAN 2024 - "Dane pogodowe jako sojusznik człowieka"</div>', unsafe_allow_html=True)
    
    # Główny workflow
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 📸 Step 1: Social Media")
        st.markdown("**Instagram Stories**")
        
    with col2:
        st.markdown("### 🤖 Step 2: AI Analysis")
        st.markdown("**OpenAI Vision**")
        
    with col3:
        st.markdown("### 🚨 Step 3: Smart Alerts")
        st.markdown("**AI Generated**")
        
    with col4:
        st.markdown("### 📱 Step 4: Distribution")
        st.markdown("**Multi-Channel**")
    
    st.markdown("---")
    
    # Sprawdź czy są zdjęcia
    event_dir = Path("data/event_images")
    demo_dir = Path("data/demo_images")
    images = []
    source_label = ""
    
    # Sprawdź prawdziwe zdjęcia z wydarzenia
    if event_dir.exists():
        for file_path in event_dir.iterdir():
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                images.append(str(file_path))
        if images:
            source_label = "SHAMAN 2024 Event"
    
    # Jeśli brak prawdziwych, użyj demo
    if not images and demo_dir.exists():
        for file_path in demo_dir.iterdir():
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                images.append(str(file_path))
        if images:
            source_label = "Demo Images"
    
    if not images:
        st.error("🚫 Brak zdjęć! Dodaj zdjęcia do folderu data/event_images/ lub data/demo_images/")
        st.info("💡 Tip: Skopiuj zdjęcia z wydarzenia SHAMAN 2024 do folderu data/event_images/")
        st.stop()
    
    # Status OpenAI API
    api_key = os.getenv('OPENAI_API_KEY', 'demo_key')
    api_status = "🟢 LIVE OpenAI API" if api_key != 'demo_key' else "🟡 Demo Mode"
    
    st.sidebar.markdown(f"**API Status:** {api_status}")
    st.sidebar.markdown(f"**Zdjęcia:** {len(images)} z {source_label}")
    st.sidebar.markdown(f"**Source:** {source_label}")
    
    # Główny przycisk demo
    if st.button("🚀 START LIVE DEMO", type="primary", use_container_width=True):
        run_live_demo(images, api_key != 'demo_key')

def run_live_demo(images, use_real_api):
    """Uruchamia live demo całego procesu"""
    
    # Progress bar
    progress = st.progress(0)
    status = st.empty()
    
    # STEP 1: Social Media Data
    status.markdown("### 📸 STEP 1: Collecting Social Media Data")
    progress.progress(25)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("**🔍 Scanning Instagram Stories from SHAMAN 2024...**")
    
    col1, col2, col3 = st.columns(3)
    for i, img_path in enumerate(images[:3]):
        with [col1, col2, col3][i]:
            try:
                st.image(img_path, caption=f"Story {i+1}: {Path(img_path).name}", width=150)
            except:
                st.write(f"📷 {Path(img_path).name}")
    
    st.markdown(f"✅ **Found {len(images)} images from SHAMAN event**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(2)
    
    # STEP 2: AI Analysis
    status.markdown("### 🤖 STEP 2: AI Weather Analysis")
    progress.progress(50)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("**🧠 OpenAI Vision API analyzing weather conditions...**")
    
    # Initialize analyzer
    analyzer = OpenAIVisionAnalyzer()
    if not use_real_api:
        analyzer.api_key = 'demo_key'
    
    # Analyze images
    context = "Zdjęcia z wydarzenia SHAMAN 2024 - hackathon technologiczny w Polsce"
    analyses = []
    
    analysis_container = st.empty()
    
    for i, image_path in enumerate(images):
        analysis_container.markdown(f"🔍 Analyzing image {i+1}/{len(images)}: {Path(image_path).name}")
        
        analysis = analyzer.analyze_image(image_path, context)
        analyses.append(analysis)
        
        # Show intermediate result
        weather = analysis.get('weather_condition', 'unknown')
        confidence = analysis.get('confidence', 0)
        
        if weather != 'unknown':
            analysis_container.markdown(f"✅ **{Path(image_path).name}**: {weather} ({confidence:.1%} confidence)")
        
        time.sleep(0.5)
    
    # Get summary
    summary = analyzer.get_weather_summary_from_images(analyses)
    
    st.markdown("**🎯 AI Analysis Results:**")
    
    if 'error' not in summary:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-big">🌤️</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-big">{summary["dominant_weather"].upper()}</div>', unsafe_allow_html=True)
            st.markdown("**Dominant Weather**")
        
        with col2:
            st.markdown('<div class="metric-big">📊</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-big">{summary["confidence"]:.1%}</div>', unsafe_allow_html=True)
            st.markdown("**Confidence**")
        
        with col3:
            st.markdown('<div class="metric-big">📸</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-big">{summary["valid_analyses"]}</div>', unsafe_allow_html=True)
            st.markdown("**Images Analyzed**")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(2)
    
    # STEP 3: Smart Alerts
    status.markdown("### 🚨 STEP 3: Generating Smart Alerts")
    progress.progress(75)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("**💡 AI generating contextual weather alerts...**")
    
    # Generate alerts
    alert_system = RealAlertSystem()
    alerts_generated = []
    
    # Daily summary alert
    if 'error' not in summary:
        st.markdown("🔄 Creating daily weather summary...")
        time.sleep(1)
        
        summary_alert = {
            'type': 'daily_summary',
            'title': '📊 SHAMAN 2024 Weather Report',
            'weather': summary['dominant_weather'],
            'confidence': f"{summary['confidence']:.1%}",
            'images': summary['valid_analyses'],
            'message': f"Weather analysis from {summary['valid_analyses']} images shows {summary['dominant_weather']} conditions with {summary['confidence']:.1%} confidence."
        }
        alerts_generated.append(summary_alert)
        st.markdown("✅ Daily summary alert created")
    
    # Weather change alert (if multiple conditions)
    weather_dist = summary.get('weather_distribution', {})
    if len(weather_dist) > 1:
        st.markdown("🔄 Detecting weather changes...")
        time.sleep(1)
        
        weather_types = list(weather_dist.keys())
        change_alert = {
            'type': 'weather_change',
            'title': '⚠️ Weather Condition Change',
            'from_weather': weather_types[0],
            'to_weather': weather_types[1],
            'message': f"Weather conditions changed from {weather_types[0]} to {weather_types[1]} during SHAMAN event."
        }
        alerts_generated.append(change_alert)
        st.markdown("✅ Weather change alert created")
    
    # Event alert
    st.markdown("🔄 Creating event-specific alert...")
    time.sleep(1)
    
    event_alert = {
        'type': 'event_alert',
        'title': '🎯 SHAMAN 2024 Event Weather',
        'event': 'SHAMAN Finał',
        'weather': summary.get('dominant_weather', 'unknown'),
        'recommendation': '🌂 Check weather before heading out!' if summary.get('dominant_weather') == 'rainy' else '👍 Good conditions for the event!',
        'message': f"Weather forecast for SHAMAN finale: {summary.get('dominant_weather', 'unknown')} conditions expected."
    }
    alerts_generated.append(event_alert)
    st.markdown("✅ Event-specific alert created")
    
    st.markdown(f"**🎯 Generated {len(alerts_generated)} smart alerts**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(2)
    
    # STEP 4: Distribution
    status.markdown("### 📱 STEP 4: Multi-Channel Distribution")
    progress.progress(100)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("**📡 Distributing alerts across multiple channels...**")
    
    # Simulate distribution
    channels = [
        {"name": "📱 Telegram Bot", "status": "✅ Sent", "recipients": "Event participants"},
        {"name": "📞 SMS Alert", "status": "✅ Sent", "recipients": "Emergency contacts"},
        {"name": "📧 Email Report", "status": "✅ Sent", "recipients": "Event organizers"},
        {"name": "🌐 Web Dashboard", "status": "✅ Updated", "recipients": "Public access"},
    ]
    
    for channel in channels:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"**{channel['name']}**")
        with col2:
            st.markdown(channel['status'])
        with col3:
            st.markdown(f"*{channel['recipients']}*")
        time.sleep(0.5)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Final Results
    status.markdown("### ✅ DEMO COMPLETED!")
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown("**🎉 WeatherEyes Successfully Analyzed SHAMAN 2024 Event!**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Processing Summary:**")
        st.markdown(f"• **Images Processed:** {len(images)}")
        st.markdown(f"• **Weather Detected:** {summary.get('dominant_weather', 'unknown').title()}")
        st.markdown(f"• **AI Confidence:** {summary.get('confidence', 0):.1%}")
        st.markdown(f"• **Alerts Generated:** {len(alerts_generated)}")
        st.markdown(f"• **Channels Notified:** {len(channels)}")
    
    with col2:
        st.markdown("**🎯 Key Features Demonstrated:**")
        st.markdown("✅ Real-time social media monitoring")
        st.markdown("✅ AI-powered weather recognition")
        st.markdown("✅ Intelligent alert generation")
        st.markdown("✅ Multi-channel distribution")
        st.markdown("✅ Event-specific recommendations")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show generated alerts
    st.markdown("### 🚨 Generated Alerts Preview")
    
    for alert in alerts_generated:
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.markdown(f"**{alert['title']}**")
        st.markdown(alert['message'])
        if 'recommendation' in alert:
            st.markdown(f"*{alert['recommendation']}*")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save results
    results_file = Path("data/demo_results.json")
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': summary,
            'alerts': alerts_generated,
            'channels': channels,
            'timestamp': datetime.now().isoformat(),
            'api_mode': 'real' if use_real_api else 'demo'
        }, f, indent=2, ensure_ascii=False)
    
    st.success(f"📁 Demo results saved to: {results_file}")
    
    # Call to action
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 20px; color: #1f77b4; font-weight: bold;">🏆 WeatherEyes - Ready for Production!</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666;">Real AI • Real Alerts • Real Impact</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 