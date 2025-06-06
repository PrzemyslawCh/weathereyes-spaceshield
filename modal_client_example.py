"""
Example client for using WeatherEyes Modal deployment
Shows how to interact with the deployed serverless functions
"""

import requests
import json
from typing import Dict, List
import time

# Replace with your actual Modal endpoint
MODAL_ENDPOINT = "https://YOUR-USERNAME--weathereyes-app-weather-api.modal.run"


class WeatherEyesClient:
    """Client for interacting with WeatherEyes Modal deployment"""
    
    def __init__(self, endpoint: str = MODAL_ENDPOINT):
        self.endpoint = endpoint
    
    def analyze_image_url(self, image_url: str) -> Dict:
        """
        Analyze weather from an image URL
        
        Args:
            image_url: Public URL of the image to analyze
            
        Returns:
            Dict with weather analysis results
        """
        response = requests.post(
            self.endpoint,
            json={"image_url": image_url},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"Request failed with status {response.status_code}",
                "details": response.text
            }
    
    def analyze_multiple_images(self, image_urls: List[str]) -> List[Dict]:
        """
        Analyze multiple images and aggregate results
        
        Args:
            image_urls: List of image URLs to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        
        for url in image_urls:
            print(f"Analyzing: {url}")
            result = self.analyze_image_url(url)
            results.append(result)
            time.sleep(0.5)  # Be nice to the API
        
        return results
    
    def get_weather_summary(self, analyses: List[Dict]) -> Dict:
        """
        Get summary from multiple analyses
        
        Args:
            analyses: List of analysis results
            
        Returns:
            Summary with dominant weather and confidence
        """
        weather_counts = {}
        total_confidence = 0
        valid_count = 0
        
        for analysis in analyses:
            if analysis.get("status") == "success":
                weather = analysis["analysis"]["weather_condition"]
                confidence = analysis["analysis"]["confidence"]
                
                weather_counts[weather] = weather_counts.get(weather, 0) + 1
                total_confidence += confidence
                valid_count += 1
        
        if valid_count == 0:
            return {"error": "No valid analyses"}
        
        # Find dominant weather
        dominant_weather = max(weather_counts.items(), key=lambda x: x[1])[0]
        avg_confidence = total_confidence / valid_count
        
        return {
            "dominant_weather": dominant_weather,
            "confidence": avg_confidence,
            "weather_distribution": weather_counts,
            "total_images": len(analyses),
            "valid_analyses": valid_count
        }


def demo_single_image():
    """Demo: Analyze a single image"""
    print("=== Single Image Analysis Demo ===")
    
    client = WeatherEyesClient()
    
    # Example image URL (replace with actual weather image)
    image_url = "https://example.com/weather-photo.jpg"
    
    result = client.analyze_image_url(image_url)
    
    if result.get("status") == "success":
        analysis = result["analysis"]
        print(f"Weather: {analysis['weather_condition']}")
        print(f"Confidence: {analysis['confidence']:.1%}")
        print(f"Description: {analysis.get('description', 'N/A')}")
    else:
        print(f"Error: {result.get('message')}")


def demo_batch_analysis():
    """Demo: Analyze multiple images"""
    print("\n=== Batch Analysis Demo ===")
    
    client = WeatherEyesClient()
    
    # Example image URLs (replace with actual weather images)
    image_urls = [
        "https://example.com/sunny-day.jpg",
        "https://example.com/cloudy-sky.jpg",
        "https://example.com/rain-storm.jpg"
    ]
    
    # Analyze all images
    results = client.analyze_multiple_images(image_urls)
    
    # Get summary
    summary = client.get_weather_summary(results)
    
    print(f"\nSummary:")
    print(f"Dominant Weather: {summary.get('dominant_weather', 'Unknown')}")
    print(f"Average Confidence: {summary.get('confidence', 0):.1%}")
    print(f"Weather Distribution: {summary.get('weather_distribution', {})}")
    print(f"Valid Analyses: {summary.get('valid_analyses', 0)}/{summary.get('total_images', 0)}")


def demo_webhook_integration():
    """Demo: Webhook-style integration"""
    print("\n=== Webhook Integration Demo ===")
    
    # This would typically be called from your webhook endpoint
    def process_new_image(image_url: str, source: str = "instagram"):
        client = WeatherEyesClient()
        
        print(f"New image from {source}: {image_url}")
        result = client.analyze_image_url(image_url)
        
        if result.get("status") == "success":
            weather = result["analysis"]["weather_condition"]
            confidence = result["analysis"]["confidence"]
            
            # Trigger alerts based on conditions
            if weather in ["stormy", "severe"] and confidence > 0.8:
                print(f"🚨 ALERT: {weather} weather detected with {confidence:.1%} confidence!")
                # Here you would trigger your alert system
            else:
                print(f"✅ Normal conditions: {weather} ({confidence:.1%} confidence)")
        
        return result
    
    # Simulate webhook call
    process_new_image("https://example.com/storm-photo.jpg", "instagram")


def demo_monitoring_dashboard():
    """Demo: Data for monitoring dashboard"""
    print("\n=== Monitoring Dashboard Demo ===")
    
    client = WeatherEyesClient()
    
    # This would typically run periodically
    def get_dashboard_data():
        # Recent analyses (mock data)
        recent_images = [
            "https://example.com/img1.jpg",
            "https://example.com/img2.jpg",
            "https://example.com/img3.jpg"
        ]
        
        results = client.analyze_multiple_images(recent_images)
        summary = client.get_weather_summary(results)
        
        dashboard_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "current_weather": summary.get("dominant_weather", "Unknown"),
            "confidence": summary.get("confidence", 0),
            "recent_analyses": len(results),
            "weather_distribution": summary.get("weather_distribution", {}),
            "alerts_triggered": 0  # Would be populated from alert system
        }
        
        return dashboard_data
    
    data = get_dashboard_data()
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    print("WeatherEyes Modal Client Examples")
    print("=================================")
    print(f"Endpoint: {MODAL_ENDPOINT}")
    print("\nNote: Replace the endpoint and image URLs with your actual values!\n")
    
    # Run demos
    demo_single_image()
    demo_batch_analysis()
    demo_webhook_integration()
    demo_monitoring_dashboard()
    
    print("\n✅ All demos completed!")