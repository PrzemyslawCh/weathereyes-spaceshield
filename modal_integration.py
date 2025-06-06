"""
WeatherEyes Modal Integration
Deploy AI weather analysis as serverless functions
"""

import modal
import os
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

# Create Modal app
app = modal.App("weathereyes-app")

# Define the image with our dependencies
image = modal.Image.debian_slim().pip_install(
    "openai>=1.3.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
    "Pillow>=10.1.0",
    "python-telegram-bot>=20.0",
    "twilio>=8.10.0"
)

# Create secrets for API keys
secrets = modal.Secret.from_name("weathereyes-secrets")

# Mount the project code
project_mount = modal.Mount.from_local_dir(
    Path(__file__).parent,
    remote_path="/app",
    condition=lambda path: not any(
        part in str(path) for part in [".git", "__pycache__", ".env", "venv"]
    )
)


@app.cls(
    image=image,
    secrets=[secrets],
    mounts=[project_mount],
    gpu=None,  # Add gpu="T4" if you need GPU acceleration
)
class WeatherAnalyzer:
    """Serverless weather analysis using OpenAI Vision"""
    
    def __init__(self):
        import sys
        sys.path.append("/app")
        from ai_model.openai_vision import OpenAIVisionAnalyzer
        
        # Initialize with API key from Modal secrets
        self.analyzer = OpenAIVisionAnalyzer()
        self.analyzer.api_key = os.environ.get("OPENAI_API_KEY")
    
    @modal.method()
    def analyze_image(self, image_path: str, context: str = "") -> Dict:
        """Analyze a single image for weather conditions"""
        return self.analyzer.analyze_image(image_path, context)
    
    @modal.method()
    def analyze_batch(self, image_paths: List[str], context: str = "") -> Dict:
        """Analyze multiple images and get weather summary"""
        analyses = []
        for image_path in image_paths:
            analysis = self.analyzer.analyze_image(image_path, context)
            analyses.append(analysis)
        
        return self.analyzer.get_weather_summary_from_images(analyses)


@app.cls(
    image=image,
    secrets=[secrets],
    mounts=[project_mount],
)
class AlertDispatcher:
    """Serverless alert distribution system"""
    
    def __init__(self):
        import sys
        sys.path.append("/app")
        from bot.real_alerts import RealAlertSystem
        
        self.alert_system = RealAlertSystem()
    
    @modal.method()
    def send_telegram_alert(self, message: str, chat_id: Optional[str] = None) -> bool:
        """Send alert via Telegram"""
        return self.alert_system.send_telegram_message(message, chat_id)
    
    @modal.method()
    def send_sms_alert(self, message: str, to_number: Optional[str] = None) -> bool:
        """Send alert via SMS"""
        return self.alert_system.send_sms_alert(message, to_number)
    
    @modal.method()
    def send_multi_channel_alert(
        self, 
        weather_condition: str, 
        context: str, 
        channels: List[str] = ["telegram", "sms"]
    ) -> Dict:
        """Send alerts across multiple channels"""
        results = {}
        
        message = f"🌤️ Weather Alert: {weather_condition}\n{context}"
        
        if "telegram" in channels:
            results["telegram"] = self.send_telegram_alert(message)
        
        if "sms" in channels:
            results["sms"] = self.send_sms_alert(message)
        
        return results


@app.function(
    image=image,
    secrets=[secrets],
    mounts=[project_mount],
    schedule=modal.Period(minutes=30),  # Run every 30 minutes
)
def scheduled_weather_monitor():
    """Scheduled function to monitor weather from configured sources"""
    analyzer = WeatherAnalyzer()
    dispatcher = AlertDispatcher()
    
    # This is where you'd add logic to:
    # 1. Fetch images from social media or other sources
    # 2. Analyze them
    # 3. Send alerts if significant weather detected
    
    # Example implementation:
    event_dir = Path("/app/data/event_images")
    if event_dir.exists():
        images = [str(f) for f in event_dir.iterdir() 
                  if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        
        if images:
            # Analyze images
            summary = analyzer.analyze_batch.remote(
                images, 
                "Scheduled weather monitoring"
            )
            
            # Send alert if weather detected
            if summary.get("dominant_weather") != "unknown":
                dispatcher.send_multi_channel_alert.remote(
                    summary["dominant_weather"],
                    f"Confidence: {summary['confidence']:.1%}",
                    ["telegram"]
                )
    
    return {"status": "completed", "timestamp": datetime.now().isoformat()}


@app.function(
    image=image,
    secrets=[secrets],
    mounts=[project_mount],
)
def analyze_uploaded_image(image_data: bytes, filename: str) -> Dict:
    """Web endpoint for analyzing uploaded images"""
    import tempfile
    from PIL import Image
    import io
    
    analyzer = WeatherAnalyzer()
    
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(suffix=f"_{filename}", delete=False) as tmp:
        # Convert bytes to image and save
        image = Image.open(io.BytesIO(image_data))
        image.save(tmp.name)
        
        # Analyze the image
        result = analyzer.analyze_image.remote(
            tmp.name,
            f"User uploaded image: {filename}"
        )
    
    return result


@app.local_entrypoint()
def main():
    """Test the Modal functions locally"""
    print("🚀 WeatherEyes Modal Integration")
    print("\nAvailable functions:")
    print("1. WeatherAnalyzer - Serverless image analysis")
    print("2. AlertDispatcher - Multi-channel notifications")
    print("3. scheduled_weather_monitor - Automated monitoring")
    print("4. analyze_uploaded_image - Web API endpoint")
    
    # Example: Test weather analysis
    analyzer = WeatherAnalyzer()
    test_image = "/app/data/demo_images/sample.jpg"  # Add a test image
    
    if Path(test_image).exists():
        print(f"\nTesting analysis on {test_image}...")
        result = analyzer.analyze_image.remote(test_image, "Test analysis")
        print(f"Result: {json.dumps(result, indent=2)}")


# Web endpoint using Modal's web capabilities
@app.function(
    image=image,
    secrets=[secrets],
    mounts=[project_mount],
)
@modal.web_endpoint(method="POST")
def weather_api(item: Dict) -> Dict:
    """
    REST API endpoint for weather analysis
    
    Example usage:
    curl -X POST https://your-modal-endpoint.modal.run \
         -H "Content-Type: application/json" \
         -d '{"image_url": "https://example.com/weather.jpg"}'
    """
    import requests
    from PIL import Image
    import io
    
    analyzer = WeatherAnalyzer()
    
    if "image_url" in item:
        # Download image from URL
        response = requests.get(item["image_url"])
        image_data = response.content
        
        # Analyze
        result = analyze_uploaded_image.remote(
            image_data, 
            item.get("filename", "downloaded.jpg")
        )
        
        return {
            "status": "success",
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }
    
    return {"status": "error", "message": "No image_url provided"}


if __name__ == "__main__":
    main()