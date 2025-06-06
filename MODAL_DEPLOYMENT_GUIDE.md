# Modal Deployment Guide for WeatherEyes

## 🚀 What Modal Enables

With Modal, WeatherEyes becomes a scalable, serverless application with:

1. **Serverless Functions** - No infrastructure management
2. **Auto-scaling** - Handle any load automatically
3. **Scheduled Jobs** - Automated weather monitoring
4. **REST API** - Weather analysis as a service
5. **Cost-effective** - Pay only for compute time used

## 📋 Prerequisites

1. **Modal Account**: Sign up at [modal.com](https://modal.com)
2. **Modal CLI**: Install with `pip install modal`
3. **API Keys**: Your OpenAI, Telegram, and Twilio keys

## 🛠️ Setup Steps

### 1. Install Modal CLI
```bash
pip install modal
```

### 2. Authenticate Modal
```bash
modal setup
```

### 3. Create Modal Secrets
Store your API keys securely in Modal:

```bash
modal secret create weathereyes-secrets \
  OPENAI_API_KEY=your_openai_key \
  TELEGRAM_BOT_TOKEN=your_telegram_token \
  TELEGRAM_CHAT_ID=your_chat_id \
  TWILIO_ACCOUNT_SID=your_twilio_sid \
  TWILIO_AUTH_TOKEN=your_twilio_auth \
  TWILIO_FROM_NUMBER=your_twilio_number \
  TWILIO_TO_NUMBER=recipient_number
```

### 4. Deploy to Modal
```bash
modal deploy modal_integration.py
```

## 🎯 Available Functions

### 1. **WeatherAnalyzer** - Serverless Image Analysis
```python
# Analyze single image
modal run modal_integration.py::WeatherAnalyzer.analyze_image \
  --image-path /path/to/image.jpg \
  --context "Event photo"

# Analyze batch of images
modal run modal_integration.py::WeatherAnalyzer.analyze_batch \
  --image-paths ["/path/to/img1.jpg", "/path/to/img2.jpg"]
```

### 2. **AlertDispatcher** - Multi-channel Notifications
```python
# Send Telegram alert
modal run modal_integration.py::AlertDispatcher.send_telegram_alert \
  --message "⛈️ Storm detected with 95% confidence"

# Send multi-channel alert
modal run modal_integration.py::AlertDispatcher.send_multi_channel_alert \
  --weather-condition "stormy" \
  --context "High confidence detection" \
  --channels ["telegram", "sms"]
```

### 3. **Scheduled Monitor** - Automated Monitoring
The system automatically runs every 30 minutes to:
- Check for new images
- Analyze weather conditions
- Send alerts if needed

### 4. **REST API** - Weather Analysis Endpoint
After deployment, you'll get an endpoint URL:
```bash
https://YOUR-USERNAME--weathereyes-app-weather-api.modal.run
```

Use it to analyze images:
```bash
curl -X POST https://YOUR-ENDPOINT.modal.run \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/weather-photo.jpg"}'
```

## 📱 Integration Examples

### Python Client
```python
import requests

def analyze_weather_image(image_url):
    response = requests.post(
        "https://YOUR-ENDPOINT.modal.run",
        json={"image_url": image_url}
    )
    return response.json()

# Example usage
result = analyze_weather_image("https://example.com/storm.jpg")
print(f"Weather: {result['analysis']['weather_condition']}")
print(f"Confidence: {result['analysis']['confidence']}")
```

### JavaScript/Node.js Client
```javascript
async function analyzeWeather(imageUrl) {
    const response = await fetch('https://YOUR-ENDPOINT.modal.run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_url: imageUrl })
    });
    return await response.json();
}

// Example usage
const result = await analyzeWeather('https://example.com/storm.jpg');
console.log(`Weather: ${result.analysis.weather_condition}`);
```

### Mobile App Integration
```swift
// iOS Swift example
func analyzeWeatherImage(imageUrl: String) async throws -> WeatherAnalysis {
    let url = URL(string: "https://YOUR-ENDPOINT.modal.run")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = ["image_url": imageUrl]
    request.httpBody = try JSONEncoder().encode(body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(WeatherAnalysis.self, from: data)
}
```

## 🔧 Advanced Configuration

### Custom Schedule
Modify the schedule in `modal_integration.py`:
```python
@app.function(schedule=modal.Period(minutes=10))  # Run every 10 minutes
# or
@app.function(schedule=modal.Cron("0 */2 * * *"))  # Run every 2 hours
```

### GPU Acceleration
For faster image processing:
```python
@app.cls(gpu="T4")  # or "A10G" for more power
```

### Increase Memory/CPU
```python
@app.cls(cpu=2.0, memory=4096)  # 2 CPUs, 4GB RAM
```

## 📊 Monitoring & Logs

### View Logs
```bash
modal logs -f weathereyes-app
```

### Monitor Function Calls
```bash
modal app list
modal app stats weathereyes-app
```

## 💰 Cost Optimization

1. **Use Scheduled Functions Wisely**: Adjust frequency based on needs
2. **Batch Processing**: Analyze multiple images in one call
3. **Cache Results**: Store recent analyses to avoid redundant API calls
4. **Set Timeouts**: Prevent runaway functions

```python
@app.function(timeout=300)  # 5-minute timeout
```

## 🚨 Production Checklist

- [ ] Set up Modal secrets with production API keys
- [ ] Configure appropriate schedules
- [ ] Set up monitoring/alerting
- [ ] Test all endpoints thoroughly
- [ ] Configure rate limiting if needed
- [ ] Set up error handling and retries
- [ ] Document API endpoints for team

## 🆘 Troubleshooting

### Common Issues

1. **"Secret not found"**: Ensure you created the secret with exact name
2. **"Import error"**: Check that all files are properly mounted
3. **"API limit exceeded"**: Implement rate limiting or caching
4. **"Timeout error"**: Increase function timeout or optimize code

### Debug Mode
```bash
modal run --debug modal_integration.py
```

## 🎉 Next Steps

1. **Add Social Media Integration**: Fetch images from Instagram/Twitter
2. **Implement Caching**: Redis for recent analyses
3. **Add Dashboard**: Real-time monitoring dashboard
4. **Set Up Webhooks**: Trigger analysis from external events
5. **Create Mobile SDK**: Native mobile integration

---

**Ready to scale WeatherEyes to production with Modal!** 🚀