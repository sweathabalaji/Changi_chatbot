#!/bin/bash

# Script to check and install Vercel CLI

echo "🔍 Checking if Vercel CLI is installed..."

if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI is already installed!"
    echo "Current version: $(vercel --version)"
    exit 0
fi

echo "❌ Vercel CLI is not installed."
echo ""
echo "Select installation method:"
echo "1) Install with npm (requires Node.js)"
echo "2) Install with yarn (requires Yarn)"
echo "3) Exit and install manually"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Installing Vercel CLI with npm..."
        npm install -g vercel
        ;;        
    2)
        echo "Installing Vercel CLI with yarn..."
        yarn global add vercel
        ;;        
    3)
        echo "Exiting. Please install Vercel CLI manually."
        echo "Visit https://vercel.com/docs/cli for more information."
        exit 0
        ;;        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;        
esac

# Check if installation was successful
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI installed successfully!"
    echo "Current version: $(vercel --version)"
    echo ""
    echo "You can now run './deploy.sh' to deploy your application."
else
    echo "❌ Installation failed. Please try installing manually:"
    echo "npm install -g vercel"
    echo "or"
    echo "yarn global add vercel"
    echo ""
    echo "Visit https://vercel.com/docs/cli for more information."
    exit 1
fi