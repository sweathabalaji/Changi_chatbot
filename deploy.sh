#!/bin/bash

# Changi Chatbot Deployment Script

echo "🚀 Starting Changi Chatbot deployment to Vercel"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "Please install it with one of the following commands:"
    echo "  npm: npm install -g vercel"
    echo "  yarn: yarn global add vercel"
    echo ""
    echo "Alternatively, you can deploy manually through the Vercel dashboard:"
    echo "1. Push your code to GitHub"
    echo "2. Visit https://vercel.com/new to import your repository"
    echo "3. Configure your project and deploy"
    echo ""
    echo "After installing Vercel CLI, run this script again."
    exit 0
fi

# Check if user is logged in to Vercel
vercel whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ You are not logged in to Vercel. Please login with: vercel login"
    exit 1
fi

# Ensure the environment file exists
if [ ! -f ".env" ]; then
    echo "⚠️ Warning: .env file not found. Make sure to set environment variables in Vercel dashboard."
fi

# Copy requirements-vercel.txt to requirements.txt for deployment
echo "📦 Preparing requirements for Vercel deployment..."
cp requirements.txt requirements.txt.backup
cp requirements-vercel.txt requirements.txt

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

# Restore original requirements.txt
echo "🧹 Cleaning up..."
mv requirements.txt.backup requirements.txt

echo "✅ Deployment process completed!"
echo "📝 Note: Make sure to set GOOGLE_API_KEY in your Vercel project settings."