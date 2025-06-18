#!/bin/bash

echo -e "\n🔧 Setting up NANO TOOL...\n"

# Check if nmap is installed
if ! command -v nmap &> /dev/null; then
    echo -e "❌ Nmap is not installed. Installing it now..."
    sudo apt update && sudo apt install -y nmap
else
    echo -e "✅ Nmap is already installed."
fi

echo -e "\n📦 Installing Python dependencies (system-wide):"
echo -e "   pip install xmltodict tabulate --break-system-packages"

echo -e "\n💡 Use '--break-system-packages' only if you're not using a virtual environment."
echo -e "   This ensures compatibility with Kali Linux and similar systems."

echo -e "\n🎉 Setup complete!"
echo -e "💻 You can now run the tool with: python3 NanoTool.py\n"

