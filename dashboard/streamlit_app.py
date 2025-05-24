"""
WeatherEyes Live Dashboard
Streamlit app dla live demo na prezentacji
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

# Add project modules to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.weather_api import WeatherAPI
from ai_model.weather_classifier import WeatherClassifier
from bot.alert_system import WeatherAlertSystem

# Page config
st.set_page_config(
    page_title="WeatherEyes Live Demo",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.alert-high {
    background-color: #ffe6e6;
    border-left: 5px solid #ff4444;
    padding: 1rem;
    margin: 0.5rem 0;
}
.alert-medium {
    background-color: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 1rem;
    margin: 0.5rem 0;
}
.alert-low {
    background-color: #e6f3ff;
    border-left: 5px solid #007bff;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_mock_data():
    """Load mock Instagram data"""
    try:
        with open('data/mock_instagram_posts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "posts": [
                {
                    "id": "demo_1",
                    "description": "Sunny day at SHAMAN! ☀️",
                    "weather_detected": "sunny",
                    "confidence": 0.95,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }

@st.cache_resource
def init_components():
    """Initialize WeatherEyes components"""
    return {
        'weather_api': WeatherAPI(),
        'ai_classifier': WeatherClassifier(),
        'alert_system': WeatherAlertSystem()
    }

def main():
    # Header
    st.markdown('<p class="big-font">🌤️ WeatherEyes - Live Demo</p>', unsafe_allow_html=True)
    st.markdown("**SHAMAN 2024 - Dane pogodowe jako sojusznik człowieka**")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Demo Controls")
    
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=False)
    demo_mode = st.sidebar.selectbox(
        "Demo Mode", 
        ["Live Analysis", "Historical Data", "Alert Simulation"]
    )
    
    # Initialize components
    components = init_components()
    mock_data = load_mock_data()
    
    # Main content area
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.subheader("📱 Social Media Analysis")
        
        # AI Classification results
        ai_results = components['ai_classifier'].batch_classify(mock_data['posts'])
        weather_summary = components['ai_classifier'].get_weather_summary(ai_results)
        
        # Weather distribution chart
        weather_dist = weather_summary['weather_distribution']
        if weather_dist:
            weather_df = pd.DataFrame([
                {'Weather': k, 'Count': v['count'], 'Avg_Confidence': v['total_confidence']/v['count']}
                for k, v in weather_dist.items()
            ])
            
            fig = px.bar(weather_df, x='Weather', y='Count', 
                        color='Avg_Confidence', color_continuous_scale='viridis',
                        title="Weather Detection from Social Media")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent posts
        st.subheader("🆕 Recent Posts Analyzed")
        for i, result in enumerate(ai_results[:3]):
            post = result['original_post']
            classification = result['classification']
            
            with st.expander(f"Post {i+1}: {post.get('description', 'No description')[:50]}..."):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Weather:** {classification['predicted_weather']}")
                    st.write(f"**Confidence:** {classification['confidence']:.1%}")
                with col_b:
                    st.write(f"**Source:** {post.get('user', 'Unknown')}")
                    st.write(f"**Time:** {post.get('timestamp', 'Unknown')}")
    
    with col2:
        st.subheader("🌍 Official Weather API")
        
        # Current weather
        current_weather = components['weather_api'].get_current_weather("Warsaw")
        
        # Weather metrics
        col_temp, col_condition = st.columns(2)
        with col_temp:
            st.metric("Temperature", f"{current_weather['temperature']}°C")
        with col_condition:
            st.metric("Condition", current_weather['condition'].title())
        
        st.metric("Humidity", f"{current_weather['humidity']}%")
        st.metric("Wind Speed", f"{current_weather['wind_speed']} km/h")
        
        # Comparison with social media
        comparison = components['weather_api'].compare_with_social_data(
            weather_summary['dominant_weather'], "Warsaw"
        )
        
        st.subheader("🔍 Data Comparison")
        match_color = "green" if comparison['match'] else "red"
        match_text = "✅ MATCH" if comparison['match'] else "❌ MISMATCH"
        
        st.markdown(f"""
        <div class="metric-container">
            <strong>Social Media:</strong> {weather_summary['dominant_weather']}<br>
            <strong>Official API:</strong> {current_weather['condition']}<br>
            <strong>Status:</strong> <span style="color: {match_color}">{match_text}</span><br>
            <strong>Confidence:</strong> {comparison['confidence']:.1%}
        </div>
        """, unsafe_allow_html=True)
        
        # Time series simulation
        st.subheader("📈 Weather Trend (Last 24h)")
        
        # Generate mock time series data
        hours = list(range(24))
        temps = [15 + 5 * (i/24) + 3 * (i % 6) / 6 for i in hours]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=hours, y=temps, mode='lines+markers', name='Temperature'))
        fig_trend.update_layout(
            title="Temperature Trend",
            xaxis_title="Hour",
            yaxis_title="Temperature (°C)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col3:
        st.subheader("🚨 Live Alerts")
        
        # Generate sample alerts
        alerts = []
        
        # Daily summary
        daily_alert = components['alert_system'].create_daily_summary_alert(weather_summary)
        alerts.append(daily_alert)
        
        # Weather change alert
        change_alert = components['alert_system'].create_weather_change_alert(
            "sunny", "cloudy", 0.85
        )
        if change_alert:
            alerts.append(change_alert)
        
        # Event alert
        event_time = datetime.now() + timedelta(hours=2)
        event_alert = components['alert_system'].create_event_alert(
            "SHAMAN Finał", event_time, current_weather
        )
        if event_alert:
            alerts.append(event_alert)
        
        # Display alerts
        for alert in alerts:
            priority = alert['priority']
            css_class = f"alert-{priority}" if priority in ['high', 'medium', 'low'] else "alert-low"
            
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{alert['title']}</strong><br>
                <small>{alert['message'][:100]}...</small><br>
                <em>Priority: {priority.upper()}</em>
            </div>
            """, unsafe_allow_html=True)
        
        # Alert statistics
        st.subheader("📊 Alert Stats")
        stats = components['alert_system'].get_alert_stats()
        
        st.metric("Total Alerts", stats['total_alerts'])
        st.metric("Pending", stats['pending_alerts'])
        
        # Alert types breakdown
        if stats['by_type']:
            alert_types_df = pd.DataFrame([
                {'Type': k.replace('_', ' ').title(), 'Count': v}
                for k, v in stats['by_type'].items()
            ])
            
            fig_alerts = px.pie(alert_types_df, values='Count', names='Type',
                               title="Alert Types Distribution")
            st.plotly_chart(fig_alerts, use_container_width=True)
    
    # Bottom section - Live feed simulation
    st.subheader("📡 Live Feed Simulation")
    
    if st.button("🔴 Start Live Demo"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        live_data = st.empty()
        
        for i in range(10):
            # Simulate processing
            progress_bar.progress((i + 1) / 10)
            status_text.text(f"Processing post {i+1}/10...")
            
            # Simulate new data
            new_weather = ["sunny", "cloudy", "rainy", "clear"][i % 4]
            confidence = 0.7 + (i % 3) * 0.1
            
            live_data.json({
                "timestamp": datetime.now().isoformat(),
                "detected_weather": new_weather,
                "confidence": confidence,
                "source": f"instagram_post_{i+1}"
            })
            
            time.sleep(0.5)
        
        status_text.text("✅ Live demo completed!")
        progress_bar.progress(1.0)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <strong>WeatherEyes - Event Edition</strong><br>
        <em>"Dane pogodowe jako sojusznik człowieka"</em><br>
        SHAMAN 2024 Hackathon
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 