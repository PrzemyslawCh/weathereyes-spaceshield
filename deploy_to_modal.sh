#!/bin/bash

# WeatherEyes Modal Deployment Script
# This script helps deploy WeatherEyes to Modal

echo "🚀 WeatherEyes Modal Deployment"
echo "=============================="

# Check if modal is installed
if ! command -v modal &> /dev/null; then
    echo "❌ Modal CLI not found. Installing..."
    pip install modal
else
    echo "✅ Modal CLI found"
fi

# Check if authenticated
if ! modal token info &> /dev/null; then
    echo "🔐 Please authenticate with Modal..."
    modal setup
else
    echo "✅ Modal authenticated"
fi

# Check for secrets
echo ""
echo "📋 Checking Modal secrets..."
if modal secret list | grep -q "weathereyes-secrets"; then
    echo "✅ Secrets found"
else
    echo "❌ Secrets not found. Creating..."
    echo ""
    echo "Please enter your API keys:"
    read -p "OpenAI API Key: " OPENAI_KEY
    read -p "Telegram Bot Token (optional): " TELEGRAM_TOKEN
    read -p "Telegram Chat ID (optional): " TELEGRAM_CHAT
    read -p "Twilio Account SID (optional): " TWILIO_SID
    read -p "Twilio Auth Token (optional): " TWILIO_AUTH
    read -p "Twilio From Number (optional): " TWILIO_FROM
    read -p "Twilio To Number (optional): " TWILIO_TO
    
    # Create secrets
    modal secret create weathereyes-secrets \
        OPENAI_API_KEY="$OPENAI_KEY" \
        TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN" \
        TELEGRAM_CHAT_ID="$TELEGRAM_CHAT" \
        TWILIO_ACCOUNT_SID="$TWILIO_SID" \
        TWILIO_AUTH_TOKEN="$TWILIO_AUTH" \
        TWILIO_FROM_NUMBER="$TWILIO_FROM" \
        TWILIO_TO_NUMBER="$TWILIO_TO"
    
    echo "✅ Secrets created"
fi

# Deploy
echo ""
echo "🚀 Deploying to Modal..."
modal deploy modal_integration.py

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Check your Modal dashboard for the endpoint URL"
echo "2. Test the API with: modal run modal_integration.py"
echo "3. Use modal_client_example.py to interact with your deployment"
echo ""
echo "📊 Monitor your deployment:"
echo "   modal logs -f weathereyes-app"
echo ""
echo "🎉 Happy weather monitoring!"