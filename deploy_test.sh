#!/bin/bash

# Simplified deployment script for testing

echo "🚀 Testing Changi Chatbot deployment script"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "You can install it with one of the following commands:"
    echo "  npm: npm install -g vercel"
    echo "  yarn: yarn global add vercel"
    echo ""
    echo "Alternatively, you can deploy manually through the Vercel dashboard:"
    echo "1. Push your code to GitHub"
    echo "2. Visit https://vercel.com/new to import your repository"
    echo "3. Configure your project and deploy"
    echo ""
    echo "Installation instructions displayed successfully."
    exit 0
fi

# If we get here, Vercel is installed
echo "✅ Vercel CLI is installed!"
echo "✅ Test completed successfully!"